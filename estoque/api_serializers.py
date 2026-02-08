"""
Serializers para API REST do módulo de Estoque.

Utilizados para serializar dados de Produtos para a API de catálogo
de vendedores e consultas rápidas.

Autor: Manus AI
Data: 2025-12-07
"""

from rest_framework import serializers
from .models import Produto, MovimentacaoEstoque


class ProdutoListaSerializer(serializers.ModelSerializer):
    """
    Serializer para listar produtos no catálogo de vendedores.
    
    Inclui apenas as informações essenciais para consulta rápida.
    """
    
    margem_lucro = serializers.SerializerMethodField()
    estoque_status = serializers.SerializerMethodField()
    
    class Meta:
        model = Produto
        fields = [
            'id',
            'nome',
            'sku',
            'preco_venda',
            'estoque_atual',
            'estoque_status',
            'categoria',
            'marca',
            'imagem',
            'margem_lucro',
            'ean_gtin'
        ]
    
    def get_margem_lucro(self, obj):
        """Calcula a margem de lucro."""
        return float(obj.calcular_margem_lucro())
    
    def get_estoque_status(self, obj):
        """Retorna o status do estoque."""
        if obj.estoque_baixo():
            return 'BAIXO'
        elif obj.estoque_alto():
            return 'ALTO'
        return 'NORMAL'


class ProdutoDetalheSerializer(serializers.ModelSerializer):
    """
    Serializer detalhado para consulta completa de um produto.
    
    Inclui todas as informações fiscais, logísticas e de estoque.
    """
    
    margem_lucro = serializers.SerializerMethodField()
    lucro_unitario = serializers.SerializerMethodField()
    valor_total_estoque = serializers.SerializerMethodField()
    fornecedor_nome = serializers.CharField(source='fornecedor.nome', read_only=True)
    
    class Meta:
        model = Produto
        fields = [
            'id',
            'nome',
            'descricao',
            'sku',
            'ncm',
            'cest',
            'ean_gtin',
            'preco_custo',
            'preco_venda',
            'margem_lucro',
            'lucro_unitario',
            'estoque_atual',
            'estoque_minimo',
            'estoque_maximo',
            'valor_total_estoque',
            'categoria',
            'subcategoria',
            'marca',
            'fornecedor_nome',
            'peso_kg',
            'altura_cm',
            'largura_cm',
            'profundidade_cm',
            'volume_m3',
            'localizacao_estoque',
            'icms_aliquota',
            'ipi_aliquota',
            'pis_aliquota',
            'cofins_aliquota',
            'imagem',
            'visivel_catalogo',
            'ativo',
            'data_criacao',
            'data_modificacao'
        ]
    
    def get_margem_lucro(self, obj):
        """Calcula a margem de lucro."""
        return float(obj.calcular_margem_lucro())
    
    def get_lucro_unitario(self, obj):
        """Calcula o lucro unitário."""
        return float(obj.calcular_lucro_unitario())
    
    def get_valor_total_estoque(self, obj):
        """Calcula o valor total do estoque."""
        return float(obj.valor_total_estoque())


class ProdutoCatalogoSerializer(serializers.ModelSerializer):
    """
    Serializer otimizado para exibição no catálogo de vendedores.
    
    Inclui apenas campos visíveis e relevantes para vendedores.
    """
    
    margem_lucro = serializers.SerializerMethodField()
    
    class Meta:
        model = Produto
        fields = [
            'id',
            'nome',
            'sku',
            'preco_venda',
            'estoque_atual',
            'categoria',
            'subcategoria',
            'marca',
            'imagem',
            'margem_lucro',
            'ean_gtin',
            'descricao'
        ]
    
    def get_margem_lucro(self, obj):
        """Calcula a margem de lucro."""
        return float(obj.calcular_margem_lucro())


class MovimentacaoEstoqueSerializer(serializers.ModelSerializer):
    """
    Serializer para movimentações de estoque.
    """
    
    produto_nome = serializers.CharField(source='produto.nome', read_only=True)
    usuario_nome = serializers.CharField(source='usuario.username', read_only=True)
    valor_total = serializers.SerializerMethodField()
    
    class Meta:
        model = MovimentacaoEstoque
        fields = [
            'id',
            'produto',
            'produto_nome',
            'tipo',
            'quantidade',
            'valor_unitario',
            'valor_total',
            'observacao',
            'usuario_nome',
            'data_movimentacao'
        ]
        read_only_fields = [
            'id',
            'usuario_nome',
            'data_movimentacao'
        ]
    
    def get_valor_total(self, obj):
        """Calcula o valor total da movimentação."""
        return float(obj.calcular_valor_total())
