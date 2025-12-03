"""
Modelos do módulo Financeiro.

Este arquivo define os modelos de dados relacionados ao controle financeiro,
incluindo receitas, despesas, capital de giro e indicadores financeiros.

Autor: Manus AI
Data: 2025-12-02
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.db.models import Sum


class Receita(models.Model):
    """
    Modelo que representa uma receita (entrada de dinheiro).
    
    Receitas podem ser provenientes de vendas, serviços prestados,
    ou outras fontes de entrada de capital.
    
    Attributes:
        descricao (str): Descrição da receita
        valor (Decimal): Valor da receita
        data (date): Data em que a receita foi recebida
        categoria (str): Categoria da receita
        usuario (User): Usuário que registrou a receita
        data_criacao (datetime): Data de criação do registro
    """
    
    # Categorias de receita
    CATEGORIAS = (
        ('VENDA', 'Venda de Produtos'),
        ('SERVICO', 'Prestação de Serviços'),
        ('INVESTIMENTO', 'Retorno de Investimento'),
        ('OUTROS', 'Outros'),
    )
    
    # Descrição da receita
    descricao = models.CharField(
        max_length=200,
        verbose_name="Descrição",
        help_text="Descrição detalhada da receita"
    )
    
    # Valor da receita
    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Valor",
        help_text="Valor da receita em R$"
    )
    
    # Data da receita
    data = models.DateField(
        verbose_name="Data da Receita",
        help_text="Data em que a receita foi recebida"
    )
    
    # Categoria da receita
    categoria = models.CharField(
        max_length=20,
        choices=CATEGORIAS,
        default='VENDA',
        verbose_name="Categoria",
        help_text="Categoria da receita"
    )
    
    # Rastreamento de usuário
    usuario = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='receitas_registradas',
        default=1,
        verbose_name="Registrado por",
        help_text="Usuário que registrou a receita"
    )
    
    # Data de criação do registro
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )
    
    class Meta:
        verbose_name = "Receita"
        verbose_name_plural = "Receitas"
        ordering = ['-data']  # Mais recentes primeiro
    
    def __str__(self):
        """Retorna representação em string da receita."""
        return f"Receita: {self.descricao} (R$ {self.valor})"


class Despesa(models.Model):
    """
    Modelo que representa uma despesa (saída de dinheiro).
    
    Despesas incluem custos operacionais, compras, salários,
    e outras saídas de capital.
    
    Attributes:
        descricao (str): Descrição da despesa
        valor (Decimal): Valor da despesa
        data (date): Data em que a despesa foi realizada
        categoria (str): Categoria da despesa
        usuario (User): Usuário que registrou a despesa
        data_criacao (datetime): Data de criação do registro
    """
    
    # Categorias de despesa
    CATEGORIAS = (
        ('COMPRA', 'Compra de Produtos'),
        ('SALARIO', 'Salários e Encargos'),
        ('ALUGUEL', 'Aluguel e Condomínio'),
        ('SERVICO', 'Serviços Contratados'),
        ('IMPOSTO', 'Impostos e Taxas'),
        ('OUTROS', 'Outros'),
    )
    
    # Descrição da despesa
    descricao = models.CharField(
        max_length=200,
        verbose_name="Descrição",
        help_text="Descrição detalhada da despesa"
    )
    
    # Valor da despesa
    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Valor",
        help_text="Valor da despesa em R$"
    )
    
    # Data da despesa
    data = models.DateField(
        verbose_name="Data da Despesa",
        help_text="Data em que a despesa foi realizada"
    )
    
    # Categoria da despesa
    categoria = models.CharField(
        max_length=20,
        choices=CATEGORIAS,
        default='OUTROS',
        verbose_name="Categoria",
        help_text="Categoria da despesa"
    )
    
    # Rastreamento de usuário
    usuario = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='despesas_registradas',
        default=1,
        verbose_name="Registrado por",
        help_text="Usuário que registrou a despesa"
    )
    
    # Data de criação do registro
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )
    
    class Meta:
        verbose_name = "Despesa"
        verbose_name_plural = "Despesas"
        ordering = ['-data']  # Mais recentes primeiro
    
    def __str__(self):
        """Retorna representação em string da despesa."""
        return f"Despesa: {self.descricao} (R$ {self.valor})"


class CapitalGiro(models.Model):
    """
    Modelo que representa o capital de giro da empresa.
    
    O capital de giro é o valor disponível para operações diárias.
    Este modelo mantém um histórico de todas as alterações no capital.
    
    Attributes:
        valor_anterior (Decimal): Valor antes da movimentação
        valor_novo (Decimal): Valor após a movimentação
        tipo_movimentacao (str): Tipo de movimentação (ENTRADA ou SAIDA)
        descricao (str): Descrição da movimentação
        usuario (User): Usuário responsável pela movimentação
        data_movimentacao (datetime): Data e hora da movimentação
    """
    
    # Tipos de movimentação
    TIPO_MOVIMENTACAO = (
        ('ENTRADA', 'Entrada de Capital'),
        ('SAIDA', 'Saída de Capital'),
        ('AJUSTE', 'Ajuste Manual'),
    )
    
    # Valores
    valor_anterior = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Valor Anterior",
        help_text="Valor do capital antes da movimentação"
    )
    
    valor_novo = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Valor Novo",
        help_text="Valor do capital após a movimentação"
    )
    
    # Tipo de movimentação
    tipo_movimentacao = models.CharField(
        max_length=10,
        choices=TIPO_MOVIMENTACAO,
        verbose_name="Tipo de Movimentação"
    )
    
    # Descrição
    descricao = models.TextField(
        verbose_name="Descrição",
        help_text="Descrição detalhada da movimentação"
    )
    
    # Rastreamento de usuário
    usuario = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='movimentacoes_capital',
        default=1,
        verbose_name="Responsável",
        help_text="Usuário que realizou a movimentação"
    )
    
    # Data da movimentação
    data_movimentacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data da Movimentação"
    )
    
    class Meta:
        verbose_name = "Capital de Giro"
        verbose_name_plural = "Histórico de Capital de Giro"
        ordering = ['-data_movimentacao']
    
    def __str__(self):
        """Retorna representação em string da movimentação."""
        return f"{self.tipo_movimentacao}: R$ {self.valor_anterior} → R$ {self.valor_novo}"
    
    def calcular_diferenca(self):
        """
        Calcula a diferença entre o valor novo e o anterior.
        
        Returns:
            Decimal: Diferença (positiva para entrada, negativa para saída)
        """
        return self.valor_novo - self.valor_anterior
    
    @classmethod
    def obter_capital_atual(cls):
        """
        Obtém o valor atual do capital de giro.
        
        Returns:
            Decimal: Valor atual do capital de giro
        """
        ultima_movimentacao = cls.objects.first()  # Mais recente
        if ultima_movimentacao:
            return ultima_movimentacao.valor_novo
        return Decimal('0.00')
    
    @classmethod
    def adicionar_capital(cls, valor, descricao, usuario):
        """
        Adiciona capital de giro.
        
        Args:
            valor (Decimal): Valor a ser adicionado
            descricao (str): Descrição da entrada
            usuario (User): Usuário responsável
            
        Returns:
            CapitalGiro: Instância da movimentação criada
        """
        capital_atual = cls.obter_capital_atual()
        novo_capital = capital_atual + valor
        
        return cls.objects.create(
            valor_anterior=capital_atual,
            valor_novo=novo_capital,
            tipo_movimentacao='ENTRADA',
            descricao=descricao,
            usuario=usuario
        )
    
    @classmethod
    def retirar_capital(cls, valor, descricao, usuario):
        """
        Retira capital de giro.
        
        Args:
            valor (Decimal): Valor a ser retirado
            descricao (str): Descrição da saída
            usuario (User): Usuário responsável
            
        Returns:
            CapitalGiro: Instância da movimentação criada
            
        Raises:
            ValueError: Se não houver capital suficiente
        """
        capital_atual = cls.obter_capital_atual()
        
        if capital_atual < valor:
            raise ValueError(
                f"Capital insuficiente! Disponível: R$ {capital_atual}, "
                f"Solicitado: R$ {valor}"
            )
        
        novo_capital = capital_atual - valor
        
        return cls.objects.create(
            valor_anterior=capital_atual,
            valor_novo=novo_capital,
            tipo_movimentacao='SAIDA',
            descricao=descricao,
            usuario=usuario
        )


class IndicadorFinanceiro(models.Model):
    """
    Modelo que armazena indicadores financeiros calculados.
    
    Este modelo é atualizado automaticamente com base nas movimentações
    de estoque e transações financeiras.
    
    Attributes:
        periodo (date): Período de referência (mês/ano)
        total_receitas (Decimal): Total de receitas no período
        total_despesas (Decimal): Total de despesas no período
        lucro_bruto (Decimal): Receitas - Despesas
        margem_lucro (Decimal): Percentual de margem de lucro
        data_atualizacao (datetime): Data da última atualização
    """
    
    # Período de referência
    periodo = models.DateField(
        unique=True,
        verbose_name="Período",
        help_text="Primeiro dia do mês de referência"
    )
    
    # Totalizadores
    total_receitas = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Total de Receitas"
    )
    
    total_despesas = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Total de Despesas"
    )
    
    lucro_bruto = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Lucro Bruto"
    )
    
    margem_lucro = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Margem de Lucro (%)"
    )
    
    # Data de atualização
    data_atualizacao = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Atualização"
    )
    
    class Meta:
        verbose_name = "Indicador Financeiro"
        verbose_name_plural = "Indicadores Financeiros"
        ordering = ['-periodo']
    
    def __str__(self):
        """Retorna representação em string do indicador."""
        return f"Indicadores de {self.periodo.strftime('%m/%Y')}"
    
    def calcular_indicadores(self):
        """
        Calcula os indicadores financeiros do período.
        
        Atualiza os valores de receitas, despesas, lucro e margem.
        """
        # Filtrar receitas e despesas do período
        ano = self.periodo.year
        mes = self.periodo.month
        
        # Total de receitas
        receitas = Receita.objects.filter(
            data__year=ano,
            data__month=mes
        ).aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
        
        # Total de despesas
        despesas = Despesa.objects.filter(
            data__year=ano,
            data__month=mes
        ).aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
        
        # Atualizar valores
        self.total_receitas = receitas
        self.total_despesas = despesas
        self.lucro_bruto = receitas - despesas
        
        # Calcular margem de lucro
        if receitas > 0:
            self.margem_lucro = (self.lucro_bruto / receitas) * 100
        else:
            self.margem_lucro = Decimal('0.00')
        
        self.save()
