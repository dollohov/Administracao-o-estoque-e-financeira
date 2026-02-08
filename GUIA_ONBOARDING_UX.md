# 🚀 Guia de Onboarding e Manual de UX - Gestão ERP

Este documento serve como o manual de identidade e experiência do usuário para o software **Gestão ERP**. Ele foi projetado para garantir que qualquer empresa ou funcionário que utilize o sistema entenda rapidamente sua finalidade e como operá-lo com eficiência.

---

## 1. 🎯 Propósito do Software
O **Gestão ERP** não é apenas um banco de dados; é uma ferramenta de **tomada de decisão**. 
*   **Para o Empresário:** Oferece visão clara do lucro real e saúde financeira.
*   **Para o Funcionário:** Simplifica tarefas repetitivas e garante que o estoque esteja sempre correto.

---

## 2. 🏁 Onboarding: Primeiros Passos (Checklist)

Para uma nova empresa cliente, siga esta ordem de configuração para garantir o sucesso:

### Passo 1: Identidade e Segurança
*   [ ] **Configurar Usuários:** Crie contas para cada funcionário com o nível de acesso correto (Vendedor, Gerente ou Admin).
*   [ ] **Personalizar Perfil:** Garanta que cada usuário tenha seu nome completo para que a **Auditoria** funcione corretamente.

### Passo 2: Estrutura de Dados
*   [ ] **Cadastrar Fornecedores:** Antes de cadastrar produtos, registre quem os fornece.
*   [ ] **Definir Categorias:** Organize seu catálogo (ex: Eletrônicos, Limpeza, Escritório).

### Passo 3: Inventário Inicial
*   [ ] **Carga de Estoque:** Use a **Importação de NF-e** para cadastrar produtos em massa de forma automática e precisa.
*   [ ] **Conferência:** Verifique se os preços de custo e venda estão corretos para garantir cálculos de lucro precisos.

### Passo 4: Saúde Financeira
*   [ ] **Capital de Giro:** Defina o valor inicial em caixa para que o sistema possa monitorar o fluxo de caixa.

---

## 3. 🎨 Manual de Identidade Visual e UX

### Linguagem de Cores (Semântica)
O sistema utiliza cores para comunicar estados sem a necessidade de leitura:
*   🔵 **Azul (Primary):** Ações principais, navegação e informações neutras.
*   🟢 **Verde (Success):** Entradas de estoque, receitas financeiras, ações concluídas com sucesso.
*   🔴 **Vermelho (Danger):** Saídas de estoque, despesas, alertas críticos, erros.
*   🟡 **Amarelo (Warning):** Alertas de atenção (estoque baixo), edições de registros.

### Uso de Ícones e Abstração
Sempre utilize ícones ao lado de textos de ação. O cérebro processa imagens 60.000 vezes mais rápido que texto.
*   **Botões de Ação:** Devem ter um ícone à esquerda (ex: `<i class="bi bi-plus-circle"></i> Novo`).
*   **Estatísticas:** Devem ter um ícone grande ao fundo para identificação rápida do contexto.

---

## 4. 📖 Glossário de Campos (O que é o quê?)

Para facilitar o entendimento dos funcionários, aqui estão as definições dos termos técnicos usados no sistema:

| Termo | O que significa? | Por que é importante? |
| :--- | :--- | :--- |
| **SKU** | Stock Keeping Unit | Seu código "apelido" para o produto. Facilita a busca rápida. |
| **NCM** | Nomenclatura Comum do Mercosul | Código fiscal obrigatório. Sem ele, você não emite nota fiscal. |
| **Capital de Giro** | Dinheiro em caixa | É o "combustível" da empresa para pagar contas e comprar estoque. |
| **Margem de Lucro** | Porcentagem de ganho | Mostra quanto de cada venda realmente sobra para a empresa. |
| **Auditoria** | Rastro digital | Registro de "quem fez o quê e quando". Garante segurança e evita erros. |

---

## 5. 💡 Dicas de Ouro para o Usuário
1.  **Passe o mouse:** Sempre que vir um ícone de interrogação (`?`), passe o mouse para ler uma explicação detalhada.
2.  **Use a Busca:** O catálogo possui filtros poderosos. Não perca tempo rolando páginas, use o SKU ou Nome.
3.  **NF-e é sua amiga:** Sempre que possível, importe o XML da nota. Isso evita erros de digitação e economiza horas de trabalho.

---

## 🛠️ Suporte e Manutenção
Em caso de dúvidas técnicas, consulte o administrador do sistema ou abra um chamado através do módulo de suporte.
