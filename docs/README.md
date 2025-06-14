# Documentação da Plataforma Kognia One

Esta documentação fornece informações detalhadas sobre a arquitetura, instalação, configuração e uso da plataforma Kognia One.

## Índice

1. [Visão Geral](#visão-geral)
2. [Arquitetura](#arquitetura)
3. [Instalação](#instalação)
4. [Configuração](#configuração)
5. [Desenvolvimento](#desenvolvimento)
6. [Implantação](#implantação)
7. [API Reference](#api-reference)
8. [Customização](#customização)
9. [Troubleshooting](#troubleshooting)

## Visão Geral

A Kognia One é uma plataforma integrada que utiliza múltiplos modelos de IA para fornecer soluções inteligentes e personalizadas. A plataforma é construída com Python, Streamlit e Semantic UI, oferecendo uma interface amigável e altamente customizável.

## Arquitetura

A plataforma Kognia One segue uma arquitetura em camadas:

- **Frontend**: Interface de usuário construída com Streamlit e Semantic UI
- **API**: Camada de serviços RESTful construída com FastAPI
- **Backend**: Lógica de negócios e processamento de dados
- **Agents**: Agentes inteligentes para automação de tarefas
- **LLMs**: Integração com múltiplos modelos de linguagem (OpenAI, Google Gemini, Claude, etc.)
- **Database**: Armazenamento de dados usando MySQL

![Arquitetura](./images/architecture.png)

## Instalação

### Pré-requisitos

- Python 3.9+
- MySQL 5.6.23+
- Docker e Docker Compose (para ambiente de desenvolvimento)
- Terraform (para implantação em nuvem)

### Instalação Local

1. Clone o repositório:
   ```bash
   git clone https://github.com/kognia/kognia-one.git
   cd kognia-one
   ```

2. Configure as variáveis de ambiente:
   ```bash
   cp .env.example .env
   # Edite o arquivo .env com suas configurações
   ```

3. Inicie os containers:
   ```bash
   docker-compose up -d
   ```

4. Acesse a aplicação:
   - Frontend: http://localhost:8501
   - API: http://localhost:8000/docs

## Configuração

### Variáveis de Ambiente

A plataforma utiliza diversas variáveis de ambiente para configuração. As principais são:

- `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`: Configurações do banco de dados
- `OPENAI_API_KEY`, `GOOGLE_GEMINI_API_KEY`, etc.: Chaves de API para os modelos de linguagem
- `APP_SECRET_KEY`: Chave secreta para criptografia e tokens JWT
- `APP_DEBUG`: Modo de depuração (True/False)

### Configuração de LLMs

Para adicionar ou configurar modelos de linguagem, edite os arquivos na pasta `llms/`.

## Desenvolvimento

### Estrutura do Projeto

```
KogniaOne/
├── frontend/                # Camada de front-end (Streamlit + Semantic UI)
├── api/                     # Camada de API (FastAPI)
├── backend/                 # Camada de backend (lógica de negócios)
├── agents/                  # Camada de agentes inteligentes
├── llms/                    # Camada de integração com LLMs
├── database/                # Scripts SQL e migrações
├── assets/                  # Recursos estáticos (imagens, CSS, etc.)
├── infrastructure/          # Configurações de infraestrutura (Terraform, Docker)
├── tests/                   # Testes automatizados
└── docs/                    # Documentação
```

### Fluxo de Desenvolvimento

1. Crie uma branch para sua feature:
   ```bash
   git checkout -b feature/nome-da-feature
   ```

2. Implemente suas alterações e adicione testes

3. Execute os testes:
   ```bash
   pytest tests/
   ```

4. Envie um Pull Request para a branch `develop`

## Implantação

### Implantação com Terraform

1. Configure as credenciais da AWS:
   ```bash
   export AWS_ACCESS_KEY_ID=your_access_key
   export AWS_SECRET_ACCESS_KEY=your_secret_key
   export AWS_REGION=us-east-1
   ```

2. Inicialize o Terraform:
   ```bash
   cd infrastructure/terraform
   terraform init
   ```

3. Aplique a configuração:
   ```bash
   terraform apply
   ```

### CI/CD

A plataforma utiliza GitHub Actions para CI/CD. O pipeline inclui:

1. Execução de testes automatizados
2. Build e push de imagens Docker para ECR
3. Implantação com Terraform (apenas na branch `main`)

## API Reference

A documentação completa da API está disponível em `/api/docs` quando a aplicação está em execução.

## Customização

### Customização de Layout

A plataforma permite customização completa do layout através de:

1. Temas personalizados (claro/escuro)
2. Cores primárias e secundárias
3. Fontes e estilos
4. CSS personalizado

### Customização de Componentes

Para adicionar ou modificar componentes, edite os arquivos na pasta `frontend/components/`.

## Troubleshooting

Consulte o [Guia de Troubleshooting](./troubleshooting.md) para soluções de problemas comuns.