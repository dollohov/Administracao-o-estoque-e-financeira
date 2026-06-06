# 🔧 Guia de Manutenção - ERP + Telegram Seguro

## 📋 Checklist de Manutenção Regular

### Diário
- [ ] Verificar logs do servidor
- [ ] Confirmar que o bot Telegram está respondendo
- [ ] Testar endpoint `/health`

### Semanal
- [ ] Revisar logs de erro
- [ ] Verificar uso de recursos (CPU, memória)
- [ ] Testar fluxo completo de criptografia/descriptografia
- [ ] Confirmar que mensagens estão sendo entregues

### Mensal
- [ ] Rotacionar chaves de criptografia
- [ ] Revisar logs de segurança
- [ ] Atualizar dependências
- [ ] Fazer backup de configurações
- [ ] Testar plano de disaster recovery

## 🔐 Rotação de Chaves

### Quando Rotacionar
- A cada 90 dias (recomendado)
- Após suspeita de comprometimento
- Quando trocar de ambiente
- Antes de mudanças de pessoal

### Como Rotacionar

1. **Gerar novas chaves**
```bash
# Nova chave AES-256
NEW_KEY=$(node -e "console.log(require('crypto').randomBytes(32).toString('hex'))")
echo "Nova chave: $NEW_KEY"

# Novo IV
NEW_IV=$(node -e "console.log(require('crypto').randomBytes(16).toString('hex'))")
echo "Novo IV: $NEW_IV"
```

2. **Atualizar variáveis de ambiente**
   - No Render: Settings → Environment
   - Atualize `AES_ENCRYPTION_KEY` e `AES_IV`

3. **Reiniciar serviço**
   - No Render: Manual Redeploy
   - Ou aguarde redeploy automático

4. **Testar funcionamento**
```bash
curl http://seu-dominio.onrender.com/health
```

5. **Documentar mudança**
   - Data da rotação
   - Motivo (rotina, segurança, etc)
   - Quem realizou

## 🚨 Troubleshooting

### Problema: Servidor não responde

**Solução:**
```bash
# 1. Verificar status
curl https://seu-dominio.onrender.com/health

# 2. Verificar logs
# No Render Dashboard → Logs

# 3. Reiniciar
# No Render Dashboard → Manual Redeploy

# 4. Verificar variáveis de ambiente
# No Render Dashboard → Environment
```

### Problema: Mensagens não chegam no Telegram

**Checklist:**
1. Verificar se `TELEGRAM_BOT_TOKEN` está correto
2. Verificar se `TELEGRAM_CHAT_ID` está correto
3. Confirmar que o bot tem permissão para enviar mensagens
4. Verificar se há limite de rate limiting do Telegram
5. Revisar logs do servidor

**Solução:**
```bash
# Testar bot token manualmente
curl -X GET "https://api.telegram.org/bot{TOKEN}/getMe"

# Testar envio de mensagem
curl -X POST "https://api.telegram.org/bot{TOKEN}/sendMessage" \
  -H "Content-Type: application/json" \
  -d '{"chat_id":"{CHAT_ID}","text":"Teste"}'
```

### Problema: Criptografia/Descriptografia falhando

**Checklist:**
1. Confirmar que a chave tem 64 caracteres hexadecimais
2. Confirmar que o IV tem 32 caracteres hexadecimais
3. Verificar se a chave não foi alterada entre criptografia e descriptografia
4. Revisar logs de erro

**Teste:**
```bash
# Testar criptografia
curl -X POST http://localhost:3000/api/encrypt \
  -H "Content-Type: application/json" \
  -d '{"message":"Teste"}'

# Copiar valores retornados e testar descriptografia
curl -X POST http://localhost:3000/api/decrypt \
  -H "Content-Type: application/json" \
  -d '{"encrypted":"...","iv":"...","key":"..."}'
```

## 📊 Monitoramento

### Métricas Importantes

1. **Uptime**: Deve estar acima de 99.5%
2. **Response Time**: Deve estar abaixo de 500ms
3. **Error Rate**: Deve estar abaixo de 0.1%
4. **CPU Usage**: Deve estar abaixo de 70%
5. **Memory Usage**: Deve estar abaixo de 80%

### Ferramentas de Monitoramento

- **Render Dashboard**: https://dashboard.render.com
- **Uptime Monitoring**: Use serviços como UptimeRobot
- **Logs**: Render fornece logs em tempo real

## 🔄 Backup e Disaster Recovery

### O que Fazer Backup

1. **Variáveis de Ambiente**
   - Salvar em local seguro (password manager, vault)
   - Nunca commitar no Git

2. **Configurações do Bot**
   - Token do Telegram
   - Chat IDs
   - Permissões

3. **Histórico de Chaves**
   - Manter registro de rotações
   - Datas de validade

### Plano de Recuperação

1. **Falha de Servidor**
   - Render faz redeploy automático
   - Se necessário, fazer manual redeploy
   - Verificar logs

2. **Perda de Credenciais**
   - Regenerar token do Telegram
   - Gerar novas chaves de criptografia
   - Atualizar variáveis de ambiente

3. **Comprometimento de Segurança**
   - Rotacionar todas as chaves imediatamente
   - Revogar token do Telegram
   - Gerar novo bot
   - Revisar logs para atividades suspeitas

## 📈 Escalabilidade

### Quando Escalar

- Response time > 1000ms
- CPU usage > 80%
- Memory usage > 90%
- Erro rate > 1%

### Como Escalar no Render

1. Upgrade do plano (Free → Starter → Professional)
2. Aumentar recursos (CPU, RAM)
3. Adicionar réplicas (load balancing)

## 🔍 Auditorias de Segurança

### Checklist Mensal

- [ ] Revisar logs de acesso
- [ ] Verificar se há tentativas de ataque
- [ ] Confirmar que chaves não foram expostas
- [ ] Revisar permissões de usuários
- [ ] Testar plano de disaster recovery

### Checklist Trimestral

- [ ] Rotacionar chaves
- [ ] Atualizar dependências
- [ ] Revisar código para vulnerabilidades
- [ ] Fazer teste de penetração
- [ ] Revisar políticas de segurança

## 📞 Contatos de Suporte

- **Render Support**: https://render.com/support
- **Telegram Bot API**: https://core.telegram.org/bots/api
- **Node.js**: https://nodejs.org/en/docs/

## 📝 Documentação de Mudanças

### Formato de Log

```
Data: YYYY-MM-DD
Tipo: [Manutenção/Emergência/Rotina]
Descrição: ...
Responsável: ...
Resultado: [Sucesso/Falha]
Notas: ...
```

### Exemplo

```
Data: 2026-06-06
Tipo: Manutenção
Descrição: Rotação de chaves de criptografia
Responsável: Admin
Resultado: Sucesso
Notas: Nenhuma incidência. Sistema operacional normal.
```

---

**Última atualização:** Junho 2026
**Próxima revisão:** Julho 2026
