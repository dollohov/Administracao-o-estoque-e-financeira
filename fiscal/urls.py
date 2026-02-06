"""
URLs do módulo Fiscal.

Autor: Manus AI
Data: 2026-02-05
"""

from django.urls import path
from . import views

app_name = 'fiscal'

urlpatterns = [
    # Dashboard
    path('', views.dashboard_fiscal, name='dashboard'),
    
    # NF-e
    path('importar/', views.importar_nfe, name='importar_nfe'),
    path('nfes/', views.lista_nfes, name='lista_nfes'),
    path('nfes/<int:pk>/', views.detalhe_nfe, name='detalhe_nfe'),
    
    # Fornecedores
    path('fornecedores/', views.lista_fornecedores, name='lista_fornecedores'),
    path('fornecedores/<int:pk>/', views.detalhe_fornecedor, name='detalhe_fornecedor'),
]
