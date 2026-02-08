"""
Modelos estendidos do módulo Financeiro.

Este arquivo define modelos adicionais para Contas a Pagar, Contas a Receber
e Fluxo de Caixa Projetado.

Autor: Manus AI
Data: 2026-02-08
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.utils import timezone


class ContaPagar(models.Model):
    """
    Modelo que representa uma conta a pagar (obrigação financeira).
    
    Attributes:
        fornecedor: Fornecedor a quem se deve pagar
        descricao: Descrição da conta
        valor: Valor a pagar
        data_vencimento: Data de vencimento da conta
        data_pagamento: Data em que foi pago (se aplicável)
        status: Status do pagamento
        usuario_criacao: Usuário que criou o registro
        data_criacao: Data de criação
    """
    
    STATUS_CHOICES = (
        ('PENDENTE', 'Pendente'),
        ('PAGO', 'Pago'),
        ('ATRASADO', 'Atrasado'),
        ('CANCELADO', 'Cancelado'),
    )
    
    fornecedor = models.ForeignKey(
        'fiscal.Fornecedor',
        on_delete=models.PROTECT,
        related_name='contas_pagar',
        verbose_name="Fornecedor"
    )
    
    descricao = models.CharField(
        max_length=200,
        verbose_name="Descrição"
    )
    
    valor = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Valor"
    )
    
    data_vencimento = models.DateField(
        verbose_name="Data de Vencimento"
    )
    
    data_pagamento = models.DateField(
        blank=True,
        null=True,
        verbose_name="Data de Pagamento"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDENTE',
        verbose_name="Status"
    )
    
    usuario_criacao = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='contas_pagar_criadas',
        default=1,
        verbose_name="Criado por"
    )
    
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )
    
    class Meta:
        verbose_name = "Conta a Pagar"
        verbose_name_plural = "Contas a Pagar"
        ordering = ['data_vencimento']
    
    def __str__(self):
        return f"{self.fornecedor} - R$ {self.valor}"
    
    @property
    def dias_para_vencer(self):
        """Retorna o número de dias até o vencimento."""
        from datetime import date
        delta = self.data_vencimento - date.today()
        return delta.days
    
    @property
    def esta_atrasada(self):
        """Verifica se a conta está atrasada."""
        from datetime import date
        return self.status == 'PENDENTE' and self.data_vencimento < date.today()


class ContaReceber(models.Model):
    """
    Modelo que representa uma conta a receber (direito financeiro).
    
    Attributes:
        cliente: Cliente que deve pagar
        descricao: Descrição da conta
        valor: Valor a receber
        data_vencimento: Data de vencimento
        data_recebimento: Data em que foi recebido
        status: Status do recebimento
        usuario_criacao: Usuário que criou o registro
        data_criacao: Data de criação
    """
    
    STATUS_CHOICES = (
        ('PENDENTE', 'Pendente'),
        ('RECEBIDO', 'Recebido'),
        ('ATRASADO', 'Atrasado'),
        ('CANCELADO', 'Cancelado'),
    )
    
    cliente = models.ForeignKey(
        'clientes.Cliente',
        on_delete=models.PROTECT,
        related_name='contas_receber',
        verbose_name="Cliente"
    )
    
    descricao = models.CharField(
        max_length=200,
        verbose_name="Descrição"
    )
    
    valor = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Valor"
    )
    
    data_vencimento = models.DateField(
        verbose_name="Data de Vencimento"
    )
    
    data_recebimento = models.DateField(
        blank=True,
        null=True,
        verbose_name="Data de Recebimento"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDENTE',
        verbose_name="Status"
    )
    
    usuario_criacao = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='contas_receber_criadas',
        default=1,
        verbose_name="Criado por"
    )
    
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )
    
    class Meta:
        verbose_name = "Conta a Receber"
        verbose_name_plural = "Contas a Receber"
        ordering = ['data_vencimento']
    
    def __str__(self):
        return f"{self.cliente} - R$ {self.valor}"
    
    @property
    def dias_para_vencer(self):
        """Retorna o número de dias até o vencimento."""
        from datetime import date
        delta = self.data_vencimento - date.today()
        return delta.days
    
    @property
    def esta_atrasada(self):
        """Verifica se a conta está atrasada."""
        from datetime import date
        return self.status == 'PENDENTE' and self.data_vencimento < date.today()


class FluxoCaixaProjetado(models.Model):
    """
    Modelo que representa uma projeção de fluxo de caixa.
    
    Attributes:
        mes: Mês da projeção
        ano: Ano da projeção
        receitas_projetadas: Total de receitas esperadas
        despesas_projetadas: Total de despesas esperadas
        saldo_projetado: Saldo esperado (receitas - despesas)
        receitas_reais: Receitas reais no período
        despesas_reais: Despesas reais no período
        saldo_real: Saldo real (receitas - despesas)
    """
    
    mes = models.IntegerField(
        choices=[(i, f"Mês {i}") for i in range(1, 13)],
        verbose_name="Mês"
    )
    
    ano = models.IntegerField(
        verbose_name="Ano"
    )
    
    receitas_projetadas = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Receitas Projetadas"
    )
    
    despesas_projetadas = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Despesas Projetadas"
    )
    
    receitas_reais = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Receitas Reais"
    )
    
    despesas_reais = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Despesas Reais"
    )
    
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )
    
    data_atualizacao = models.DateTimeField(
        auto_now=True,
        verbose_name="Data de Atualização"
    )
    
    class Meta:
        verbose_name = "Fluxo de Caixa Projetado"
        verbose_name_plural = "Fluxos de Caixa Projetados"
        ordering = ['-ano', '-mes']
        unique_together = ('mes', 'ano')
    
    def __str__(self):
        return f"Fluxo de Caixa - {self.mes}/{self.ano}"
    
    @property
    def saldo_projetado(self):
        """Calcula o saldo projetado."""
        return self.receitas_projetadas - self.despesas_projetadas
    
    @property
    def saldo_real(self):
        """Calcula o saldo real."""
        return self.receitas_reais - self.despesas_reais
    
    @property
    def variacao(self):
        """Calcula a variação entre projetado e real."""
        return self.saldo_real - self.saldo_projetado
