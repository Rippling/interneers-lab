# Variables
VENV = venv
VENV = venv
BACKEND_DIR = backend\python
FRONTEND_DIR = frontend
PYTHON = $(VENV)\Scripts\python
PIP = $(VENV)\Scripts\pip

# Create virtual environment
venv:
	python -m venv $(VENV)

# Install backend dependencies
install-backend: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r $(BACKEND_DIR)\requirements.txt

# Install frontend dependencies
install-frontend:
	cd $(FRONTEND_DIR) && yarn install

# Setup everything
setup: install-backend install-frontend

# Run backend
backend:
	cd $(BACKEND_DIR) && ../../$(PYTHON) manage.py runserver

# Run frontend
frontend:
	cd $(FRONTEND_DIR) && yarn start

#containerize backend
containerize-backend:
	cd $(BACKEND_DIR) && docker compose up --build

#decontainerize backend
decontainerize-backend:
	cd $(BACKEND_DIR) && docker compose down	

# Run tests
test:
	cd $(BACKEND_DIR) && $(PYTHON) -m pytest 

# Run coverage
coverage:
	cd $(BACKEND_DIR) && $(PYTHON) -m pytest --cov=. --cov-report=term-missing

html-coverage:
	cd $(BACKEND_DIR) && $(PYTHON) -m pytest --cov=. --cov-report=html	

# Lint
lint:
	$(PYTHON) -m flake8 .

# Format
format:
	$(PYTHON) -m black .