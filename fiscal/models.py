"""
Modelos do módulo Fiscal.

Este arquivo define os modelos de dados relacionados à gestão fiscal,
incluindo importação de NF-e (Nota Fiscal Eletrônica) e seus itens.

Autor: Manus AI
Data: 2026-02-05
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
from estoque.models import Produto


class Fornecedor(models.Model):
    """
    Modelo que representa um fornecedor.
    
    Attributes:
        razao_social (str): Razão social do fornecedor
        nome_fantasia (str): Nome fantasia
        cnpj (str): CNPJ do fornecedor
        inscricao_estadual (str): Inscrição estadual
        endereco (str): Endereço completo
        cidade (str): Cidade
        estado (str): Estado (UF)
        cep (str): CEP
        telefone (str): Telefone de contato
        email (str): Email de contato
        ativo (bool): Indica se o fornecedor está ativo
        usuario_criacao (User): Usuário que cadastrou o fornecedor
        data_criacao (datetime): Data de criação do registro
    """
    
    razao_social = models.CharField(
        max_length=200,
        verbose_name="Razão Social",
        help_text="Razão social do fornecedor"
    )
    
    nome_fantasia = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Nome Fantasia",
        help_text="Nome fantasia do fornecedor"
    )
    
    cnpj = models.CharField(
        max_length=18,
        unique=True,
        verbose_name="CNPJ",
        help_text="CNPJ do fornecedor (formato: 00.000.000/0000-00)"
    )
    
    inscricao_estadual = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Inscrição Estadual"
    )
    
    endereco = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        verbose_name="Endereço"
    )
    
    cidade = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Cidade"
    )
    
    estado = models.CharField(
        max_length=2,
        blank=True,
        null=True,
        verbose_name="Estado (UF)"
    )
    
    cep = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name="CEP"
    )
    
    telefone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Telefone"
    )
    
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name="Email"
    )
    
    ativo = models.BooleanField(
        default=True,
        verbose_name="Fornecedor Ativo"
    )
    
    usuario_criacao = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='fornecedores_criados',
        default=1,
        verbose_name="Criado por"
    )
    
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )
    
    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"
        ordering = ['razao_social']
    
    def __str__(self):
        return self.nome_fantasia or self.razao_social


class NotaFiscalEletronica(models.Model):
    """
    Modelo que representa uma Nota Fiscal Eletrônica (NF-e).
    
    Armazena os dados principais da NF-e importada via XML.
    
    Attributes:
        chave_acesso (str): Chave de acesso da NF-e (44 dígitos)
        numero (str): Número da nota fiscal
        serie (str): Série da nota fiscal
        fornecedor (Fornecedor): Fornecedor emissor da NF-e
        data_emissao (date): Data de emissão da NF-e
        valor_total (Decimal): Valor total da NF-e
        valor_produtos (Decimal): Valor total dos produtos
        valor_icms (Decimal): Valor do ICMS
        valor_ipi (Decimal): Valor do IPI
        valor_pis (Decimal): Valor do PIS
        valor_cofins (Decimal): Valor do COFINS
        valor_frete (Decimal): Valor do frete
        valor_desconto (Decimal): Valor de desconto
        natureza_operacao (str): Natureza da operação
        cfop (str): Código Fiscal de Operações e Prestações
        xml_arquivo (file): Arquivo XML da NF-e
        status (str): Status da importação
        observacoes (str): Observações sobre a NF-e
        usuario_importacao (User): Usuário que importou a NF-e
        data_importacao (datetime): Data de importação
    """
    
    STATUS_CHOICES = (
        ('PENDENTE', 'Pendente de Processamento'),
        ('PROCESSADA', 'Processada com Sucesso'),
        ('ERRO', 'Erro no Processamento'),
        ('CANCELADA', 'Cancelada'),
    )
    
    chave_acesso = models.CharField(
        max_length=44,
        unique=True,
        verbose_name="Chave de Acesso",
        help_text="Chave de acesso da NF-e (44 dígitos)"
    )
    
    numero = models.CharField(
        max_length=20,
        verbose_name="Número da NF-e"
    )
    
    serie = models.CharField(
        max_length=10,
        verbose_name="Série"
    )
    
    fornecedor = models.ForeignKey(
        Fornecedor,
        on_delete=models.PROTECT,
        related_name='notas_fiscais',
        verbose_name="Fornecedor"
    )
    
    data_emissao = models.DateField(
        verbose_name="Data de Emissão"
    )
    
    # Valores da NF-e
    valor_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Valor Total"
    )
    
    valor_produtos = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Valor dos Produtos"
    )
    
    valor_icms = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Valor ICMS"
    )
    
    valor_ipi = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Valor IPI"
    )
    
    valor_pis = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Valor PIS"
    )
    
    valor_cofins = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Valor COFINS"
    )
    
    valor_frete = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Valor do Frete"
    )
    
    valor_desconto = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Valor de Desconto"
    )
    
    natureza_operacao = models.CharField(
        max_length=100,
        verbose_name="Natureza da Operação"
    )
    
    cfop = models.CharField(
        max_length=10,
        verbose_name="CFOP",
        help_text="Código Fiscal de Operações e Prestações"
    )
    
    xml_arquivo = models.FileField(
        upload_to='nfe_xml/%Y/%m/',
        verbose_name="Arquivo XML"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDENTE',
        verbose_name="Status"
    )
    
    observacoes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Observações"
    )
    
    usuario_importacao = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='nfes_importadas',
        default=1,
        verbose_name="Importado por"
    )
    
    data_importacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Importação"
    )
    
    class Meta:
        verbose_name = "Nota Fiscal Eletrônica"
        verbose_name_plural = "Notas Fiscais Eletrônicas"
        ordering = ['-data_emissao', '-numero']
    
    def __str__(self):
        return f"NF-e {self.numero}/{self.serie} - {self.fornecedor}"
    
    def calcular_total_impostos(self):
        """Calcula o total de impostos da NF-e."""
        return (self.valor_icms + self.valor_ipi + 
                self.valor_pis + self.valor_cofins)


class ItemNotaFiscal(models.Model):
    """
    Modelo que representa um item de uma Nota Fiscal Eletrônica.
    
    Cada item corresponde a um produto na NF-e.
    
    Attributes:
        nota_fiscal (NotaFiscalEletronica): NF-e relacionada
        numero_item (int): Número sequencial do item na NF-e
        produto (Produto): Produto relacionado (se existir no cadastro)
        codigo_produto (str): Código do produto no XML
        descricao (str): Descrição do produto
        ncm (str): Nomenclatura Comum do Mercosul
        cfop (str): CFOP do item
        unidade (str): Unidade de medida
        quantidade (Decimal): Quantidade
        valor_unitario (Decimal): Valor unitário
        valor_total (Decimal): Valor total do item
        valor_desconto (Decimal): Valor de desconto
        valor_frete (Decimal): Valor do frete
        valor_icms (Decimal): Valor do ICMS
        valor_ipi (Decimal): Valor do IPI
        aliquota_icms (Decimal): Alíquota do ICMS
        aliquota_ipi (Decimal): Alíquota do IPI
        criado_automaticamente (bool): Se o produto foi criado automaticamente
    """
    
    nota_fiscal = models.ForeignKey(
        NotaFiscalEletronica,
        on_delete=models.CASCADE,
        related_name='itens',
        verbose_name="Nota Fiscal"
    )
    
    numero_item = models.IntegerField(
        verbose_name="Número do Item"
    )
    
    produto = models.ForeignKey(
        Produto,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='itens_nfe',
        verbose_name="Produto Cadastrado"
    )
    
    codigo_produto = models.CharField(
        max_length=100,
        verbose_name="Código do Produto"
    )
    
    descricao = models.CharField(
        max_length=300,
        verbose_name="Descrição"
    )
    
    ncm = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name="NCM"
    )
    
    cfop = models.CharField(
        max_length=10,
        verbose_name="CFOP"
    )
    
    unidade = models.CharField(
        max_length=10,
        verbose_name="Unidade"
    )
    
    quantidade = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        validators=[MinValueValidator(Decimal('0.0001'))],
        verbose_name="Quantidade"
    )
    
    valor_unitario = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        validators=[MinValueValidator(Decimal('0.0001'))],
        verbose_name="Valor Unitário"
    )
    
    valor_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Valor Total"
    )
    
    valor_desconto = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Valor de Desconto"
    )
    
    valor_frete = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Valor do Frete"
    )
    
    valor_icms = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Valor ICMS"
    )
    
    valor_ipi = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Valor IPI"
    )
    
    aliquota_icms = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Alíquota ICMS (%)"
    )
    
    aliquota_ipi = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Alíquota IPI (%)"
    )
    
    criado_automaticamente = models.BooleanField(
        default=False,
        verbose_name="Produto Criado Automaticamente",
        help_text="Indica se o produto foi criado automaticamente durante a importação"
    )
    
    class Meta:
        verbose_name = "Item de Nota Fiscal"
        verbose_name_plural = "Itens de Nota Fiscal"
        ordering = ['nota_fiscal', 'numero_item']
        unique_together = ['nota_fiscal', 'numero_item']
    
    def __str__(self):
        return f"Item {self.numero_item} - {self.descricao}"
    
    def calcular_custo_unitario_real(self):
        """
        Calcula o custo unitário real incluindo impostos e frete.
        
        Returns:
            Decimal: Custo unitário real
        """
        custo_adicional = (self.valor_frete + self.valor_icms + 
                          self.valor_ipi) / self.quantidade
        return self.valor_unitario + custo_adicional

class ProdutoFiscal(Produto):
    """
    Proxy model para permitir a gestão de produtos dentro do módulo Fiscal.
    """
    class Meta:
        proxy = True
        verbose_name = "Produto (Fiscal)"
        verbose_name_plural = "Produtos (Fiscal)"
