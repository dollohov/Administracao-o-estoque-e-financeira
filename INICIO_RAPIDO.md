# 🚀 Guia de Início Rápido - Sistema ERP

## Instalação em 5 Minutos

### 1️⃣ Preparar o Ambiente

```bash
# Clonar o repositório
git clone https://github.com/dollohov/Administracao-o-estoque-e-financeira.git
cd Administracao-o-estoque-e-financeira

# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows
```

### 2️⃣ Instalar Dependências

```bash
pip install -r requirements.txt
```

### 3️⃣ Configurar Banco de Dados

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4️⃣ Configurar Permissões e Usuários

```bash
python setup_permissions.py
```

**Usuários criados automaticamente:**
- `admin` / `admin123` (Administrador)
- `gerente` / `gerente123` (Gerente)
- `funcionario` / `func123` (Funcionário)

### 5️⃣ Iniciar o Servidor

```bash
python manage.py runserver
```

Acesse: **http://127.0.0.1:8000/**

---

## 📋 Primeiros Passos

### Após o Login

1. **Cadastre produtos** (Menu: Estoque → Produtos → Novo Produto)
2. **Defina capital inicial** (Menu: Financeiro → Capital de Giro)
3. **Registre movimentações** (Menu: Estoque → Nova Movimentação)

---

## 👥 Grupos de Usuários

| Grupo | Acesso | Uso Recomendado |
|-------|--------|-----------------|
| **Administradores** | Total | Proprietários, Diretores |
| **Gerentes** | Visualização + Edição Limitada | Gerentes, Supervisores |
| **Funcionários** | Operações Básicas | Vendedores, Operadores |

---

## 🔑 Funcionalidades Principais

### ✅ Estoque
- Cadastro de produtos
- Controle de entradas e saídas
- Alertas de estoque baixo
- Cálculo de margem de lucro

### 💰 Financeiro
- Registro de receitas e despesas
- Controle de capital de giro
- Cálculo automático de lucros/perdas
- Relatórios financeiros

### 🔒 Segurança
- Sistema de permissões por grupo
- Rastreamento de todas as operações
- Auditoria completa de usuários

---

## 📊 Fluxo Básico de Uso

### Registrar uma Venda

1. Acesse: **Estoque → Nova Movimentação**
2. Selecione o produto
3. Tipo: **SAÍDA**
4. Informe quantidade e valor de venda
5. Confirme

**O sistema automaticamente:**
- ✅ Atualiza o estoque
- ✅ Adiciona ao capital de giro
- ✅ Registra seu usuário
- ✅ Calcula o lucro

### Registrar uma Compra

1. Acesse: **Estoque → Nova Movimentação**
2. Selecione o produto
3. Tipo: **ENTRADA**
4. Informe quantidade e valor de custo
5. Confirme

**O sistema automaticamente:**
- ✅ Atualiza o estoque
- ✅ Subtrai do capital de giro
- ✅ Registra seu usuário

---

## 🆘 Problemas Comuns

### "Estoque insuficiente"
➡️ Verifique a quantidade disponível do produto

### "Capital insuficiente"
➡️ Adicione capital de giro em: Financeiro → Capital de Giro

### Sem permissões
➡️ Verifique se seu usuário está em um grupo (contate o administrador)

---

## 📚 Documentação Completa

Para mais detalhes, consulte: **[DOCUMENTACAO.md](DOCUMENTACAO.md)**

---

## 🎯 Próximos Passos

1. ✅ Cadastre seus produtos reais
2. ✅ Configure o capital de giro inicial
3. ✅ Crie usuários para sua equipe
4. ✅ Comece a registrar operações
5. ✅ Explore os relatórios e dashboards

---

## 💡 Dicas

- Use o **painel admin** (`/admin/`) para configurações avançadas
- Todos os dashboards são atualizados em **tempo real**
- O sistema **calcula automaticamente** lucros e perdas
- **Todas as operações** são rastreadas com usuário e data

---

**Desenvolvido com ❤️ por Denis Barbosa**
