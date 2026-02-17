"""
Modelos do módulo de Estoque.

Este arquivo define os modelos de dados relacionados ao controle de estoque,
incluindo produtos e suas movimentações (entradas e saídas).

Autor: Manus AI
Data: 2025-12-02
"""

from django.db import models, transaction
from django.db.models import F
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from decimal import Decimal
from base.models import TenantModel


class Produto(TenantModel):
    """
    Modelo que representa um produto no sistema de estoque.
    
    Agora o Produto "percebe" a empresa herdando de TenantModel.
    """
    
    # =============================================================================
    # INFORMAÇÕES BÁSICAS DO PRODUTO
    # =============================================================================
    
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
    
    # =============================================================================
    # INFORMAÇÕES FINANCEIRAS
    # =============================================================================
    
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
    
    # =============================================================================
    # CONTROLE DE ESTOQUE
    # =============================================================================
    
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
    
    estoque_maximo = models.IntegerField(
        default=100,
        validators=[MinValueValidator(0)],
        verbose_name="Estoque Máximo",
        help_text="Quantidade máxima recomendada em estoque"
    )
    
    # =============================================================================
    # INFORMAÇÕES FISCAIS E IDENTIFICAÇÃO
    # =============================================================================
    
    sku = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="SKU (Código Interno)",
        help_text="Código único para identificação do produto na empresa"
    )
    
    ncm = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name="NCM (Nomenclatura Comum do Mercosul)",
        help_text="Código NCM com 8 dígitos. Ex: 12345678 - Obrigatório para NF-e"
    )
    
    cest = models.CharField(
        max_length=7,
        blank=True,
        null=True,
        verbose_name="CEST (Código Especificador da Substituição Tributária)",
        help_text="Código CEST com 7 dígitos (opcional). Ex: 1234567"
    )
    
    ean_gtin = models.CharField(
        max_length=14,
        blank=True,
        null=True,
        unique=True,
        verbose_name="EAN/GTIN (Código de Barras)",
        help_text="Código de barras EAN-13 ou EAN-14 com dígito verificador"
    )
    
    # =============================================================================
    # INFORMAÇÕES LOGÍSTICAS E DIMENSÕES
    # =============================================================================
    
    peso_kg = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal('0.001'))],
        verbose_name="Peso (kg)",
        help_text="Peso do produto em quilogramas (para cálculo de frete)"
    )
    
    altura_cm = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Altura (cm)",
        help_text="Altura do produto em centímetros"
    )
    
    largura_cm = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Largura (cm)",
        help_text="Largura do produto em centímetros"
    )
    
    profundidade_cm = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Profundidade (cm)",
        help_text="Profundidade do produto em centímetros"
    )
    
    volume_m3 = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        blank=True,
        null=True,
        verbose_name="Volume (m3)",
        help_text="Volume do produto em metros cúbicos (calculado automaticamente)"
    )
    
    # =============================================================================
    # INFORMAÇÕES DE ARMAZENAMENTO
    # =============================================================================
    
    localizacao_estoque = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Localização no Estoque",
        help_text="Ex: Corredor A, Estante 2, Prateleira 3, Caixa 5"
    )
    
    categoria = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Categoria do Produto",
        help_text="Ex: Eletrônicos, Vestuário, Alimentos"
    )
    
    subcategoria = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Subcategoria",
        help_text="Ex: Notebooks, Camisetas, Bebidas"
    )
    
    marca = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Marca do Produto",
        help_text="Marca ou fabricante do produto"
    )
    
    fornecedor = models.ForeignKey(
        'fornecedores.Fornecedor',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='produtos',
        verbose_name="Fornecedor Principal",
        help_text="Fornecedor padrão para reposição de estoque"
    )
    
    # =============================================================================
    # INFORMAÇÕES DE IMPOSTOS
    # =============================================================================
    
    icms_aliquota = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name="Alíquota ICMS (%)",
        help_text="Percentual de ICMS aplicável (ex: 18.00)"
    )
    
    ipi_aliquota = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name="Alíquota IPI (%)",
        help_text="Percentual de IPI aplicável (ex: 15.00)"
    )
    
    pis_aliquota = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name="Alíquota PIS (%)",
        help_text="Percentual de PIS aplicável"
    )
    
    cofins_aliquota = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name="Alíquota COFINS (%)",
        help_text="Percentual de COFINS aplicável"
    )
    
    # =============================================================================
    # INFORMAÇÕES DE IMAGEM E CATÁLOGO
    # =============================================================================
    
    imagem = models.ImageField(
        upload_to='produtos/',
        blank=True,
        null=True,
        verbose_name="Imagem do Produto",
        help_text="Foto do produto para o catálogo de vendedores"
    )
    
    visivel_catalogo = models.BooleanField(
        default=True,
        verbose_name="Visível no Catálogo de Vendedores",
        help_text="Se marcado, o produto aparecerá no catálogo para consulta de vendedores"
    )
    
    # =============================================================================
    # STATUS DO PRODUTO
    # =============================================================================
    
    ativo = models.BooleanField(
        default=True,
        verbose_name="Produto Ativo",
        help_text="Indica se o produto está disponível para movimentação"
    )
    
    # =============================================================================
    # RASTREAMENTO DE USUÁRIOS E DATAS
    # =============================================================================
    
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
        ordering = ['nome']
        unique_together = [['company', 'sku']]
        indexes = [
            models.Index(fields=['company', 'sku']),
            models.Index(fields=['ncm']),
            models.Index(fields=['ean_gtin']),
            models.Index(fields=['categoria']),
            models.Index(fields=['visivel_catalogo', 'ativo']),
        ]

    def __str__(self):
        return f"{self.nome} ({self.company.name})" if self.company else self.nome

    def clean(self):
        super().clean()
        if self.ncm:
            ncm_limpo = ''.join(filter(str.isdigit, self.ncm))
            if len(ncm_limpo) != 8:
                raise ValidationError({
                    'ncm': 'O NCM deve possuir exatamente 8 dígitos numéricos.'
                })
            self.ncm = ncm_limpo
    
    def calcular_margem_lucro(self):
        if self.preco_custo > 0:
            margem = ((self.preco_venda - self.preco_custo) / self.preco_custo) * 100
            return round(margem, 2)
        return Decimal('0.00')
    
    def calcular_lucro_unitario(self):
        return self.preco_venda - self.preco_custo
    
    def estoque_baixo(self):
        return self.estoque_atual < self.estoque_minimo
    
    def estoque_alto(self):
        return self.estoque_atual > self.estoque_maximo
    
    def valor_total_estoque(self):
        return self.preco_custo * self.estoque_atual
    
    def calcular_volume(self):
        if self.altura_cm and self.largura_cm and self.profundidade_cm:
            volume = (self.altura_cm * self.largura_cm * self.profundidade_cm) / 1000000
            return round(volume, 6)
        return None

    def get_imagem_url(self):
        if self.imagem:
            return self.imagem.url
        return None

    def status_estoque(self):
        if self.estoque_atual <= 0:
            return "Sem Estoque"
        if self.estoque_baixo():
            return "Estoque Baixo"
        if self.estoque_alto():
            return "Estoque Alto"
        return "Normal"
    
    def save(self, *args, **kwargs):
        if self.altura_cm and self.largura_cm and self.profundidade_cm:
            self.volume_m3 = self.calcular_volume()
        super().save(*args, **kwargs)


class MovimentacaoEstoque(models.Model):
    """
    Modelo que registra as movimentações de estoque (entradas e saídas).
    """
    
    TIPO_MOVIMENTACAO = (
        ('ENTRADA', 'Entrada'),
        ('SAIDA', 'Saída'),
    )
    
    produto = models.ForeignKey(
        Produto,
        on_delete=models.PROTECT,
        related_name='movimentacoes',
        verbose_name="Produto"
    )
    
    tipo = models.CharField(
        max_length=7,
        choices=TIPO_MOVIMENTACAO,
        verbose_name="Tipo de Movimentação"
    )
    
    quantidade = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Quantidade",
        help_text="Quantidade de itens movimentados"
    )
    
    valor_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Valor Unitário",
        help_text="Valor unitário do produto nesta movimentação"
    )
    
    observacao = models.TextField(
        blank=True,
        null=True,
        verbose_name="Observação",
        help_text="Informações adicionais sobre a movimentação"
    )
    
    usuario = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='movimentacoes_estoque',
        default=1,
        verbose_name="Responsável",
        help_text="Usuário que realizou a movimentação"
    )
    
    data_movimentacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data da Movimentação"
    )
    
    class Meta:
        verbose_name = "Movimentação de Estoque"
        verbose_name_plural = "Movimentações de Estoque"
        ordering = ['-data_movimentacao']
        indexes = [
            models.Index(fields=['produto', '-data_movimentacao']),
            models.Index(fields=['tipo', '-data_movimentacao']),
        ]
    
    def __str__(self):
        return f"{self.tipo} de {self.quantidade}x {self.produto.nome}"
    
    def calcular_valor_total(self):
        return self.quantidade * self.valor_unitario
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        
        if is_new:
            with transaction.atomic():
                produto = Produto.objects.select_for_update().get(pk=self.produto.pk)
                
                if self.tipo == 'ENTRADA':
                    produto.estoque_atual = F('estoque_atual') + self.quantidade
                elif self.tipo == 'SAIDA':
                    if produto.estoque_atual < self.quantidade:
                        raise ValueError(
                            f"Estoque insuficiente! Disponível: {produto.estoque_atual}, "
                            f"Solicitado: {self.quantidade}"
                        )
                    produto.estoque_atual = F('estoque_atual') - self.quantidade
                
                produto.save()
                produto.refresh_from_db()
                self.produto = produto
                
                super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)


# Importar modelos estendidos se existirem
try:
    from .models_extended import CategoriaProduto, ProdutoAtributo, ImagemProduto
except ImportError:
    pass
