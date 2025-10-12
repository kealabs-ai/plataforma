# Imagem base com Python
FROM python:3.11-slim

# Troca para root para garantir permissões durante a instalação
USER root

# Diretório de trabalho
WORKDIR /app

# Instala dependências do sistema e Docker CLI
RUN apt-get update && apt-get install -y \
    curl \
    git \
    docker.io \
    && rm -rf /var/lib/apt/lists/*

# Adiciona grupo docker e inclui o usuário padrão (opcional, se for usar outro usuário)
RUN groupadd docker || true

# Copia e instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instala Flask e servidor de produção
RUN pip install --no-cache-dir flask flask-cors gunicorn

# Copia os arquivos da aplicação
COPY . .

# Define permissões
RUN chmod -R 755 /app

# Expõe a porta da aplicação
EXPOSE 8501

# Healthcheck para monitoramento
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8501 || exit 1

# Comando de inicialização
CMD ["gunicorn", "--bind", "0.0.0.0:8501", "--workers", "2", "--timeout", "120", "app_flask:app"]
