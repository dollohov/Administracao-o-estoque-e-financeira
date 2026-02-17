#!/usr/bin/env python3
"""
Script de teste funcional para verificar todas as funcionalidades do sistema.
Testa operações CRUD, lógica de negócio e integrações.
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao_erp.settings')
django.setup()

from django.contrib.auth.models import User
from django.test import RequestFactory
from decimal import Decimal
from datetime import datetime

# Importar models
from estoque.models import Produto, MovimentacaoEstoque, CategoriaProduto
from financeiro.models import Receita, Despesa, CapitalGiro
from fornecedores.models import Fornecedor
from clientes.models import Cliente
from companies.models import Company

def test_company_creation():
    """Testa criação de empresa."""
    print("\n" + "="*80)
    print("TESTE 1: CRIAÇÃO DE EMPRESA")
    print("="*80)
    
    try:
        company, created = Company.objects.get_or_create(
            name="Empresa Teste",
            defaults={
                'cnpj': '12.345.678/0001-99',
                'plano': 'BASIC',
                'active': True
            }
        )
        if created:
            print(f"✅ Empresa criada: {company.name}")
        else:
            print(f"✅ Empresa já existe: {company.name}")
        return company, []
    except Exception as e:
        print(f"❌ Erro ao criar empresa: {str(e)}")
        return None, [("Company Creation", str(e))]

def test_user_creation(company):
    """Testa criação de usuário."""
    print("\n" + "="*80)
    print("TESTE 2: CRIAÇÃO DE USUÁRIO")
    print("="*80)
    
    try:
        user, created = User.objects.get_or_create(
            username='teste_user',
            defaults={
                'email': 'teste@user.com',
                'first_name': 'Teste',
                'last_name': 'User'
            }
        )
        if created:
            user.set_password('teste123')
            user.save()
            print(f"✅ Usuário criado: {user.username}")
        else:
            print(f"✅ Usuário já existe: {user.username}")
        
        # Associar usuário à empresa
        from companies.models import UserCompany
        uc, created = UserCompany.objects.get_or_create(
            user=user,
            company=company,
            defaults={'role': 'admin'}
        )
        print(f"✅ Usuário associado à empresa")
        
        return user, []
    except Exception as e:
        print(f"❌ Erro ao criar usuário: {str(e)}")
        return None, [("User Creation", str(e))]

def test_fornecedor_crud(company, user):
    """Testa operações CRUD de fornecedor."""
    print("\n" + "="*80)
    print("TESTE 3: CRUD DE FORNECEDOR")
    print("="*80)
    
    errors = []
    
    try:
        # CREATE
        fornecedor, created = Fornecedor.objects.get_or_create(
            cnpj='98765432000188',
            company=company,
            defaults={
                'razao_social': 'Fornecedor Teste Ltda',
                'nome_fantasia': 'Fornecedor Teste',
                'email': 'contato@fornecedor.com',
                'telefone': '11988888888',
                'criado_por': user
            }
        )
        if created:
            print(f"✅ CREATE: Fornecedor criado - {fornecedor.razao_social}")
        else:
            print(f"✅ CREATE: Fornecedor já existe - {fornecedor.razao_social}")
        
        # READ
        fornecedor_lido = Fornecedor.objects.get(id=fornecedor.id)
        print(f"✅ READ: Fornecedor lido - {fornecedor_lido.razao_social}")
        
        # UPDATE
        fornecedor.telefone = '11977777777'
        fornecedor.modificado_por = user
        fornecedor.save()
        print(f"✅ UPDATE: Telefone atualizado - {fornecedor.telefone}")
        
        # LIST
        total_fornecedores = Fornecedor.objects.filter(company=company).count()
        print(f"✅ LIST: Total de fornecedores - {total_fornecedores}")
        
        return fornecedor, errors
        
    except Exception as e:
        print(f"❌ Erro no CRUD de fornecedor: {str(e)}")
        errors.append(("Fornecedor CRUD", str(e)))
        return None, errors

def test_cliente_crud(company, user):
    """Testa operações CRUD de cliente."""
    print("\n" + "="*80)
    print("TESTE 4: CRUD DE CLIENTE")
    print("="*80)
    
    errors = []
    
    try:
        # CREATE
        cliente, created = Cliente.objects.get_or_create(
            cpf_cnpj='12345678901',
            company=company,
            defaults={
                'nome': 'Cliente Teste',
                'email': 'cliente@teste.com',
                'telefone': '11966666666',
                'criado_por': user
            }
        )
        if created:
            print(f"✅ CREATE: Cliente criado - {cliente.nome}")
        else:
            print(f"✅ CREATE: Cliente já existe - {cliente.nome}")
        
        # READ
        cliente_lido = Cliente.objects.get(id=cliente.id)
        print(f"✅ READ: Cliente lido - {cliente_lido.nome}")
        
        # UPDATE
        cliente.telefone = '11955555555'
        cliente.modificado_por = user
        cliente.save()
        print(f"✅ UPDATE: Telefone atualizado - {cliente.telefone}")
        
        # LIST
        total_clientes = Cliente.objects.filter(company=company).count()
        print(f"✅ LIST: Total de clientes - {total_clientes}")
        
        return cliente, errors
        
    except Exception as e:
        print(f"❌ Erro no CRUD de cliente: {str(e)}")
        errors.append(("Cliente CRUD", str(e)))
        return None, errors

def test_produto_crud(company, user):
    """Testa operações CRUD de produto."""
    print("\n" + "="*80)
    print("TESTE 5: CRUD DE PRODUTO")
    print("="*80)
    
    errors = []
    
    try:
        # CREATE
        produto, created = Produto.objects.get_or_create(
            sku='PROD001',
            company=company,
            defaults={
                'nome': 'Produto Teste',
                'descricao': 'Descrição do produto teste',
                'preco_custo': Decimal('10.00'),
                'preco_venda': Decimal('20.00'),
                'estoque_atual': 100,
                'estoque_minimo': 10,
                'criado_por': user
            }
        )
        if created:
            print(f"✅ CREATE: Produto criado - {produto.nome}")
        else:
            print(f"✅ CREATE: Produto já existe - {produto.nome}")
        
        # READ
        produto_lido = Produto.objects.get(id=produto.id)
        print(f"✅ READ: Produto lido - {produto_lido.nome}")
        
        # UPDATE
        produto.preco_venda = Decimal('25.00')
        produto.modificado_por = user
        produto.save()
        print(f"✅ UPDATE: Preço atualizado - R$ {produto.preco_venda}")
        
        # Calcular valor total do estoque
        valor_total = produto.valor_total_estoque()
        print(f"✅ CÁLCULO: Valor total em estoque - R$ {valor_total}")
        
        # Calcular margem de lucro
        margem = produto.margem_lucro()
        print(f"✅ CÁLCULO: Margem de lucro - {margem}%")
        
        # LIST
        total_produtos = Produto.objects.filter(company=company).count()
        print(f"✅ LIST: Total de produtos - {total_produtos}")
        
        return produto, errors
        
    except Exception as e:
        print(f"❌ Erro no CRUD de produto: {str(e)}")
        errors.append(("Produto CRUD", str(e)))
        return None, errors

def test_movimentacao_estoque(produto, user):
    """Testa movimentação de estoque."""
    print("\n" + "="*80)
    print("TESTE 6: MOVIMENTAÇÃO DE ESTOQUE")
    print("="*80)
    
    errors = []
    
    try:
        estoque_inicial = produto.estoque_atual
        print(f"📦 Estoque inicial: {estoque_inicial}")
        
        # ENTRADA
        movimentacao_entrada = MovimentacaoEstoque.objects.create(
            produto=produto,
            tipo='ENTRADA',
            quantidade=50,
            valor_unitario=Decimal('10.00'),
            observacao='Entrada de teste',
            usuario=user
        )
        produto.refresh_from_db()
        print(f"✅ ENTRADA: +50 unidades - Estoque atual: {produto.estoque_atual}")
        
        # SAÍDA
        movimentacao_saida = MovimentacaoEstoque.objects.create(
            produto=produto,
            tipo='SAIDA',
            quantidade=20,
            valor_unitario=Decimal('25.00'),
            observacao='Saída de teste',
            usuario=user
        )
        produto.refresh_from_db()
        print(f"✅ SAÍDA: -20 unidades - Estoque atual: {produto.estoque_atual}")
        
        # Verificar histórico
        total_movimentacoes = MovimentacaoEstoque.objects.filter(produto=produto).count()
        print(f"✅ HISTÓRICO: Total de movimentações - {total_movimentacoes}")
        
        return True, errors
        
    except Exception as e:
        print(f"❌ Erro na movimentação de estoque: {str(e)}")
        errors.append(("Movimentação Estoque", str(e)))
        return False, errors

def test_financeiro(company, user):
    """Testa módulo financeiro."""
    print("\n" + "="*80)
    print("TESTE 7: MÓDULO FINANCEIRO")
    print("="*80)
    
    errors = []
    
    try:
        # RECEITA
        receita = Receita.objects.create(
            company=company,
            descricao='Venda de teste',
            valor=Decimal('500.00'),
            data=datetime.now().date(),
            categoria='VENDAS',
            criado_por=user
        )
        print(f"✅ RECEITA: Criada - R$ {receita.valor}")
        
        # DESPESA
        despesa = Despesa.objects.create(
            company=company,
            descricao='Compra de teste',
            valor=Decimal('200.00'),
            data=datetime.now().date(),
            categoria='COMPRAS',
            criado_por=user
        )
        print(f"✅ DESPESA: Criada - R$ {despesa.valor}")
        
        # CAPITAL DE GIRO
        capital, created = CapitalGiro.objects.get_or_create(
            company=company,
            defaults={'saldo_atual': Decimal('1000.00')}
        )
        print(f"✅ CAPITAL DE GIRO: Saldo - R$ {capital.saldo_atual}")
        
        # Calcular resultado
        total_receitas = Receita.objects.filter(company=company).aggregate(
            total=models.Sum('valor')
        )['total'] or Decimal('0')
        
        total_despesas = Despesa.objects.filter(company=company).aggregate(
            total=models.Sum('valor')
        )['total'] or Decimal('0')
        
        resultado = total_receitas - total_despesas
        print(f"✅ RESULTADO: Receitas R$ {total_receitas} - Despesas R$ {total_despesas} = R$ {resultado}")
        
        return True, errors
        
    except Exception as e:
        print(f"❌ Erro no módulo financeiro: {str(e)}")
        errors.append(("Financeiro", str(e)))
        return False, errors

def main():
    """Executa todos os testes funcionais."""
    print("\n" + "="*80)
    print("INICIANDO TESTES FUNCIONAIS DO SISTEMA")
    print("="*80)
    
    all_errors = []
    
    # Executar testes em sequência
    company, errors = test_company_creation()
    all_errors.extend(errors)
    
    if company:
        user, errors = test_user_creation(company)
        all_errors.extend(errors)
        
        if user:
            fornecedor, errors = test_fornecedor_crud(company, user)
            all_errors.extend(errors)
            
            cliente, errors = test_cliente_crud(company, user)
            all_errors.extend(errors)
            
            produto, errors = test_produto_crud(company, user)
            all_errors.extend(errors)
            
            if produto:
                _, errors = test_movimentacao_estoque(produto, user)
                all_errors.extend(errors)
            
            _, errors = test_financeiro(company, user)
            all_errors.extend(errors)
    
    # Relatório final
    print("\n" + "="*80)
    print("RELATÓRIO FINAL DOS TESTES FUNCIONAIS")
    print("="*80)
    
    if all_errors:
        print(f"\n❌ TOTAL DE ERROS ENCONTRADOS: {len(all_errors)}\n")
        for item, error in all_errors:
            print(f"  • {item}")
            print(f"    └─ {error}\n")
        return 1
    else:
        print("\n✅ TODOS OS TESTES FUNCIONAIS PASSARAM COM SUCESSO!")
        print("✅ Todas as operações CRUD e lógica de negócio estão funcionando!\n")
        return 0

if __name__ == '__main__':
    from django.db import models
    sys.exit(main())
