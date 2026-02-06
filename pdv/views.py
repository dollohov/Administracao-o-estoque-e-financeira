from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction
from datetime import datetime, timedelta
from estoque.models import Produto
from clientes.models import Cliente
from .models import Venda, ItemVenda, Caixa

@login_required
def dashboard_pdv(request):
    """
    Dashboard do PDV com informações sobre vendas do dia.
    """
    hoje = datetime.now().date()
    vendas_hoje = Venda.objects.filter(
        data_venda__date=hoje,
        usuario=request.user
    )
    
    total_vendas = sum(v.total for v in vendas_hoje)
    quantidade_vendas = vendas_hoje.count()
    
    # Caixa aberto
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
    View para criar uma nova venda no PDV.
    """
    # Verificar se há caixa aberto
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
                # Criar venda
                venda = Venda(
                    metodo_pagamento=request.POST.get('metodo_pagamento'),
                    usuario=request.user,
                    observacoes=request.POST.get('observacoes', '')
                )
                
                # Adicionar cliente se fornecido
                cliente_id = request.POST.get('cliente_id')
                if cliente_id:
                    venda.cliente = Cliente.objects.get(id=cliente_id)
                
                venda.save()
                
                # Adicionar itens
                produtos_ids = request.POST.getlist('produto_id')
                quantidades = request.POST.getlist('quantidade')
                precos = request.POST.getlist('preco')
                
                for produto_id, quantidade, preco in zip(produtos_ids, quantidades, precos):
                    if produto_id and quantidade:
                        produto = Produto.objects.get(id=produto_id)
                        item = ItemVenda(
                            venda=venda,
                            produto=produto,
                            quantidade=int(quantidade),
                            preco_unitario=float(preco)
                        )
                        item.save()
                        
                        # Atualizar estoque
                        produto.estoque_atual -= int(quantidade)
                        produto.save()
                
                # Calcular total
                venda.calcular_total()
                venda.total_itens = venda.itens.count()
                venda.save()
                
                # Atualizar caixa
                caixa.total_vendas += venda.total
                caixa.save()
                
                messages.success(request, f'Venda #{venda.numero_venda} realizada com sucesso!')
                return redirect('pdv:detalhes_venda', pk=venda.numero_venda)
        except Exception as e:
            messages.error(request, f'Erro ao realizar venda: {str(e)}')
    
    # Obter produtos disponíveis
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
    # Verificar se já há caixa aberto
    caixa_aberto = Caixa.objects.filter(
        usuario_abertura=request.user,
        data_fechamento__isnull=True
    ).first()
    
    if caixa_aberto:
        messages.warning(request, 'Você já possui um caixa aberto.')
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
        messages.error(request, 'Não há caixa aberto para fechar.')
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
    API para buscar produtos no PDV.
    """
    termo = request.GET.get('termo', '')
    
    if len(termo) < 2:
        return JsonResponse({'produtos': []})
    
    produtos = Produto.objects.filter(
        nome__icontains=termo,
        ativo=True,
        estoque_atual__gt=0
    )[:10]
    
    dados = [
        {
            'id': p.id,
            'nome': p.nome,
            'preco': float(p.preco_venda),
            'estoque': p.estoque_atual,
        }
        for p in produtos
    ]
    
    return JsonResponse({'produtos': dados})
