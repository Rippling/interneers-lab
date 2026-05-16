# Product API

A REST API built with Django for managing warehouse products. Supports full CRUD operations, pagination, and validation — backed by MongoDB and structured using the Controller-Service-Repository (CSR) architecture.

## Table of Contents
- [Description](#description)
- [Installation](#installation)
- [API Endpoints](#api-endpoints)
- [Usage](#usage)
- [Validations](#validations)
- [Pagination](#pagination)
- [Error Handling](#error-handling)
- [License](#license)

---

## Description

This project is a Django-based REST API that allows you to manage products in a warehouse. It was built to practice REST API design principles including:

- Clean URL structure using nouns over verbs
- Proper use of HTTP methods (GET, POST, PUT, PATCH, DELETE)
- Meaningful error responses
- Paginated list endpoints
- Controller-Service-Repository (CSR) architecture
- MongoDB persistence via MongoEngine ODM
- Audit fields (created_at, updated_at) on all records

---

## Architecture

The API follows the CSR pattern with clear separation of concerns:
```
views.py         → Controller  — HTTP parsing and responses only
services.py      → Service     — business logic and validation
repositories.py  → Repository  — all persistence operations
models.py        → Domain      — Product structure via MongoEngine
```

---

## Installation

### Prerequisites
- Python 3.14+
- Docker Desktop
```bash
# 1. Clone the repository
git clone <your-repo-url>
cd <your-repo-name>

# 2. Install dependencies
pip install django mongoengine

# 3. Start MongoDB via Docker
docker-compose up

# 4. In a separate terminal, run the server
python manage.py runserver
```

MongoDB will be available at `localhost:27019`.

---

## API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | /products/ | Get all products (paginated) |
| POST | /products/ | Create a new product |
| GET | /products/{id}/ | Get a single product |
| PUT | /products/{id}/ | Full update (all fields required) |
| PATCH | /products/{id}/ | Partial update (only send changed fields) |
| DELETE | /products/{id}/ | Delete a product |

> **Note:** Product IDs are MongoDB ObjectId strings e.g. `64b1f2e3c9a4e500123abcde`

---

## Usage

### Create a product
Send a POST request to `/products/` with this JSON body:
```json
{
    "name": "iPhone 15",
    "description": "Latest Apple smartphone",
    "category": "Electronics",
    "price": 999.99,
    "brand": "Apple",
    "quantity": 50
}
```

### Get all products
```
GET /products/
```

### Get a single product
```
GET /products/64b1f2e3c9a4e500123abcde/
```

### Full update a product
Send a PUT request with all fields:
```json
{
    "name": "iPhone 15 Pro",
    "description": "Updated description",
    "category": "Electronics",
    "price": 1199.99,
    "brand": "Apple",
    "quantity": 30
}
```

### Partial update a product
Send a PATCH request with only the fields you want to change:
```json
{
    "price": 899.99
}
```

### Delete a product
```
DELETE /products/64b1f2e3c9a4e500123abcde/
```

---

## Validations

All fields are required when creating a product. The following rules apply:

- `name` — required, must be a string, max 255 characters
- `description` — required, must be a string
- `category` — required, must be a string
- `price` — required, must be a positive non-zero number, no booleans
- `brand` — required, must be a string
- `quantity` — required, must be a positive non-zero integer, no booleans

For partial updates (PATCH), only the fields you send are validated.

---

## Pagination

The fetch all products endpoint supports pagination via query parameters:
```
GET /products/?page=1&page_size=5
```

Response includes:
```json
{
    "page": 1,
    "page_size": 5,
    "total_products": 10,
    "total_pages": 2,
    "products": [...]
}
```

---

## Error Handling

All errors return a structured JSON response:
```json
{
    "error": "Validation failed",
    "message": "One or more fields are invalid.",
    "details": {
        "price": "Price must be a positive non-zero number"
    }
}
```

---