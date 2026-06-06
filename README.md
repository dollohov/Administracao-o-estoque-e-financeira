# 🔐 ERP + Telegram Seguro

Sistema integrado de gestão empresarial com envio de mensagens criptografadas via Telegram usando AES-256.

## 🚀 Funcionalidades

- ✅ **Criptografia AES-256-CBC**: Todas as mensagens são criptografadas com segurança de nível empresarial
- ✅ **Integração Telegram**: Envio de mensagens, relatórios e alertas em tempo real
- ✅ **API REST Completa**: Endpoints para criptografia, descriptografia e gerenciamento de mensagens
- ✅ **Segurança**: Chaves de criptografia não são expostas no código
- ✅ **Pronto para Produção**: Deployable no Render, Railway, Vercel e outras plataformas

## 📋 Requisitos

- Node.js 18+
- pnpm (ou npm/yarn)
- Telegram Bot Token
- Telegram Chat ID

## 🔧 Instalação Local

```bash
# Clonar repositório
git clone https://github.com/dollohov/Administracao-o-estoque-e-financeira.git
cd Administracao-o-estoque-e-financeira
git checkout nodejs-react-erp

# Instalar dependências
pnpm install

# Configurar variáveis de ambiente
cat > .env << EOF
TELEGRAM_BOT_TOKEN=seu_bot_token
TELEGRAM_CHAT_ID=seu_chat_id
AES_ENCRYPTION_KEY=$(node -e "console.log(require('crypto').randomBytes(32).toString('hex'))")
AES_IV=$(node -e "console.log(require('crypto').randomBytes(16).toString('hex'))")
PORT=3000
NODE_ENV=development
EOF
```

## 🏃 Executar Localmente

```bash
# Modo desenvolvimento
pnpm dev

# Apenas servidor
pnpm server

# Build para produção
pnpm build

# Executar em produção
pnpm start
```

## 📡 Endpoints da API

### 1. Health Check
```bash
GET /health
```
Retorna o status do servidor e configuração do Telegram.

### 2. Enviar Mensagem Criptografada
```bash
POST /api/telegram/send
Content-Type: application/json

{
  "message": "Sua mensagem aqui",
  "encrypted": true
}
```

### 3. Criptografar Mensagem
```bash
POST /api/encrypt
Content-Type: application/json

{
  "message": "Texto a criptografar"
}

Response:
{
  "success": true,
  "encrypted": "...",
  "iv": "...",
  "key": "..."
}
```

### 4. Descriptografar Mensagem
```bash
POST /api/decrypt
Content-Type: application/json

{
  "encrypted": "texto_criptografado",
  "iv": "seu_iv",
  "key": "sua_chave"
}

Response:
{
  "success": true,
  "message": "Texto descriptografado"
}
```

### 5. Enviar Relatório
```bash
POST /api/telegram/report
Content-Type: application/json

{
  "title": "Relatório de Estoque",
  "data": {
    "total": 1000,
    "disponível": 850,
    "reservado": 150
  }
}
```

### 6. Enviar Alerta
```bash
POST /api/telegram/alert
Content-Type: application/json

{
  "type": "Estoque Baixo",
  "message": "Produto X com estoque abaixo do mínimo"
}
```

## 🔐 Segurança

### Geração de Chaves Seguras

```bash
# Gerar chave AES-256 (64 caracteres hexadecimais)
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"

# Gerar IV (32 caracteres hexadecimais)
node -e "console.log(require('crypto').randomBytes(16).toString('hex'))"
```

### Boas Práticas

1. **Nunca compartilhe chaves**: As chaves de criptografia devem ser mantidas seguras
2. **Use HTTPS**: Em produção, sempre use HTTPS
3. **Valide entrada**: Todas as entradas são validadas
4. **Rotação de chaves**: Altere as chaves periodicamente
5. **Logs**: Dados sensíveis não são registrados

## 🚀 Deploy no Render

1. Conecte seu repositório GitHub ao Render
2. Selecione a branch `nodejs-react-erp`
3. Configure as variáveis de ambiente:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
   - `AES_ENCRYPTION_KEY`
   - `AES_IV`
   - `NODE_ENV=production`
4. Build command: `pnpm build`
5. Start command: `pnpm start`

## 🧪 Testes

```bash
# Testar health check
curl http://localhost:3000/health

# Testar criptografia
curl -X POST http://localhost:3000/api/encrypt \
  -H "Content-Type: application/json" \
  -d '{"message":"Teste"}'

# Executar suite de testes
pnpm test
```

## 📊 Monitoramento e Manutenção

### Logs
- Verifique os logs do Render em: https://dashboard.render.com
- Logs locais em: `.manus-logs/` (se usando Manus)

### Health Checks
- Endpoint: `GET /health`
- Frequência recomendada: A cada 5 minutos

### Rotação de Chaves
1. Gere novas chaves
2. Atualize as variáveis de ambiente
3. Reinicie o serviço
4. Verifique os logs

## 🔄 Fluxo de Funcionamento

```
Cliente
   ↓
POST /api/telegram/send
   ↓
Servidor Express
   ├─ Criptografa mensagem (AES-256)
   ├─ Envia para Telegram API
   └─ Retorna sucesso/erro
   ↓
Telegram Bot
   ↓
Usuário recebe mensagem criptografada
```

## 📚 Estrutura do Projeto

```
├── server.ts           # Servidor Express
├── package.json        # Dependências
├── tsconfig.json       # Configuração TypeScript
├── test-api.sh         # Script de testes
├── .env.example        # Variáveis de exemplo
└── README.md           # Este arquivo
```

## 🤝 Suporte

Para dúvidas ou problemas:
1. Verifique os logs
2. Confirme as variáveis de ambiente
3. Teste os endpoints manualmente
4. Abra uma issue no repositório

## 📝 Licença

MIT

---

**Desenvolvido com ❤️ para segurança e eficiência**

**Última atualização:** Junho 2026
