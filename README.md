# Interneers Lab

A full-stack inventory management system built as a learning project. The backend exposes a REST API for managing products and categories, backed by MongoDB. The frontend is a React + TypeScript app that consumes it.

```
backend/
  python/      # Django REST API — products, categories, CSV import
frontend/      # React + TypeScript inventory UI
```

---

## Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.14+ | Django backend |
| Node.js | LTS | Frontend |
| Yarn | 1.x | Frontend package manager |
| Docker Desktop | Latest | MongoDB via Compose |

---

## Quick Start

### 1. Clone

```bash
git clone git@github.com:<YourUsername>/interneers-lab.git
cd interneers-lab
```

### 2. Start MongoDB

```bash
cd backend/python
docker compose up -d
```

MongoDB runs on `localhost:27019`. Credentials are in `backend/python/.env`.

### 3. Django backend

```bash
cd backend/python

cp .env.example .env          # edit as needed (see Environment below)
pip install -r requirements.txt
python manage.py runserver    # http://localhost:8000
```

### 4. Frontend

```bash
cd frontend
yarn install
yarn start                    # http://localhost:3000
```

---

## Environment Configuration

All Django runtime settings are driven by `backend/python/.env`. Copy from `.env.example` and fill in your own values:

```env
SECRET_KEY=                   # generate a strong random key
DEBUG=True                    # set False in production

MONGO_HOST=
MONGO_PORT=
MONGO_DB=
MONGO_USERNAME=
MONGO_PASSWORD=
MONGO_AUTH_SOURCE=
MONGO_TEST_DB=

# CORS — True only for local dev
# In production set to False and list origins below
CORS_ALLOW_ALL_ORIGINS=True
# CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
```

---

## API Overview

Base URL: `http://localhost:8000`

### Products

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/products/` | List products (paginated, filterable) |
| POST | `/products/` | Create a product |
| GET | `/products/<id>/` | Get a product |
| PUT | `/products/<id>/` | Full update |
| PATCH | `/products/<id>/` | Partial update |
| DELETE | `/products/<id>/` | Delete a product |
| POST | `/products/bulk-import/` | Bulk create from CSV |

**Filters on `GET /products/`:** `search`, `brand`, `category_id`, `min_price`, `max_price`, `min_quantity`, `page`, `page_size`, `sort` (`price_asc` / `price_desc`)

### Categories

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/categories/` | List all categories |
| POST | `/categories/` | Create a category |
| GET | `/categories/<id>/` | Get a category |
| PUT | `/categories/<id>/` | Full update |
| DELETE | `/categories/<id>/` | Delete a category |
| GET | `/categories/<id>/products/` | Products in a category |

---

## Architecture (Django backend)

The backend follows a Controller–Service–Repository (CSR) pattern:

```
views.py          → HTTP layer — parse requests, return responses
services.py       → Business logic — validation, orchestration
repositories.py   → Persistence — all MongoDB queries
models.py         → Documents — MongoEngine ODM schemas
validators.py     → Input validation — field rules
```

`Product` references `ProductCategory` as a MongoEngine `ReferenceField`. Audit fields (`created_at`, `updated_at`) are set automatically.

---

## Running Tests

### Django (Python)

```bash
cd backend/python
python manage.py test
```

Uses a dedicated test database (`MONGO_TEST_DB`).

### Frontend

```bash
cd frontend

# Unit tests (Jest)
yarn test

# E2E tests (Playwright) — install browsers once
yarn playwright install
yarn playwright test
yarn playwright show-report
```

Playwright CI runs automatically on push/PR via `.github/workflows/playwright.yml`.

---

## Project Structure

```
backend/python/
  django_app/       # Django settings, root URLconf
  Product/          # Product & Category app
    models.py
    repositories.py
    services.py
    views.py
    validators.py
    urls.py
    migrations/
    tests/

frontend/
  src/
    api/            # Typed API client
    components/     # Shared UI components
    hooks/          # useProducts, etc.
    pages/          # Route-level page components
  public/
    week6/          # Vanilla JS demo page
  playwright/       # E2E tests

.github/
  workflows/
    playwright.yml  # Playwright CI
```

---

## Further Reading

- [Django](https://docs.djangoproject.com/)
- [MongoEngine](https://docs.mongoengine.org/)
- [React](https://react.dev/learn)
- [React Router](https://reactrouter.com/home)
- [TypeScript](https://www.typescriptlang.org/docs/)
- [Playwright](https://playwright.dev/docs/intro)
- [MongoDB](https://docs.mongodb.com/)
- [Docker Compose](https://docs.docker.com/compose/)
