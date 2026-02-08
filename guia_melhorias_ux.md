# 🎨 Guia de Melhorias de UX e Abstração Visual - Gestão ERP

Este guia apresenta uma série de recomendações e melhorias práticas para tornar o software mais intuitivo, facilitando a adoção por novos funcionários e empresas clientes.

---

## 1. 🧩 Abstração Visual com Ícones

O uso de ícones deve ser consistente em todo o sistema para que o usuário identifique a função antes mesmo de ler o texto.

### Padronização de Ícones (Bootstrap Icons)

| Módulo / Ação | Ícone Sugerido | Finalidade |
| :--- | :--- | :--- |
| **Estoque** | `bi-box-seam` | Representa produtos físicos e armazenamento. |
| **Financeiro** | `bi-cash-coin` | Representa dinheiro, fluxo de caixa e transações. |
| **Fiscal** | `bi-file-earmark-medical` | Representa documentos oficiais e notas fiscais. |
| **Vendas** | `bi-cart-check` | Representa o ato de vender e pedidos concluídos. |
| **Entrada** | `bi-arrow-down-circle` | Movimentação de entrada (cor verde). |
| **Saída** | `bi-arrow-up-circle` | Movimentação de saída (cor vermelha). |
| **Relatórios** | `bi-graph-up-arrow` | Análise de dados e crescimento. |
| **Ajuda/Info** | `bi-question-circle` | Dicas e explicações de campos. |

---

## 2. 💡 Dicas de Contexto (Tooltips e Help Texts)

Para que o usuário entenda "para que serve cada campo", devemos implementar três níveis de ajuda:

### A. Tooltips (Dicas ao passar o mouse)
Adicionar um pequeno ícone de interrogação ao lado dos rótulos (labels) dos campos mais complexos.
*   **Exemplo (NCM):** "Código de 8 dígitos que identifica a categoria do produto para fins fiscais."
*   **Exemplo (SKU):** "Seu código interno para organizar o estoque (ex: CAM-AZUL-G)."

### B. Help Texts (Textos de apoio fixos)
Textos curtos logo abaixo do campo de entrada.
*   **Exemplo (Preço de Venda):** "O sistema calculará automaticamente o lucro com base no preço de custo."

### C. Placeholders Inteligentes
Usar o campo vazio para mostrar um exemplo de preenchimento.
*   **Exemplo (Localização):** "Ex: Corredor A, Prateleira 2"

---

## 3. 🚀 Onboarding: O "Dashboard de Boas-Vindas"

Para uma empresa que acaba de adquirir o software, o primeiro acesso é crucial.

### Sugestão de "Guia de Configuração Inicial"
No topo da página inicial, exibir um card de progresso para o administrador:
1.  [ ] **Configurar Dados da Empresa** (Razão Social, CNPJ)
2.  [ ] **Cadastrar Primeiro Fornecedor**
3.  [ ] **Importar Primeira NF-e ou Cadastrar Produto**
4.  [ ] **Definir Capital de Giro Inicial**

---

## 4. 📊 Dashboards Autoexplicativos

Os gráficos não devem apenas mostrar números, mas contar uma história.

*   **Status de Saúde:** Em vez de apenas "Saldo: R$ 10.000", usar "Seu saldo atual cobre as despesas dos próximos 15 dias" (baseado na média de gastos).
*   **Alertas Visuais:** Produtos abaixo do estoque mínimo devem ter um ícone de "⚠️" piscando ou uma linha vermelha na tabela.

---

## 5. 🛠️ Implementação Técnica (Exemplos)

### Como adicionar um Tooltip no Django/Bootstrap:
```html
<label for="ncm">
    NCM 
    <i class="bi bi-question-circle text-muted" 
       data-bs-toggle="tooltip" 
       data-bs-placement="top" 
       title="Código fiscal de 8 dígitos para identificação da mercadoria.">
    </i>
</label>
```

### Como adicionar Help Text dinâmico:
```html
<input type="number" id="preco_venda" class="form-control">
<div class="form-text text-info">
    <i class="bi bi-info-circle"></i> 
    Dica: Margem de lucro sugerida para esta categoria é de 30%.
</div>
```

---

## 📈 Próximos Passos Sugeridos

1.  **Revisão de Labels:** Trocar termos técnicos por termos mais amigáveis (ex: "Movimentação de Estoque" -> "Entrada/Saída de Mercadoria").
2.  **Cores Semânticas:** Garantir que o sistema use Verde para Sucesso/Entrada, Vermelho para Erro/Saída/Crítico e Amarelo para Alerta/Atenção.
3.  **Feedback Visual:** Adicionar animações simples de "Loading" ao processar NF-e para o usuário saber que o sistema está trabalhando.
