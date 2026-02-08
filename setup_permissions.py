"""
Script para configurar grupos de usuários e permissões do sistema ERP.

Este script cria quatro grupos principais:
1. Administradores - Acesso total ao sistema
2. Gerentes - Acesso a relatórios e visualização
3. Funcionários - Operações básicas de estoque
4. Vendedores - Acesso exclusivo ao Catálogo de Produtos

Autor: Manus AI
Data: 2026-02-08
"""

import os
import django

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao_erp.settings')
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


def criar_grupos_e_permissoes():
    """
    Cria os grupos de usuários e atribui as permissões apropriadas.
    """
    print("Iniciando configuração de grupos e permissões...")
    
    # ========================================
    # GRUPO: ADMINISTRADORES
    # ========================================
    grupo_admin, created = Group.objects.get_or_create(name='Administradores')
    if created:
        print("✓ Grupo 'Administradores' criado")
    
    todas_permissoes = Permission.objects.all()
    grupo_admin.permissions.set(todas_permissoes)
    print(f"  - {todas_permissoes.count()} permissões atribuídas aos Administradores")
    
    # ========================================
    # GRUPO: GERENTES
    # ========================================
    grupo_gerente, created = Group.objects.get_or_create(name='Gerentes')
    if created:
        print("✓ Grupo 'Gerentes' criado")
    
    permissoes_gerente = Permission.objects.filter(
        codename__in=[
            'view_produto', 'add_produto', 'change_produto',
            'view_movimentacaoestoque', 'add_movimentacaoestoque',
            'view_receita', 'add_receita', 'change_receita',
            'view_despesa', 'add_despesa', 'change_despesa',
            'view_fornecedor', 'add_fornecedor', 'change_fornecedor',
            'view_cliente', 'add_cliente', 'change_cliente',
        ]
    )
    grupo_gerente.permissions.set(permissoes_gerente)
    print(f"  - {permissoes_gerente.count()} permissões atribuídas aos Gerentes")
    
    # ========================================
    # GRUPO: VENDEDORES (Novo)
    # ========================================
    grupo_vendedor, created = Group.objects.get_or_create(name='Vendedores')
    if created:
        print("✓ Grupo 'Vendedores' criado")
    
    # Vendedores podem apenas visualizar produtos (Catálogo)
    permissoes_vendedor = Permission.objects.filter(
        codename__in=[
            'view_produto',
        ]
    )
    grupo_vendedor.permissions.set(permissoes_vendedor)
    print(f"  - {permissoes_vendedor.count()} permissões atribuídas aos Vendedores")
    
    print("\n✓ Configuração concluída!")


def criar_usuarios_exemplo():
    from django.contrib.auth.models import User
    
    # Usuário Vendedor de Exemplo
    if not User.objects.filter(username='vendedor').exists():
        vendedor = User.objects.create_user(
            username='vendedor',
            email='vendedor@empresa.com',
            password='vendedor123',
            first_name='Carlos',
            last_name='Vendedor',
            is_staff=True
        )
        grupo_vendedor = Group.objects.get(name='Vendedores')
        vendedor.groups.add(grupo_vendedor)
        print("✓ Usuário 'vendedor' criado (senha: vendedor123)")


if __name__ == '__main__':
    criar_grupos_e_permissoes()
    criar_usuarios_exemplo()
