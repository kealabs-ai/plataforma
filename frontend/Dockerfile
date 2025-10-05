FROM python:3.11-slim

WORKDIR /app

# Instala dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instala Flask
RUN pip install --no-cache-dir flask flask-cors

# Copia arquivos da aplicação
COPY . .

# Expõe a porta do Flask
EXPOSE 8501

# Comando para iniciar a aplicação Flask
CMD ["python", "app_flask.py"]