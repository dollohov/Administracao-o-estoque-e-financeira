# Guia de Integração das Novas Views do PDV

Este guia explica como integrar as novas views otimizadas (`pdv/views_v2.py`) ao seu projeto.

## Passo 1: Atualizar URLs do PDV

Edite o arquivo `pdv/urls.py` e adicione as novas rotas:

```python
from django.urls import path
from . import views, views_v2

app_name = 'pdv'

urlpatterns = [
    # Views originais
    path('', views.dashboard_pdv, name='dashboard'),
    path('nova-venda/', views.nova_venda, name='nova_venda'),
    path('venda/<int:pk>/', views.detalhes_venda, name='detalhes_venda'),
    path('abrir-caixa/', views.abrir_caixa, name='abrir_caixa'),
    path('fechar-caixa/', views.fechar_caixa, name='fechar_caixa'),
    
    # APIs melhoradas
    path('api/buscar-produto/', views_v2.buscar_produto, name='buscar_produto'),
    path('api/buscar-cliente/', views_v2.buscar_cliente, name='buscar_cliente'),
    path('api/obter-detalhes-produto/<int:produto_id>/', views_v2.obter_detalhes_produto, name='obter_detalhes_produto'),
]
```

## Passo 2: Atualizar Templates do PDV

No template `pdv/nova_venda.html`, atualize o JavaScript para usar os novos endpoints:

```html
<!-- Busca por código de barras -->
<input type="text" id="codigo-barras" placeholder="Código de barras (EAN)">

<script>
document.getElementById('codigo-barras').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        const codigo = this.value;
        
        // Chamar a API melhorada
        fetch(`/pdv/api/buscar-produto/?termo=${codigo}&tipo=barcode`)
            .then(response => response.json())
            .then(data => {
                if (data.produtos.length > 0) {
                    const produto = data.produtos[0];
                    
                    // Obter detalhes completos
                    fetch(`/pdv/api/obter-detalhes-produto/${produto.id}/`)
                        .then(r => r.json())
                        .then(detalhes => {
                            // Exibir imagem e detalhes
                            console.log(detalhes);
                            // Adicionar à venda
                        });
                }
            });
    }
});
</script>
```

## Passo 3: Verificar Dependências

Certifique-se de que o modelo `Produto` possui os novos campos:

```python
# Em estoque/models.py
class Produto(models.Model):
    # ... campos existentes ...
    sku = models.CharField(max_length=100, blank=True, null=True)
    ncm = models.CharField(max_length=10, blank=True, null=True)
    ean_gtin = models.CharField(max_length=14, blank=True, null=True)
    localizacao_estoque = models.CharField(max_length=50, blank=True, null=True)
```

## Passo 4: Testar as APIs

```bash
# Teste de busca por código de barras
curl "http://localhost:8000/pdv/api/buscar-produto/?termo=7891234567890&tipo=barcode"

# Teste de busca por nome
curl "http://localhost:8000/pdv/api/buscar-produto/?termo=Camisa&tipo=text"

# Teste de busca de cliente
curl "http://localhost:8000/pdv/api/buscar-cliente/?termo=João"

# Teste de detalhes do produto
curl "http://localhost:8000/pdv/api/obter-detalhes-produto/1/"
```

## Passo 5: Configurar Permissões

Adicione as permissões necessárias no Django Admin:

```python
# Em pdv/admin.py
from django.contrib import admin
from .models import Venda, ItemVenda, Caixa

@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = ['numero_venda', 'usuario', 'data_venda', 'total']
    list_filter = ['data_venda', 'metodo_pagamento']
    search_fields = ['numero_venda', 'usuario__username']
    readonly_fields = ['numero_venda', 'data_venda', 'total']
```

## Passo 6: Migrar Dados (Opcional)

Se você tem produtos existentes, atualize os campos fiscais:

```python
# Script para popular campos fiscais
from estoque.models import Produto

for produto in Produto.objects.all():
    if not produto.sku:
        produto.sku = f"SKU-{produto.id:06d}"
    if not produto.ean_gtin:
        # Gerar EAN aleatório para teste
        produto.ean_gtin = f"{produto.id:013d}"
    produto.save()
```

## Troubleshooting

### Erro: "Module 'pdv.views_v2' not found"

Certifique-se de que o arquivo `pdv/views_v2.py` está no diretório correto:
```
projeto_erp_repo/
├── pdv/
│   ├── views.py
│   ├── views_v2.py  ← Deve estar aqui
│   ├── urls.py
│   └── ...
```

### Erro: "Produto não tem atributo 'imagens'"

Certifique-se de que o modelo `ImagemProduto` está importado em `estoque/models.py`:

```python
# Em estoque/models.py
from .models_extended import CategoriaProduto, ProdutoAtributo, ImagemProduto
```

### API retorna lista vazia

Verifique se:
1. O produto existe no banco de dados
2. O produto está ativo (`ativo=True`)
3. O produto tem estoque (`estoque_atual > 0`)
4. O código de barras ou SKU está preenchido corretamente

## Próximas Melhorias

- [ ] Interface visual com drag-and-drop para adicionar itens
- [ ] Integração com leitores de código de barras USB
- [ ] Suporte a múltiplas formas de pagamento
- [ ] Emissão de NF-e diretamente do PDV
- [ ] Sincronização com sistema de entrega

---

**Desenvolvido por:** Denis Barbosa  
**Data:** 07 de Fevereiro de 2026
