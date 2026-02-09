"""
Views do módulo de Estoque.

Este arquivo contém as views (controladores) para o módulo de estoque,
incluindo listagem de produtos, registro de movimentações e dashboards.

Autor: Manus AI
Data: 2025-12-02
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db import models
from django.db.models import Sum, Q
from django.http import JsonResponse
from datetime import datetime, timedelta
from decimal import Decimal, InvalidOperation
import os
from .models import Produto, MovimentacaoEstoque
from .services import EstoqueService
from financeiro.models import CapitalGiro
from fornecedores.models import Fornecedor


@login_required
def dashboard_estoque(request):
    """
    View principal do dashboard de estoque.
    """
    # Obter todos os produtos ativos
    produtos = Produto.objects.filter(ativo=True)
    
    # Calcular estatísticas
    total_produtos = produtos.count()
    produtos_estoque_baixo = produtos.filter(
        estoque_atual__lt=models.F('estoque_minimo')
    ).count()
    
    # Calcular valor total do estoque
    valor_total_estoque = sum(
        produto.valor_total_estoque() for produto in produtos
    )
    
    # Obter movimentações recentes (últimos 7 dias)
    data_limite = datetime.now() - timedelta(days=7)
    movimentacoes_recentes = MovimentacaoEstoque.objects.filter(
        data_movimentacao__gte=data_limite
    ).select_related('produto', 'usuario')[:10]
    
    # Produtos com estoque baixo
    produtos_alerta = produtos.filter(
        estoque_atual__lt=models.F('estoque_minimo')
    ).order_by('estoque_atual')[:5]
    
    # Preparar contexto para o template
    context = {
        'total_produtos': total_produtos,
        'produtos_estoque_baixo': produtos_estoque_baixo,
        'valor_total_estoque': valor_total_estoque,
        'movimentacoes_recentes': movimentacoes_recentes,
        'produtos_alerta': produtos_alerta,
    }
    
    return render(request, 'estoque/dashboard.html', context)


@login_required
def lista_produtos(request):
    """
    View para listar todos os produtos cadastrados com filtros aprimorados.
    """
    # Obter parâmetros de filtro da URL
    busca = request.GET.get('busca', '')
    mostrar_inativos = request.GET.get('inativos', 'false') == 'true'
    categoria_filtro = request.GET.get('categoria', '')
    marca_filtro = request.GET.get('marca', '')
    
    # Iniciar query com todos os produtos
    produtos = Produto.objects.all()
    
    # Aplicar filtro de busca por nome, SKU ou descrição
    if busca:
        produtos = produtos.filter(
            Q(nome__icontains=busca) | 
            Q(descricao__icontains=busca) |
            Q(sku__icontains=busca) |
            Q(ean_gtin__icontains=busca)
        )
    
    # Aplicar filtro de categoria
    if categoria_filtro:
        produtos = produtos.filter(categoria=categoria_filtro)
        
    # Aplicar filtro de marca
    if marca_filtro:
        produtos = produtos.filter(marca=marca_filtro)
    
    # Aplicar filtro de status
    if not mostrar_inativos:
        produtos = produtos.filter(ativo=True)
    
    # Ordenar por nome
    produtos = produtos.order_by('nome').select_related(
        'usuario_criacao', 'usuario_modificacao'
    )
    
    # Obter categorias e marcas únicas para os filtros
    categorias = Produto.objects.filter(categoria__isnull=False).exclude(categoria='').values_list('categoria', flat=True).distinct().order_by('categoria')
    marcas = Produto.objects.filter(marca__isnull=False).exclude(marca='').values_list('marca', flat=True).distinct().order_by('marca')
    
    # Preparar contexto
    context = {
        'produtos': produtos,
        'busca': busca,
        'mostrar_inativos': mostrar_inativos,
        'categorias': categorias,
        'marcas': marcas,
        'categoria_selecionada': categoria_filtro,
        'marca_selecionada': marca_filtro,
    }
    
    return render(request, 'estoque/lista_produtos.html', context)


@login_required
@permission_required('estoque.view_produto', raise_exception=True)
def detalhes_produto(request, produto_id):
    """
    View para exibir detalhes de um produto específico.
    """
    # Obter o produto ou retornar 404
    produto = get_object_or_404(
        Produto.objects.select_related('usuario_criacao', 'usuario_modificacao'),
        pk=produto_id
    )
    
    # Obter movimentações do produto
    movimentacoes = produto.movimentacoes.all().select_related('usuario')[:20]
    
    # Calcular estatísticas
    total_entradas = produto.movimentacoes.filter(tipo='ENTRADA').aggregate(
        total=Sum('quantidade')
    )['total'] or 0
    
    total_saidas = produto.movimentacoes.filter(tipo='SAIDA').aggregate(
        total=Sum('quantidade')
    )['total'] or 0
    
    # Preparar contexto
    context = {
        'produto': produto,
        'movimentacoes': movimentacoes,
        'total_entradas': total_entradas,
        'total_saidas': total_saidas,
        'margem_lucro': produto.calcular_margem_lucro(),
        'lucro_unitario': produto.calcular_lucro_unitario(),
    }
    
    return render(request, 'estoque/detalhes_produto.html', context)


def parse_decimal(value, default=Decimal('0.00')):
    """Auxiliar para converter string em Decimal com segurança."""
    if value is None or (isinstance(value, str) and value.strip() == ''):
        return default
    try:
        if isinstance(value, str):
            # Substituir vírgula por ponto se necessário
            value = value.replace(',', '.')
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        return default


def get_produto_data_from_post(request):
    """Auxiliar para extrair e validar dados do produto do POST."""
    data = {
        'nome': request.POST.get('nome'),
        'descricao': request.POST.get('descricao', ''),
        'marca': request.POST.get('marca', ''),
        'categoria': request.POST.get('categoria', ''),
        'subcategoria': request.POST.get('subcategoria', ''),
        'sku': request.POST.get('sku', '') or None,
        'ncm': request.POST.get('ncm', '') or None,
        'cest': request.POST.get('cest', '') or None,
        'ean_gtin': request.POST.get('ean_gtin', '') or None,
        'preco_custo': parse_decimal(request.POST.get('preco_custo')),
        'preco_venda': parse_decimal(request.POST.get('preco_venda')),
        'estoque_minimo': int(request.POST.get('estoque_minimo') or 10),
        'estoque_maximo': int(request.POST.get('estoque_maximo') or 100),
        'peso_kg': parse_decimal(request.POST.get('peso_kg'), None),
        'altura_cm': parse_decimal(request.POST.get('altura_cm'), None),
        'largura_cm': parse_decimal(request.POST.get('largura_cm'), None),
        'profundidade_cm': parse_decimal(request.POST.get('profundidade_cm'), None),
        'localizacao_estoque': request.POST.get('localizacao_estoque', ''),
        'icms_aliquota': parse_decimal(request.POST.get('icms_aliquota')),
        'ipi_aliquota': parse_decimal(request.POST.get('ipi_aliquota')),
        'pis_aliquota': parse_decimal(request.POST.get('pis_aliquota')),
        'cofins_aliquota': parse_decimal(request.POST.get('cofins_aliquota')),
        'visivel_catalogo': request.POST.get('visivel_catalogo') == 'on',
        'ativo': request.POST.get('ativo') == 'on',
    }
    
    # Tratar fornecedor
    fornecedor_id = request.POST.get('fornecedor')
    if fornecedor_id and fornecedor_id.isdigit():
        data['fornecedor'] = get_object_or_404(Fornecedor, pk=fornecedor_id)
    else:
        data['fornecedor'] = None
        
    return data


@login_required
@permission_required('estoque.add_produto', raise_exception=True)
def cadastrar_produto(request):
    """
    View para cadastrar um novo produto com suporte a upload de imagem.
    """
    if request.method == 'POST':
        try:
            data = get_produto_data_from_post(request)
            data['estoque_atual'] = int(request.POST.get('estoque_inicial') or 0)
            data['usuario_criacao'] = request.user
            
            produto = Produto(**data)
            
            # Tratar imagem se enviada
            if request.FILES.get('imagem'):
                produto.imagem = request.FILES.get('imagem')
                
            produto.save()
            
            messages.success(request, f'Produto "{produto.nome}" cadastrado com sucesso!')
            return redirect('estoque:lista_produtos')
            
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar produto: {str(e)}')
    
    fornecedores = Fornecedor.objects.filter(ativo=True)
    return render(request, 'estoque/cadastrar_produto.html', {'fornecedores': fornecedores})


@permission_required('estoque.change_produto', raise_exception=True)
def editar_produto(request, produto_id):
    """
    View para editar um produto existente com suporte a alteração e exclusão de imagem.
    """
    produto = get_object_or_404(Produto, pk=produto_id)
    
    if request.method == 'POST':
        try:
            # Verificar se o usuário solicitou a exclusão da imagem
            if request.POST.get('remover_imagem') == 'true':
                if produto.imagem:
                    # Remover arquivo físico se existir
                    if os.path.isfile(produto.imagem.path):
                        os.remove(produto.imagem.path)
                    produto.imagem = None
            
            data = get_produto_data_from_post(request)
            
            for key, value in data.items():
                setattr(produto, key, value)
                
            # Tratar nova imagem se enviada (sobrescreve a anterior)
            if request.FILES.get('imagem'):
                # Remover imagem antiga fisicamente se houver uma nova sendo enviada
                if produto.imagem and os.path.isfile(produto.imagem.path):
                    os.remove(produto.imagem.path)
                produto.imagem = request.FILES.get('imagem')
                
            produto.usuario_modificacao = request.user
            produto.save()
            
            messages.success(request, f'Produto "{produto.nome}" atualizado com sucesso!')
            return redirect('estoque:lista_produtos')
            
        except Exception as e:
            messages.error(request, f'Erro ao atualizar produto: {str(e)}')
    
    fornecedores = Fornecedor.objects.filter(ativo=True)
    context = {
        'produto': produto,
        'is_edit': True,
        'fornecedores': fornecedores
    }
    
    return render(request, 'estoque/cadastrar_produto.html', context)


@permission_required('estoque.add_movimentacaoestoque', raise_exception=True)
def registrar_movimentacao(request):
    """
    View para registrar uma movimentação de estoque.
    """
    if request.method == 'POST':
        try:
            # Obter dados do formulário
            produto_id = request.POST.get('produto')
            tipo = request.POST.get('tipo')
            quantidade = int(request.POST.get('quantidade'))
            valor_unitario = float(request.POST.get('valor_unitario'))
            observacao = request.POST.get('observacao', '')
            
            # Chamar o serviço para registrar a movimentação (estoque + financeiro)
            movimentacao = EstoqueService.registrar_movimentacao(
                produto_id=produto_id,
                tipo=tipo,
                quantidade=quantidade,
                valor_unitario=valor_unitario,
                usuario=request.user,
                observacao=observacao
            )
            
            messages.success(
                request,
                f'Movimentação registrada com sucesso! '
                f'{tipo} de {quantidade}x {movimentacao.produto.nome}'
            )
            
            return redirect('estoque:dashboard')
            
        except ValueError as e:
            messages.error(request, f"Falha na Transação: {str(e)}")
        except Exception as e:
            messages.error(
                request,
                f'Erro ao registrar movimentação: {str(e)}'
            )
    
    # Obter lista de produtos ativos para o formulário
    produtos = Produto.objects.filter(ativo=True).order_by('nome')
    
    context = {
        'produtos': produtos,
    }
    
    return render(request, 'estoque/registrar_movimentacao.html', context)


@login_required
def relatorio_estoque(request):
    """
    View para gerar relatório completo de estoque.
    """
    if not request.user.has_perm('estoque.view_produto'):
        messages.error(request, 'Você não tem permissão para acessar relatórios.')
        return redirect('estoque:dashboard')
    
    # Obter todos os produtos ativos
    produtos = Produto.objects.filter(ativo=True)
    
    # Calcular produtos mais vendidos (últimos 30 dias)
    data_limite = datetime.now() - timedelta(days=30)
    produtos_mais_vendidos = []
    
    for produto in produtos:
        total_vendido = produto.movimentacoes.filter(
            tipo='SAIDA',
            data_movimentacao__gte=data_limite
        ).aggregate(total=Sum('quantidade'))['total'] or 0
        
        if total_vendido > 0:
            produtos_mais_vendidos.append({
                'produto': produto,
                'quantidade': total_vendido,
                'receita': total_vendido * produto.preco_venda
            })
    
    # Ordenar por quantidade vendida
    produtos_mais_vendidos.sort(key=lambda x: x['quantidade'], reverse=True)
    produtos_mais_vendidos = produtos_mais_vendidos[:10]
    
    # Preparar contexto
    context = {
        'produtos': produtos,
        'produtos_mais_vendidos': produtos_mais_vendidos,
        'data_inicio': data_limite.date(),
        'data_fim': datetime.now().date(),
    }
    
    return render(request, 'estoque/relatorio.html', context)


@login_required
def catalogo_vendedores(request):
    """
    View do Catálogo de Produtos otimizada para consulta de vendedores.
    Exibe apenas produtos marcados como 'visivel_catalogo' e 'ativo'.
    """
    busca = request.GET.get('busca', '')
    categoria_filtro = request.GET.get('categoria', '')
    marca_filtro = request.GET.get('marca', '')
    
    # Filtrar apenas produtos ativos e visíveis no catálogo
    produtos = Produto.objects.filter(ativo=True, visivel_catalogo=True)
    
    if busca:
        produtos = produtos.filter(
            Q(nome__icontains=busca) | 
            Q(descricao__icontains=busca) |
            Q(sku__icontains=busca) |
            Q(ean_gtin__icontains=busca)
        )
    
    if categoria_filtro:
        produtos = produtos.filter(categoria=categoria_filtro)
        
    if marca_filtro:
        produtos = produtos.filter(marca=marca_filtro)
    
    produtos = produtos.order_by('nome')
    
    # Obter categorias e marcas para filtros
    categorias = Produto.objects.filter(ativo=True, visivel_catalogo=True, categoria__isnull=False).exclude(categoria='').values_list('categoria', flat=True).distinct().order_by('categoria')
    marcas = Produto.objects.filter(ativo=True, visivel_catalogo=True, marca__isnull=False).exclude(marca='').values_list('marca', flat=True).distinct().order_by('marca')
    
    context = {
        'produtos': produtos,
        'busca': busca,
        'categorias': categorias,
        'marcas': marcas,
        'categoria_selecionada': categoria_filtro,
        'marca_selecionada': marca_filtro,
    }
    
    return render(request, 'estoque/catalogo.html', context)
