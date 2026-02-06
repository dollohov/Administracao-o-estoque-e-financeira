from django.urls import path
from . import views

app_name = 'fornecedores'

urlpatterns = [
    path('', views.lista_fornecedores, name='lista_fornecedores'),
    path('novo/', views.novo_fornecedor, name='novo_fornecedor'),
    path('<int:pk>/', views.detalhe_fornecedor, name='detalhe_fornecedor'),
    path('<int:pk>/editar/', views.editar_fornecedor, name='editar_fornecedor'),
    path('<int:pk>/excluir/', views.excluir_fornecedor, name='excluir_fornecedor'),
]
