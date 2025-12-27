.PHONY: help install setup test lint format clean run deploy docker-build docker-run

# Variables
PYTHON = python3.10
PIP = pip3
VENV = .venv
BIN = $(VENV)/bin
PROJECT = enhanced-budget-pro
PORT = 8501

# Colors
RED = \033[0;31m
GREEN = \033[0;32m
YELLOW = \033[1;33m
NC = \033[0m # No Color

help: ## Show this help message
	@echo 'Usage:'
	@echo '  ${YELLOW}make${NC} ${GREEN}<target>${NC}'
	@echo ''
	@echo 'Targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  ${YELLOW}%-20s${NC} ${GREEN}%s${NC}\n", $$1, $$2}'

setup: ## Setup development environment
	@echo "${GREEN}Setting up development environment...${NC}"
	$(PYTHON) -m venv $(VENV)
	$(BIN)/pip install --upgrade pip setuptools wheel
	$(BIN)/pip install -e ".[dev]"
	@echo "${GREEN}✓ Environment setup complete${NC}"

install: ## Install package in development mode
	@echo "${GREEN}Installing package...${NC}"
	$(BIN)/pip install -e "."

install-dev: ## Install development dependencies
	@echo "${GREEN}Installing development dependencies...${NC}"
	$(BIN)/pip install -r requirements-dev.txt

install-full: ## Install all dependencies
	@echo "${GREEN}Installing all dependencies...${NC}"
	$(BIN)/pip install -e ".[full]"

test: ## Run tests
	@echo "${GREEN}Running tests...${NC}"
	$(BIN)/pytest tests/ -v --cov=src --cov-report=term-missing

test-cov: ## Run tests with coverage report
	@echo "${GREEN}Running tests with coverage...${NC}"
	$(BIN)/pytest tests/ --cov=src --cov-report=html
	@echo "${GREEN}Coverage report: htmlcov/index.html${NC}"

lint: ## Run linters
	@echo "${GREEN}Running linters...${NC}"
	$(BIN)/black --check src tests
	$(BIN)/flake8 src tests
	$(BIN)/mypy src

format: ## Format code
	@echo "${GREEN}Formatting code...${NC}"
	$(BIN)/black src tests
	$(BIN)/isort src tests

pre-commit: ## Run pre-commit hooks
	@echo "${GREEN}Running pre-commit hooks...${NC}"
	$(BIN)/pre-commit run --all-files

clean: ## Clean build artifacts
	@echo "${GREEN}Cleaning build artifacts...${NC}"
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	rm -rf __pycache__/
	rm -rf src/__pycache__/
	rm -rf tests/__pycache__/
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

run: ## Run the application
	@echo "${GREEN}Starting Enhanced Budget Pro...${NC}"
	$(BIN)/streamlit run ui_app.py --server.port $(PORT) --server.address 0.0.0.0

run-dev: ## Run with development settings
	@echo "${GREEN}Starting in development mode...${NC}"
	$(BIN)/streamlit run ui_app.py --server.port $(PORT) --server.address 0.0.0.0 --server.runOnSave true

docker-build: ## Build Docker image
	@echo "${GREEN}Building Docker image...${NC}"
	docker build -t $(PROJECT):latest .

docker-run: ## Run Docker container
	@echo "${GREEN}Running Docker container...${NC}"
	docker run -p $(PORT):$(PORT) $(PROJECT):latest

deploy-local: ## Deploy locally (build and run)
	@echo "${GREEN}Deploying locally...${NC}"
	make clean
	make install-full
	make test
	make run

benchmark: ## Run performance benchmarks
	@echo "${GREEN}Running benchmarks...${NC}"
	$(BIN)/python tests/benchmark_parser.py

profile: ## Profile the application
	@echo "${GREEN}Profiling...${NC}"
	$(BIN)/python -m cProfile -o profile.stats ui_app.py

update-deps: ## Update dependencies
	@echo "${GREEN}Updating dependencies...${NC}"
	$(BIN)/pip install --upgrade pip
	$(BIN)/pip install --upgrade -r requirements.txt
	$(BIN)/pip install --upgrade -r requirements-dev.txt

venv: ## Create virtual environment
	@echo "${GREEN}Creating virtual environment...${NC}"
	$(PYTHON) -m venv $(VENV)
	@echo "${GREEN}✓ Virtual environment created${NC}"
	@echo "${YELLOW}To activate:${NC}"
	@echo "  source $(VENV)/bin/activate"
	@echo "  make install"

freeze: ## Freeze dependencies
	@echo "${GREEN}Freezing dependencies...${NC}"
	$(BIN)/pip freeze > requirements-frozen.txt

security-check: ## Run security checks
	@echo "${GREEN}Running security checks...${NC}"
	$(BIN)/bandit -r src -f html -o bandit-report.html
	$(BIN)/safety check

docs: ## Build documentation
	@echo "${GREEN}Building documentation...${NC}"
	$(BIN)/sphinx-build -b html docs/source docs/build

check: ## Run all checks (test, lint, security)
	@echo "${GREEN}Running all checks...${NC}"
	make test
	make lint
	make security-check
	@echo "${GREEN}✓ All checks passed!${NC}"

init-git: ## Initialize git hooks
	@echo "${GREEN}Initializing git hooks...${NC}"
	$(BIN)/pre-commit install
	$(BIN)/pre-commit autoupdate

# Docker commands
compose-up: ## Start Docker Compose
	docker-compose up -d

compose-down: ## Stop Docker Compose
	docker-compose down

compose-logs: ## View Docker Compose logs
	docker-compose logs -f

# Database commands
db-init: ## Initialize database
	@echo "${GREEN}Initializing database...${NC}"
	$(BIN)/python scripts/init_db.py

db-migrate: ## Run database migrations
	@echo "${GREEN}Running migrations...${NC}"
	$(BIN)/alembic upgrade head

db-reset: ## Reset database
	@echo "${GREEN}Resetting database...${NC}"
	$(BIN)/python scripts/reset_db.py

# Backup commands
backup: ## Backup database and configs
	@echo "${GREEN}Creating backup...${NC}"
	$(BIN)/python scripts/backup.py

restore: ## Restore from backup
	@echo "${GREEN}Restoring from backup...${NC}"
	$(BIN)/python scripts/restore.py