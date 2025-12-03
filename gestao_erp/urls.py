"""
URLs principais do projeto Gestão ERP.

Define as rotas principais e inclui as URLs dos módulos.

Autor: Manus AI
Data: 2025-12-02
"""

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    """
    View da página inicial do sistema.
    
    Redireciona para o dashboard apropriado baseado nas permissões do usuário.
    
    Args:
        request: Objeto HttpRequest do Django
        
    Returns:
        HttpResponse: Renderiza o template da página inicial
    """
    # Verificar grupo do usuário para personalizar a página inicial
    usuario = request.user
    
    # Contexto para o template
    context = {
        'usuario': usuario,
        'is_admin': usuario.groups.filter(name='Administradores').exists(),
        'is_gerente': usuario.groups.filter(name='Gerentes').exists(),
        'is_funcionario': usuario.groups.filter(name='Funcionários').exists(),
    }
    
    return render(request, 'index.html', context)


# URLs principais do projeto
urlpatterns = [
    # Página inicial
    path('', index, name='index'),
    
    # Painel de administração do Django
    path('admin/', admin.site.urls),
    
    # Autenticação
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    
    path('logout/', auth_views.LogoutView.as_view(
        next_page='login'
    ), name='logout'),
    
    # Módulos do sistema
    path('estoque/', include('estoque.urls')),
    path('financeiro/', include('financeiro.urls')),
]
