# Product Service & Product Category API

This repository contains backend services for managing **Products** and **Product Categories**.
The project includes APIs, service layers, unit tests, integration tests, and automated development workflows using a **Makefile**.

---

## Project Structure
```
├── backend/
│   ├── python/
│   │   ├── django_app/
│   │   ├── htmlcov/
│   │   ├── product_service/
│   │   ├── product_category/
│   │   ├── warehouse/
│   │   ├── docker-compose.yaml
│   │   ├── pytest.ini
│   │   └── requirements.txt
|   |
│   └── go/
│
├── frontend/
│
├── Makefile
├── README.md
└── CHANGELOG.md
```
---

## Features

* Product CRUD APIs
* Product Category APIs
* Service layer abstraction
* Unit and integration tests
* Test coverage reporting
* Automated development commands using Makefile

---

## Prerequisites

Before running the project ensure the following are installed:

* Python 3.10+
* pip
* Node.js (for frontend)
* Yarn
* Make

---

## Setup Instructions

Clone the repository:

```bash
git clone <repository-url>
cd interneers-lab
```

Create virtual environment and install dependencies:

```bash
make setup
```

This command will:

* Create a Python virtual environment
* Install backend dependencies
* Install frontend dependencies

---

## Running the Backend

Start the backend server:

```bash
make backend
```

---

## Running the Frontend

Start the frontend application:

```bash
make frontend
```

---

## Running Tests

Execute all tests:

```bash
make test
```

This will run **pytest test suites** including unit tests.

---

## Running Tests with Coverage

Generate test coverage:

```bash
make coverage
```

Example output:

```
---------- coverage ----------
Name                              Stmts   Miss  Cover
----------------------------------------------
product_service/service.py         45      3    93%
product_category/service.py        30      2    93%
----------------------------------------------
TOTAL                              75      5    93%
```

---

## Development Workflow

Typical development workflow:

```bash
make setup
make test
make coverage
```

---

## Testing Overview

The project includes:

### Unit Tests

* Test service layer logic
* Mock repository layers

### Integration Tests

* Validate API endpoints
* Test full request-response flow

Integration tests may require additional services (e.g. MongoDB) and may be skipped if dependencies are unavailable.
