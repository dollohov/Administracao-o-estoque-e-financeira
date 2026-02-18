"""
Middleware para identificação e isolamento de empresa (Tenant).

Este middleware identifica a empresa atual do usuário logado e a armazena
no objeto request para uso global nas views e modelos.

Autor: Denis Barbosa (Todos os direitos reservados)
Data: 2026-02-17
"""

from .models import UserCompany

class TenantMiddleware:
    """
    Identifica a empresa ativa do usuário logado.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Se o usuário não estiver autenticado, não há empresa
        if not request.user.is_authenticated:
            request.company = None
            return self.get_response(request)
        
        # Tenta obter a empresa ativa da sessão (se o usuário puder estar em várias)
        # Por padrão, pega a primeira empresa associada ao usuário
        user_company = UserCompany.objects.filter(user=request.user, company__active=True).first()
        
        if user_company:
            request.company = user_company.company
            request.user_role = user_company.role
        else:
            request.company = None
            request.user_role = None
            
        return self.get_response(request)
