@echo off
echo Iniciando os containers do Kognia One...
cd infrastructure
docker-compose up -d
echo Containers iniciados! Acesse:
echo Frontend: http://localhost:8501
echo API: http://localhost:8000/docs