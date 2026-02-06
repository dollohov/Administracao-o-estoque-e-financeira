# Guia Rápido - Importação de NF-e

## 🚀 Como Importar uma Nota Fiscal Eletrônica

### Passo 1: Preparar o Arquivo XML

Certifique-se de ter o arquivo XML da NF-e. O arquivo deve ter a extensão `.xml` e conter os dados completos da nota fiscal eletrônica.

### Passo 2: Acessar o Sistema

1. Faça login no sistema ERP
2. No menu lateral, clique em **Fiscal**
3. Selecione **Importar NF-e**

### Passo 3: Fazer Upload do XML

1. Na tela de importação, clique em **Escolher arquivo** ou arraste o XML para a área indicada
2. Selecione o arquivo XML da NF-e
3. Clique no botão **Importar NF-e**

### Passo 4: Aguardar o Processamento

O sistema irá automaticamente:

✅ Extrair dados do fornecedor (emitente da nota)  
✅ Criar ou atualizar o cadastro do fornecedor  
✅ Registrar a nota fiscal no sistema  
✅ Processar todos os itens da nota  
✅ Criar produtos automaticamente (se não existirem)  
✅ Gerar movimentações de entrada no estoque  
✅ Registrar a despesa no módulo financeiro  
✅ Atualizar o capital de giro  

### Passo 5: Verificar o Resultado

Após o processamento, você será redirecionado para a página de detalhes da NF-e, onde poderá visualizar:

- Dados completos da nota fiscal
- Informações do fornecedor
- Lista de todos os itens importados
- Valores e impostos detalhados
- Status da importação

---

## 📋 O Que Acontece Durante a Importação

### 1. Fornecedor

- Se o fornecedor **já existir** (mesmo CNPJ): os dados são atualizados
- Se o fornecedor **não existir**: um novo cadastro é criado automaticamente

### 2. Produtos

- O sistema busca produtos existentes pela descrição
- Se o produto **não existir**: é criado automaticamente com:
  - Nome e descrição da NF-e
  - Preço de custo do XML
  - Preço de venda com margem de 30%
  - Estoque inicial zerado (será atualizado pela movimentação)

### 3. Estoque

- Para cada item da NF-e, uma **movimentação de entrada** é criada
- O estoque do produto é **atualizado automaticamente**
- A movimentação fica vinculada à NF-e para rastreabilidade

### 4. Financeiro

- Uma **despesa** é registrada com o valor total da NF-e
- O **capital de giro** é reduzido (saída de capital)
- Se não houver capital suficiente, um aviso é registrado

---

## 🔍 Visualizar NF-es Importadas

### Acessar a Lista

1. Menu **Fiscal** → **NF-es**
2. Visualize todas as notas fiscais importadas

### Filtrar NF-es

Você pode filtrar por:
- **Status**: Pendente, Processada, Erro, Cancelada
- **Fornecedor**: Selecione um fornecedor específico

### Ver Detalhes

Clique em qualquer NF-e da lista para visualizar:
- Chave de acesso
- Número e série
- Fornecedor emissor
- Data de emissão
- Valores totais e impostos
- Lista completa de itens
- Arquivo XML original

---

## 👥 Gerenciar Fornecedores

### Acessar Fornecedores

1. Menu **Fiscal** → **Fornecedores**
2. Visualize todos os fornecedores cadastrados

### Ver Histórico de Compras

1. Clique em um fornecedor da lista
2. Visualize:
   - Dados cadastrais completos
   - Todas as NF-es deste fornecedor
   - Valor total de compras
   - Quantidade de notas fiscais

---

## ⚠️ Tratamento de Erros

### NF-e Duplicada

Se você tentar importar uma NF-e que já foi importada anteriormente (mesma chave de acesso), o sistema irá:
- Detectar a duplicação
- Exibir mensagem de erro
- **Não processar** novamente

### XML Inválido

Se o arquivo XML estiver malformado ou incompleto:
- O sistema exibirá uma mensagem de erro detalhada
- A NF-e será marcada com status **ERRO**
- Verifique o arquivo e tente novamente

### Capital Insuficiente

Se não houver capital de giro suficiente para registrar a compra:
- A NF-e será processada normalmente
- Um **aviso** será registrado nas observações
- O estoque será atualizado
- Você deverá ajustar o capital de giro manualmente

---

## 📊 Exemplo de Uso

### Cenário: Importar NF-e de Compra

**Situação**: Você recebeu uma compra de 10 unidades do Produto A e 5 unidades do Produto B, com NF-e no valor total de R$ 1.100,00.

**Ação**: Importar o XML da NF-e

**Resultado Automático**:

1. **Fornecedor**
   - Fornecedor "Exemplo LTDA" criado/atualizado
   - CNPJ: 12.345.678/0001-90

2. **Produtos**
   - Produto A: criado com estoque inicial 0
   - Produto B: criado com estoque inicial 0

3. **Estoque**
   - Produto A: +10 unidades (entrada)
   - Produto B: +5 unidades (entrada)

4. **Financeiro**
   - Despesa: R$ 1.100,00 (Compra de Mercadorias)
   - Capital de Giro: -R$ 1.100,00

5. **NF-e**
   - Status: Processada
   - 2 itens registrados
   - Impostos calculados: ICMS R$ 180,00, IPI R$ 100,00

---

## 🎯 Dicas e Boas Práticas

### ✅ Faça Sempre

- Verifique se o XML está completo antes de importar
- Confira os dados da NF-e após a importação
- Revise os produtos criados automaticamente
- Ajuste preços de venda se necessário
- Mantenha o capital de giro atualizado

### ❌ Evite

- Importar XMLs incompletos ou corrompidos
- Importar a mesma NF-e múltiplas vezes
- Modificar produtos enquanto a NF-e está sendo processada
- Deletar fornecedores com NF-es vinculadas

---

## 🔧 Solução de Problemas

### Problema: "Erro ao processar XML"

**Solução**:
1. Verifique se o arquivo é um XML válido
2. Abra o arquivo em um editor de texto e verifique a estrutura
3. Certifique-se de que é um XML de NF-e (modelo 55)

### Problema: "NF-e já foi importada"

**Solução**:
1. Verifique a lista de NF-es importadas
2. Se for uma duplicação legítima, ignore o erro
3. Se precisar reimportar, delete a NF-e anterior primeiro (via admin)

### Problema: "Capital insuficiente"

**Solução**:
1. Acesse **Financeiro** → **Capital de Giro**
2. Clique em **Ajustar Capital**
3. Adicione capital suficiente
4. A NF-e já terá sido processada normalmente

---

## 📞 Suporte

Para dúvidas ou problemas:
- Consulte a documentação completa em `DOCUMENTACAO.md`
- Verifique os logs em `logs/django.log`
- Entre em contato com o administrador do sistema

---

## 📝 Arquivo de Exemplo

Um arquivo XML de exemplo está disponível em:
```
exemplo_nfe.xml
```

Você pode usar este arquivo para testar a funcionalidade de importação.

---

**Última atualização**: 05 de Fevereiro de 2026  
**Versão do Sistema**: 3.0
