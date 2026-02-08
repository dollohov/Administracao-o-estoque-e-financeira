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
from .models import Produto, MovimentacaoEstoque
from financeiro.models import CapitalGiro
from fornecedores.models import Fornecedor


@login_required
def dashboard_estoque(request):
    """
    View principal do dashboard de estoque.
    
    Exibe informações resumidas sobre o estoque, incluindo:
    - Total de produtos cadastrados
    - Produtos com estoque baixo
    - Movimentações recentes
    - Valor total do estoque
    
    Args:
        request: Objeto HttpRequest do Django
        
    Returns:
        HttpResponse: Renderiza o template do dashboard
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
    View para listar todos os produtos cadastrados.
    
    Permite filtrar produtos por nome e status (ativo/inativo).
    
    Args:
        request: Objeto HttpRequest do Django
        
    Returns:
        HttpResponse: Renderiza o template com a lista de produtos
    """
    # Obter parâmetros de filtro da URL
    busca = request.GET.get('busca', '')
    mostrar_inativos = request.GET.get('inativos', 'false') == 'true'
    
    # Iniciar query com todos os produtos
    produtos = Produto.objects.all()
    
    # Aplicar filtro de busca por nome
    if busca:
        produtos = produtos.filter(
            Q(nome__icontains=busca) | Q(descricao__icontains=busca)
        )
    
    # Aplicar filtro de status
    if not mostrar_inativos:
        produtos = produtos.filter(ativo=True)
    
    # Ordenar por nome
    produtos = produtos.order_by('nome').select_related(
        'usuario_criacao', 'usuario_modificacao'
    )
    
    # Preparar contexto
    context = {
        'produtos': produtos,
        'busca': busca,
        'mostrar_inativos': mostrar_inativos,
    }
    
    return render(request, 'estoque/lista_produtos.html', context)


@login_required
@permission_required('estoque.view_produto', raise_exception=True)
def detalhes_produto(request, produto_id):
    """
    View para exibir detalhes de um produto específico.
    
    Mostra informações completas do produto, incluindo:
    - Dados cadastrais
    - Histórico de movimentações
    - Cálculos de margem de lucro
    
    Args:
        request: Objeto HttpRequest do Django
        produto_id (int): ID do produto a ser exibido
        
    Returns:
        HttpResponse: Renderiza o template com detalhes do produto
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


def get_produto_data_from_post(request):
    """Auxiliar para extrair dados do produto do POST."""
    data = {
        'nome': request.POST.get('nome'),
        'descricao': request.POST.get('descricao', ''),
        'marca': request.POST.get('marca', ''),
        'categoria': request.POST.get('categoria', ''),
        'subcategoria': request.POST.get('subcategoria', ''),
        'sku': request.POST.get('sku', ''),
        'ncm': request.POST.get('ncm', ''),
        'cest': request.POST.get('cest', ''),
        'ean_gtin': request.POST.get('ean_gtin', ''),
        'preco_custo': request.POST.get('preco_custo'),
        'preco_venda': request.POST.get('preco_venda'),
        'estoque_minimo': request.POST.get('estoque_minimo', 10),
        'estoque_maximo': request.POST.get('estoque_maximo', 100),
        'peso_kg': request.POST.get('peso_kg') or None,
        'altura_cm': request.POST.get('altura_cm') or None,
        'largura_cm': request.POST.get('largura_cm') or None,
        'profundidade_cm': request.POST.get('profundidade_cm') or None,
        'localizacao_estoque': request.POST.get('localizacao_estoque', ''),
        'icms_aliquota': request.POST.get('icms_aliquota', 0),
        'ipi_aliquota': request.POST.get('ipi_aliquota', 0),
        'pis_aliquota': request.POST.get('pis_aliquota', 0),
        'cofins_aliquota': request.POST.get('cofins_aliquota', 0),
        'visivel_catalogo': request.POST.get('visivel_catalogo') == 'on',
        'ativo': request.POST.get('ativo') == 'on',
    }
    
    # Tratar fornecedor
    fornecedor_id = request.POST.get('fornecedor')
    if fornecedor_id:
        data['fornecedor'] = get_object_or_404(Fornecedor, pk=fornecedor_id)
    else:
        data['fornecedor'] = None
        
    # Tratar imagem se enviada
    if request.FILES.get('imagem'):
        data['imagem'] = request.FILES.get('imagem')
        
    return data


@login_required
@permission_required('estoque.add_produto', raise_exception=True)
def cadastrar_produto(request):
    """
    View para cadastrar um novo produto com todos os campos.
    """
    if request.method == 'POST':
        try:
            data = get_produto_data_from_post(request)
            data['estoque_atual'] = request.POST.get('estoque_inicial', 0)
            data['usuario_criacao'] = request.user
            
            produto = Produto(**data)
            produto.save()
            
            messages.success(request, f'Produto "{produto.nome}" cadastrado com sucesso!')
            return redirect('estoque:lista_produtos')
            
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar produto: {str(e)}')
    
    fornecedores = Fornecedor.objects.filter(ativo=True)
    return render(request, 'estoque/cadastrar_produto.html', {'fornecedores': fornecedores})


@login_required
@permission_required('estoque.change_produto', raise_exception=True)
def editar_produto(request, produto_id):
    """
    View para editar um produto existente com todos os campos.
    """
    produto = get_object_or_404(Produto, pk=produto_id)
    
    if request.method == 'POST':
        try:
            data = get_produto_data_from_post(request)
            
            for key, value in data.items():
                setattr(produto, key, value)
                
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


@login_required
@permission_required('estoque.add_movimentacaoestoque', raise_exception=True)
def registrar_movimentacao(request):
    """
    View para registrar uma movimentação de estoque.
    
    Permite registrar entradas e saídas de produtos, atualizando
    automaticamente o estoque e o capital de giro.
    
    Args:
        request: Objeto HttpRequest do Django
        
    Returns:
        HttpResponse: Renderiza formulário ou redireciona após salvar
    """
    if request.method == 'POST':
        try:
            # Obter dados do formulário
            produto_id = request.POST.get('produto')
            tipo = request.POST.get('tipo')
            quantidade = int(request.POST.get('quantidade'))
            valor_unitario = float(request.POST.get('valor_unitario'))
            observacao = request.POST.get('observacao', '')
            
            # Obter o produto
            produto = get_object_or_404(Produto, pk=produto_id)
            
            # Criar a movimentação
            movimentacao = MovimentacaoEstoque(
                produto=produto,
                tipo=tipo,
                quantidade=quantidade,
                valor_unitario=valor_unitario,
                observacao=observacao,
                usuario=request.user
            )
            movimentacao.save()
            
            # Atualizar capital de giro
            valor_total = movimentacao.calcular_valor_total()
            
            if tipo == 'ENTRADA':
                # Entrada de estoque = saída de capital (compra)
                CapitalGiro.retirar_capital(
                    valor=valor_total,
                    descricao=f'Compra de {quantidade}x {produto.nome}',
                    usuario=request.user
                )
            elif tipo == 'SAIDA':
                # Saída de estoque = entrada de capital (venda)
                CapitalGiro.adicionar_capital(
                    valor=valor_total,
                    descricao=f'Venda de {quantidade}x {produto.nome}',
                    usuario=request.user
                )
            
            # Mensagem de sucesso
            messages.success(
                request,
                f'Movimentação registrada com sucesso! '
                f'{tipo} de {quantidade}x {produto.nome}'
            )
            
            return redirect('estoque:dashboard')
            
        except ValueError as e:
            # Erro de validação (ex: estoque insuficiente)
            messages.error(request, str(e))
        except Exception as e:
            # Outros erros
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
    
    Exibe análises detalhadas sobre o estoque, incluindo:
    - Produtos mais vendidos
    - Produtos com menor giro
    - Análise de lucratividade
    
    Args:
        request: Objeto HttpRequest do Django
        
    Returns:
        HttpResponse: Renderiza o template do relatório
    """
    # Verificar permissão
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
