.PHONY: help install setup test lint format clean run

# Variables
PYTHON = python
PIP = pip
VENV = .venv
BIN = $(VENV)/Scripts
PROJECT = enhanced-budget-pro
PORT = 8501

help:
	@echo Available commands:
	@echo   make setup      - Setup development environment
	@echo   make install    - Install dependencies
	@echo   make test       - Run tests
	@echo   make lint       - Run linters
	@echo   make format     - Format code
	@echo   make clean      - Clean build artifacts
	@echo   make run        - Run the application
	@echo   make run-dev    - Run with development settings

setup:
	@echo Setting up development environment...
	$(PYTHON) -m venv $(VENV)
	$(BIN)\pip install --upgrade pip setuptools wheel
	$(BIN)\pip install -r requirements.txt
	@echo ✓ Environment setup complete

install:
	@echo Installing dependencies...
	$(BIN)\pip install -r requirements.txt

test:
	@echo Running tests...
	pytest

lint:
	@echo Running linters...
	flake8 .

format:
	@echo Formatting code...
	black .

clean:
	@echo Cleaning build artifacts...
	rmdir /s /q build 2>nul || true
	rmdir /s /q dist 2>nul || true
	rmdir /s /q *.egg-info 2>nul || true
	rmdir /s /q .pytest_cache 2>nul || true
	rmdir /s /q .coverage 2>nul || true
	rmdir /s /q htmlcov 2>nul || true
	rmdir /s /q .mypy_cache 2>nul || true
	rmdir /s /q __pycache__ 2>nul || true
	del /s /q *.pyc 2>nul || true

run:
	@echo Starting Enhanced Budget Pro...
	$(BIN)\streamlit run ui_app.py --server.port $(PORT) --server.address 0.0.0.0

run-dev:
	@echo Starting in development mode...
	$(BIN)\streamlit run ui_app.py --server.port $(PORT) --server.address 0.0.0.0 --server.runOnSave true
