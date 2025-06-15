# Kognia One

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