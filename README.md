# 🏢 Gestão ERP - Sistema de Administração de Estoque e Financeira

<div align="center">

![Django](https://img.shields.io/badge/Django-5.2.9-green)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.3-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

**Sistema ERP completo para gestão de estoque e controle financeiro**

[Documentação](DOCUMENTACAO.md) • [Início Rápido](INICIO_RAPIDO.md) • [Demo](#demo)

</div>

---

## 📋 Sobre o Projeto

Sistema de Planejamento de Recursos Empresariais (ERP) desenvolvido em Django com foco em **simplicidade**, **segurança** e **rastreabilidade**. Ideal para pequenas e médias empresas que precisam de controle eficiente de estoque e finanças.

### ✨ Destaques da Versão 2.0

- ✅ **Sistema de Permissões** completo (Administradores, Gerentes, Funcionários)
- ✅ **Rastreamento de Usuários** em todas as operações
- ✅ **Controle de Capital de Giro** automático
- ✅ **Cálculo de Lucros e Perdas** em tempo real
- ✅ **Interface Visual Moderna** e responsiva
- ✅ **Código 100% Comentado** e documentado

---

## 🚀 Funcionalidades

### 📦 Módulo de Estoque

- Cadastro completo de produtos
- Controle de entradas e saídas
- Alertas de estoque baixo
- Cálculo automático de margem de lucro
- Histórico de movimentações
- Relatórios de produtos mais vendidos

### 💰 Módulo Financeiro

- Registro de receitas e despesas
- Gestão de capital de giro
- Cálculo automático de lucro/prejuízo
- Indicadores financeiros por período
- Relatórios por categoria
- Gráficos e visualizações

### 🔒 Segurança e Controle

- Sistema de autenticação robusto
- Grupos de usuários com permissões específicas
- Rastreamento completo de operações
- Auditoria de todas as ações
- Proteção CSRF e XSS

---

## 🎯 Grupos de Usuários

| Grupo | Permissões | Ideal Para |
|-------|-----------|------------|
| **👑 Administradores** | Acesso total ao sistema | Proprietários, Diretores |
| **📊 Gerentes** | Visualização + Edição limitada | Gerentes, Supervisores |
| **👤 Funcionários** | Operações básicas de estoque | Vendedores, Operadores |

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

### Usuários de Teste

| Usuário | Senha | Grupo |
|---------|-------|-------|
| admin | admin123 | Administrador |
| gerente | gerente123 | Gerente |
| funcionario | func123 | Funcionário |

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

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👨‍💻 Autor

**Desenvolvido por:** Manus AI  
**Data:** Dezembro de 2025  
**Versão:** 2.0

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
