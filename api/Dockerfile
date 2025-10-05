FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .
RUN chmod -R 755 /app

# Expose API port
EXPOSE 8000

# Set environment variables
ENV DOCKER_ENV=true
ENV API_PORT=8000

# Start the application
CMD ["python", "test_api.py"]