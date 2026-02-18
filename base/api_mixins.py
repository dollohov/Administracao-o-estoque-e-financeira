"""
Mixins para a API REST do Sistema ERP.

Garante que as consultas da API respeitem o isolamento por empresa (Multi-tenancy).

Autor: Denis Barbosa (Todos os direitos reservados)
"""

from rest_framework import serializers

class TenantViewSetMixin:
    """
    Mixin para ViewSets que garante o isolamento de dados por empresa.
    
    Filtra o queryset automaticamente baseado na empresa do usuário logado.
    Também associa a empresa automaticamente ao criar novos registros.
    """
    
    def get_queryset(self):
        """
        Sobrescreve o queryset padrão para filtrar pela empresa do usuário.
        """
        user = self.request.user
        
        # Se for superusuário, pode ver tudo (opcional, dependendo da regra de negócio)
        # if user.is_superuser:
        #     return super().get_queryset()
            
        # Obter a empresa associada ao usuário através do UserCompany
        try:
            user_company = user.user_companies.first()
            if user_company:
                return super().get_queryset().filter(company=user_company.company)
        except AttributeError:
            pass
            
        # Se não houver empresa associada, retorna queryset vazio por segurança
        return super().get_queryset().none()

    def perform_create(self, serializer):
        """
        Associa automaticamente a empresa do usuário ao criar um novo registro.
        """
        user = self.request.user
        user_company = user.user_companies.first()
        
        if user_company:
            serializer.save(company=user_company.company)
        else:
            # Se o modelo exigir company e o usuário não tiver uma, 
            # o Django lançará um erro de integridade, o que é o comportamento esperado.
            serializer.save()
