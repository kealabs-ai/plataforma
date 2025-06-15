#!/bin/bash

echo "Iniciando o projeto Kognia One..."

# Verificando se o Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "Docker não encontrado. Por favor, instale o Docker."
    exit 1
fi

# Verificando se o Docker está em execução
if ! docker info &> /dev/null; then
    echo "Docker não está em execução. Por favor, inicie o serviço Docker."
    exit 1
fi

# Construindo e iniciando os containers
echo "Construindo e iniciando os containers..."
docker-compose up --build -d

echo ""
echo "Projeto Kognia One iniciado com sucesso!"
echo ""
echo "Frontend: http://localhost:8501"
echo "API: http://localhost:8000"
echo ""
echo "Para parar o projeto, execute: docker-compose down"