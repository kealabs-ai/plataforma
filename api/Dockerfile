FROM python:3.9-slim

WORKDIR /app

# Instala dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install email-validator pymysql

# Copia arquivos da aplicação
COPY . .

# Expõe a porta da API
EXPOSE 8000

# Define variável de ambiente para indicar que está rodando em Docker
ENV DOCKER_ENV=true

# Comando para iniciar a aplicação
CMD ["python", "main.py"]