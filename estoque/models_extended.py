"""
Modelos estendidos para o módulo de Estoque.

Adiciona funcionalidades de categorias, imagens, códigos de barras e atributos avançados.

Autor: Denis Barbosa (Todos os direitos reservados)
Data: 2026-02-05
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
from .models import Produto


class CategoriaProduto(models.Model):
    """
    Modelo para categorização hierárquica de produtos.
    
    Permite criar categorias e subcategorias ilimitadas.
    
    Attributes:
        nome (str): Nome da categoria
        descricao (str): Descrição da categoria
        categoria_pai (CategoriaProduto): Categoria pai (para hierarquia)
        ativa (bool): Se a categoria está ativa
        ordem (int): Ordem de exibição
        usuario_criacao (User): Usuário que criou a categoria
        data_criacao (datetime): Data de criação
    """
    
    nome = models.CharField(
        max_length=100,
        verbose_name="Nome da Categoria"
    )
    
    descricao = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descrição"
    )
    
    categoria_pai = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategorias',
        verbose_name="Categoria Pai"
    )
    
    ativa = models.BooleanField(
        default=True,
        verbose_name="Categoria Ativa"
    )
    
    ordem = models.IntegerField(
        default=0,
        verbose_name="Ordem de Exibição"
    )
    
    usuario_criacao = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='categorias_criadas',
        default=1,
        verbose_name="Criado por"
    )
    
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )
    
    class Meta:
        verbose_name = "Categoria de Produto"
        verbose_name_plural = "Categorias de Produtos"
        ordering = ['ordem', 'nome']
    
    def __str__(self):
        if self.categoria_pai:
            return f"{self.categoria_pai.nome} > {self.nome}"
        return self.nome
    
    def get_nivel(self):
        """Retorna o nível hierárquico da categoria."""
        nivel = 0
        categoria = self.categoria_pai
        while categoria:
            nivel += 1
            categoria = categoria.categoria_pai
        return nivel


class ProdutoAtributo(models.Model):
    """
    Modelo para atributos adicionais de produtos.
    
    Permite adicionar campos customizados aos produtos como:
    código de barras, NCM, marca, fabricante, etc.
    
    Attributes:
        produto (Produto): Produto relacionado
        codigo_barras (str): Código de barras (EAN/UPC)
        sku (str): Stock Keeping Unit (código único)
        ncm (str): Nomenclatura Comum do Mercosul
        marca (str): Marca do produto
        fabricante (str): Fabricante do produto
        unidade_medida (str): Unidade de medida
        peso (Decimal): Peso em kg
        altura (Decimal): Altura em cm
        largura (Decimal): Largura em cm
        profundidade (Decimal): Profundidade em cm
        categoria (CategoriaProduto): Categoria do produto
    """
    
    UNIDADES_MEDIDA = (
        ('UN', 'Unidade'),
        ('KG', 'Quilograma'),
        ('G', 'Grama'),
        ('L', 'Litro'),
        ('ML', 'Mililitro'),
        ('M', 'Metro'),
        ('CM', 'Centímetro'),
        ('M2', 'Metro Quadrado'),
        ('M3', 'Metro Cúbico'),
        ('CX', 'Caixa'),
        ('PC', 'Peça'),
        ('PAR', 'Par'),
        ('DZ', 'Dúzia'),
    )
    
    produto = models.OneToOneField(
        Produto,
        on_delete=models.CASCADE,
        related_name='atributos',
        verbose_name="Produto"
    )
    
    codigo_barras = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        unique=True,
        verbose_name="Código de Barras (EAN/UPC)"
    )
    
    sku = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        unique=True,
        verbose_name="SKU (Código Único)"
    )
    
    ncm = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name="NCM",
        help_text="Nomenclatura Comum do Mercosul"
    )
    
    marca = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Marca"
    )
    
    fabricante = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Fabricante"
    )
    
    unidade_medida = models.CharField(
        max_length=10,
        choices=UNIDADES_MEDIDA,
        default='UN',
        verbose_name="Unidade de Medida"
    )
    
    peso = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.001'))],
        verbose_name="Peso (kg)"
    )
    
    altura = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Altura (cm)"
    )
    
    largura = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Largura (cm)"
    )
    
    profundidade = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Profundidade (cm)"
    )
    
    categoria = models.ForeignKey(
        CategoriaProduto,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='produtos',
        verbose_name="Categoria"
    )
    
    class Meta:
        verbose_name = "Atributos do Produto"
        verbose_name_plural = "Atributos dos Produtos"
    
    def __str__(self):
        return f"Atributos de {self.produto.nome}"
    
    def calcular_volume(self):
        """Calcula o volume do produto em cm³."""
        if self.altura and self.largura and self.profundidade:
            return self.altura * self.largura * self.profundidade
        return None


class ImagemProduto(models.Model):
    """
    Modelo para armazenar múltiplas imagens de produtos.
    
    Attributes:
        produto (Produto): Produto relacionado
        imagem (ImageField): Arquivo de imagem
        principal (bool): Se é a imagem principal do produto
        ordem (int): Ordem de exibição
        descricao (str): Descrição da imagem
        data_upload (datetime): Data de upload
    """
    
    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        related_name='imagens',
        verbose_name="Produto"
    )
    
    imagem = models.ImageField(
        upload_to='produtos/%Y/%m/',
        verbose_name="Imagem"
    )
    
    principal = models.BooleanField(
        default=False,
        verbose_name="Imagem Principal"
    )
    
    ordem = models.IntegerField(
        default=0,
        verbose_name="Ordem"
    )
    
    descricao = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Descrição"
    )
    
    data_upload = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Upload"
    )
    
    class Meta:
        verbose_name = "Imagem de Produto"
        verbose_name_plural = "Imagens de Produtos"
        ordering = ['produto', 'ordem']
    
    def __str__(self):
        return f"Imagem de {self.produto.nome}"
    
    def save(self, *args, **kwargs):
        """Garante que apenas uma imagem seja marcada como principal."""
        if self.principal:
            # Desmarcar outras imagens principais do mesmo produto
            ImagemProduto.objects.filter(
                produto=self.produto,
                principal=True
            ).update(principal=False)
        super().save(*args, **kwargs)
