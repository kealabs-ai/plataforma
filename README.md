# Kognia One Platform

Plataforma integrada Kognia One com suporte a múltiplos modelos de IA e interface customizável.

## Estrutura do Projeto

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

## Requisitos

- Python 3.9+
- MySQL 5.6.23+
- Docker e Docker Compose
- Terraform (para implantação em nuvem)

## Configuração

1. Clone o repositório
2. Copie `.env.example` para `.env` e configure as variáveis de ambiente
3. Execute `docker-compose up` para iniciar o ambiente de desenvolvimento

## Desenvolvimento

Consulte a documentação em `docs/` para instruções detalhadas sobre desenvolvimento, implantação e customização.

## Licença

Proprietary - Kognia