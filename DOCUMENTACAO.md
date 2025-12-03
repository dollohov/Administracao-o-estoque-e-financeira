# Documentação do Sistema ERP - Gestão de Estoque e Financeira

## Índice

1. [Visão Geral](#visão-geral)
2. [Melhorias Implementadas](#melhorias-implementadas)
3. [Instalação e Configuração](#instalação-e-configuração)
4. [Sistema de Permissões](#sistema-de-permissões)
5. [Módulos do Sistema](#módulos-do-sistema)
6. [Fluxo de Trabalho](#fluxo-de-trabalho)
7. [Guia de Uso](#guia-de-uso)
8. [Manutenção e Suporte](#manutenção-e-suporte)

---

## Visão Geral

O Sistema ERP de Gestão de Estoque e Financeira é uma aplicação web desenvolvida em Django que oferece controle completo sobre as operações de estoque e finanças de uma empresa. O sistema foi completamente reformulado com foco em usabilidade, segurança e rastreabilidade.

### Tecnologias Utilizadas

- **Backend:** Django 5.2.9 (Python)
- **Frontend:** Bootstrap 5.3.3
- **Banco de Dados:** SQLite (desenvolvimento) / PostgreSQL (produção recomendado)
- **Ícones:** Bootstrap Icons 1.11.3
- **Gráficos:** Chart.js 4.4.1

---

## Melhorias Implementadas

### 1. Sistema de Permissões e Grupos de Usuários

O sistema agora possui três grupos de usuários com permissões distintas:

#### **Administradores**
- Acesso total ao sistema
- Gerenciamento de usuários e permissões
- Acesso ao painel administrativo do Django
- Visualização e edição de todos os dados
- Gestão de capital de giro

#### **Gerentes**
- Visualização de todos os dados
- Edição de produtos e movimentações de estoque
- Cadastro de receitas e despesas
- Visualização de relatórios financeiros
- Visualização do capital de giro (sem edição)

#### **Funcionários/Vendedores**
- Visualização de produtos
- Registro de movimentações de estoque (entradas e saídas)
- Visualização de receitas de vendas
- Acesso limitado apenas às operações do dia a dia

### 2. Rastreamento de Usuários

Todos os registros agora incluem informações sobre:
- **Usuário que criou o registro**
- **Data e hora de criação**
- **Usuário que modificou o registro** (quando aplicável)
- **Data e hora da última modificação**

Isso garante total rastreabilidade e auditoria de todas as operações do sistema.

### 3. Controle de Capital de Giro

Novo módulo para gerenciamento do capital de giro da empresa:
- **Histórico completo** de todas as movimentações
- **Atualização automática** com base em receitas e despesas
- **Integração** com movimentações de estoque
- **Visualização** do saldo atual em tempo real
- **Alertas** de capital insuficiente

### 4. Cálculo de Lucros e Perdas

O sistema agora calcula automaticamente:
- **Margem de lucro** por produto
- **Lucro unitário** de cada item
- **Resultado mensal** (receitas - despesas)
- **Margem de lucro percentual** do período
- **Indicadores financeiros** por categoria

### 5. Interface Visual Aprimorada

Completamente redesenhada com:
- **Design moderno** e responsivo
- **Sidebar** de navegação intuitiva
- **Cards informativos** com estatísticas
- **Gráficos** e visualizações de dados
- **Tabelas** organizadas e filtráveis
- **Cores** e ícones intuitivos para cada tipo de operação
- **Compatibilidade mobile** total

### 6. Código Comentado

Todo o código foi documentado com:
- **Docstrings** em todas as funções e classes
- **Comentários explicativos** em trechos complexos
- **Organização** lógica dos arquivos
- **Padrões** de nomenclatura consistentes

---

## Instalação e Configuração

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Virtualenv (recomendado)

### Passo 1: Clonar o Repositório

```bash
git clone https://github.com/dollohov/Administracao-o-estoque-e-financeira.git
cd Administracao-o-estoque-e-financeira
```

### Passo 2: Criar Ambiente Virtual

```bash
python3 -m venv venv
source venv/bin/activate  # No Linux/macOS
# venv\Scripts\activate  # No Windows
```

### Passo 3: Instalar Dependências

```bash
pip install -r requirements.txt
```

### Passo 4: Configurar Banco de Dados

```bash
python manage.py makemigrations
python manage.py migrate
```

### Passo 5: Configurar Grupos e Permissões

```bash
python setup_permissions.py
```

Este script irá:
- Criar os três grupos de usuários (Administradores, Gerentes, Funcionários)
- Atribuir as permissões apropriadas a cada grupo
- Criar usuários de exemplo (opcional)

**Usuários de exemplo criados:**
- **admin** / admin123 (Administrador)
- **gerente** / gerente123 (Gerente)
- **funcionario** / func123 (Funcionário)

### Passo 6: Inicializar Capital de Giro (Opcional)

Para definir um capital de giro inicial, acesse o shell do Django:

```bash
python manage.py shell
```

Execute:

```python
from financeiro.models import CapitalGiro
from django.contrib.auth.models import User

admin = User.objects.get(username='admin')
CapitalGiro.objects.create(
    valor_anterior=0,
    valor_novo=10000.00,  # Valor inicial desejado
    tipo_movimentacao='ENTRADA',
    descricao='Capital inicial da empresa',
    usuario=admin
)
```

### Passo 7: Executar o Servidor

```bash
python manage.py runserver
```

Acesse: `http://127.0.0.1:8000/`

---

## Sistema de Permissões

### Estrutura de Grupos

O sistema utiliza o sistema de grupos e permissões nativo do Django. Cada grupo possui um conjunto específico de permissões que determina o que seus membros podem fazer.

### Atribuindo Usuários a Grupos

#### Via Painel Admin:

1. Acesse `/admin/`
2. Vá em "Usuários"
3. Selecione o usuário
4. Na seção "Permissões", adicione o grupo desejado
5. Salve

#### Via Shell do Django:

```python
from django.contrib.auth.models import User, Group

# Obter usuário e grupo
usuario = User.objects.get(username='nome_usuario')
grupo = Group.objects.get(name='Gerentes')

# Adicionar ao grupo
usuario.groups.add(grupo)
```

### Criando Novos Usuários

```bash
python manage.py createsuperuser
```

Ou via código:

```python
from django.contrib.auth.models import User, Group

# Criar usuário
usuario = User.objects.create_user(
    username='novo_usuario',
    email='usuario@empresa.com',
    password='senha_segura',
    first_name='Nome',
    last_name='Sobrenome',
    is_staff=True  # Permite acesso ao admin
)

# Adicionar ao grupo
grupo = Group.objects.get(name='Funcionários')
usuario.groups.add(grupo)
```

---

## Módulos do Sistema

### Módulo de Estoque

#### Funcionalidades:
- Cadastro de produtos
- Controle de estoque atual
- Definição de estoque mínimo
- Alertas de estoque baixo
- Registro de movimentações (entradas e saídas)
- Cálculo de margem de lucro
- Relatórios de produtos mais vendidos

#### Modelos:

**Produto:**
- Nome e descrição
- Preço de custo e venda
- Estoque atual e mínimo
- Status (ativo/inativo)
- Rastreamento de usuário

**MovimentacaoEstoque:**
- Produto relacionado
- Tipo (entrada/saída)
- Quantidade
- Valor unitário
- Observações
- Usuário responsável

### Módulo Financeiro

#### Funcionalidades:
- Registro de receitas
- Registro de despesas
- Gestão de capital de giro
- Cálculo de lucro/prejuízo
- Indicadores financeiros
- Relatórios por categoria
- Histórico de movimentações

#### Modelos:

**Receita:**
- Descrição
- Valor
- Data
- Categoria
- Usuário responsável

**Despesa:**
- Descrição
- Valor
- Data
- Categoria
- Usuário responsável

**CapitalGiro:**
- Valor anterior e novo
- Tipo de movimentação
- Descrição
- Usuário responsável
- Data e hora

**IndicadorFinanceiro:**
- Período (mês/ano)
- Total de receitas
- Total de despesas
- Lucro bruto
- Margem de lucro

---

## Fluxo de Trabalho

### Fluxo de Compra de Produtos

1. **Funcionário/Gerente** acessa "Estoque" → "Nova Movimentação"
2. Seleciona o produto
3. Escolhe tipo "ENTRADA"
4. Informa quantidade e valor unitário
5. Adiciona observações (opcional)
6. Confirma a operação

**O sistema automaticamente:**
- Adiciona a quantidade ao estoque
- Registra o usuário responsável
- Subtrai o valor do capital de giro (compra = saída de capital)
- Atualiza os indicadores

### Fluxo de Venda de Produtos

1. **Funcionário/Gerente** acessa "Estoque" → "Nova Movimentação"
2. Seleciona o produto
3. Escolhe tipo "SAÍDA"
4. Informa quantidade e valor unitário (preço de venda)
5. Adiciona observações (opcional)
6. Confirma a operação

**O sistema automaticamente:**
- Subtrai a quantidade do estoque
- Verifica se há estoque suficiente
- Registra o usuário responsável
- Adiciona o valor ao capital de giro (venda = entrada de capital)
- Gera uma receita automaticamente
- Atualiza os indicadores

### Fluxo de Registro de Despesa

1. **Gerente/Administrador** acessa "Financeiro" → "Nova Despesa"
2. Preenche descrição e valor
3. Seleciona a data
4. Escolhe a categoria
5. Confirma a operação

**O sistema automaticamente:**
- Registra a despesa
- Subtrai o valor do capital de giro
- Verifica se há capital suficiente
- Atualiza os indicadores do período

---

## Guia de Uso

### Para Administradores

#### Gerenciar Usuários:
1. Acesse `/admin/`
2. Vá em "Usuários"
3. Crie, edite ou desative usuários
4. Atribua grupos e permissões

#### Visualizar Logs:
- Todos os registros possuem informações de rastreamento
- Acesse o painel admin para ver quem criou/modificou cada registro

#### Ajustar Capital de Giro:
1. Acesse "Financeiro" → "Capital de Giro"
2. Clique em "Ajustar Capital"
3. Escolha entrada ou saída
4. Informe o valor e descrição
5. Confirme

### Para Gerentes

#### Cadastrar Produto:
1. Acesse "Estoque" → "Produtos" → "Novo Produto"
2. Preencha os dados do produto
3. Defina preços e estoque mínimo
4. Salve

#### Gerar Relatórios:
1. Acesse "Estoque" → "Relatórios" ou "Financeiro" → "Relatórios"
2. Selecione o período desejado
3. Visualize os indicadores e gráficos

### Para Funcionários

#### Registrar Venda:
1. Acesse "Estoque" → "Nova Movimentação"
2. Selecione o produto vendido
3. Tipo: "SAÍDA"
4. Informe quantidade e valor
5. Confirme

#### Registrar Entrada de Estoque:
1. Acesse "Estoque" → "Nova Movimentação"
2. Selecione o produto
3. Tipo: "ENTRADA"
4. Informe quantidade e valor de custo
5. Confirme

---

## Manutenção e Suporte

### Backup do Banco de Dados

#### SQLite:
```bash
cp db.sqlite3 backup_$(date +%Y%m%d).sqlite3
```

#### PostgreSQL:
```bash
pg_dump nome_banco > backup_$(date +%Y%m%d).sql
```

### Atualização do Sistema

1. Faça backup do banco de dados
2. Atualize o código
3. Execute as migrações:
```bash
python manage.py makemigrations
python manage.py migrate
```
4. Colete arquivos estáticos (se necessário):
```bash
python manage.py collectstatic
```

### Logs do Sistema

Os logs são armazenados em `logs/django.log` e incluem:
- Erros do sistema
- Avisos
- Informações de acesso

### Solução de Problemas Comuns

#### Erro: "Estoque insuficiente"
- Verifique a quantidade disponível do produto
- Certifique-se de que o estoque foi atualizado corretamente

#### Erro: "Capital insuficiente"
- Verifique o saldo do capital de giro
- Adicione capital se necessário

#### Usuário sem permissões:
- Verifique se o usuário está atribuído a um grupo
- Confirme as permissões do grupo no painel admin

### Contato para Suporte

Para dúvidas ou problemas:
- Consulte esta documentação
- Entre em contato com o administrador do sistema
- Abra uma issue no repositório GitHub

---

## Considerações de Segurança

### Em Produção:

1. **Altere a SECRET_KEY** em `settings.py`
2. **Defina DEBUG=False**
3. **Configure ALLOWED_HOSTS** com seus domínios
4. **Use HTTPS** (SSL/TLS)
5. **Configure backup automático** do banco de dados
6. **Use PostgreSQL** ao invés de SQLite
7. **Habilite as configurações de segurança** comentadas em `settings.py`
8. **Use variáveis de ambiente** para dados sensíveis

### Boas Práticas:

- Troque as senhas padrão imediatamente
- Use senhas fortes para todos os usuários
- Revise as permissões regularmente
- Monitore os logs do sistema
- Mantenha o Django e dependências atualizados

---

## Licença

Este projeto é de código aberto e está disponível sob a licença MIT.

---

## Créditos

**Desenvolvido por:** Manus AI  
**Data:** Dezembro de 2025  
**Versão:** 2.0  

---

**Última atualização:** 02/12/2025
