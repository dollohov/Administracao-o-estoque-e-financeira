"""
URLs para a API REST do módulo de Estoque.

Autor: Manus AI
Data: 2025-12-07
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import ProdutoViewSet, MovimentacaoEstoqueViewSet

# Criar router para ViewSets
router = DefaultRouter()
router.register(r'produtos', ProdutoViewSet, basename='produto')
router.register(r'movimentacoes', MovimentacaoEstoqueViewSet, basename='movimentacao')

# URLs da API
urlpatterns = [
    path('', include(router.urls)),
]
