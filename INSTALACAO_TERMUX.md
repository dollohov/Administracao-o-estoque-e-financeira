# Guia de Instalação no Termux

Este documento fornece instruções para instalar e executar o projeto de Gestão ERP no Termux (Android).

## Pré-requisitos

- Termux instalado no seu dispositivo Android
- Conexão com a internet
- Espaço em disco suficiente (~500MB)

## Passo 1: Atualizar o Termux

```bash
pkg update
pkg upgrade
```

## Passo 2: Instalar Dependências do Sistema

```bash
pkg install python git clang libffi openssl libjpeg-turbo libpng zlib
```

## Passo 3: Clonar o Repositório

```bash
cd ~
git clone https://github.com/dollohov/Administracao-o-estoque-e-financeira.git
cd Administracao-o-estoque-e-financeira
```

## Passo 4: Criar Ambiente Virtual

```bash
python -m venv venv
source venv/bin/activate
```

## Passo 5: Instalar Dependências Python

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Nota sobre WeasyPrint no Termux

O WeasyPrint pode ser problemático no Termux devido a dependências de sistema. Se encontrar erros ao instalar:

```bash
# Alternativa 1: Instalar sem WeasyPrint (a geração de PDF será desabilitada)
pip install -r requirements.txt --ignore-installed WeasyPrint
```

**Ou**

```bash
# Alternativa 2: Instalar dependências adicionais
pkg install libxml2 libxslt
pip install WeasyPrint
```

Se nenhuma das alternativas funcionar, o sistema funcionará normalmente, mas a geração de PDF será desabilitada com uma mensagem amigável ao usuário.

## Passo 6: Configurar o Banco de Dados

```bash
python manage.py migrate
python manage.py createsuperuser
```

## Passo 7: Executar o Servidor

```bash
python manage.py runserver 0.0.0.0:8000
```

Acesse a aplicação em: `http://localhost:8000` ou `http://<seu-ip>:8000`

## Solução de Problemas

### Erro: "ModuleNotFoundError: No module named 'weasyprint'"

Este é um erro esperado no Termux. A aplicação foi configurada para funcionar sem WeasyPrint:
- A geração de PDF será desabilitada
- Você receberá uma mensagem amigável ao tentar gerar um PDF
- Todas as outras funcionalidades continuarão funcionando normalmente

### Erro: "Permission denied" ao clonar repositório

Use HTTPS em vez de SSH:
```bash
git clone https://github.com/dollohov/Administracao-o-estoque-e-financeira.git
```

### Erro: "No space left on device"

Libere espaço no seu dispositivo e tente novamente.

### Erro: "ModuleNotFoundError" para outras bibliotecas

Certifique-se de que o ambiente virtual está ativado:
```bash
source venv/bin/activate
```

## Próximos Passos

1. Acesse o painel administrativo em `/admin`
2. Crie usuários e configure os grupos de permissão
3. Comece a usar o sistema!

## Suporte

Se encontrar problemas, verifique:
- Se o ambiente virtual está ativado (`source venv/bin/activate`)
- Se todas as dependências foram instaladas (`pip list`)
- Os logs do servidor Django para mensagens de erro específicas
