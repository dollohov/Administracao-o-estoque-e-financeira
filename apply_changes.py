"""
Script para aplicar migrações e mudanças de banco de dados.
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao_erp.settings')
django.setup()

from django.core.management import call_command

def run():
    print("Gerando migrações para os novos apps e alterações...")
    call_command('makemigrations', 'companies')
    call_command('makemigrations', 'estoque')
    call_command('makemigrations', 'clientes')
    call_command('makemigrations', 'fornecedores')
    call_command('makemigrations', 'financeiro')
    
    print("Aplicando migrações ao banco de dados...")
    call_command('migrate')
    
    print("Concluído com sucesso!")

if __name__ == "__main__":
    run()
