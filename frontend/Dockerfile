FROM python:3.11.2

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Set permissions
RUN chmod -R 755 /app

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8501 || exit 1

# Set Python path and working directory
ENV PYTHONPATH=/app
WORKDIR /app

# Start the application
CMD ["gunicorn", "--bind", "0.0.0.0:8501", "--workers", "2", "--timeout", "120", "--chdir", "/app", "wsgi:app"]