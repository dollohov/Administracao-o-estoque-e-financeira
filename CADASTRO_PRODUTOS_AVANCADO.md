# Guia de Cadastro Avançado de Produtos

Este documento descreve todos os campos disponíveis no novo sistema de cadastro de produtos, otimizado para conformidade fiscal, logística e integração com o catálogo de vendedores.

---

## 1. Acessar o Cadastro de Produtos

1. Acesse o **Painel Administrativo** em `http://seu-dominio.com/admin/`
2. Navegue até **Estoque → Produtos**
3. Clique em **Adicionar Produto** para criar um novo ou edite um existente

---

## 2. Campos Disponíveis

### 2.1 Informações Básicas

| Campo | Tipo | Obrigatório | Descrição |
| :--- | :--- | :--- | :--- |
| **Nome** | Texto (200 caracteres) | ✅ Sim | Nome completo do produto |
| **Descrição** | Texto longo | ❌ Não | Descrição detalhada para o catálogo |
| **Marca** | Texto (100 caracteres) | ❌ Não | Marca ou fabricante do produto |
| **Categoria** | Texto (100 caracteres) | ❌ Não | Ex: Eletrônicos, Vestuário, Alimentos |
| **Subcategoria** | Texto (100 caracteres) | ❌ Não | Ex: Notebooks, Camisetas, Bebidas |

**Exemplo:**
- Nome: `Notebook Dell Inspiron 15 3000`
- Marca: `Dell`
- Categoria: `Eletrônicos`
- Subcategoria: `Computadores`

---

### 2.2 Identificação e Códigos Fiscais

Estes campos são **essenciais para emissão de NF-e e conformidade fiscal**.

| Campo | Tipo | Obrigatório | Descrição | Exemplo |
| :--- | :--- | :--- | :--- | :--- |
| **SKU** | Texto único (100 caracteres) | ❌ Não | Código interno único da empresa | `DELL-I15-3000-001` |
| **NCM** | Número (8 dígitos) | ⚠️ Recomendado | Nomenclatura Comum do Mercosul | `84715000` |
| **CEST** | Número (7 dígitos) | ❌ Não | Código Especificador da Substituição Tributária | `0100100` |
| **EAN/GTIN** | Número (13-14 dígitos) | ❌ Não | Código de barras com dígito verificador | `5901234123457` |

**Como encontrar o NCM:**

1. Acesse [Tabela NCM do MDIC](https://www.gov.br/produtividade-e-comercio-exterior/pt-br/assuntos/comercio-exterior/ncm)
2. Busque pelo nome do produto
3. Copie o código de 8 dígitos

**Validação do EAN:**
- EAN-13: 13 dígitos (mais comum)
- EAN-14: 14 dígitos (para embalagens logísticas)
- O último dígito é um verificador calculado automaticamente

---

### 2.3 Precificação

| Campo | Tipo | Obrigatório | Descrição |
| :--- | :--- | :--- | :--- |
| **Preço de Custo** | Decimal (2 casas) | ✅ Sim | Valor pago pelo produto (custo de aquisição) |
| **Preço de Venda** | Decimal (2 casas) | ✅ Sim | Valor de venda ao cliente |
| **Margem de Lucro** | Calculado automaticamente | - | Percentual de lucro (somente leitura) |

**Exemplo:**
- Preço de Custo: `R$ 1.500,00`
- Preço de Venda: `R$ 2.500,00`
- Margem de Lucro: `66,67%` (calculado automaticamente)

---

### 2.4 Controle de Estoque

| Campo | Tipo | Obrigatório | Descrição |
| :--- | :--- | :--- | :--- |
| **Estoque Atual** | Inteiro | ✅ Sim | Quantidade disponível em estoque |
| **Estoque Mínimo** | Inteiro | ✅ Sim (padrão: 10) | Quantidade mínima para alerta de reposição |
| **Estoque Máximo** | Inteiro | ✅ Sim (padrão: 100) | Quantidade máxima recomendada |
| **Valor Total em Estoque** | Calculado | - | Valor investido no estoque (somente leitura) |

**Alertas Automáticos:**
- 🔴 **Estoque Baixo**: Quando `Estoque Atual < Estoque Mínimo`
- 🟠 **Estoque Alto**: Quando `Estoque Atual > Estoque Máximo`
- 🟢 **Estoque Normal**: Quando está entre mínimo e máximo

---

### 2.5 Dimensões e Logística

Estes campos são usados para cálculo de frete e otimização de armazenamento.

| Campo | Tipo | Obrigatório | Descrição | Unidade |
| :--- | :--- | :--- | :--- | :--- |
| **Peso** | Decimal (3 casas) | ❌ Não | Peso do produto | kg |
| **Altura** | Decimal (2 casas) | ❌ Não | Altura da embalagem | cm |
| **Largura** | Decimal (2 casas) | ❌ Não | Largura da embalagem | cm |
| **Profundidade** | Decimal (2 casas) | ❌ Não | Profundidade da embalagem | cm |
| **Volume** | Decimal (6 casas) | Calculado | Volume total (altura × largura × profundidade) | m³ |

**Exemplo de Cálculo de Volume:**
- Altura: `30 cm`
- Largura: `20 cm`
- Profundidade: `15 cm`
- Volume: `0,009 m³` (calculado automaticamente)

---

### 2.6 Localização no Estoque

| Campo | Tipo | Obrigatório | Descrição |
| :--- | :--- | :--- | :--- |
| **Localização no Estoque** | Texto (100 caracteres) | ❌ Não | Endereço físico no armazém |

**Exemplo de Formato:**
- `Corredor A, Estante 2, Prateleira 3, Caixa 5`
- `Sala 1, Rack 5, Posição 12`
- `Zona A, Bloco 2, Nível 3`

---

### 2.7 Impostos

Alíquotas aplicáveis ao produto para cálculo fiscal em NF-e.

| Campo | Tipo | Obrigatório | Descrição |
| :--- | :--- | :--- | :--- |
| **Alíquota ICMS** | Decimal (2 casas) | ❌ Não | Percentual de ICMS (ex: 18.00) |
| **Alíquota IPI** | Decimal (2 casas) | ❌ Não | Percentual de IPI (ex: 15.00) |
| **Alíquota PIS** | Decimal (2 casas) | ❌ Não | Percentual de PIS |
| **Alíquota COFINS** | Decimal (2 casas) | ❌ Não | Percentual de COFINS |

**Alíquotas Padrão (Brasil):**
- ICMS: 18% (varia por estado)
- IPI: 0% a 35% (depende do produto)
- PIS: 1,65% ou 7,6%
- COFINS: 7,6% ou 9,25%

---

### 2.8 Imagem e Catálogo

| Campo | Tipo | Obrigatório | Descrição |
| :--- | :--- | :--- | :--- |
| **Imagem** | Arquivo (JPG, PNG) | ❌ Não | Foto do produto para catálogo |
| **Visível no Catálogo** | Checkbox | ✅ Sim (padrão: Sim) | Se marcado, aparece no catálogo de vendedores |

**Recomendações de Imagem:**
- Formato: JPG ou PNG
- Tamanho: Máximo 5 MB
- Resolução: Mínimo 800×600 pixels
- Fundo: Branco ou neutro para melhor visualização

---

### 2.9 Fornecedor

| Campo | Tipo | Obrigatório | Descrição |
| :--- | :--- | :--- | :--- |
| **Fornecedor Principal** | Seleção | ❌ Não | Fornecedor padrão para reposição |

**Como usar:**
1. Selecione um fornecedor já cadastrado
2. Este será usado como padrão em pedidos de compra
3. Pode ser alterado em cada compra específica

---

### 2.10 Status

| Campo | Tipo | Obrigatório | Descrição |
| :--- | :--- | :--- | :--- |
| **Produto Ativo** | Checkbox | ✅ Sim (padrão: Sim) | Se desmarcado, o produto não aparece em vendas |

---

## 3. API de Consulta para Vendedores

O sistema fornece uma API REST para que vendedores consultem produtos em tempo real.

### 3.1 Endpoints Disponíveis

#### Listar Produtos (com filtros)
```
GET /api/estoque/produtos/
```

**Filtros disponíveis:**
- `categoria`: Filtrar por categoria
- `marca`: Filtrar por marca
- `search`: Buscar por nome, SKU ou descrição
- `ordering`: Ordenar por (nome, preco_venda, estoque_atual)

**Exemplo:**
```
GET /api/estoque/produtos/?categoria=Eletrônicos&search=notebook
```

**Resposta:**
```json
[
  {
    "id": 1,
    "nome": "Notebook Dell Inspiron 15 3000",
    "sku": "DELL-I15-3000-001",
    "preco_venda": "2500.00",
    "estoque_atual": 15,
    "estoque_status": "NORMAL",
    "categoria": "Eletrônicos",
    "marca": "Dell",
    "imagem": "/media/produtos/dell_notebook.jpg",
    "margem_lucro": 66.67,
    "ean_gtin": "5901234123457"
  }
]
```

#### Buscar Produto por SKU
```
GET /api/estoque/produtos/buscar/por-sku/?sku=DELL-I15-3000-001
```

**Resposta Completa:**
```json
{
  "id": 1,
  "nome": "Notebook Dell Inspiron 15 3000",
  "descricao": "Notebook com processador Intel Core i5...",
  "sku": "DELL-I15-3000-001",
  "ncm": "84715000",
  "cest": "0100100",
  "ean_gtin": "5901234123457",
  "preco_custo": "1500.00",
  "preco_venda": "2500.00",
  "margem_lucro": 66.67,
  "lucro_unitario": "1000.00",
  "estoque_atual": 15,
  "estoque_minimo": 5,
  "estoque_maximo": 50,
  "valor_total_estoque": "22500.00",
  "categoria": "Eletrônicos",
  "subcategoria": "Computadores",
  "marca": "Dell",
  "peso_kg": "2.500",
  "altura_cm": "35.00",
  "largura_cm": "25.00",
  "profundidade_cm": "20.00",
  "volume_m3": "0.017500",
  "localizacao_estoque": "Corredor A, Estante 2",
  "icms_aliquota": "18.00",
  "ipi_aliquota": "0.00",
  "pis_aliquota": "1.65",
  "cofins_aliquota": "7.60",
  "imagem": "/media/produtos/dell_notebook.jpg",
  "visivel_catalogo": true,
  "ativo": true,
  "data_criacao": "2025-12-07T10:30:00Z",
  "data_modificacao": "2025-12-07T15:45:00Z"
}
```

#### Buscar Produto por Código de Barras
```
GET /api/estoque/produtos/buscar/por-codigo-barras/?ean=5901234123457
```

#### Catálogo para Vendedores
```
GET /api/estoque/produtos/catalogo/vendedores/
```

Retorna apenas produtos visíveis no catálogo com informações essenciais.

#### Produtos com Estoque Baixo
```
GET /api/estoque/produtos/estoque/baixo/
```

Útil para alertas de reposição.

#### Buscar Múltiplos Produtos
```
POST /api/estoque/produtos/buscar-multiplos/
```

**Body:**
```json
{
  "skus": ["DELL-I15-3000-001", "HP-PAVILION-15"],
  "eans": ["5901234123457", "5901234123458"]
}
```

---

## 4. Fluxo de Entrada/Saída de Produtos

### 4.1 Registrar Entrada de Estoque

1. Acesse **Estoque → Movimentações de Estoque**
2. Clique em **Adicionar Movimentação**
3. Preencha:
   - **Produto**: Selecione o produto
   - **Tipo**: Selecione `ENTRADA`
   - **Quantidade**: Quantidade recebida
   - **Valor Unitário**: Preço pago
   - **Observação**: Ex: "Nota Fiscal NF-e 123456"
4. Clique em **Salvar**

O estoque será atualizado automaticamente.

### 4.2 Registrar Saída de Estoque

1. Acesse **Estoque → Movimentações de Estoque**
2. Clique em **Adicionar Movimentação**
3. Preencha:
   - **Produto**: Selecione o produto
   - **Tipo**: Selecione `SAÍDA`
   - **Quantidade**: Quantidade vendida/devolvida
   - **Valor Unitário**: Preço de venda
   - **Observação**: Ex: "Venda PDV #123" ou "Devolução cliente"
4. Clique em **Salvar**

O sistema verificará se há estoque suficiente antes de permitir a saída.

---

## 5. Conformidade Fiscal

### 5.1 Campos Obrigatórios para NF-e

Para emitir uma Nota Fiscal Eletrônica (NF-e), o produto deve ter:

- ✅ **Nome**: Preenchido
- ✅ **NCM**: Código de 8 dígitos
- ✅ **Preço de Venda**: Preenchido

### 5.2 Campos Recomendados

- 📋 **SKU**: Para rastreamento interno
- 📋 **EAN/GTIN**: Para código de barras
- 📋 **CEST**: Se aplicável (substituição tributária)
- 📋 **Alíquotas de Impostos**: Para cálculo correto

---

## 6. Boas Práticas

### 6.1 Nomenclatura de SKU

Use um padrão consistente:
- **Formato**: `MARCA-CATEGORIA-MODELO-VERSAO`
- **Exemplo**: `DELL-NOTEBOOK-I15-001`
- **Benefício**: Fácil identificação e rastreamento

### 6.2 Organização de Estoque

Mantenha a localização atualizada:
- Use um mapa visual do armazém
- Atualize quando produtos são movidos
- Facilita picking e contagem de estoque

### 6.3 Imagens de Produtos

- Tire fotos em boa iluminação
- Use fundo branco ou neutro
- Mostre o produto de vários ângulos
- Comprima para máximo 1 MB

### 6.4 Atualização de Preços

- Revise preços de custo regularmente
- Acompanhe inflação e custos operacionais
- Mantenha margem de lucro competitiva

---

## 7. Troubleshooting

### Erro: "NCM inválido"
- Verifique se tem exatamente 8 dígitos
- Consulte a tabela NCM oficial

### Erro: "EAN/GTIN já existe"
- O código de barras já está cadastrado em outro produto
- Verifique se não é duplicação

### Erro: "Estoque insuficiente"
- Não há quantidade suficiente para saída
- Registre uma entrada antes de fazer a saída

---

**Desenvolvido por**: Denis Barbosa  
**Data**: 07 de Dezembro de 2025
