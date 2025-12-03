"""
Modelos do módulo de Estoque.

Este arquivo define os modelos de dados relacionados ao controle de estoque,
incluindo produtos e suas movimentações (entradas e saídas).

Autor: Manus AI
Data: 2025-12-02
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal


class Produto(models.Model):
    """
    Modelo que representa um produto no sistema de estoque.
    
    Attributes:
        nome (str): Nome do produto (máximo 200 caracteres)
        descricao (str): Descrição detalhada do produto (opcional)
        preco_custo (Decimal): Preço de custo do produto
        preco_venda (Decimal): Preço de venda do produto
        estoque_atual (int): Quantidade atual em estoque
        estoque_minimo (int): Quantidade mínima de estoque (alerta)
        ativo (bool): Indica se o produto está ativo no sistema
        usuario_criacao (User): Usuário que cadastrou o produto
        data_criacao (datetime): Data e hora de criação do registro
        usuario_modificacao (User): Último usuário que modificou o produto
        data_modificacao (datetime): Data e hora da última modificação
    """
    
    # Informações básicas do produto
    nome = models.CharField(
        max_length=200,
        verbose_name="Nome do Produto",
        help_text="Nome completo do produto"
    )
    
    descricao = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descrição",
        help_text="Descrição detalhada do produto (opcional)"
    )
    
    # Informações financeiras
    preco_custo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Preço de Custo",
        help_text="Valor pago pelo produto (custo de aquisição)"
    )
    
    preco_venda = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Preço de Venda",
        help_text="Valor de venda do produto ao cliente"
    )
    
    # Controle de estoque
    estoque_atual = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Estoque Atual",
        help_text="Quantidade disponível em estoque"
    )
    
    estoque_minimo = models.IntegerField(
        default=10,
        validators=[MinValueValidator(0)],
        verbose_name="Estoque Mínimo",
        help_text="Quantidade mínima para alerta de reposição"
    )
    
    # Status do produto
    ativo = models.BooleanField(
        default=True,
        verbose_name="Produto Ativo",
        help_text="Indica se o produto está disponível para movimentação"
    )
    
    # Rastreamento de usuários e datas
    usuario_criacao = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='produtos_criados',
        default=1,
        verbose_name="Criado por",
        help_text="Usuário que cadastrou o produto"
    )
    
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )
    
    usuario_modificacao = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='produtos_modificados',
        null=True,
        blank=True,
        verbose_name="Modificado por",
        help_text="Último usuário que modificou o produto"
    )
    
    data_modificacao = models.DateTimeField(
        auto_now=True,
        verbose_name="Data de Modificação"
    )
    
    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ['nome']  # Ordenar alfabeticamente por nome
    
    def __str__(self):
        """Retorna representação em string do produto."""
        return self.nome
    
    def calcular_margem_lucro(self):
        """
        Calcula a margem de lucro do produto.
        
        Returns:
            Decimal: Percentual de margem de lucro
        """
        if self.preco_custo > 0:
            margem = ((self.preco_venda - self.preco_custo) / self.preco_custo) * 100
            return round(margem, 2)
        return Decimal('0.00')
    
    def calcular_lucro_unitario(self):
        """
        Calcula o lucro unitário do produto.
        
        Returns:
            Decimal: Valor do lucro por unidade
        """
        return self.preco_venda - self.preco_custo
    
    def estoque_baixo(self):
        """
        Verifica se o estoque está abaixo do mínimo.
        
        Returns:
            bool: True se estoque atual < estoque mínimo
        """
        return self.estoque_atual < self.estoque_minimo
    
    def valor_total_estoque(self):
        """
        Calcula o valor total do estoque atual (custo).
        
        Returns:
            Decimal: Valor total investido no estoque deste produto
        """
        return self.preco_custo * self.estoque_atual


class MovimentacaoEstoque(models.Model):
    """
    Modelo que registra as movimentações de estoque (entradas e saídas).
    
    Cada movimentação afeta o estoque atual do produto e pode gerar
    impactos financeiros (receitas em vendas, custos em compras).
    
    Attributes:
        produto (Produto): Produto relacionado à movimentação
        tipo (str): Tipo de movimentação (ENTRADA ou SAIDA)
        quantidade (int): Quantidade movimentada
        valor_unitario (Decimal): Valor unitário da movimentação
        observacao (str): Observações sobre a movimentação
        usuario (User): Usuário responsável pela movimentação
        data_movimentacao (datetime): Data e hora da movimentação
    """
    
    # Tipos de movimentação possíveis
    TIPO_MOVIMENTACAO = (
        ('ENTRADA', 'Entrada'),  # Compra, devolução de cliente, etc.
        ('SAIDA', 'Saída'),      # Venda, perda, devolução ao fornecedor, etc.
    )
    
    # Relacionamento com o produto
    produto = models.ForeignKey(
        Produto,
        on_delete=models.PROTECT,  # Não permite deletar produto com movimentações
        related_name='movimentacoes',
        verbose_name="Produto"
    )
    
    # Tipo de movimentação
    tipo = models.CharField(
        max_length=7,
        choices=TIPO_MOVIMENTACAO,
        verbose_name="Tipo de Movimentação"
    )
    
    # Quantidade movimentada
    quantidade = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Quantidade",
        help_text="Quantidade de itens movimentados"
    )
    
    # Valor unitário da movimentação
    valor_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Valor Unitário",
        help_text="Valor unitário do produto nesta movimentação"
    )
    
    # Observações
    observacao = models.TextField(
        blank=True,
        null=True,
        verbose_name="Observação",
        help_text="Informações adicionais sobre a movimentação"
    )
    
    # Rastreamento de usuário
    usuario = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='movimentacoes_estoque',
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
        verbose_name = "Movimentação de Estoque"
        verbose_name_plural = "Movimentações de Estoque"
        ordering = ['-data_movimentacao']  # Mais recentes primeiro
    
    def __str__(self):
        """Retorna representação em string da movimentação."""
        return f"{self.tipo} de {self.quantidade}x {self.produto.nome}"
    
    def calcular_valor_total(self):
        """
        Calcula o valor total da movimentação.
        
        Returns:
            Decimal: Quantidade × Valor Unitário
        """
        return self.quantidade * self.valor_unitario
    
    def save(self, *args, **kwargs):
        """
        Sobrescreve o método save para atualizar o estoque automaticamente.
        
        Ao salvar uma movimentação:
        - ENTRADA: adiciona ao estoque
        - SAIDA: subtrai do estoque
        """
        # Verificar se é uma nova movimentação
        is_new = self.pk is None
        
        if is_new:
            # Atualizar estoque do produto
            if self.tipo == 'ENTRADA':
                self.produto.estoque_atual += self.quantidade
            elif self.tipo == 'SAIDA':
                # Verificar se há estoque suficiente
                if self.produto.estoque_atual < self.quantidade:
                    raise ValueError(
                        f"Estoque insuficiente! Disponível: {self.produto.estoque_atual}, "
                        f"Solicitado: {self.quantidade}"
                    )
                self.produto.estoque_atual -= self.quantidade
            
            # Salvar o produto com o estoque atualizado
            self.produto.save()
        
        # Salvar a movimentação
        super().save(*args, **kwargs)
