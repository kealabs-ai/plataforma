#!/bin/bash

# Script de health check para containers Docker
# Verifica se os serviços estão funcionando corretamente

API_PORT=${API_PORT:-8000}
FRONTEND_PORT=${FRONTEND_PORT:-8501}

echo "🔍 Verificando saúde dos containers..."

# Verificar API
echo "Testando API na porta $API_PORT..."
if curl -f -s http://localhost:$API_PORT/status > /dev/null; then
    echo "✅ API está funcionando"
    API_STATUS="OK"
else
    echo "❌ API não está respondendo"
    API_STATUS="FAIL"
fi

# Verificar Frontend
echo "Testando Frontend na porta $FRONTEND_PORT..."
if curl -f -s http://localhost:$FRONTEND_PORT > /dev/null; then
    echo "✅ Frontend está funcionando"
    FRONTEND_STATUS="OK"
else
    echo "❌ Frontend não está respondendo"
    FRONTEND_STATUS="FAIL"
fi

# Mostrar status dos containers
echo "📊 Status dos containers:"
docker ps --filter "name=kealabs-" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Verificar logs se houver problemas
if [ "$API_STATUS" = "FAIL" ]; then
    echo "📋 Logs da API:"
    docker logs kealabs-api --tail 10
fi

if [ "$FRONTEND_STATUS" = "FAIL" ]; then
    echo "📋 Logs do Frontend:"
    docker logs kealabs-frontend --tail 10
fi

# Retornar código de saída
if [ "$API_STATUS" = "OK" ] && [ "$FRONTEND_STATUS" = "OK" ]; then
    echo "🎉 Todos os serviços estão funcionando!"
    exit 0
else
    echo "⚠️  Alguns serviços apresentam problemas"
    exit 1
fi