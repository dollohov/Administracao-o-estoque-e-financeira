import os
import django
import threading
from decimal import Decimal
import time

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao_erp.settings')
django.setup()

from django.contrib.auth.models import User
from estoque.models import Produto, MovimentacaoEstoque
from estoque.services import EstoqueService
from companies.models import Company, UserCompany
from financeiro.models import CapitalGiro

def run_stress_test():
    print("🚀 Iniciando Teste de Estresse de Estoque...")
    
    # 1. Setup de dados de teste
    company, _ = Company.objects.get_or_create(
        name="Stress Test Company",
        defaults={'cnpj': '00.000.000/0001-00'}
    )
    
    user, created = User.objects.get_or_create(username='stress_user')
    if created:
        user.set_password('pass123')
        user.save()
    
    UserCompany.objects.get_or_create(user=user, company=company, defaults={'role': 'ADMIN'})
    
    # Resetar dados de teste
    Produto.objects.filter(company=company, nome="Stress Test Product").delete()
    CapitalGiro.objects.filter(company=company).delete()

    # Criar produto com estoque inicial 100
    produto = Produto.objects.create(
        company=company,
        nome="Stress Test Product",
        preco_custo=Decimal('10.00'),
        preco_venda=Decimal('20.00'),
        estoque_atual=100,
        usuario_criacao=user
    )
    
    # Inicializar capital de giro
    CapitalGiro.adicionar_capital(company, Decimal('1000.00'), "Initial Capital", user)
    
    errors = []
    
    def simulate_sales(num_sales, thread_id):
        for i in range(num_sales):
            success = False
            retries = 10
            while not success and retries > 0:
                try:
                    EstoqueService.registrar_movimentacao(
                        produto_id=produto.id,
                        tipo='SAIDA',
                        quantidade=1,
                        valor_unitario=20.00,
                        usuario=user,
                        observacao=f"Sale {i} from thread {thread_id}"
                    )
                    success = True
                except Exception as e:
                    if "database is locked" in str(e):
                        retries -= 1
                        time.sleep(0.1)
                    else:
                        errors.append(f"Thread {thread_id} - Sale {i}: {str(e)}")
                        break
            if not success and retries == 0:
                errors.append(f"Thread {thread_id} - Sale {i}: database is locked after retries")

    # Simular 5 threads tentando vender 20 itens cada (total 100)
    threads = []
    for i in range(5):
        t = threading.Thread(target=simulate_sales, args=(20, i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # Verificar resultados finais
    produto.refresh_from_db()
    final_capital = CapitalGiro.obter_capital_atual(company)
    
    print("\n--- Resultados do Teste de Estresse ---")
    print(f"Estoque Final: {produto.estoque_atual} (Esperado: 0)")
    print(f"Capital Final: R$ {final_capital} (Esperado: R$ 3000.00)")
    print(f"Total de Erros: {len(errors)}")
    
    if produto.estoque_atual == 0 and final_capital == Decimal('3000.00'):
        print("\n✅ TESTE DE ESTRESSE PASSOU! Concorrência tratada corretamente.")
        return True
    else:
        print("\n❌ TESTE DE ESTRESSE FALHOU! Problemas de concorrência detectados.")
        for err in errors[:5]: print(f"  - {err}")
        return False

if __name__ == "__main__":
    # Limpar dados anteriores se necessário ou usar banco em memória
    # Para simplificar, vamos rodar no banco atual (sqlite)
    run_stress_test()
