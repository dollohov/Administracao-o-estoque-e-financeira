# Solução para Erro do WeasyPrint no Termux

## Problema
Você está recebendo um erro similar a:
```
OSError: cannot load library 'libpango-1.0-0': dlopen failed: library "libpango-1.0-0" not found
```

Isso ocorre porque o WeasyPrint foi instalado, mas as bibliotecas de sistema necessárias (Pango, Cairo, etc.) não estão disponíveis no Termux.

## Solução Recomendada

### Opção 1: Desinstalar WeasyPrint (Recomendado para Termux)

O sistema foi atualizado para funcionar **sem o WeasyPrint**. Se você não precisa gerar PDFs no celular, simplesmente desinstale:

```bash
pip uninstall WeasyPrint -y
```

Após isso, o servidor iniciará normalmente e todas as funcionalidades funcionarão, exceto a geração de PDF (que exibirá uma mensagem amigável).

### Opção 2: Tentar Instalar Dependências de Sistema

Se você realmente precisa da geração de PDF, tente instalar as bibliotecas necessárias:

```bash
pkg install pango cairo libffi libpng libjpeg-turbo
pip install WeasyPrint
```

**Nota:** Essa abordagem pode não funcionar completamente no Termux devido a limitações do ambiente.

## Verificar se o Problema foi Resolvido

Após desinstalar o WeasyPrint, tente iniciar o servidor:

```bash
python manage.py runserver
```

Se o servidor iniciar sem erros, o problema foi resolvido!

## Próximos Passos

1. Crie um superusuário:
```bash
python manage.py createsuperuser
```

2. Inicie o servidor:
```bash
python manage.py runserver 0.0.0.0:8000
```

3. Acesse a aplicação em seu navegador

## Funcionalidades sem o WeasyPrint

Todas as funcionalidades funcionarão normalmente:
- ✅ Cadastro de produtos
- ✅ Gestão de estoque
- ✅ Criação de pedidos
- ✅ Relatórios e dashboards
- ✅ Notificações
- ✅ Contas a pagar/receber
- ❌ Geração de PDF (exibirá mensagem amigável)

## Alternativa para Gerar PDFs

Se você precisar gerar PDFs, considere:
1. Usar um computador com a versão completa do sistema
2. Usar um serviço online de conversão HTML para PDF
3. Exportar dados para Excel/CSV no celular

## Suporte

Se o problema persistir após seguir essas instruções, verifique:
- Se o ambiente virtual está ativado: `source venv/bin/activate`
- Se o WeasyPrint foi realmente desinstalado: `pip list | grep -i weasy`
- Os logs do servidor para mensagens de erro adicionais
