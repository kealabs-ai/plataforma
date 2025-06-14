.PHONY: setup run-api run-frontend test lint format clean docker-build docker-up docker-down

# Configurações
PYTHON = python
PIP = pip
DOCKER_COMPOSE = docker-compose

# Comandos principais
setup:
	$(PIP) install -r requirements.txt

run-api:
	cd api && uvicorn main:app --reload --host 127.0.0.1 --port 8000

run-frontend:
	cd frontend && streamlit run app.py

test:
	pytest tests/ --cov=./ --cov-report=term-missing

lint:
	flake8 .
	mypy .

format:
	black .
	isort .

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

# Docker
docker-build:
	$(DOCKER_COMPOSE) -f infrastructure/docker-compose.yml build

docker-up:
	$(DOCKER_COMPOSE) -f infrastructure/docker-compose.yml up -d

docker-down:
	$(DOCKER_COMPOSE) -f infrastructure/docker-compose.yml down

# Banco de dados
db-init:
	mysql -u $(DB_USER) -p$(DB_PASSWORD) < database/schema.sql

db-migrate:
	for file in database/migrations/*.sql; do \
		mysql -u $(DB_USER) -p$(DB_PASSWORD) $(DB_NAME) < $$file; \
	done

# Terraform
tf-init:
	cd infrastructure/terraform && terraform init

tf-plan:
	cd infrastructure/terraform && terraform plan

tf-apply:
	cd infrastructure/terraform && terraform apply

tf-destroy:
	cd infrastructure/terraform && terraform destroy