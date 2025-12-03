"""
URLs do módulo Financeiro.

Define as rotas (URLs) para as views do módulo financeiro.

Autor: Manus AI
Data: 2025-12-02
"""

from django.urls import path
from . import views

# Namespace para as URLs do financeiro
app_name = 'financeiro'

urlpatterns = [
    # Dashboard principal do financeiro
    path('', views.dashboard_financeiro, name='dashboard'),
    
    # Gestão de receitas
    path('receitas/', views.lista_receitas, name='lista_receitas'),
    path('receitas/cadastrar/', views.cadastrar_receita, name='cadastrar_receita'),
    
    # Gestão de despesas
    path('despesas/', views.lista_despesas, name='lista_despesas'),
    path('despesas/cadastrar/', views.cadastrar_despesa, name='cadastrar_despesa'),
    
    # Capital de giro
    path('capital-giro/', views.gerenciar_capital_giro, name='capital_giro'),
    
    # Relatórios
    path('relatorio/', views.relatorio_financeiro, name='relatorio'),
    
    # API para gráficos
    path('api/indicadores/', views.api_indicadores, name='api_indicadores'),
]
