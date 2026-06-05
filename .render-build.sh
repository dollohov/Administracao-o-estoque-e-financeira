#!/bin/bash
set -e

echo "🔨 Iniciando build para Render..."

# Instalar dependências
echo "📦 Instalando dependências..."
pnpm install --frozen-lockfile

# Build do projeto
echo "🏗️ Fazendo build..."
pnpm build

echo "✅ Build concluído com sucesso!"
