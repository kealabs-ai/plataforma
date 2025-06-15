@echo off
echo Iniciando o projeto Kognia One...

REM Verificando se o Docker está instalado
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Docker não encontrado. Por favor, instale o Docker Desktop.
    exit /b 1
)

REM Verificando se o Docker está em execução
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo Docker não está em execução. Por favor, inicie o Docker Desktop.
    exit /b 1
)

REM Construindo e iniciando os containers
echo Construindo e iniciando os containers...
docker-compose up --build -d

echo.
echo Projeto Kognia One iniciado com sucesso!
echo.
echo Frontend: http://localhost:8501
echo API: http://localhost:8000
echo.
echo Para parar o projeto, execute: docker-compose down