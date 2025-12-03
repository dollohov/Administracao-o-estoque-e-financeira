"""
Views do módulo Financeiro.

Este arquivo contém as views (controladores) para o módulo financeiro,
incluindo controle de receitas, despesas, capital de giro e indicadores.

Autor: Manus AI
Data: 2025-12-02
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Sum, Q
from django.http import JsonResponse
from datetime import datetime, timedelta
from decimal import Decimal
from .models import Receita, Despesa, CapitalGiro, IndicadorFinanceiro


@login_required
def dashboard_financeiro(request):
    """
    View principal do dashboard financeiro.
    
    Exibe informações resumidas sobre a situação financeira, incluindo:
    - Capital de giro atual
    - Receitas e despesas do mês
    - Lucro/prejuízo do período
    - Gráficos e indicadores
    
    Args:
        request: Objeto HttpRequest do Django
        
    Returns:
        HttpResponse: Renderiza o template do dashboard
    """
    # Obter capital de giro atual
    capital_atual = CapitalGiro.obter_capital_atual()
    
    # Obter período atual (mês corrente)
    hoje = datetime.now().date()
    primeiro_dia_mes = hoje.replace(day=1)
    
    # Calcular totais do mês
    receitas_mes = Receita.objects.filter(
        data__year=hoje.year,
        data__month=hoje.month
    ).aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
    
    despesas_mes = Despesa.objects.filter(
        data__year=hoje.year,
        data__month=hoje.month
    ).aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
    
    # Calcular lucro/prejuízo
    resultado_mes = receitas_mes - despesas_mes
    
    # Obter transações recentes
    receitas_recentes = Receita.objects.all().select_related('usuario')[:5]
    despesas_recentes = Despesa.objects.all().select_related('usuario')[:5]
    
    # Obter movimentações de capital recentes
    movimentacoes_capital = CapitalGiro.objects.all().select_related('usuario')[:5]
    
    # Calcular indicadores
    if receitas_mes > 0:
        margem_lucro = (resultado_mes / receitas_mes) * 100
    else:
        margem_lucro = Decimal('0.00')
    
    # Preparar contexto
    context = {
        'capital_atual': capital_atual,
        'receitas_mes': receitas_mes,
        'despesas_mes': despesas_mes,
        'resultado_mes': resultado_mes,
        'margem_lucro': margem_lucro,
        'receitas_recentes': receitas_recentes,
        'despesas_recentes': despesas_recentes,
        'movimentacoes_capital': movimentacoes_capital,
        'mes_atual': hoje.strftime('%B/%Y'),
    }
    
    return render(request, 'financeiro/dashboard.html', context)


@login_required
def lista_receitas(request):
    """
    View para listar todas as receitas cadastradas.
    
    Permite filtrar receitas por período e categoria.
    
    Args:
        request: Objeto HttpRequest do Django
        
    Returns:
        HttpResponse: Renderiza o template com a lista de receitas
    """
    # Obter parâmetros de filtro
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    categoria = request.GET.get('categoria')
    
    # Iniciar query
    receitas = Receita.objects.all().select_related('usuario')
    
    # Aplicar filtros
    if data_inicio:
        receitas = receitas.filter(data__gte=data_inicio)
    if data_fim:
        receitas = receitas.filter(data__lte=data_fim)
    if categoria:
        receitas = receitas.filter(categoria=categoria)
    
    # Calcular total
    total_receitas = receitas.aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
    
    # Preparar contexto
    context = {
        'receitas': receitas,
        'total_receitas': total_receitas,
        'categorias': Receita.CATEGORIAS,
        'filtros': {
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'categoria': categoria,
        }
    }
    
    return render(request, 'financeiro/lista_receitas.html', context)


@login_required
def lista_despesas(request):
    """
    View para listar todas as despesas cadastradas.
    
    Permite filtrar despesas por período e categoria.
    
    Args:
        request: Objeto HttpRequest do Django
        
    Returns:
        HttpResponse: Renderiza o template com a lista de despesas
    """
    # Obter parâmetros de filtro
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    categoria = request.GET.get('categoria')
    
    # Iniciar query
    despesas = Despesa.objects.all().select_related('usuario')
    
    # Aplicar filtros
    if data_inicio:
        despesas = despesas.filter(data__gte=data_inicio)
    if data_fim:
        despesas = despesas.filter(data__lte=data_fim)
    if categoria:
        despesas = despesas.filter(categoria=categoria)
    
    # Calcular total
    total_despesas = despesas.aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
    
    # Preparar contexto
    context = {
        'despesas': despesas,
        'total_despesas': total_despesas,
        'categorias': Despesa.CATEGORIAS,
        'filtros': {
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'categoria': categoria,
        }
    }
    
    return render(request, 'financeiro/lista_despesas.html', context)


@login_required
@permission_required('financeiro.add_receita', raise_exception=True)
def cadastrar_receita(request):
    """
    View para cadastrar uma nova receita.
    
    Args:
        request: Objeto HttpRequest do Django
        
    Returns:
        HttpResponse: Renderiza formulário ou redireciona após salvar
    """
    if request.method == 'POST':
        try:
            # Criar nova receita
            receita = Receita(
                descricao=request.POST.get('descricao'),
                valor=request.POST.get('valor'),
                data=request.POST.get('data'),
                categoria=request.POST.get('categoria', 'OUTROS'),
                usuario=request.user
            )
            receita.save()
            
            # Adicionar ao capital de giro
            CapitalGiro.adicionar_capital(
                valor=receita.valor,
                descricao=f'Receita: {receita.descricao}',
                usuario=request.user
            )
            
            # Mensagem de sucesso
            messages.success(
                request,
                f'Receita de R$ {receita.valor} cadastrada com sucesso!'
            )
            
            return redirect('financeiro:lista_receitas')
            
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar receita: {str(e)}')
    
    # Preparar contexto para o formulário
    context = {
        'categorias': Receita.CATEGORIAS,
        'data_hoje': datetime.now().date(),
    }
    
    return render(request, 'financeiro/cadastrar_receita.html', context)


@login_required
@permission_required('financeiro.add_despesa', raise_exception=True)
def cadastrar_despesa(request):
    """
    View para cadastrar uma nova despesa.
    
    Args:
        request: Objeto HttpRequest do Django
        
    Returns:
        HttpResponse: Renderiza formulário ou redireciona após salvar
    """
    if request.method == 'POST':
        try:
            # Criar nova despesa
            despesa = Despesa(
                descricao=request.POST.get('descricao'),
                valor=request.POST.get('valor'),
                data=request.POST.get('data'),
                categoria=request.POST.get('categoria', 'OUTROS'),
                usuario=request.user
            )
            despesa.save()
            
            # Retirar do capital de giro
            CapitalGiro.retirar_capital(
                valor=despesa.valor,
                descricao=f'Despesa: {despesa.descricao}',
                usuario=request.user
            )
            
            # Mensagem de sucesso
            messages.success(
                request,
                f'Despesa de R$ {despesa.valor} cadastrada com sucesso!'
            )
            
            return redirect('financeiro:lista_despesas')
            
        except ValueError as e:
            # Erro de capital insuficiente
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar despesa: {str(e)}')
    
    # Preparar contexto para o formulário
    context = {
        'categorias': Despesa.CATEGORIAS,
        'data_hoje': datetime.now().date(),
        'capital_atual': CapitalGiro.obter_capital_atual(),
    }
    
    return render(request, 'financeiro/cadastrar_despesa.html', context)


@login_required
@permission_required('financeiro.view_capitalgiro', raise_exception=True)
def gerenciar_capital_giro(request):
    """
    View para gerenciar o capital de giro.
    
    Permite visualizar o histórico e realizar ajustes manuais no capital.
    Acesso restrito a administradores e gerentes.
    
    Args:
        request: Objeto HttpRequest do Django
        
    Returns:
        HttpResponse: Renderiza o template de gerenciamento
    """
    # Obter capital atual
    capital_atual = CapitalGiro.obter_capital_atual()
    
    # Obter histórico de movimentações
    historico = CapitalGiro.objects.all().select_related('usuario')[:50]
    
    # Processar formulário de ajuste
    if request.method == 'POST' and request.user.has_perm('financeiro.add_capitalgiro'):
        try:
            tipo = request.POST.get('tipo')
            valor = Decimal(request.POST.get('valor'))
            descricao = request.POST.get('descricao')
            
            if tipo == 'ENTRADA':
                CapitalGiro.adicionar_capital(
                    valor=valor,
                    descricao=descricao,
                    usuario=request.user
                )
                messages.success(request, f'Capital adicionado: R$ {valor}')
            elif tipo == 'SAIDA':
                CapitalGiro.retirar_capital(
                    valor=valor,
                    descricao=descricao,
                    usuario=request.user
                )
                messages.success(request, f'Capital retirado: R$ {valor}')
            
            return redirect('financeiro:capital_giro')
            
        except ValueError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f'Erro ao ajustar capital: {str(e)}')
    
    # Preparar contexto
    context = {
        'capital_atual': capital_atual,
        'historico': historico,
        'pode_editar': request.user.has_perm('financeiro.add_capitalgiro'),
    }
    
    return render(request, 'financeiro/capital_giro.html', context)


@login_required
def relatorio_financeiro(request):
    """
    View para gerar relatório financeiro completo.
    
    Exibe análises detalhadas incluindo:
    - Evolução de receitas e despesas
    - Análise por categoria
    - Indicadores de desempenho
    - Projeções
    
    Args:
        request: Objeto HttpRequest do Django
        
    Returns:
        HttpResponse: Renderiza o template do relatório
    """
    # Verificar permissão
    if not request.user.has_perm('financeiro.view_receita'):
        messages.error(request, 'Você não tem permissão para acessar relatórios.')
        return redirect('financeiro:dashboard')
    
    # Obter período (últimos 6 meses)
    hoje = datetime.now().date()
    seis_meses_atras = hoje - timedelta(days=180)
    
    # Calcular totais por categoria
    receitas_por_categoria = Receita.objects.filter(
        data__gte=seis_meses_atras
    ).values('categoria').annotate(
        total=Sum('valor')
    ).order_by('-total')
    
    despesas_por_categoria = Despesa.objects.filter(
        data__gte=seis_meses_atras
    ).values('categoria').annotate(
        total=Sum('valor')
    ).order_by('-total')
    
    # Calcular totais gerais
    total_receitas = sum(item['total'] for item in receitas_por_categoria)
    total_despesas = sum(item['total'] for item in despesas_por_categoria)
    resultado = total_receitas - total_despesas
    
    # Preparar contexto
    context = {
        'receitas_por_categoria': receitas_por_categoria,
        'despesas_por_categoria': despesas_por_categoria,
        'total_receitas': total_receitas,
        'total_despesas': total_despesas,
        'resultado': resultado,
        'periodo_inicio': seis_meses_atras,
        'periodo_fim': hoje,
        'capital_atual': CapitalGiro.obter_capital_atual(),
    }
    
    return render(request, 'financeiro/relatorio.html', context)


@login_required
def api_indicadores(request):
    """
    API para retornar indicadores financeiros em JSON.
    
    Útil para gráficos e dashboards dinâmicos.
    
    Args:
        request: Objeto HttpRequest do Django
        
    Returns:
        JsonResponse: Dados dos indicadores em formato JSON
    """
    # Obter período
    meses = int(request.GET.get('meses', 6))
    
    # Calcular dados por mês
    dados = []
    hoje = datetime.now().date()
    
    for i in range(meses):
        # Calcular o primeiro dia do mês
        if hoje.month - i <= 0:
            mes = 12 + (hoje.month - i)
            ano = hoje.year - 1
        else:
            mes = hoje.month - i
            ano = hoje.year
        
        # Calcular totais do mês
        receitas = Receita.objects.filter(
            data__year=ano,
            data__month=mes
        ).aggregate(total=Sum('valor'))['total'] or 0
        
        despesas = Despesa.objects.filter(
            data__year=ano,
            data__month=mes
        ).aggregate(total=Sum('valor'))['total'] or 0
        
        dados.append({
            'mes': f'{mes:02d}/{ano}',
            'receitas': float(receitas),
            'despesas': float(despesas),
            'lucro': float(receitas - despesas)
        })
    
    # Inverter para ordem cronológica
    dados.reverse()
    
    return JsonResponse({'dados': dados})
