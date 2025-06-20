@echo off
echo Verificando conexão com a API...
python check_api.py
if %errorlevel% neq 0 (
    echo.
    echo Pressione qualquer tecla para sair...
    pause > nul
)