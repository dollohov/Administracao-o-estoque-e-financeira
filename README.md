# Gestão ERP - Administração de Estoque e Financeira

Este é um projeto básico de ERP (Enterprise Resource Planning) desenvolvido em **Django (Python)** com frontend utilizando **Bootstrap 5**. O objetivo é fornecer uma solução simples para a administração de estoque e controle financeiro (receitas e despesas).

## Funcionalidades

*   **Estoque:** Cadastro de produtos e registro de movimentações de estoque (entrada/saída).
*   **Financeiro:** Registro de receitas e despesas.
*   **Interface:** Painel de administração do Django e visualização de dados com Bootstrap.

## Instalação e Configuração

### 1. Clonar o Repositório

```bash
git clone https://github.com/dollohov/Administracao-o-estoque-e-financeira.git
cd Administracao-o-estoque-e-financeira
```

### 2. Configurar o Ambiente Virtual

É altamente recomendável usar um ambiente virtual para isolar as dependências do projeto.

```bash
python3 -m venv venv
source venv/bin/activate  # No Linux/macOS
# venv\Scripts\activate  # No Windows
```

### 3. Instalar Dependências

Instale todas as dependências necessárias usando o arquivo `requirements.txt`.

```bash
pip install -r requirements.txt
```

### 4. Configurar o Banco de Dados

O projeto utiliza o SQLite por padrão. Você precisa aplicar as migrações para criar o banco de dados.

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Criar Superusuário (Admin)

Para acessar o painel de administração, crie um superusuário.

```bash
python manage.py createsuperuser
# Siga as instruções na tela
```

**Credenciais Padrão (Criadas automaticamente para este projeto):**
*   **Usuário:** `admin`
*   **Senha:** `admin`

## Execução do Projeto

Para iniciar o servidor de desenvolvimento do Django:

```bash
python manage.py runserver
```

O projeto estará acessível em `http://127.0.0.1:8000/`.

## Acesso ao Painel de Administração

O painel de administração está disponível em `http://127.0.0.1:8000/admin/`. Use as credenciais do superusuário para fazer login e gerenciar:
*   Produtos
*   Movimentações de Estoque
*   Receitas
*   Despesas
