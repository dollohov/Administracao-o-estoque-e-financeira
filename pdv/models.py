from django.db import models
from django.contrib.auth.models import User
from estoque.models import Produto
from clientes.models import Cliente
from decimal import Decimal

class Venda(models.Model):
    """
    Modelo para armazenar vendas realizadas no PDV.
    
    Atributos:
        numero_venda: Número sequencial da venda
        cliente: Cliente que realizou a compra (opcional)
        data_venda: Data e hora da venda
        total_itens: Total de itens vendidos
        subtotal: Subtotal da venda (sem descontos)
        desconto: Valor de desconto aplicado
        total: Total da venda (com descontos)
        metodo_pagamento: Método de pagamento utilizado
        usuario: Usuário que realizou a venda
        observacoes: Observações sobre a venda
    """
    
    METODO_PAGAMENTO_CHOICES = [
        ('DINHEIRO', 'Dinheiro'),
        ('CARTAO_CREDITO', 'Cartão de Crédito'),
        ('CARTAO_DEBITO', 'Cartão de Débito'),
        ('PIX', 'PIX'),
        ('BOLETO', 'Boleto'),
        ('CHEQUE', 'Cheque'),
        ('CREDITO_LOJA', 'Crédito em Loja'),
    ]
    
    numero_venda = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='vendas'
    )
    data_venda = models.DateTimeField(auto_now_add=True, db_index=True)
    total_itens = models.IntegerField(default=0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    metodo_pagamento = models.CharField(max_length=20, choices=METODO_PAGAMENTO_CHOICES)
    usuario = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='vendas_realizadas'
    )
    observacoes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'pdv_venda'
        verbose_name = 'Venda'
        verbose_name_plural = 'Vendas'
        ordering = ['-data_venda']
        indexes = [
            models.Index(fields=['-data_venda']),
            models.Index(fields=['usuario', '-data_venda']),
        ]
    
    def __str__(self):
        return f"Venda #{self.numero_venda} - {self.data_venda.strftime('%d/%m/%Y %H:%M')}"
    
    def calcular_total(self):
        """Calcula o total da venda baseado nos itens."""
        self.subtotal = sum(item.subtotal for item in self.itens.all())
        self.total = self.subtotal - self.desconto
        return self.total


class ItemVenda(models.Model):
    """
    Modelo para armazenar itens de uma venda.
    
    Atributos:
        venda: Referência para a venda
        produto: Produto vendido
        quantidade: Quantidade vendida
        preco_unitario: Preço unitário do produto na venda
        subtotal: Subtotal do item (quantidade * preço_unitario)
    """
    
    venda = models.ForeignKey(
        Venda,
        on_delete=models.CASCADE,
        related_name='itens'
    )
    produto = models.ForeignKey(
        Produto,
        on_delete=models.PROTECT,
        related_name='vendas_pdv'
    )
    quantidade = models.IntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'pdv_item_venda'
        verbose_name = 'Item de Venda'
        verbose_name_plural = 'Itens de Venda'
    
    def __str__(self):
        return f"{self.produto.nome} x{self.quantidade} - Venda #{self.venda.numero_venda}"
    
    def save(self, *args, **kwargs):
        """Calcula o subtotal antes de salvar."""
        self.subtotal = self.quantidade * self.preco_unitario
        super().save(*args, **kwargs)


class Caixa(models.Model):
    """
    Modelo para controlar o caixa do PDV.
    
    Atributos:
        data_abertura: Data e hora de abertura do caixa
        data_fechamento: Data e hora de fechamento do caixa
        usuario_abertura: Usuário que abriu o caixa
        usuario_fechamento: Usuário que fechou o caixa
        valor_inicial: Valor inicial do caixa
        valor_final: Valor final do caixa
        total_vendas: Total de vendas no período
        diferenca: Diferença entre o valor final e esperado
    """
    
    data_abertura = models.DateTimeField(auto_now_add=True)
    data_fechamento = models.DateTimeField(null=True, blank=True)
    usuario_abertura = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='caixas_abertos'
    )
    usuario_fechamento = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='caixas_fechados'
    )
    valor_inicial = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_final = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_vendas = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    diferenca = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    class Meta:
        db_table = 'pdv_caixa'
        verbose_name = 'Caixa'
        verbose_name_plural = 'Caixas'
        ordering = ['-data_abertura']
    
    def __str__(self):
        status = "Fechado" if self.data_fechamento else "Aberto"
        return f"Caixa {status} - {self.data_abertura.strftime('%d/%m/%Y %H:%M')}"
    
    def fechar_caixa(self, valor_final):
        """Fecha o caixa com o valor final."""
        self.valor_final = valor_final
        self.data_fechamento = models.functions.Now()
        self.diferenca = valor_final - (self.valor_inicial + self.total_vendas)
        self.save()
