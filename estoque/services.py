from django.db import transaction
from .models import MovimentacaoEstoque, Produto
from financeiro.models import CapitalGiro

class EstoqueService:
    @staticmethod
    def registrar_movimentacao(produto_id, tipo, quantidade, valor_unitario, usuario, observacao=''):
        """
        Registra uma movimentação de estoque e realiza o lançamento financeiro correspondente.
        Garante a atomicidade da operação: ou ambos (estoque e financeiro) são atualizados, ou nenhum.
        """
        with transaction.atomic():
            # 1. Obter o produto (com lock para evitar race conditions)
            produto = Produto.objects.select_for_update().get(pk=produto_id)
            
            # 2. Criar a movimentação de estoque
            # O método save() de MovimentacaoEstoque já trata a atualização do estoque_atual do Produto
            movimentacao = MovimentacaoEstoque(
                produto=produto,
                tipo=tipo,
                quantidade=quantidade,
                valor_unitario=valor_unitario,
                observacao=observacao,
                usuario=usuario
            )
            movimentacao.save()
            
            # 3. Calcular valor total para o financeiro
            valor_total = movimentacao.calcular_valor_total()
            
            # 4. Realizar lançamento no Capital de Giro
            if tipo == 'ENTRADA':
                # Entrada no estoque = Saída de capital (compra)
                CapitalGiro.retirar_capital(
                    valor=valor_total,
                    descricao=f'Compra de {quantidade}x {produto.nome}',
                    usuario=usuario
                )
            elif tipo == 'SAIDA':
                # Saída do estoque = Entrada de capital (venda)
                CapitalGiro.adicionar_capital(
                    valor=valor_total,
                    descricao=f'Venda de {quantidade}x {produto.nome}',
                    usuario=usuario
                )
            
            return movimentacao
