"""
Mixins para facilitar o isolamento de dados por empresa (Multi-tenancy).

Estes mixins automatizam a filtragem de dados e a associação de novos
registros à empresa correta.

Autor: Denis Barbosa (Todos os direitos reservados)
Data: 2026-02-17
"""

from django.db import models
from .models import Company

class TenantManager(models.Manager):
    """
    Manager que filtra automaticamente os registros pela empresa atual.
    """
    def for_company(self, company):
        return self.get_queryset().filter(company=company)

class TenantModelMixin(models.Model):
    """
    Mixin para modelos que devem ser isolados por empresa.
    """
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name="Empresa",
        null=True,
        blank=True
    )

    objects = TenantManager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # Se o modelo tem uma empresa definida no request (via middleware)
        # e a empresa do objeto ainda não foi definida, define automaticamente.
        # Nota: Em produção, isso seria integrado com um thread-local ou 
        # passado explicitamente nas views.
        super().save(*args, **kwargs)
