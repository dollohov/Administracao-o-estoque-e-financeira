from django.urls import path
from . import views

app_name = 'estoque'
urlpatterns = [
    path('produtos/', views.lista_produtos, name='lista_produtos'),
]
