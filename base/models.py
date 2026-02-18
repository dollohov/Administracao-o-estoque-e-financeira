"""
Modelos Base para o Sistema ERP.

Este arquivo define a classe abstrata TenantModel, que serve como base
para todos os modelos que necessitam de isolamento por empresa.

Autor: Denis Barbosa (Todos os direitos reservados) 
Data: 2026-02-17
"""

from django.db import models
from companies.models import Company

class TenantModel(models.Model):
    """
    Classe pai abstrata para garantir que cada registro no banco de dados
    tenha um 'dono' (Company).
    
    Aplica o princípio DRY (Don't Repeat Yourself).
    """
    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE, 
        related_name="%(class)s_related",
        verbose_name="Empresa"
    )

    class Meta:
        abstract = True # Isso diz ao Django para não criar uma tabela para esta classe
