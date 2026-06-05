# 🚀 Guia de Deployment no Render

## Passo 1: Acessar o Render Dashboard
1. Abra: https://dashboard.render.com
2. Faça login com sua conta

## Passo 2: Criar Novo Serviço Web
1. Clique em **"+ New"** (canto superior direito)
2. Selecione **"Web Service"**

## Passo 3: Conectar o Repositório GitHub
1. Clique em **"Connect a repository"**
2. Autorize o Render a acessar seu GitHub (se necessário)
3. Selecione: `Administracao-o-estoque-e-financeira`
4. Clique em **"Connect"**

## Passo 4: Configurar o Serviço
Na próxima tela, preencha:

| Campo | Valor |
|-------|-------|
| **Name** | `erp-telegram-secure` |
| **Branch** | `nodejs-react-erp` |
| **Runtime** | `Node` |
| **Build Command** | `bash .render-build.sh` |
| **Start Command** | `pnpm start` |
| **Plan** | `Starter` (ou `Free` se preferir) |
| **Region** | `US East (N. Virginia)` |

## Passo 5: Adicionar Variáveis de Ambiente
Clique em **"Advanced"** e adicione:

```
NODE_ENV = production
PORT = 3000
VITE_APP_TITLE = Gestão ERP + Telegram Seguro
```

Se você tiver banco de dados, adicione também:
```
DATABASE_URL = sua_url_do_banco_de_dados
JWT_SECRET = sua_chave_secreta_aqui
```

## Passo 6: Criar o Serviço
1. Clique em **"Create Web Service"**
2. Aguarde o build completar (2-5 minutos)
3. Seu app estará online em: `https://erp-telegram-secure.onrender.com`

## ✅ Pronto!
Seu projeto está em produção! 🎉

---

## Troubleshooting

### Build falha?
- Verifique se a branch `nodejs-react-erp` existe no GitHub
- Verifique se o arquivo `.render-build.sh` está no repositório

### App não inicia?
- Verifique os logs no Render Dashboard
- Confirme que as variáveis de ambiente estão corretas

### Precisa de banco de dados?
O Render oferece PostgreSQL gratuito. Para adicionar:
1. No dashboard, clique em **"+ New"**
2. Selecione **"PostgreSQL"**
3. Configure e conecte ao seu serviço web

---

**Dúvidas?** Acesse: https://render.com/docs
