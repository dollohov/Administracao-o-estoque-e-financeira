from django.urls import path
from . import views

app_name = 'auditoria'

urlpatterns = [
    path('dashboard/', views.dashboard_auditoria, name='dashboard'),
    path('acessos-sensiveis/', views.relatorio_acessos_sensiveis, name='acessos_sensiveis'),
    path('solicitacoes-lgpd/', views.gerenciar_solicitacoes_lgpd, name='solicitacoes_lgpd'),
]
