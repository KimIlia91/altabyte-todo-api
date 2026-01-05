.PHONY: help build up down logs run shell migrate migrate-create clean install

COMPOSE = docker-compose
PYTHON = python
VENV = venv

help: ## Show help
	@echo "Available commands:"
	@echo ""
	@echo "  install            Create venv and install dependencies"
	@echo "  venv               Create venv"
	@echo "  build              Build Docker images"
	@echo "  up                 Start containers"
	@echo "  down               Stop containers"
	@echo "  logs               Show logs"
	@echo "  run                Run API locally"
	@echo ""
	@echo "For detailed information use: make <command>"

venv:
	$(PYTHON) -m venv $(VENV)

install: ## Install dependencies
	pip install -r requirements.txt --upgrade

build: ## Build Docker images
	$(COMPOSE) build

up: ## Start containers
	$(COMPOSE) up -d

down: ## Stop containers
	$(COMPOSE) down

logs: ## Show logs
	$(COMPOSE) logs -f

run: ## Run API locally
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
