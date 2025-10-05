# Kealabs Intelligence

Plataforma integrada que utiliza múltiplos modelos de IA para fornecer soluções inteligentes e personalizadas.

## Requisitos

- Docker
- Docker Compose

## Estrutura do Projeto

- `api/`: Backend da aplicação (FastAPI)
- `frontend/`: Interface de usuário (Streamlit)
- `backend/`: Módulos compartilhados do backend
- `llms/`: Integrações com modelos de linguagem
- `agents/`: Agentes inteligentes para automação


## Componentes

- **Frontend**: Interface de usuário construída com Streamlit
- **API**: Backend construído com FastAPI
- **Database**: MySQL para armazenamento de dados


## Como Iniciar

### Windows

```bash
# Execute o script de inicialização
start.bat
```

### Linux/macOS

```bash
# Dê permissão de execução ao script
chmod +x start.sh

# Execute o script de inicialização
./start.sh
```

Ou inicie manualmente:

```bash
# Construa e inicie os containers
docker-compose up --build -d
```

## Acessando a Aplicação

- Frontend: http://localhost:8501
- API: http://localhost:8000


## Parando a Aplicação

```bash
docker-compose down
```

## Desenvolvimento

Para desenvolvimento local sem Docker:

### API (Backend)

```bash
cd api
pip install -r requirements.txt
python main.py
```

### Frontend

```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

## Variáveis de Ambiente

As variáveis de ambiente estão definidas no arquivo `.env` na raiz do projeto.

## CI/CD com Jenkins

O projeto inclui um `Jenkinsfile` configurado para pipeline automatizado:

### Configuração
1. Criar Pipeline job no Jenkins
2. Configurar SCM para o repositório
3. Apontar para `Jenkinsfile` na raiz

### Pipeline
- **Build**: Docker Compose build
- **Test**: Health checks nas APIs (8000, 8501)
- **Deploy**: Automático na branch main

### Portas Testadas
- API: http://localhost:8000/status
- Frontend: http://localhost:8501