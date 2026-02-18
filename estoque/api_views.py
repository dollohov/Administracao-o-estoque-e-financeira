"""
Views da API REST para o módulo de Estoque.

Fornece endpoints para consulta de produtos, catálogo de vendedores
e movimentações de estoque.

Autor: Denis Barbosa (Todos os direitos reservados)
Data: 2025-12-07
"""

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Produto, MovimentacaoEstoque
from .api_serializers import (
    ProdutoListaSerializer,
    ProdutoDetalheSerializer,
    ProdutoCatalogoSerializer,
    MovimentacaoEstoqueSerializer
)


class ProdutoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de produtos.
    
    Endpoints:
    - GET /api/produtos/ - Listar produtos
    - GET /api/produtos/{id}/ - Detalhes do produto
    - POST /api/produtos/ - Criar produto
    - PUT /api/produtos/{id}/ - Atualizar produto
    - DELETE /api/produtos/{id}/ - Deletar produto
    - GET /api/produtos/catalogo/vendedores/ - Catálogo para vendedores
    - GET /api/produtos/buscar/por-sku/ - Buscar por SKU
    - GET /api/produtos/buscar/por-codigo-barras/ - Buscar por EAN
    - GET /api/produtos/estoque/baixo/ - Produtos com estoque baixo
    """
    
    queryset = Produto.objects.filter(ativo=True)
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categoria', 'marca', 'visivel_catalogo', 'ativo']
    search_fields = ['nome', 'sku', 'ncm', 'ean_gtin', 'descricao']
    ordering_fields = ['nome', 'preco_venda', 'estoque_atual', 'data_criacao']
    ordering = ['nome']
    
    def get_serializer_class(self):
        """Retorna o serializer apropriado baseado na ação."""
        if self.action == 'retrieve':
            return ProdutoDetalheSerializer
        elif self.action == 'catalogo_vendedores':
            return ProdutoCatalogoSerializer
        return ProdutoListaSerializer
    
    @action(detail=False, methods=['get'], url_path='catalogo/vendedores')
    def catalogo_vendedores(self, request):
        """
        Retorna o catálogo de produtos visíveis para vendedores.
        
        Filtros disponíveis:
        - categoria: Filtrar por categoria
        - marca: Filtrar por marca
        - search: Buscar por nome, SKU ou descrição
        """
        queryset = self.get_queryset().filter(visivel_catalogo=True)
        
        # Aplicar filtros
        queryset = self.filter_queryset(queryset)
        
        # Paginar
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='buscar/por-sku')
    def buscar_por_sku(self, request):
        """
        Busca um produto pelo SKU.
        
        Parâmetros:
        - sku: Código SKU do produto
        """
        sku = request.query_params.get('sku')
        
        if not sku:
            return Response(
                {'erro': 'Parâmetro "sku" é obrigatório'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            produto = Produto.objects.get(sku=sku, ativo=True)
            serializer = ProdutoDetalheSerializer(produto)
            return Response(serializer.data)
        except Produto.DoesNotExist:
            return Response(
                {'erro': f'Produto com SKU "{sku}" não encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'], url_path='buscar/por-codigo-barras')
    def buscar_por_codigo_barras(self, request):
        """
        Busca um produto pelo código de barras (EAN/GTIN).
        
        Parâmetros:
        - ean: Código EAN/GTIN do produto
        """
        ean = request.query_params.get('ean')
        
        if not ean:
            return Response(
                {'erro': 'Parâmetro "ean" é obrigatório'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            produto = Produto.objects.get(ean_gtin=ean, ativo=True)
            serializer = ProdutoDetalheSerializer(produto)
            return Response(serializer.data)
        except Produto.DoesNotExist:
            return Response(
                {'erro': f'Produto com EAN "{ean}" não encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'], url_path='estoque/baixo')
    def estoque_baixo(self, request):
        """
        Retorna produtos com estoque abaixo do mínimo.
        
        Útil para alertas de reposição.
        """
        queryset = self.get_queryset().filter(
            estoque_atual__lt=models.F('estoque_minimo')
        )
        
        serializer = ProdutoListaSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='estoque/alto')
    def estoque_alto(self, request):
        """
        Retorna produtos com estoque acima do máximo.
        
        Útil para identificar excesso de estoque.
        """
        queryset = self.get_queryset().filter(
            estoque_atual__gt=models.F('estoque_maximo')
        )
        
        serializer = ProdutoListaSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'], url_path='movimentacoes')
    def movimentacoes(self, request, pk=None):
        """
        Retorna o histórico de movimentações de um produto.
        """
        produto = self.get_object()
        movimentacoes = produto.movimentacoes.all()
        
        serializer = MovimentacaoEstoqueSerializer(movimentacoes, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], url_path='buscar-multiplos')
    def buscar_multiplos(self, request):
        """
        Busca múltiplos produtos por SKU ou EAN.
        
        Body JSON:
        {
            "skus": ["SKU1", "SKU2"],
            "eans": ["EAN1", "EAN2"]
        }
        """
        skus = request.data.get('skus', [])
        eans = request.data.get('eans', [])
        
        queryset = Produto.objects.filter(ativo=True)
        
        if skus:
            queryset = queryset.filter(sku__in=skus)
        elif eans:
            queryset = queryset.filter(ean_gtin__in=eans)
        else:
            return Response(
                {'erro': 'Forneça "skus" ou "eans"'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = ProdutoListaSerializer(queryset, many=True)
        return Response(serializer.data)


class MovimentacaoEstoqueViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de movimentações de estoque.
    
    Endpoints:
    - GET /api/movimentacoes/ - Listar movimentações
    - POST /api/movimentacoes/ - Registrar movimentação
    - GET /api/movimentacoes/{id}/ - Detalhes da movimentação
    """
    
    queryset = MovimentacaoEstoque.objects.all()
    serializer_class = MovimentacaoEstoqueSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['tipo', 'produto', 'usuario']
    ordering_fields = ['data_movimentacao']
    ordering = ['-data_movimentacao']
    
    def perform_create(self, serializer):
        """Registra o usuário ao criar uma movimentação."""
        serializer.save(usuario=self.request.user)
    
    @action(detail=False, methods=['get'], url_path='por-tipo')
    def por_tipo(self, request):
        """
        Retorna movimentações filtradas por tipo.
        
        Parâmetros:
        - tipo: ENTRADA ou SAIDA
        """
        tipo = request.query_params.get('tipo')
        
        if tipo not in ['ENTRADA', 'SAIDA']:
            return Response(
                {'erro': 'Tipo deve ser "ENTRADA" ou "SAIDA"'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.get_queryset().filter(tipo=tipo)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='resumo')
    def resumo(self, request):
        """
        Retorna um resumo das movimentações do período.
        """
        from django.db.models import Sum, Count
        from datetime import timedelta
        from django.utils import timezone
        
        dias = int(request.query_params.get('dias', 30))
        data_inicio = timezone.now() - timedelta(days=dias)
        
        movimentacoes = self.get_queryset().filter(data_movimentacao__gte=data_inicio)
        
        entradas = movimentacoes.filter(tipo='ENTRADA').aggregate(
            quantidade=Sum('quantidade'),
            valor=Sum('quantidade') * Sum('valor_unitario'),
            count=Count('id')
        )
        
        saidas = movimentacoes.filter(tipo='SAIDA').aggregate(
            quantidade=Sum('quantidade'),
            valor=Sum('quantidade') * Sum('valor_unitario'),
            count=Count('id')
        )
        
        return Response({
            'periodo_dias': dias,
            'entradas': entradas,
            'saidas': saidas,
            'total_movimentacoes': movimentacoes.count()
        })


# Importar models para usar em queries
from django.db import models
