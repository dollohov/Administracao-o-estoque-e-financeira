"""
URLs do módulo de Estoque.

Define as rotas (URLs) para as views do módulo de estoque.

Autor: Manus AI
Data: 2025-12-02
"""

from django.urls import path
from . import views

# Namespace para as URLs do estoque
app_name = 'estoque'

urlpatterns = [
    # Dashboard principal do estoque
    path('', views.dashboard_estoque, name='dashboard'),
    
    # Gestão de produtos
    path('produtos/', views.lista_produtos, name='lista_produtos'),
    path('produtos/<int:produto_id>/', views.detalhes_produto, name='detalhes_produto'),
    path('produtos/cadastrar/', views.cadastrar_produto, name='cadastrar_produto'),
    
    # Movimentações de estoque
    path('movimentacao/', views.registrar_movimentacao, name='registrar_movimentacao'),
    
    # Relatórios
    path('relatorio/', views.relatorio_estoque, name='relatorio'),
]
