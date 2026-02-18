# 🏢 Gestão ERP - Sistema de Administração de Estoque e Financeira

<div align="center">

![Django](https://img.shields.io/badge/Django-5.2.9-green)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.3-purple)
![License](https://img.shields.io/badge/License-Proprietário-red)

**Sistema ERP completo para gestão de estoque e controle financeiro**

[Documentação](DOCUMENTACAO.md) • [Início Rápido](INICIO_RAPIDO.md) • [Demo](#demo)

</div>

---

## 📋 Sobre o Projeto

Sistema de Planejamento de Recursos Empresariais (ERP) desenvolvido em Django com foco em **simplicidade**, **segurança** e **rastreabilidade**. Ideal para pequenas e médias empresas que precisam de controle eficiente de estoque e finanças.

### ✨ Destaques da Versão 3.5

- ✅ **Módulo Fiscal**: Importação automática de NF-e via XML.
- ✅ **Catálogo de Vendedores**: Interface otimizada para consulta de vendas.
- ✅ **Sistema de Permissões**: Grupos (Admin, Gerente, Funcionário, Vendedor).
- ✅ **Gestão de Imagens**: Suporte a múltiplas fotos de produtos.
- ✅ **Rastreamento de Usuários**: Auditoria completa em todas as operações.
- ✅ **Controle de Capital de Giro**: Integrado com compras (NF-e) e vendas.

---

## 🚀 Funcionalidades

### 📦 Módulo de Estoque e Catálogo
- **Cadastro Completo**: Produtos com SKU, NCM, CEST, EAN/GTIN, dimensões e pesos.
- **Catálogo de Vendedores**: Visualização em grade (cards) com fotos e preços.
- **Gestão de Imagens**: Upload e gerenciamento de fotos de produtos.
- **Alertas**: Notificações visuais para estoque baixo ou crítico.

### 📄 Módulo Fiscal
- **Importação de NF-e**: Processamento automático de arquivos XML.
- **Automação**: Criação de produtos e fornecedores a partir da nota fiscal.
- **Gestão de Fornecedores**: Cadastro completo e histórico de compras.

### 💰 Módulo Financeiro
- **Capital de Giro**: Controle em tempo real integrado ao estoque.
- **Fluxo de Caixa**: Registro automático de despesas e receitas.
- **Indicadores**: Margem de lucro, valor de estoque e giro de produtos.

### 🔒 Segurança e Controle
- **Níveis de Acesso**: Admin, Gerente, Funcionário e Vendedor.
- **Auditoria**: Registro de quem criou e modificou cada registro.
- **Proteção**: Conformidade com boas práticas de segurança Django.

---

## 🎯 Grupos de Usuários

| Grupo | Permissões | Ideal Para |
|-------|-----------|------------|
| **👑 Administradores** | Acesso total ao sistema | Proprietários, Diretores |
| **📊 Gerentes** | Gestão de estoque e financeiro | Gerentes, Supervisores |
| **👤 Funcionários** | Operações de movimentação | Operadores de Estoque |
| **🛍️ Vendedores** | Acesso exclusivo ao Catálogo | Equipe de Vendas |

---

## 📸 Screenshots

### Dashboard Principal
![Dashboard](https://via.placeholder.com/800x400/667eea/ffffff?text=Dashboard+Principal)

### Controle de Estoque
![Estoque](https://via.placeholder.com/800x400/11998e/ffffff?text=Controle+de+Estoque)

### Dashboard Financeiro
![Financeiro](https://via.placeholder.com/800x400/f093fb/ffffff?text=Dashboard+Financeiro)

---

## 🛠️ Tecnologias

- **Backend:** Django 5.2.9 (Python)
- **Frontend:** Bootstrap 5.3.3
- **Banco de Dados:** SQLite (dev) / PostgreSQL (produção)
- **Ícones:** Bootstrap Icons 1.11.3
- **Gráficos:** Chart.js 4.4.1

---

## 📦 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip
- virtualenv (recomendado)

### Instalação Rápida

```bash
# 1. Clonar o repositório
git clone https://github.com/dollohov/Administracao-o-estoque-e-financeira.git
cd Administracao-o-estoque-e-financeira

# 2. Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Configurar banco de dados
python manage.py makemigrations
python manage.py migrate

# 5. Configurar permissões e criar usuários
python setup_permissions.py

# 6. Iniciar servidor
python manage.py runserver
```

Acesse: **http://127.0.0.1:8000/**

### 🔐 Acesso ao Sistema

O sistema já vem com um usuário administrador padrão criado automaticamente durante a migração do banco de dados.

| Usuário | Senha | Grupo | Observação |
|---------|-------|-------|------------|
| **admin** | **admin123** | Administrador | Criado automaticamente |
| gerente | gerente123 | Gerente | Criar via painel admin |
| funcionario | func123 | Funcionário | Criar via painel admin |

> **Dica:** Toda vez que você clonar o repositório e rodar `python manage.py migrate`, o usuário **admin** será garantido com a senha **admin123**.

---

## 📖 Documentação

- **[Documentação Completa](DOCUMENTACAO.md)** - Guia detalhado do sistema
- **[Início Rápido](INICIO_RAPIDO.md)** - Comece em 5 minutos
- **[Changelog](CHANGELOG.md)** - Histórico de versões

---

## 🎓 Como Usar

### Exemplo: Registrar uma Venda

```python
# O sistema faz tudo automaticamente!
# 1. Acesse: Estoque → Nova Movimentação
# 2. Selecione o produto
# 3. Tipo: SAÍDA
# 4. Quantidade e valor
# 5. Confirme

# O sistema automaticamente:
# ✅ Atualiza o estoque
# ✅ Adiciona ao capital de giro
# ✅ Registra seu usuário
# ✅ Calcula o lucro
```

### Exemplo: Visualizar Relatórios

```python
# Acesse: Financeiro → Relatórios
# Visualize:
# - Receitas vs Despesas
# - Lucro/Prejuízo do período
# - Gráficos por categoria
# - Indicadores financeiros
```

---

## 🔧 Configuração Avançada

### Usar PostgreSQL em Produção

```python
# Em settings.py, substitua:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'gestao_erp',
        'USER': 'seu_usuario',
        'PASSWORD': 'sua_senha',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Habilitar HTTPS

```python
# Em settings.py, descomente:
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

---

## 📝 Melhorias Implementadas (v2.0)

### ✅ Sistema de Permissões
- Três grupos de usuários com permissões específicas
- Controle granular de acesso
- Isolamento entre áreas de funcionários e administração

### ✅ Rastreamento de Usuários
- Registro de quem criou cada item
- Registro de quem modificou cada item
- Data e hora de todas as operações
- Auditoria completa do sistema

### ✅ Capital de Giro
- Controle automático do capital disponível
- Histórico de todas as movimentações
- Integração com vendas e compras
- Alertas de capital insuficiente

### ✅ Lucros e Perdas
- Cálculo automático de margem de lucro por produto
- Resultado mensal (receitas - despesas)
- Indicadores financeiros por período
- Gráficos e visualizações

### ✅ Interface Visual
- Design moderno com Bootstrap 5
- Sidebar de navegação intuitiva
- Cards informativos e estatísticas
- Gráficos interativos
- Totalmente responsivo

### ✅ Código Comentado
- Docstrings em todas as funções
- Comentários explicativos
- Documentação inline
- Padrões de código consistentes

---

## 🐛 Problemas Conhecidos

Nenhum problema conhecido no momento. Reporte bugs através das [Issues](https://github.com/dollohov/Administracao-o-estoque-e-financeira/issues).

---

## 📜 Licença

Este software é de autoria de **Denis Barbosa**. Todos os direitos são reservados. O uso, cópia ou distribuição não autorizada é estritamente proibida.

---

## 👨‍💻 Autor

**Desenvolvido por:** Denis Barbosa  
**Data:** Fevereiro de 2026  
**Versão:** 3.5 (Estável)

---

## 🙏 Agradecimentos

- Django Software Foundation
- Bootstrap Team
- Comunidade Python
- Todos os contribuidores

---

## 📞 Suporte

Para dúvidas ou suporte:
- 📧 Email: [suporte@exemplo.com](mailto:suporte@exemplo.com)
- 🐛 Issues: [GitHub Issues](https://github.com/dollohov/Administracao-o-estoque-e-financeira/issues)
- 📖 Documentação: [DOCUMENTACAO.md](DOCUMENTACAO.md)

---

<div align="center">

**⭐ Se este projeto foi útil, considere dar uma estrela!**

[⬆ Voltar ao topo](#-gestão-erp---sistema-de-administração-de-estoque-e-financeira)

</div>
