from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2)
    estoque_atual = models.IntegerField(default=0)

    def __str__(self):
        return self.nome

class MovimentacaoEstoque(models.Model):
    TIPO_MOVIMENTACAO = (
        ('ENTRADA', 'Entrada'),
        ('SAIDA', 'Saída'),
    )
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=7, choices=TIPO_MOVIMENTACAO)
    quantidade = models.IntegerField()
    data_movimentacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo} de {self.quantidade}x {self.produto.nome}"

    class Meta:
        verbose_name = "Movimentação de Estoque"
        verbose_name_plural = "Movimentações de Estoque"
