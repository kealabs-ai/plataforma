@echo off
echo Limpando arquivos de cache Python...

REM Remover todos os arquivos __pycache__
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"

REM Remover arquivos .pyc
del /s /q *.pyc

echo Cache limpo com sucesso!
echo Reconstruindo containers...

docker-compose down
docker-compose build --no-cache
docker-compose up -d

echo Processo concluído!
pause