from django.shortcuts import render
from .models import Receita

def lista_receitas(request):
    receitas = Receita.objects.all()
    return render(request, 'financeiro/lista_receitas.html', {'receitas': receitas})
