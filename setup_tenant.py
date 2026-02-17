"""
Script para configurar a empresa inicial (Tenant) e associar ao usuário admin.
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao_erp.settings')
django.setup()

from django.contrib.auth.models import User
from companies.models import Company, UserCompany
from estoque.models import Produto

def run():
    print("Iniciando configuração de Tenant...")
    
    # Obter ou criar usuário admin
    admin, created = User.objects.get_or_create(username='admin')
    if created:
        admin.set_password('admin123')
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()
        print(f"Usuário 'admin' criado.")
    
    # Criar empresa inicial
    company, created = Company.objects.get_or_create(
        cnpj='00.000.000/0001-91',
        defaults={
            'nome': 'Empresa Matriz ERP',
            'plano': 'ENTERPRISE',
            'admin_principal': admin
        }
    )
    
    if created:
        print(f"Empresa '{company.nome}' criada.")
    else:
        print(f"Empresa '{company.nome}' já existe.")
        
    # Associar admin à empresa
    user_company, created = UserCompany.objects.get_or_create(
        user=admin,
        company=company,
        defaults={'role': 'ADMIN'}
    )
    
    if created:
        print(f"Usuário 'admin' associado à empresa '{company.nome}' como ADMIN.")
    
    # Associar produtos órfãos à empresa matriz
    orphans = Produto.objects.filter(company__isnull=True)
    count = orphans.count()
    if count > 0:
        orphans.update(company=company)
        print(f"{count} produtos órfãos associados à empresa matriz.")
    
    print("Configuração de Tenant concluída!")

if __name__ == "__main__":
    run()
