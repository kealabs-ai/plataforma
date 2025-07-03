import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(project_root, '.env')
load_dotenv(env_path)

# Configurações da aplicação
API_PORT = int(os.getenv("API_PORT", 8000))
APP_SECRET_KEY = os.getenv("APP_SECRET_KEY", "your_app_secret_key")
DOCKER_ENV = os.getenv("DOCKER_ENV", "false")

# Configurações do banco de dados
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root_password")
DB_NAME = os.getenv("DB_NAME", "kognia_one_db")

# Configurações de APIs externas
GOOGLE_GEMINI_API_KEY="AIzaSyC1whTg-gvTfPHCvbwfoGj2LPEmB8IUyY0"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your_openai_api_key")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "your_anthropic_api_key")

# Configurações do n8n
N8N_URL = os.getenv("N8N_URL", "http://localhost:5678")
N8N_API_KEY = os.getenv("N8N_API_KEY", "your_n8n_api_key")

# Configurações do Redis
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# URL da API para frontend
API_URL = os.getenv("API_URL", "http://localhost:8000")
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GOOGLE_GEMINI_API_KEY}"