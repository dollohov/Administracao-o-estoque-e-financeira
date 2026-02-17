import os
import django
import sys

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao_erp.settings')
django.setup()

from django.apps import apps
from django.db import connection

def check_tables():
    print("🔍 Verificando integridade das tabelas do banco de dados...")
    
    all_models = apps.get_models()
    missing_tables = []
    
    with connection.cursor() as cursor:
        # Obter lista de tabelas existentes
        table_list = connection.introspection.table_names(cursor)
        
        for model in all_models:
            table_name = model._meta.db_table
            if table_name not in table_list:
                # Alguns modelos proxy ou abstratos não têm tabelas
                if not model._meta.abstract and not model._meta.proxy:
                    missing_tables.append(f"{model._meta.label} ({table_name})")
    
    if missing_tables:
        print("❌ Tabelas Faltando:")
        for table in missing_tables:
            print(f"  - {table}")
        return False
    else:
        print("✅ Todas as tabelas dos modelos foram encontradas no banco de dados.")
        return True

def check_modules():
    print("\n🔍 Verificando carregamento dos módulos principais...")
    modules = [
        'estoque', 'financeiro', 'fiscal', 'fornecedores', 
        'clientes', 'pdv', 'auditoria', 'vendas', 
        'relatorios', 'notificacoes', 'companies'
    ]
    
    failed = []
    for mod in modules:
        try:
            apps.get_app_config(mod)
            print(f"✅ Módulo '{mod}' carregado com sucesso.")
        except Exception as e:
            print(f"❌ Falha ao carregar módulo '{mod}': {e}")
            failed.append(mod)
            
    return len(failed) == 0

if __name__ == "__main__":
    tables_ok = check_tables()
    modules_ok = check_modules()
    
    if tables_ok and modules_ok:
        print("\n🚀 INTEGRIDADE DE PRODUÇÃO VALIDADA!")
        sys.exit(0)
    else:
        print("\n⚠️ FALHAS DE INTEGRIDADE DETECTADAS!")
        sys.exit(1)
