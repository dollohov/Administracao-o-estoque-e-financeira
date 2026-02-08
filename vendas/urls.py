from django.urls import path
from . import views

app_name = 'vendas'

urlpatterns = [
    path('pedidos/', views.lista_pedidos, name='lista_pedidos'),
    path('pedidos/novo/', views.criar_pedido, name='criar_pedido'),
    path('pedidos/<int:pk>/', views.detalhe_pedido, name='detalhe_pedido'),
    path('pedidos/<int:pk>/editar/', views.editar_pedido, name='editar_pedido'),
    path('pedidos/<int:pk>/gerar_pdf/', views.gerar_pedido_pdf, name='gerar_pedido_pdf'),
    path('pedidos/<int:pk>/whatsapp/', views.enviar_whatsapp, name='enviar_whatsapp'),
]
