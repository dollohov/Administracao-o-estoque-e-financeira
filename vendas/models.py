from django.db import models
from django.contrib.auth.models import User
from estoque.models import Produto
from clientes.models import Cliente
from decimal import Decimal

class Pedido(models.Model):
    STATUS_PEDIDO = (
        ("RASCUNHO", "Rascunho"),
        ("PENDENTE", "Pendente"),
        ("APROVADO", "Aprovado"),
        ("CANCELADO", "Cancelado"),
        ("FINALIZADO", "Finalizado"),
    )

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name="pedidos",
        verbose_name="Cliente"
    )
    vendedor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="pedidos_realizados",
        verbose_name="Vendedor"
    )
    data_pedido = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data do Pedido"
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_PEDIDO,
        default="RASCUNHO",
        verbose_name="Status do Pedido"
    )
    observacoes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Observações"
    )
    valor_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name="Valor Total"
    )

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ["-data_pedido"]

    def __str__(self):
        return f"Pedido #{self.pk} - {self.cliente.nome_completo}"

    def calcular_valor_total(self):
        return sum(item.calcular_subtotal() for item in self.itens.all())

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.valor_total = self.calcular_valor_total()
        super().save(update_fields=["valor_total"])


class ItemPedido(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name="itens",
        verbose_name="Pedido"
    )
    produto = models.ForeignKey(
        Produto,
        on_delete=models.PROTECT,
        verbose_name="Produto"
    )
    quantidade = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        verbose_name="Quantidade"
    )
    preco_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Preço Unitário"
    )
    desconto = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name="Desconto (%)"
    )

    class Meta:
        verbose_name = "Item do Pedido"
        verbose_name_plural = "Itens do Pedido"

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome} em Pedido #{self.pedido.pk}"

    def calcular_subtotal(self):
        valor_bruto = self.quantidade * self.preco_unitario
        valor_com_desconto = valor_bruto * (1 - (self.desconto / 100))
        return round(valor_com_desconto, 2)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.pedido.save() # Atualiza o valor total do pedido quando um item é salvo/alterado
