"""
Script para configurar grupos de usuários e permissões do sistema ERP.

Este script cria três grupos principais:
1. Administradores - Acesso total ao sistema
2. Gerentes - Acesso a relatórios e visualização
3. Funcionários - Operações básicas de estoque

Autor: Manus AI
Data: 2025-12-02
"""

import os
import django

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao_erp.settings')
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from estoque.models import Produto, MovimentacaoEstoque
from financeiro.models import Receita, Despesa


def criar_grupos_e_permissoes():
    """
    Cria os grupos de usuários e atribui as permissões apropriadas.
    
    Returns:
        dict: Dicionário com os grupos criados
    """
    print("Iniciando configuração de grupos e permissões...")
    
    # Limpar grupos existentes (opcional - comentar se quiser manter)
    # Group.objects.all().delete()
    
    # ========================================
    # GRUPO: ADMINISTRADORES
    # ========================================
    grupo_admin, created = Group.objects.get_or_create(name='Administradores')
    if created:
        print("✓ Grupo 'Administradores' criado")
    
    # Administradores têm todas as permissões
    todas_permissoes = Permission.objects.all()
    grupo_admin.permissions.set(todas_permissoes)
    print(f"  - {todas_permissoes.count()} permissões atribuídas aos Administradores")
    
    # ========================================
    # GRUPO: GERENTES
    # ========================================
    grupo_gerente, created = Group.objects.get_or_create(name='Gerentes')
    if created:
        print("✓ Grupo 'Gerentes' criado")
    
    # Gerentes podem visualizar tudo e editar alguns itens
    permissoes_gerente = []
    
    # Permissões de visualização (view) para todos os modelos
    permissoes_gerente.extend(Permission.objects.filter(codename__startswith='view_'))
    
    # Permissões de adição e edição para estoque
    permissoes_gerente.extend(Permission.objects.filter(
        codename__in=[
            'add_movimentacaoestoque',
            'change_movimentacaoestoque',
            'add_produto',
            'change_produto'
        ]
    ))
    
    # Permissões de adição para financeiro
    permissoes_gerente.extend(Permission.objects.filter(
        codename__in=[
            'add_receita',
            'add_despesa',
            'change_receita',
            'change_despesa'
        ]
    ))
    
    grupo_gerente.permissions.set(permissoes_gerente)
    print(f"  - {len(permissoes_gerente)} permissões atribuídas aos Gerentes")
    
    # ========================================
    # GRUPO: FUNCIONÁRIOS
    # ========================================
    grupo_funcionario, created = Group.objects.get_or_create(name='Funcionários')
    if created:
        print("✓ Grupo 'Funcionários' criado")
    
    # Funcionários podem apenas visualizar produtos e adicionar movimentações
    permissoes_funcionario = Permission.objects.filter(
        codename__in=[
            'view_produto',
            'view_movimentacaoestoque',
            'add_movimentacaoestoque',
            'view_receita',  # Podem ver receitas de vendas
        ]
    )
    
    grupo_funcionario.permissions.set(permissoes_funcionario)
    print(f"  - {permissoes_funcionario.count()} permissões atribuídas aos Funcionários")
    
    print("\n✓ Configuração de grupos e permissões concluída com sucesso!")
    
    return {
        'administradores': grupo_admin,
        'gerentes': grupo_gerente,
        'funcionarios': grupo_funcionario
    }


def criar_usuarios_exemplo():
    """
    Cria usuários de exemplo para cada grupo (opcional).
    
    ATENÇÃO: Use apenas em ambiente de desenvolvimento!
    """
    from django.contrib.auth.models import User
    
    print("\nCriando usuários de exemplo...")
    
    # Criar ou obter grupos
    grupo_admin = Group.objects.get(name='Administradores')
    grupo_gerente = Group.objects.get(name='Gerentes')
    grupo_funcionario = Group.objects.get(name='Funcionários')
    
    # Usuário Administrador
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_user(
            username='admin',
            email='admin@empresa.com',
            password='admin123',
            first_name='Administrador',
            last_name='Sistema',
            is_staff=True,
            is_superuser=True
        )
        admin.groups.add(grupo_admin)
        print("✓ Usuário 'admin' criado (senha: admin123)")
    
    # Usuário Gerente
    if not User.objects.filter(username='gerente').exists():
        gerente = User.objects.create_user(
            username='gerente',
            email='gerente@empresa.com',
            password='gerente123',
            first_name='João',
            last_name='Gerente',
            is_staff=True
        )
        gerente.groups.add(grupo_gerente)
        print("✓ Usuário 'gerente' criado (senha: gerente123)")
    
    # Usuário Funcionário
    if not User.objects.filter(username='funcionario').exists():
        funcionario = User.objects.create_user(
            username='funcionario',
            email='funcionario@empresa.com',
            password='func123',
            first_name='Maria',
            last_name='Vendedora',
            is_staff=True
        )
        funcionario.groups.add(grupo_funcionario)
        print("✓ Usuário 'funcionario' criado (senha: func123)")
    
    print("\n✓ Usuários de exemplo criados com sucesso!")


if __name__ == '__main__':
    # Executar configuração de grupos e permissões
    criar_grupos_e_permissoes()
    
    # Descomentar a linha abaixo para criar usuários de exemplo
    criar_usuarios_exemplo()
    
    print("\n" + "="*50)
    print("CONFIGURAÇÃO CONCLUÍDA!")
    print("="*50)
    print("\nGrupos disponíveis:")
    print("  1. Administradores - Acesso total")
    print("  2. Gerentes - Visualização e edição limitada")
    print("  3. Funcionários - Operações básicas")
    print("\nPara atribuir um usuário a um grupo:")
    print("  user.groups.add(grupo)")
