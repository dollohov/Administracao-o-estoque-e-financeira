"""
Script para criar as migrações necessárias após as atualizações dos modelos.

Este script deve ser executado após atualizar os modelos para gerar
as migrações do banco de dados.

Autor: Manus AI
Data: 2025-12-02
"""

import os
import sys

# Adicionar o diretório do projeto ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao_erp.settings')

import django
django.setup()

from django.core.management import call_command

print("="*70)
print("CRIANDO MIGRAÇÕES PARA OS MODELOS ATUALIZADOS")
print("="*70)

# Criar migrações
print("\n1. Criando migrações...")
call_command('makemigrations', verbosity=2)

print("\n2. Aplicando migrações...")
call_command('migrate', verbosity=2)

print("\n" + "="*70)
print("MIGRAÇÕES CONCLUÍDAS COM SUCESSO!")
print("="*70)
