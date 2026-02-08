from django.urls import path
from . import views

app_name = 'notificacoes'

urlpatterns = [
    path('', views.lista_notificacoes, name='lista'),
    path('<int:pk>/marcar-lida/', views.marcar_como_lida, name='marcar_lida'),
    path('marcar-todas-lidas/', views.marcar_todas_lidas, name='marcar_todas_lidas'),
    path('api/nao-lidas/', views.api_notificacoes_nao_lidas, name='api_nao_lidas'),
]
