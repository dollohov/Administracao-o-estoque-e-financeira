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
from django.db.models import Sum, Q
from django.http import JsonResponse
from datetime import datetime, timedelta
from .models import Produto, MovimentacaoEstoque
from financeiro.models import CapitalGiro


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


@login_required
@permission_required('estoque.add_produto', raise_exception=True)
def cadastrar_produto(request):
    """
    View para cadastrar um novo produto.
    
    Args:
        request: Objeto HttpRequest do Django
        
    Returns:
        HttpResponse: Renderiza formulário ou redireciona após salvar
    """
    if request.method == 'POST':
        try:
            # Criar novo produto com dados do formulário
            produto = Produto(
                nome=request.POST.get('nome'),
                descricao=request.POST.get('descricao', ''),
                preco_custo=request.POST.get('preco_custo'),
                preco_venda=request.POST.get('preco_venda'),
                estoque_atual=request.POST.get('estoque_inicial', 0),
                estoque_minimo=request.POST.get('estoque_minimo', 10),
                usuario_criacao=request.user
            )
            produto.save()
            
            # Mensagem de sucesso
            messages.success(
                request,
                f'Produto "{produto.nome}" cadastrado com sucesso!'
            )
            
            return redirect('estoque:lista_produtos')
            
        except Exception as e:
            # Mensagem de erro
            messages.error(
                request,
                f'Erro ao cadastrar produto: {str(e)}'
            )
    
    return render(request, 'estoque/cadastrar_produto.html')


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
