# Relatório de Testes e Correções do Sistema ERP

**Data:** 17 de Fevereiro de 2026
**Autor:** Denis Barbosa

## 1. Introdução

Este relatório detalha os testes realizados no sistema ERP de Gestão de Estoque e Financeira, clonado do repositório GitHub, e as correções implementadas para garantir seu funcionamento adequado. O objetivo foi simular um ambiente de deploy e verificar as funcionalidades principais dos módulos de Estoque e Financeiro.

## 2. Configuração do Ambiente e Dependências

O ambiente de teste foi configurado com PostgreSQL para simular um ambiente de produção. As dependências Python foram instaladas e as migrações do Django foram executadas. Um superusuário `admin` foi criado e vinculado a uma empresa de teste para permitir o acesso ao sistema.

## 3. Problemas Identificados e Correções

Durante os testes, foram identificados alguns problemas que impediam o funcionamento correto de certas funcionalidades. As seguintes correções foram aplicadas:

### 3.1. Erro de CSRF

**Problema:** Ao tentar fazer login no sistema, foi identificado um erro de CSRF (Cross-Site Request Forgery), impedindo o acesso.

**Correção:** A variável `CSRF_TRUSTED_ORIGINS` foi adicionada ao arquivo `gestao_erp/settings.py` para incluir o domínio temporário exposto pelo sandbox, permitindo que o navegador enviasse requisições POST com sucesso.

### 3.2. Erro de Lookup de Campo no Middleware (Multi-empresa)

**Problema:** O middleware `TenantMiddleware` em `companies/middleware.py` estava tentando acessar o campo `ativo` em vez de `active` no modelo `Company`, resultando em um `AttributeError` e impedindo o carregamento correto da empresa associada ao usuário.

**Correção:** O nome do campo foi corrigido de `company__ativo` para `company__active` no middleware. Além disso, foi criado um script `fix_tenant.py` para criar uma empresa de teste (`Empresa de Teste`) e vincular o usuário `admin` a ela, garantindo que o sistema operasse corretamente no modo multi-empresa.

### 3.3. Erro de Atributo no Módulo Financeiro (`CapitalGiro`)

**Problema:** Ao acessar o dashboard financeiro, foi encontrado um `AttributeError` (`type object 'CapitalGiro' has no attribute 'obter_capital_atual'`). O modelo `CapitalGiro` não possuía os métodos de classe `obter_capital_atual`, `adicionar_capital` e `retirar_capital`, que eram chamados nas views financeiras.

**Correção:** Os métodos de classe `obter_capital_atual`, `adicionar_capital` e `retirar_capital` foram implementados no modelo `CapitalGiro` em `financeiro/models.py`. Esses métodos agora recebem o objeto `company` como parâmetro para garantir que as operações de capital de giro sejam realizadas no contexto da empresa correta.

### 3.4. Templates Financeiros Ausentes

**Problema:** As páginas de cadastro de receita (`cadastrar_receita.html`) e despesa (`cadastrar_despesa.html`) estavam ausentes no diretório de templates do módulo financeiro, resultando em erros `TemplateDoesNotExist` ao tentar acessá-las.

**Correção:** Os templates `cadastrar_receita.html` e `cadastrar_despesa.html` foram criados no diretório `templates/financeiro/`, utilizando a estrutura de outros templates existentes como base. Isso permitiu que as páginas de cadastro fossem renderizadas corretamente.

### 3.5. Erro de `NoReverseMatch` nos Templates Financeiros

**Problema:** Após a criação dos templates financeiros, foi identificado um erro `NoReverseMatch` ao tentar redirecionar para o dashboard financeiro, pois o nome da URL `dashboard_financeiro` estava incorreto nos templates.

**Correção:** O nome da URL foi corrigido de `dashboard_financeiro` para `dashboard` nos templates `cadastrar_receita.html` e `cadastrar_despesa.html`, conforme definido no arquivo `financeiro/urls.py`.

## 4. Testes de Funcionalidade Pós-Correção

Após a aplicação das correções, as seguintes funcionalidades foram testadas com sucesso:

### 4.1. Módulo de Estoque

- **Login:** O login com o usuário `admin` foi realizado com sucesso.
- **Cadastro de Produto:** Um produto de teste (`Produto de Teste Manus`) foi cadastrado com sucesso no módulo de estoque. A associação do produto à `Empresa de Teste` foi verificada no banco de dados.
- **Visualização de Produtos:** A lista de produtos foi acessada e o produto de teste foi exibido corretamente, filtrado pela empresa associada.

### 4.2. Módulo Financeiro

- **Acesso ao Dashboard Financeiro:** O dashboard financeiro foi acessado com sucesso, exibindo o capital de giro atual e os indicadores financeiros.
- **Cadastro de Receita:** Uma receita de teste (`Venda de Teste Manus` no valor de R$ 1500,00) foi cadastrada com sucesso. O capital de giro foi atualizado corretamente, refletindo a entrada da receita.
- **Visualização de Receitas:** A lista de receitas foi acessada e a receita de teste foi exibida corretamente.

## 5. Conclusão

O sistema ERP de Gestão de Estoque e Financeira, após as correções implementadas, está funcionando conforme o esperado em um ambiente simulado de deploy. As funcionalidades principais dos módulos de Estoque e Financeiro foram testadas e validadas. As correções abordaram problemas de configuração, lógica de negócio e templates ausentes, garantindo a integridade e a usabilidade do sistema.

Este relatório serve como um registro das etapas de teste e depuração, bem como das melhorias aplicadas para estabilizar o projeto.
