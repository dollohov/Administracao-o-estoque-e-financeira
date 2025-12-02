from django.urls import path
from . import views

app_name = 'financeiro'
urlpatterns = [
    path('receitas/', views.lista_receitas, name='lista_receitas'),
]
