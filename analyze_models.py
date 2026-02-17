#!/usr/bin/env python3
"""
Script para analisar e documentar todos os campos dos modelos.
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao_erp.settings')
django.setup()

from django.apps import apps

def analyze_model(model):
    """Analisa um modelo e retorna seus campos."""
    fields = {}
    for field in model._meta.get_fields():
        if hasattr(field, 'get_internal_type'):
            fields[field.name] = {
                'type': field.get_internal_type(),
                'null': getattr(field, 'null', False),
                'blank': getattr(field, 'blank', False),
            }
    return fields

def main():
    models_to_analyze = [
        ('estoque', 'Produto'),
        ('fornecedores', 'Fornecedor'),
        ('clientes', 'Cliente'),
        ('financeiro', 'Receita'),
        ('financeiro', 'Despesa'),
    ]
    
    for app_label, model_name in models_to_analyze:
        try:
            model = apps.get_model(app_label, model_name)
            print(f"\n{'='*80}")
            print(f"MODELO: {app_label}.{model_name}")
            print('='*80)
            
            fields = analyze_model(model)
            for field_name, field_info in sorted(fields.items()):
                print(f"  {field_name:30} | {field_info['type']:20} | null={field_info['null']}, blank={field_info['blank']}")
        except Exception as e:
            print(f"Erro ao analisar {app_label}.{model_name}: {e}")

if __name__ == '__main__':
    main()
