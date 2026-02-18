"""
Modelos do módulo de Empresas (Multi-tenancy).

Este arquivo define a entidade principal de Empresa (Tenant) que servirá
como base para o isolamento de dados no sistema SaaS.

Autor: Denis Barbosa (Todos os direitos reservados) 
Data: 2026-02-17
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Company(models.Model):
    """
    Modelo que representa uma Empresa (Tenant) no sistema.
    
    Cada empresa possui seus próprios dados isolados (estoque, financeiro, etc).
    """
    
    PLANOS = (
        ('BASIC', 'Plano Básico'),
        ('PROFESSIONAL', 'Plano Profissional'),
        ('ENTERPRISE', 'Plano Empresarial'),
    )
    
    name = models.CharField(
        max_length=255,
        verbose_name="Nome da Empresa"
    )
    
    cnpj = models.CharField(
        max_length=18,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$',
                message='CNPJ inválido. Formato: 00.000.000/0000-00'
            )
        ],
        verbose_name="CNPJ"
    )
    
    plano = models.CharField(
        max_length=20,
        choices=PLANOS,
        default='BASIC',
        verbose_name="Plano Atual"
    )
    
    active = models.BooleanField(
        default=True,
        verbose_name="Empresa Ativa"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Cadastro"
    )
    
    # Administrador principal da empresa
    admin_principal = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='empresas_administradas',
        verbose_name="Administrador Principal",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ['name']

    def __str__(self):
        return self.name

class UserCompany(models.Model):
    """
    Relacionamento entre usuários e empresas.
    Permite que um usuário pertença a uma ou mais empresas.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_companies')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_users')
    
    ROLE_CHOICES = (
        ('ADMIN', 'Administrador'),
        ('MANAGER', 'Gerente'),
        ('STAFF', 'Funcionário'),
        ('SELLER', 'Vendedor'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='STAFF')
    
    class Meta:
        unique_together = ('user', 'company')
        verbose_name = "Usuário da Empresa"
        verbose_name_plural = "Usuários das Empresas"
