#!/usr/bin/env python3
"""
Script de teste automatizado para verificar todos os módulos do sistema.
Testa importações, models, views e URLs.
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao_erp.settings')
django.setup()

from django.core.exceptions import ImproperlyConfigured
from django.urls import get_resolver
from django.apps import apps
import importlib

def test_imports():
    """Testa se todos os módulos podem ser importados."""
    print("\n" + "="*80)
    print("TESTE 1: IMPORTAÇÃO DE MÓDULOS")
    print("="*80)
    
    modules_to_test = [
        'estoque.models',
        'estoque.views',
        'financeiro.models',
        'financeiro.views',
        'fiscal.views',
        'fornecedores.models',
        'fornecedores.views',
        'clientes.models',
        'clientes.views',
        'pdv.views',
        'vendas.views',
        'relatorios.views',
        'notificacoes.views',
        'auditoria.views',
        'companies.models',
        'base.views',
    ]
    
    errors = []
    for module_name in modules_to_test:
        try:
            importlib.import_module(module_name)
            print(f"✅ {module_name}")
        except Exception as e:
            print(f"❌ {module_name}: {str(e)}")
            errors.append((module_name, str(e)))
    
    return errors

def test_models():
    """Testa se todos os models estão corretamente configurados."""
    print("\n" + "="*80)
    print("TESTE 2: VALIDAÇÃO DE MODELS")
    print("="*80)
    
    errors = []
    for app_config in apps.get_app_configs():
        if app_config.name in ['estoque', 'financeiro', 'fornecedores', 'clientes', 'companies']:
            try:
                models = app_config.get_models()
                for model in models:
                    # Tenta fazer uma query simples
                    try:
                        model.objects.count()
                        print(f"✅ {app_config.name}.{model.__name__}")
                    except Exception as e:
                        print(f"❌ {app_config.name}.{model.__name__}: {str(e)}")
                        errors.append((f"{app_config.name}.{model.__name__}", str(e)))
            except Exception as e:
                print(f"❌ {app_config.name}: {str(e)}")
                errors.append((app_config.name, str(e)))
    
    return errors

def test_urls():
    """Testa se todas as URLs estão corretamente configuradas."""
    print("\n" + "="*80)
    print("TESTE 3: VALIDAÇÃO DE URLs")
    print("="*80)
    
    errors = []
    try:
        resolver = get_resolver()
        url_patterns = resolver.url_patterns
        print(f"✅ Total de padrões de URL encontrados: {len(url_patterns)}")
        
        # Testa algumas URLs específicas importantes
        important_urls = [
            '/',
            '/estoque/',
            '/financeiro/',
            '/fiscal/',
            '/fornecedores/',
            '/clientes/',
        ]
        
        for url in important_urls:
            try:
                match = resolver.resolve(url)
                print(f"✅ URL '{url}' -> {match.view_name}")
            except Exception as e:
                print(f"❌ URL '{url}': {str(e)}")
                errors.append((url, str(e)))
                
    except Exception as e:
        print(f"❌ Erro ao carregar URLs: {str(e)}")
        errors.append(("URL Resolver", str(e)))
    
    return errors

def test_views():
    """Testa se as views principais podem ser importadas."""
    print("\n" + "="*80)
    print("TESTE 4: VALIDAÇÃO DE VIEWS")
    print("="*80)
    
    errors = []
    views_to_test = [
        ('estoque.views', ['produto_list', 'produto_create']),
        ('financeiro.views', ['dashboard_financeiro']),
        ('fornecedores.views', ['fornecedor_list']),
        ('clientes.views', ['cliente_list']),
    ]
    
    for module_name, view_names in views_to_test:
        try:
            module = importlib.import_module(module_name)
            for view_name in view_names:
                if hasattr(module, view_name):
                    print(f"✅ {module_name}.{view_name}")
                else:
                    print(f"⚠️  {module_name}.{view_name} não encontrada")
                    errors.append((f"{module_name}.{view_name}", "View não encontrada"))
        except Exception as e:
            print(f"❌ {module_name}: {str(e)}")
            errors.append((module_name, str(e)))
    
    return errors

def test_settings():
    """Testa configurações críticas do Django."""
    print("\n" + "="*80)
    print("TESTE 5: VALIDAÇÃO DE CONFIGURAÇÕES")
    print("="*80)
    
    from django.conf import settings
    
    errors = []
    
    # Testa configurações críticas
    critical_settings = [
        'SECRET_KEY',
        'DEBUG',
        'ALLOWED_HOSTS',
        'DATABASES',
        'INSTALLED_APPS',
        'MIDDLEWARE',
        'TEMPLATES',
    ]
    
    for setting in critical_settings:
        if hasattr(settings, setting):
            value = getattr(settings, setting)
            print(f"✅ {setting}: {type(value).__name__}")
        else:
            print(f"❌ {setting}: não configurado")
            errors.append((setting, "Configuração não encontrada"))
    
    # Verifica apps instalados
    print(f"\n📦 Apps instalados: {len(settings.INSTALLED_APPS)}")
    for app in settings.INSTALLED_APPS:
        if not app.startswith('django.'):
            print(f"   - {app}")
    
    return errors

def main():
    """Executa todos os testes."""
    print("\n" + "="*80)
    print("INICIANDO TESTES AUTOMATIZADOS DO SISTEMA")
    print("="*80)
    
    all_errors = []
    
    # Executa todos os testes
    all_errors.extend(test_imports())
    all_errors.extend(test_models())
    all_errors.extend(test_urls())
    all_errors.extend(test_views())
    all_errors.extend(test_settings())
    
    # Relatório final
    print("\n" + "="*80)
    print("RELATÓRIO FINAL")
    print("="*80)
    
    if all_errors:
        print(f"\n❌ TOTAL DE ERROS ENCONTRADOS: {len(all_errors)}\n")
        for item, error in all_errors:
            print(f"  • {item}")
            print(f"    └─ {error}\n")
        return 1
    else:
        print("\n✅ TODOS OS TESTES PASSARAM COM SUCESSO!")
        print("✅ O sistema está funcionando corretamente!\n")
        return 0

if __name__ == '__main__':
    sys.exit(main())
