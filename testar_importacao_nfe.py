"""
Script para testar a importação de NF-e.

Este script demonstra como usar o processador de NF-e programaticamente.

Uso:
    python testar_importacao_nfe.py
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao_erp.settings')
django.setup()

from django.contrib.auth.models import User
from fiscal.nfe_processor import NFEProcessor
from fiscal.models import NotaFiscalEletronica, Fornecedor

def testar_importacao():
    """Testa a importação do arquivo de exemplo."""
    
    print("=" * 60)
    print("TESTE DE IMPORTAÇÃO DE NF-e")
    print("=" * 60)
    print()
    
    # Obter usuário admin
    try:
        usuario = User.objects.get(username='admin')
        print(f"✓ Usuário encontrado: {usuario.username}")
    except User.DoesNotExist:
        print("✗ Usuário 'admin' não encontrado!")
        print("  Execute: python manage.py createsuperuser")
        return
    
    # Verificar arquivo de exemplo
    xml_path = 'exemplo_nfe.xml'
    if not os.path.exists(xml_path):
        print(f"✗ Arquivo {xml_path} não encontrado!")
        return
    
    print(f"✓ Arquivo XML encontrado: {xml_path}")
    print()
    
    # Processar NF-e
    print("Processando NF-e...")
    print("-" * 60)
    
    with open(xml_path, 'rb') as xml_file:
        processor = NFEProcessor(xml_file, usuario)
        sucesso, mensagem, nfe = processor.processar()
    
    print()
    if sucesso:
        print("✓ SUCESSO!")
        print(f"  {mensagem}")
        print()
        print("Detalhes da NF-e:")
        print(f"  - Número: {nfe.numero}/{nfe.serie}")
        print(f"  - Fornecedor: {nfe.fornecedor}")
        print(f"  - Valor Total: R$ {nfe.valor_total}")
        print(f"  - Itens: {nfe.itens.count()}")
        print(f"  - Status: {nfe.get_status_display()}")
        print()
        print("Itens importados:")
        for item in nfe.itens.all():
            print(f"  - {item.descricao}")
            print(f"    Quantidade: {item.quantidade}")
            print(f"    Valor Unit.: R$ {item.valor_unitario}")
            print(f"    Produto criado: {'Sim' if item.criado_automaticamente else 'Não'}")
    else:
        print("✗ ERRO!")
        print(f"  {mensagem}")
    
    print()
    print("=" * 60)
    print("Estatísticas do Sistema:")
    print("=" * 60)
    print(f"Total de NF-es: {NotaFiscalEletronica.objects.count()}")
    print(f"Total de Fornecedores: {Fornecedor.objects.count()}")
    print(f"NF-es Processadas: {NotaFiscalEletronica.objects.filter(status='PROCESSADA').count()}")
    print(f"NF-es com Erro: {NotaFiscalEletronica.objects.filter(status='ERRO').count()}")
    print()

if __name__ == '__main__':
    testar_importacao()
