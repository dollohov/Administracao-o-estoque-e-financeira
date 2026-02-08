from django.urls import path
from . import views

app_name = 'relatorios'

urlpatterns = [
    path('dashboard/', views.dashboard_relatorios, name='dashboard'),
    path('curva-abc/', views.curva_abc, name='curva_abc'),
    path('previsao-estoque/', views.previsao_estoque, name='previsao_estoque'),
    path('vendas-performance/', views.vendas_performance, name='vendas_performance'),
    path('financeiro-saude/', views.financeiro_saude, name='financeiro_saude'),
]
