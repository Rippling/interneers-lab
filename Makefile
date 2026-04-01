# -----------------------------
# Variables
# -----------------------------
BACKEND_DIR = backend/python
FRONTEND_DIR = frontend
VENV = venv

PYTHON = $(BACKEND_DIR)/$(VENV)/Scripts/python
PIP = $(BACKEND_DIR)/$(VENV)/Scripts/pip

# -----------------------------
# Setup
# -----------------------------

venv:
	cd $(BACKEND_DIR) && python -m venv $(VENV)

install-backend: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r $(BACKEND_DIR)/requirements.txt

install-frontend:
	cd $(FRONTEND_DIR) && yarn install

setup: install-backend install-frontend

# -----------------------------
# Run servers
# -----------------------------

run-backend:
	cd $(BACKEND_DIR) && $(VENV)/Scripts/python manage.py runserver

run-frontend:
	cd $(FRONTEND_DIR) && yarn start

# -----------------------------
# Testing
# -----------------------------

test:
	cd $(BACKEND_DIR) && $(VENV)/Scripts/python -m pytest

coverage:
	cd $(BACKEND_DIR) && $(VENV)/Scripts/python -m pytest --cov

html-coverage:
	cd $(BACKEND_DIR) && $(VENV)/Scripts/python -m pytest --cov --cov-report=html
