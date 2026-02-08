"""
Views melhoradas para o PDV com suporte a codigo de barras e imagens.

Autor: Manus AI
Data: 2026-02-07
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction
from django.db.models import Q
from datetime import datetime, timedelta
from decimal import Decimal
from estoque.models import Produto, MovimentacaoEstoque
from clientes.models import Cliente
from .models import Venda, ItemVenda, Caixa


@login_required
def dashboard_pdv(request):
    """
    Dashboard do PDV com informacoes sobre vendas do dia.
    """
    hoje = datetime.now().date()
    vendas_hoje = Venda.objects.filter(
        data_venda__date=hoje,
        usuario=request.user
    )
    
    total_vendas = sum(v.total for v in vendas_hoje)
    quantidade_vendas = vendas_hoje.count()
    
    caixa_aberto = Caixa.objects.filter(
        usuario_abertura=request.user,
        data_fechamento__isnull=True
    ).first()
    
    context = {
        'total_vendas': total_vendas,
        'quantidade_vendas': quantidade_vendas,
        'caixa_aberto': caixa_aberto,
        'vendas_recentes': vendas_hoje[:10],
    }
    
    return render(request, 'pdv/dashboard.html', context)


@login_required
def nova_venda(request):
    """
    View para criar uma nova venda no PDV com interface melhorada.
    """
    caixa = Caixa.objects.filter(
        usuario_abertura=request.user,
        data_fechamento__isnull=True
    ).first()
    
    if not caixa:
        messages.error(request, 'Abra o caixa antes de realizar vendas.')
        return redirect('pdv:abrir_caixa')
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                venda = Venda(
                    metodo_pagamento=request.POST.get('metodo_pagamento'),
                    usuario=request.user,
                    observacoes=request.POST.get('observacoes', '')
                )
                
                cliente_id = request.POST.get('cliente_id')
                if cliente_id:
                    venda.cliente = Cliente.objects.get(id=cliente_id)
                
                venda.save()
                
                produtos_ids = request.POST.getlist('produto_id')
                quantidades = request.POST.getlist('quantidade')
                precos = request.POST.getlist('preco')
                
                for produto_id, quantidade, preco in zip(produtos_ids, quantidades, precos):
                    if produto_id and quantidade:
                        produto = Produto.objects.get(id=produto_id)
                        
                        # Verificar estoque
                        if produto.estoque_atual < int(quantidade):
                            raise ValueError(f"Estoque insuficiente para {produto.nome}")
                        
                        item = ItemVenda(
                            venda=venda,
                            produto=produto,
                            quantidade=int(quantidade),
                            preco_unitario=float(preco)
                        )
                        item.save()
                        
                        # Criar movimentacao de estoque
                        MovimentacaoEstoque.objects.create(
                            produto=produto,
                            tipo='SAIDA',
                            quantidade=int(quantidade),
                            valor_unitario=Decimal(preco),
                            observacao=f"Venda PDV #{venda.numero_venda}",
                            usuario=request.user
                        )
                
                venda.calcular_total()
                venda.total_itens = venda.itens.count()
                venda.save()
                
                caixa.total_vendas += venda.total
                caixa.save()
                
                messages.success(request, f'Venda #{venda.numero_venda} realizada com sucesso!')
                return redirect('pdv:detalhes_venda', pk=venda.numero_venda)
        except Exception as e:
            messages.error(request, f'Erro ao realizar venda: {str(e)}')
    
    produtos = Produto.objects.filter(ativo=True, estoque_atual__gt=0)
    clientes = Cliente.objects.filter(ativo=True)
    
    context = {
        'produtos': produtos,
        'clientes': clientes,
        'caixa': caixa,
    }
    
    return render(request, 'pdv/nova_venda.html', context)


@login_required
def detalhes_venda(request, pk):
    """
    View para exibir detalhes de uma venda.
    """
    venda = get_object_or_404(Venda, numero_venda=pk)
    
    context = {
        'venda': venda,
    }
    
    return render(request, 'pdv/detalhes_venda.html', context)


@login_required
def abrir_caixa(request):
    """
    View para abrir o caixa.
    """
    caixa_aberto = Caixa.objects.filter(
        usuario_abertura=request.user,
        data_fechamento__isnull=True
    ).first()
    
    if caixa_aberto:
        messages.warning(request, 'Voce ja possui um caixa aberto.')
        return redirect('pdv:dashboard')
    
    if request.method == 'POST':
        try:
            valor_inicial = float(request.POST.get('valor_inicial', 0))
            caixa = Caixa(
                usuario_abertura=request.user,
                valor_inicial=valor_inicial
            )
            caixa.save()
            messages.success(request, 'Caixa aberto com sucesso!')
            return redirect('pdv:dashboard')
        except Exception as e:
            messages.error(request, f'Erro ao abrir caixa: {str(e)}')
    
    return render(request, 'pdv/abrir_caixa.html')


@login_required
def fechar_caixa(request):
    """
    View para fechar o caixa.
    """
    caixa = Caixa.objects.filter(
        usuario_abertura=request.user,
        data_fechamento__isnull=True
    ).first()
    
    if not caixa:
        messages.error(request, 'Nao ha caixa aberto para fechar.')
        return redirect('pdv:dashboard')
    
    if request.method == 'POST':
        try:
            valor_final = float(request.POST.get('valor_final', 0))
            caixa.fechar_caixa(valor_final)
            caixa.usuario_fechamento = request.user
            caixa.save()
            messages.success(request, 'Caixa fechado com sucesso!')
            return redirect('pdv:dashboard')
        except Exception as e:
            messages.error(request, f'Erro ao fechar caixa: {str(e)}')
    
    context = {
        'caixa': caixa,
    }
    
    return render(request, 'pdv/fechar_caixa.html', context)


@login_required
def buscar_produto(request):
    """
    API para buscar produtos no PDV com suporte a EAN/SKU/Nome.
    
    Parametros:
    - termo: Texto de busca (pode ser nome, EAN, SKU)
    - tipo: 'barcode' para busca por codigo de barras, 'text' para texto
    """
    termo = request.GET.get('termo', '').strip()
    tipo = request.GET.get('tipo', 'text')
    
    if len(termo) < 1:
        return JsonResponse({'produtos': []})
    
    # Busca por codigo de barras (EAN/GTIN)
    if tipo == 'barcode' or len(termo) >= 8:
        produtos = Produto.objects.filter(
            Q(ean_gtin=termo) | Q(sku=termo),
            ativo=True,
            estoque_atual__gt=0
        )
    else:
        # Busca por texto (nome, descricao)
        produtos = Produto.objects.filter(
            Q(nome__icontains=termo) | Q(descricao__icontains=termo),
            ativo=True,
            estoque_atual__gt=0
        )[:10]
    
    dados = []
    for p in produtos:
        imagem_principal = p.imagens.filter(principal=True).first()
        
        dados.append({
            'id': p.id,
            'nome': p.nome,
            'sku': p.sku or '',
            'ean': p.ean_gtin or '',
            'preco': float(p.preco_venda),
            'estoque': p.estoque_atual,
            'margem': float(p.calcular_margem_lucro()),
            'imagem_url': imagem_principal.imagem.url if imagem_principal else '/static/img/sem-imagem.png',
        })
    
    return JsonResponse({'produtos': dados})


@login_required
def buscar_cliente(request):
    """
    API para buscar clientes no PDV.
    
    Parametros:
    - termo: Nome, CPF/CNPJ ou email do cliente
    """
    termo = request.GET.get('termo', '').strip()
    
    if len(termo) < 2:
        return JsonResponse({'clientes': []})
    
    clientes = Cliente.objects.filter(
        Q(nome__icontains=termo) | Q(cpf_cnpj__icontains=termo) | Q(email__icontains=termo),
        ativo=True
    )[:10]
    
    dados = [
        {
            'id': c.id,
            'nome': c.nome,
            'cpf_cnpj': c.cpf_cnpj,
            'email': c.email,
            'telefone': c.telefone,
        }
        for c in clientes
    ]
    
    return JsonResponse({'clientes': dados})


@login_required
def obter_detalhes_produto(request, produto_id):
    """
    API para obter detalhes completos de um produto.
    
    Retorna informacoes como imagens, atributos, etc.
    """
    produto = get_object_or_404(Produto, id=produto_id)
    
    imagens = []
    for img in produto.imagens.all().order_by('ordem'):
        imagens.append({
            'url': img.imagem.url,
            'descricao': img.descricao or '',
            'principal': img.principal,
        })
    
    dados = {
        'id': produto.id,
        'nome': produto.nome,
        'descricao': produto.descricao or '',
        'preco_venda': float(produto.preco_venda),
        'preco_custo': float(produto.preco_custo),
        'estoque': produto.estoque_atual,
        'margem': float(produto.calcular_margem_lucro()),
        'sku': produto.sku or '',
        'ean': produto.ean_gtin or '',
        'ncm': produto.ncm or '',
        'imagens': imagens,
    }
    
    return JsonResponse(dados)
