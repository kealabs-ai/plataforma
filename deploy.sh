#!/bin/bash

# Script de deploy para VPS Hostinger
# Kealabs Intelligence Platform

set -e

echo "🚀 Iniciando deploy do Kealabs Intelligence..."

# Configurações
PROJECT_NAME="kealabs-intelligence"
NETWORK_NAME="kealabs-network"
API_PORT="8000"
FRONTEND_PORT="8501"

# Função para log
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    log "❌ Docker não encontrado. Instalando..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
    log "✅ Docker instalado com sucesso"
fi

# Verificar se .env existe
if [ ! -f ".env" ]; then
    log "⚠️  Arquivo .env não encontrado. Copiando de .env.example..."
    cp .env.example .env
fi

# Configurar .env para produção
log "🔧 Configurando ambiente de produção..."
sed -i 's/DOCKER_ENV=false/DOCKER_ENV=true/g' .env
sed -i 's/FLASK_ENV=development/FLASK_ENV=production/g' .env
sed -i 's/FLASK_DEBUG=1/FLASK_DEBUG=0/g' .env

# Parar containers existentes
log "🛑 Parando containers existentes..."
docker stop kealabs-api kealabs-frontend 2>/dev/null || true
docker rm kealabs-api kealabs-frontend 2>/dev/null || true

# Criar rede se não existir
log "🌐 Criando rede Docker..."
docker network create $NETWORK_NAME 2>/dev/null || true

# Build das imagens
log "🔨 Construindo imagem da API..."
docker build -t kealabs-api ./api

log "🔨 Construindo imagem do Frontend..."
docker build -t kealabs-frontend ./frontend

# Deploy da API
log "🚀 Fazendo deploy da API..."
docker run -d \
    --name kealabs-api \
    --network $NETWORK_NAME \
    --env-file .env \
    -p $API_PORT:8000 \
    --restart unless-stopped \
    kealabs-api

# Aguardar API inicializar
log "⏳ Aguardando API inicializar..."
sleep 30

# Verificar se API está funcionando
for i in {1..10}; do
    if curl -f http://localhost:$API_PORT/status >/dev/null 2>&1; then
        log "✅ API está funcionando!"
        break
    fi
    log "⏳ Tentativa $i/10 - Aguardando API..."
    sleep 10
done

# Deploy do Frontend
log "🚀 Fazendo deploy do Frontend..."
docker run -d \
    --name kealabs-frontend \
    --network $NETWORK_NAME \
    --env-file .env \
    -p $FRONTEND_PORT:8501 \
    --restart unless-stopped \
    kealabs-frontend

# Aguardar Frontend inicializar
log "⏳ Aguardando Frontend inicializar..."
sleep 20

# Verificar se Frontend está funcionando
for i in {1..5}; do
    if curl -f http://localhost:$FRONTEND_PORT >/dev/null 2>&1; then
        log "✅ Frontend está funcionando!"
        break
    fi
    log "⏳ Tentativa $i/5 - Aguardando Frontend..."
    sleep 10
done

# Mostrar status final
log "📊 Status dos containers:"
docker ps --filter "name=kealabs-" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

log "🎉 Deploy concluído com sucesso!"
log "🌐 API: http://localhost:$API_PORT"
log "🌐 Frontend: http://localhost:$FRONTEND_PORT"

# Mostrar logs se houver erro
if ! curl -f http://localhost:$API_PORT/status >/dev/null 2>&1; then
    log "❌ Erro na API. Logs:"
    docker logs kealabs-api --tail 20
fi

if ! curl -f http://localhost:$FRONTEND_PORT >/dev/null 2>&1; then
    log "❌ Erro no Frontend. Logs:"
    docker logs kealabs-frontend --tail 20
fi