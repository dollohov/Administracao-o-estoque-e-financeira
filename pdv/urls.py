from django.urls import path
from . import views

app_name = 'pdv'

urlpatterns = [
    path('', views.dashboard_pdv, name='dashboard'),
    path('nova-venda/', views.nova_venda, name='nova_venda'),
    path('venda/<int:pk>/', views.detalhes_venda, name='detalhes_venda'),
    path('abrir-caixa/', views.abrir_caixa, name='abrir_caixa'),
    path('fechar-caixa/', views.fechar_caixa, name='fechar_caixa'),
    path('api/buscar-produto/', views.buscar_produto, name='buscar_produto'),
]
