# Inventory and Finance Manager - TODO

## Banco de Dados
- [x] Tabela Produto (id, nome, categoria, quantidade, preco_compra, preco_venda, criado_em)
- [x] Tabela Movimentação de Estoque (id, produto_id, tipo, quantidade, data, observacao)
- [x] Tabela Transação Financeira (id, tipo, categoria, valor, data, descricao)

## Backend - API tRPC
- [x] CRUD de Produtos (criar, listar, atualizar, deletar)
- [x] Movimentação de Estoque (entrada/saida)
- [x] Registrar Transações Financeiras
- [x] Calcular Saldo Atual
- [x] Calcular Valor Total do Estoque
- [x] Alertas de Estoque Baixo
- [x] Histórico de Movimentações
- [x] Filtro por Período
- [x] Relatórios Mensais (estrutura pronta)
- [x] Exportação CSV

## Frontend - Telas
- [x] Página de Login (landing page com autenticação)
- [x] Dashboard (saldo atual, valor total estoque, gráficos)
- [x] Gestão de Produtos (CRUD completo)
- [x] Movimentação de Estoque (entradas/saidas)
- [x] Fluxo de Caixa (registrar transações, visualizar saldo)
- [x] Navegação com Sidebar

## Funcionalidades Específicas
- [x] Gráfico de Linha: Saldo mês a mês
- [x] Gráfico de Barra: Produtos mais movimentados
- [x] Alertas de Estoque Baixo
- [x] Filtro por Período (em transações)
- [x] Exportação em CSV
- [ ] Responsividade Mobile (ajustes finais)

## Testes
- [x] Testes Vitest para Produtos (5/7 passando)
- [x] Testes Vitest para Movimentação (4/6 passando)
- [x] Testes Vitest para Transações (2/6 passando)
- [ ] Corrigir testes com isolamento de dados
