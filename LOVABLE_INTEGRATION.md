# Guia de Integração Frontend Lovable (Denis Barbosa)

Este documento descreve como conectar o seu frontend no **Lovable** com o backend Django ERP de forma segura e profissional.

## 1. Configuração da API

O backend já está preparado com as seguintes tecnologias:
- **Django Rest Framework (DRF):** Para os endpoints da API.
- **JWT (JSON Web Token):** Para autenticação segura.
- **CORS Headers:** Para permitir que o Lovable acesse o backend.
- **Multi-tenancy:** Isolamento automático de dados por empresa.

### Endpoints Principais:
- **Autenticação:** `POST /api/token/` (Gera Access e Refresh Token)
- **Produtos:** `GET/POST /api/estoque/produtos/`
- **Movimentações:** `GET/POST /api/estoque/movimentacoes/`
- **Documentação:** `GET /api/docs/` (Swagger UI)

## 2. Autenticação no Lovable

No seu projeto Lovable, utilize o cabeçalho `Authorization` para todas as requisições protegidas:

```javascript
// Exemplo de chamada no Lovable (Fetch API)
const response = await fetch('https://seu-backend.com/api/estoque/produtos/', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  }
});
```

## 3. Segurança e Produção

Para garantir que **nenhum dado fictício** seja rodado em produção:

1.  **Ambiente de Produção:** Certifique-se de que a variável `DEBUG=False` esteja no seu arquivo `.env`.
2.  **CORS:** No `.env`, configure `CORS_ALLOWED_ORIGINS` com a URL final do seu app Lovable.
3.  **Banco de Dados:** Utilize um banco de dados de produção (PostgreSQL recomendado) configurado via `DATABASE_URL`.
4.  **Isolamento:** O sistema já filtra automaticamente os dados pela empresa do usuário logado. Se um usuário não estiver vinculado a uma empresa, ele não verá nenhum dado.

## 4. Como gerar a documentação para o Lovable

Você pode fornecer o arquivo de esquema da API para o Lovable entender todos os endpoints automaticamente:
- Acesse: `https://seu-backend.com/api/schema/`
- Salve o arquivo YAML/JSON e importe no Lovable se necessário.

---
**Autor:** Denis Barbosa (Todos os direitos reservados)
**Data:** 2026-02-18
