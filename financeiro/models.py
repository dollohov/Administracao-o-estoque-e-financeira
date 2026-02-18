"""
Modelos do módulo Financeiro.

Este arquivo define os modelos de dados relacionados ao controle financeiro,
incluindo receitas, despesas, capital de giro e indicadores financeiros.

Autor: Denis Barbosa (Todos os direitos reservados)
Data: 2025-12-02
"""

from django.db import models
from django.contrib.auth.models import User
from base.models import TenantModel
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from django.db.models import Sum


class Receita(TenantModel):
    """
    Modelo que representa uma receita (entrada de dinheiro).
    """
    CATEGORIAS = (('VENDA', 'Venda de Produtos'), ('SERVICO', 'Prestação de Serviços'), ('INVESTIMENTO', 'Retorno de Investimento'), ('OUTROS', 'Outros'))
    descricao = models.CharField(max_length=200, verbose_name="Descrição")
    valor = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], verbose_name="Valor")
    data = models.DateField(verbose_name="Data do Recebimento")
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, default='VENDA', verbose_name="Categoria")
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name='receitas_registradas', verbose_name="Registrado por")
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Registro")

    class Meta:
        verbose_name = "Receita"
        verbose_name_plural = "Receitas"
        ordering = ['-data']

    def __str__(self):
        return f"Receita: {self.descricao} (R$ {self.valor})"


class Despesa(TenantModel):
    """
    Modelo que representa uma despesa (saída de dinheiro).
    """
    CATEGORIAS = (('COMPRA', 'Compra de Mercadorias'), ('OPERACIONAL', 'Custos Operacionais'), ('SALARIO', 'Salários e Encargos'), ('IMPOSTO', 'Impostos e Taxas'), ('OUTROS', 'Outros'))
    descricao = models.CharField(max_length=200, verbose_name="Descrição")
    valor = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], verbose_name="Valor")
    data = models.DateField(verbose_name="Data do Pagamento")
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, default='COMPRA', verbose_name="Categoria")
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name='despesas_registradas', verbose_name="Registrado por")
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Registro")

    class Meta:
        verbose_name = "Despesa"
        verbose_name_plural = "Despesas"
        ordering = ['-data']

    def __str__(self):
        return f"Despesa: {self.descricao} (R$ {self.valor})"


class CapitalGiro(TenantModel):
    """
    Modelo que representa o histórico de capital de giro da empresa.
    """
    data_movimentacao = models.DateTimeField(auto_now_add=True)
    tipo_movimentacao = models.CharField(max_length=20)
    valor_anterior = models.DecimalField(max_digits=12, decimal_places=2)
    valor_novo = models.DecimalField(max_digits=12, decimal_places=2)
    descricao = models.CharField(max_length=255)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Movimentação de Capital"
        verbose_name_plural = "Movimentações de Capital"
        ordering = ['-data_movimentacao']

    @classmethod
    def obter_capital_atual(cls, company):
        """Retorna o saldo atual do capital de giro da empresa."""
        ultima = cls.objects.filter(company=company).first()
        return ultima.valor_novo if ultima else Decimal('0.00')

    @classmethod
    def adicionar_capital(cls, company, valor, descricao, usuario):
        """Registra uma entrada no capital de giro."""
        valor = Decimal(str(valor))
        valor_anterior = cls.obter_capital_atual(company)
        valor_novo = valor_anterior + valor
        
        return cls.objects.create(
            company=company,
            tipo_movimentacao='ENTRADA',
            valor_anterior=valor_anterior,
            valor_novo=valor_novo,
            descricao=descricao,
            usuario=usuario
        )

    @classmethod
    def retirar_capital(cls, company, valor, descricao, usuario):
        """Registra uma saída no capital de giro."""
        valor = Decimal(str(valor))
        valor_anterior = cls.obter_capital_atual(company)
        valor_novo = valor_anterior - valor
        
        return cls.objects.create(
            company=company,
            tipo_movimentacao='SAIDA',
            valor_anterior=valor_anterior,
            valor_novo=valor_novo,
            descricao=descricao,
            usuario=usuario
        )


class IndicadorFinanceiro(TenantModel):
    """
    Modelo que representa os indicadores financeiros calculados por período.
    """
    periodo = models.DateField()
    total_receitas = models.DecimalField(max_digits=12, decimal_places=2)
    total_despesas = models.DecimalField(max_digits=12, decimal_places=2)
    lucro_bruto = models.DecimalField(max_digits=12, decimal_places=2)
    margem_lucro = models.DecimalField(max_digits=5, decimal_places=2)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Indicador Financeiro"
        verbose_name_plural = "Indicadores Financeiros"


class ContaPagar(TenantModel):
    """
    Modelo que representa uma conta a pagar.
    """
    fornecedor = models.ForeignKey('fornecedores.Fornecedor', on_delete=models.PROTECT)
    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()
    data_pagamento = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=(('PENDENTE', 'Pendente'), ('PAGO', 'Pago'), ('ATRASADO', 'Atrasado')), default='PENDENTE')
    usuario_criacao = models.ForeignKey(User, on_delete=models.PROTECT)
    data_criacao = models.DateTimeField(auto_now_add=True)

    @property
    def dias_para_vencer(self):
        from datetime import date
        if self.status == 'PAGO': return 0
        delta = self.data_vencimento - date.today()
        return delta.days

    class Meta:
        verbose_name = "Conta a Pagar"
        verbose_name_plural = "Contas a Pagar"


class ContaReceber(TenantModel):
    """
    Modelo que representa uma conta a receber.
    """
    cliente = models.ForeignKey('clientes.Cliente', on_delete=models.PROTECT)
    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()
    data_recebimento = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=(('PENDENTE', 'Pendente'), ('RECEBIDO', 'Recebido'), ('ATRASADO', 'Atrasado')), default='PENDENTE')
    usuario_criacao = models.ForeignKey(User, on_delete=models.PROTECT)
    data_criacao = models.DateTimeField(auto_now_add=True)

    @property
    def dias_para_vencer(self):
        from datetime import date
        if self.status == 'RECEBIDO': return 0
        delta = self.data_vencimento - date.today()
        return delta.days

    class Meta:
        verbose_name = "Conta a Receber"
        verbose_name_plural = "Contas a Receber"


class FluxoCaixaProjetado(TenantModel):
    """
    Modelo que representa o fluxo de caixa projetado por mês/ano.
    """
    mes = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    ano = models.IntegerField()
    receitas_projetadas = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    despesas_projetadas = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    receitas_reais = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    despesas_reais = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    @property
    def saldo_projetado(self):
        return self.receitas_projetadas - self.despesas_projetadas

    @property
    def saldo_real(self):
        return self.receitas_reais - self.despesas_reais

    @property
    def variacao(self):
        return self.saldo_real - self.saldo_projetado

    def __str__(self):
        return f"Fluxo de Caixa {self.mes:02d}/{self.ano}"

    class Meta:
        verbose_name = "Fluxo de Caixa Projetado"
        verbose_name_plural = "Fluxos de Caixa Projetados"
        unique_together = [['company', 'mes', 'ano']]
