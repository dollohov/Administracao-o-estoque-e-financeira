#!/usr/bin/env python
"""
Script para criar e aplicar migracoes das melhorias.

Este script deve ser executado apos as alteracoes nos modelos:
- Adicao de campos LGPD ao modelo Cliente
- Adicao de campos fiscais ao modelo Produto

Uso:
    python criar_migracao_melhorias.py
"""

import os
import sys
import django
from django.core.management import call_command

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao_erp.settings')
django.setup()

def criar_migracao():
    """Cria as migracoes para os modelos alterados."""
    
    print("=" * 70)
    print("CRIANDO MIGRACOES PARA MELHORIAS DO ERP")
    print("=" * 70)
    print()
    
    apps_para_migrar = ['clientes', 'estoque', 'financeiro']
    
    for app in apps_para_migrar:
        print(f"Criando migracao para {app}...")
        try:
            call_command('makemigrations', app, verbosity=2)
            print(f"✓ Migracao criada para {app}")
        except Exception as e:
            print(f"✗ Erro ao criar migracao para {app}: {str(e)}")
        print()
    
    print("=" * 70)
    print("APLICANDO MIGRACOES")
    print("=" * 70)
    print()
    
    try:
        call_command('migrate', verbosity=2)
        print("✓ Todas as migracoes foram aplicadas com sucesso!")
    except Exception as e:
        print(f"✗ Erro ao aplicar migracoes: {str(e)}")
        return False
    
    print()
    print("=" * 70)
    print("RESUMO DAS MELHORIAS IMPLEMENTADAS")
    print("=" * 70)
    print()
    print("1. LGPD - Conformidade com Lei Geral de Protecao de Dados:")
    print("   - Campo: consentimento_marketing")
    print("   - Campo: consentimento_dados")
    print("   - Campo: data_consentimento")
    print("   - Campo: anonimizado")
    print("   - Campo: data_anonimizacao")
    print("   - Metodo: anonimizar_dados()")
    print()
    print("2. Campos Fiscais no Estoque:")
    print("   - Campo: sku (Stock Keeping Unit)")
    print("   - Campo: ncm (Nomenclatura Comum do Mercosul)")
    print("   - Campo: ean_gtin (Codigo de barras)")
    print("   - Campo: localizacao_estoque")
    print()
    print("3. Novos Processadores e Views:")
    print("   - fiscal/nfe_processor_v2.py (Processador melhorado de NF-e)")
    print("   - pdv/views_v2.py (PDV com suporte a codigo de barras)")
    print()
    print("=" * 70)
    
    return True


if __name__ == '__main__':
    sucesso = criar_migracao()
    sys.exit(0 if sucesso else 1)
