# WEEK 1

### What I built

A **GET endpoint** that returns a greeting message using a query parameter:

- `GET /hello-world/` → `{"message": "Hello, World!"}`
- `GET /hello-world/?name=Kreesh` → `{"message": "Hello, Kreesh!"}`

### Hexagonal architecture overview

The implementation is organized into clear layers to keep business logic independent of Django:

- **domain/**: Pure business logic (e.g., formatting/validating the greeting). No Django imports.
- **application/**: Use-case layer that coordinates the feature (calls domain and returns a result).
- **ports/**: Contract boundary for the use-case (defines what the core exposes).
- **adapters/api/**: Django HTTP layer (views + urls) that translates HTTP requests into application calls and returns JSON.

---

# WEEK 2

### What I built

In Week 2, I built a **Product CRUD API** using **Django REST Framework (DRF)**.

This API supports:

- **Create** a product
- **List** all products
- **Get** one product by ID
- **Update** a product by ID
- **Delete** a product by ID

Current endpoints:

- `GET /week2/products/`
- `POST /week2/products/`
- `GET /week2/products/<id>/`
- `PUT /week2/products/<id>/`
- `DELETE /week2/products/<id>/`

Important note: for Week 2, the implementation uses **in-memory storage**, so products are stored in a Python dictionary while the server is running. Data is **not persisted** to the database yet.

## Quick theory: what is CRUD?

CRUD stands for:

- **Create**
- **Read**
- **Update**
- **Delete**

In this project:

- `POST /week2/products/` → Create
- `GET /week2/products/` → Read all
- `GET /week2/products/<id>/` → Read one
- `PUT /week2/products/<id>/` → Update
- `DELETE /week2/products/<id>/` → Delete

---

## Week 2 architecture overview

The Week 2 implementation is split into small layers so each file has one responsibility.

### `models.py`

Defines the `Product` object structure.

This is a **plain Python class**, not a Django ORM model in this week’s version.

Responsibilities:

- define product fields
- hold product data
- convert object into dictionary using `to_dict()`

### `store.py`

Acts as a **temporary in-memory database**.

Responsibilities:

- store products in a dictionary
- generate product IDs
- create/get/list/update/delete products

### `serializers.py`

Handles validation and API data structure.

Responsibilities:

- validate incoming request data
- convert incoming data into cleaned Python data
- define the API shape for Product

### `views.py`

Handles HTTP requests and responses.

Responsibilities:

- receive request
- call serializer
- call store
- return DRF `Response`

### `urls.py`

Connects API endpoints to views.

### `django_app/urls.py`

Includes `week2.urls` under `/week2/`.

---

## Architecture flow

```text
Client (Browser / Postman / Frontend)
        ↓
HTTP Request
        ↓
request.data = {
  "name": "Wireless Mouse",
  "description": "2.4 GHz ergonomic mouse",
  "category": "Electronics",
  "price": "799.00",
  "brand": "Logitech",
  "quantity": 25
}
        ↓
django_app/urls.py
        ↓
week2/urls.py
        ↓
views.py
        ↓
serializers.py
        ↓
serializer.validated_data = {
  "name": "Wireless Mouse",
  "description": "2.4 GHz ergonomic mouse",
  "category": "Electronics",
  "price": Decimal("799.00"),
  "brand": "Logitech",
  "quantity": 25
}
        ↓
store.py
        ↓
Product(
  id=1,
  name="Wireless Mouse",
  description="2.4 GHz ergonomic mouse",
  category="Electronics",
  price=Decimal("799.00"),
  brand="Logitech",
  quantity=25
)
        ↓
to_dict()
↓
{
  "id": 1,
  "name": "Wireless Mouse",
  "description": "2.4 GHz ergonomic mouse",
  "category": "Electronics",
  "price": "799.00",
  "brand": "Logitech",
  "quantity": 25
}
        ↓
serializer.data / Response(...)
        ↓
JSON Response back to client
```

---

# Week 3

## What I Built

In Week 3, I refactored the Week 2 in-memory Product CRUD API into a more structured backend architecture using a thin controller layer, service layer, repository layer, MongoDB for persistent storage, and MongoEngine for model-based database interaction.

Unlike Week 2, where products were stored only in memory, this version stores product data in MongoDB, so data persists even after restarting the server.

---

## Architecture Flows

### Flow 1 — Request Handling Flow

```text
Client (Browser / Postman / Frontend)
        ↓
HTTP Request
        ↓
django_app/urls.py
        ↓
week3/urls.py
        ↓
views.py
        ↓
serializers.py
        ↓
services.py
        ↓
repository.py
        ↓
models.py
        ↓
MongoDB
        ↓
repository.py
        ↓
services.py
        ↓
views.py
        ↓
DRF Response
        ↓
JSON Response back to client
```

---

### Flow 2 — Docker Compose Flow

```text
docker compose up -d
        ↓
Read compose.yml
        ↓
Find services:
  - app
  - db
        ↓
Create default network
        ↓
Create db volume
        ↓
Pull postgres image
        ↓
Build app image from Dockerfile
        ↓
Create db container
        ↓
Start db container
        ↓
Create app container
        ↓
Start app container
        ↓
app talks to db using service name: db
        ↓
Both keep running in background
```

---

## Flow 3 — Django Server Startup Flow

```text
python manage.py runserver
        ↓
manage.py sets DJANGO_SETTINGS_MODULE
        ↓
django.core.management executes the runserver command
        ↓
Django imports settings.py
        ↓
App configuration is loaded
        ↓
A MongoDB setup module / connection block is imported
        ↓
mongoengine.connect(...)
        ↓
Connection is established to the MongoDB container/server
        ↓
MongoEngine Document models become usable
        ↓
Repository layer can now perform DB operations
        ↓
Service layer can call repository methods
        ↓
View layer can safely handle API requests
        ↓
Server startup completes
        ↓
Application is ready for Product CRUD with MongoDB persistence
```

---

## Example Endpoints

| Method   | Endpoint                | Description        |
| -------- | ----------------------- | ------------------ |
| `POST`   | `/week3/products/`      | Create product     |
| `GET`    | `/week3/products/`      | Fetch all products |
| `GET`    | `/week3/products/<id>/` | Fetch one product  |
| `PUT`    | `/week3/products/<id>/` | Update product     |
| `DELETE` | `/week3/products/<id>/` | Delete product     |

---

## Final Takeaway

Week 3 was about moving from a basic CRUD project to a realistic, layered backend architecture — separating responsibilities into view, service, repository, and model layers, keeping controllers thin, and using MongoDB for real persistence.

---

# Week 4

## API Reference

---

## 1. Product APIs

| Method | URL                     | Description            |
| ------ | ----------------------- | ---------------------- |
| GET    | `/week4/products/`      | List all products      |
| POST   | `/week4/products/`      | Create a new product   |
| GET    | `/week4/products/<id>/` | Get a product by ID    |
| PUT    | `/week4/products/<id>/` | Update a product by ID |
| DELETE | `/week4/products/<id>/` | Delete a product by ID |

---

## 2. Category APIs

| Method | URL                       | Description             |
| ------ | ------------------------- | ----------------------- |
| GET    | `/week4/categories/`      | List all categories     |
| POST   | `/week4/categories/`      | Create a new category   |
| GET    | `/week4/categories/<id>/` | Get a category by ID    |
| PUT    | `/week4/categories/<id>/` | Update a category by ID |
| DELETE | `/week4/categories/<id>/` | Delete a category by ID |

---

## 3. Category–Product Relation APIs

| Method | URL                                      | Description                      |
| ------ | ---------------------------------------- | -------------------------------- |
| GET    | `/week4/categories/<id>/products/`       | List all products in a category  |
| POST   | `/week4/categories/<id>/add-product/`    | Add a product to a category      |
| POST   | `/week4/categories/<id>/remove-product/` | Remove a product from a category |

---

## 4. Bulk Upload

| Method | URL                            | Description                              |
| ------ | ------------------------------ | ---------------------------------------- |
| POST   | `/week4/products/bulk-upload/` | Upload a CSV to create multiple products |

---

## 5. Filtering, Sorting & Pagination

### Products — `/week4/products/`

| Param                           | Example                               | Description                 |
| ------------------------------- | ------------------------------------- | --------------------------- |
| `name`                          | `?name=rice`                          | Filter by name              |
| `brand`                         | `?brand=dove`                         | Filter by brand             |
| `min_price` / `max_price`       | `?min_price=20&max_price=200`         | Filter by price range       |
| `min_quantity` / `max_quantity` | `?min_quantity=5&max_quantity=50`     | Filter by quantity range    |
| `category_id`                   | `?category_id=1`                      | Filter by category          |
| `sort_by`                       | `?sort_by=price` or `?sort_by=-price` | Sort ascending / descending |
| `page` / `page_size`            | `?page=1&page_size=5`                 | Paginate results            |

### Categories — `/week4/categories/`

| Param                | Example                | Description                 |
| -------------------- | ---------------------- | --------------------------- |
| `title`              | `?title=food`          | Filter by title             |
| `sort_by`            | `?sort_by=-created_at` | Sort ascending / descending |
| `page` / `page_size` | `?page=1&page_size=5`  | Paginate results            |

---

## 6. Key Business Rules

- `brand` is **required** for all product operations
- Products without a `category_id` are assigned to **Miscellaneous**
- Category **titles must be unique**
- A category **cannot be deleted** if products are assigned to it
- CSV bulk upload **validates all rows** before creating any product

---

## 7. Old Product Migration

A one-time migration script is included to update older product records created before category and strict brand handling were introduced.

The script does the following:

- Connects to MongoDB
- Checks whether the default category `Miscellaneous` exists, and creates it if needed
- Finds old products with missing category
- Finds old products with missing or blank brand
- Updates only the affected records
- Prints a summary of how many products were checked and fixed

### How to run

Start the services first:

```bash
docker compose up -d
```

Then run the migration script:

```bash
python -m week4.migrate_old_products
```

### Notes

- This is a manual one-time migration script.
- It is mainly intended for old records created before the Week 4 category changes.
- Running it again is safe because already fixed products will not be modified again.

---

## 8. Startup Seeding & Auto Migration

On every Django server startup, the app automatically seeds and migrates the database via `AppConfig.ready()`:

- Ensures the default category **Miscellaneous** exists
- Assigns `Miscellaneous` to products with a missing category
- Assigns `"Unknown"` to products with a missing or blank brand

This runs automatically — no manual step needed. The process is idempotent: already-fixed records are never modified again.

---

## 9. Bulk CSV Upload via Postman

1. **Prepare CSV** — Create a `.csv` file with columns: `name, description, price, brand, quantity, category_id`. Leave `category_id` blank to assign to _Miscellaneous_.
2. **Set request** — Method: `POST`, URL: `http://127.0.0.1:8000/week4/products/bulk-upload/`
3. **Set body** — Go to `Body → form-data`, add a key named `file`, change type to `File`, and select your CSV.
4. **Send** — Click Send. All rows are validated before any product is created.

---

# Week 5 - Interactive Data Tools

## Features

- Display inventory in a table format using Streamlit
- Add and remove products directly from UI
- Sidebar filter by product category
- Stock alert for low-quantity items
- Jupyter Notebook for MongoEngine queries and data visualization

## Files

- `dashboard.py` → Streamlit inventory dashboard
- `notebook/week5_inventory_analysis.ipynb` → Data analysis and visualization

---

# Week 6 - Structured LLM Output — Validation & JSON with Pydantic

LLMs return plain text. Even when asked for JSON, they can produce malformed output, include markdown fences, omit fields, use wrong types, or return the wrong number of items. Without validation, this silently breaks your application.

---

## Pydantic Schemas

Pydantic schemas define the exact shape and constraints data must meet — field types, min/max lengths, numeric ranges, and optional vs required fields. If the LLM response doesn't match, a `ValidationError` is raised immediately and nothing bad reaches the database.

---

## Two Layers of Enforcement

**Prompt level** — the prompt shows the exact JSON structure, uses concrete numeric examples, forbids markdown, and states field rules explicitly.

**API level** — Gemini's `response_mime_type` and `response_schema` config options constrain the model's output at generation time, before it even reaches your code.

Both layers together are more reliable than either one alone.

---

## Parse → Validate → Save

1. `model_validate_json()` parses the raw response text and validates all fields in one step.
2. Defensive checks (`.strip()`, range checks) catch edge cases that Pydantic technically allows but would produce bad data in the database.
3. `model_dump()` converts validated Pydantic objects back to plain Python dicts for JSON export or database saving.

---

## Flow

```
Prompt → Gemini API → Raw JSON → model_validate_json() → Defensive checks → MongoDB / JSON file
```

---

# Week 7 – Semantic Search & Evaluation

## Overview

This week extends the inventory system with semantic search using embeddings, evaluation metrics, and interactive comparison via Streamlit dashboard.

---

## Key Concepts

### 1. Embeddings (SBERT)

- **Model:** `all-MiniLM-L6-v2`
- Converts text → vector representation
- Used for semantic similarity

### 2. Cosine Similarity

Used to measure similarity between:

- Query embedding vs product embeddings
- Product vs product (for recommendations)

---

## Core Functionalities

### Semantic Search

```
Query → Embedding → Compare with Product Embeddings → Rank → Top K
```

Implemented in `semantic_search.py` → `semantic_search()`

### Similar Products _(Advanced Task)_

- Uses product-to-product similarity
- Triggered via **"Find Similar Products"** button in dashboard
- `find_similar_products(product_id)`

### Evaluation _(Task 4)_

| Metric          | Formula                         |
| --------------- | ------------------------------- |
| **Precision@K** | Relevant / Retrieved            |
| **Recall@K**    | Relevant Found / Total Relevant |
| **Hit@K**       | At least one relevant result    |
| **Fallout@K**   | Irrelevant retrieved            |

### Model Comparison _(Adv Task 2)_

| Model               | Characteristic |
| ------------------- | -------------- |
| `all-MiniLM-L6-v2`  | Fast           |
| `all-mpnet-base-v2` | Better quality |

Evaluated on speed (latency) and result quality (manual inspection).

### Streamlit Dashboard _(Task 5)_

- Keyword Search
- Semantic Search
- Side-by-side comparison
- Similar product recommendations

---

## Important Implementation Details

### LRU Cache

- Used for embedding model loading
- Avoids repeated model initialization

### Combined Text for Embedding

Each product is converted to:

```
name + description + brand + category
```

This improves semantic understanding.

### Unique Keys in Streamlit

Used for widgets and buttons inside loops to prevent duplicate element errors.

```
keyword_similar_button_16
semantic_similar_button_16
```

---

# Week 8 — RAG Powered Inventory Expert

A **Retrieval-Augmented Generation (RAG)** system built on top of the existing inventory project. Ask natural language questions and get grounded answers backed by real documents and live stock data.

## How It Works

1. Loads knowledge files (Product Manual, Return Policy, Vendor FAQ)
2. Splits them into chunks using **LangChain**
3. Stores embeddings in **ChromaDB**
4. Retrieves the most relevant chunks for a user query
5. Sends grounded context to **Gemini**
6. Returns an answer based only on retrieved documents
7. Optionally combines the answer with live stock data from **MongoDB**
8. Supports **LangSmith tracing** for observability

## Project Structure

```
week8/
├── config.py               # Central settings
├── knowledge_base.py       # Loads text documents
├── text_chunker.py         # Splits documents into chunks
├── vector_store.py         # ChromaDB indexing and search
├── ingest_documents.py     # Runs the full ingestion pipeline
├── retriever.py            # Retrieves relevant chunks
├── prompt_builder.py       # Builds grounded prompt
├── llm_client.py           # Calls Gemini
├── rag_pipeline.py         # End-to-end RAG flow
├── stock_lookup.py         # Fetches stock data from MongoDB
├── ask_expert_service.py   # Combines RAG + stock lookup
├── eval_retrieval.py       # Evaluates retrieval quality
├── eval_rag.py             # Evaluates final RAG answers
├── langsmith_setup.py      # Enables LangSmith tracing
├── dashboard.py            # Streamlit UI
└── knowledge/
    ├── product_manual.txt
    ├── return_policy.txt
    └── vendor_faq.txt
```

---

# Week 9/10 — AI Quote Agent

An autonomous LLM agent built on top of the existing inventory project. Customers describe what they want in natural language, and the agent identifies the product, checks stock, applies tiered discounts within a strict policy cap, and returns a structured Quote Invoice.

## How It Works

1. Receives a natural language quote request (e.g. _"I need 60 building blocks for a school project"_)
2. Uses **LangChain** to orchestrate a tool-calling agent backed by **Gemini**
3. The agent identifies the product via **semantic search** (reused from Week 7)
4. Checks current stock level from **MongoDB**
5. Caps the quoted quantity at available stock if the request exceeds it
6. Applies a **tiered discount** (0% / 5% / 10% / 15%) based on quantity
7. Enforces a hard **20% policy cap** on any discount (deterministic Python guard)
8. Produces both a customer-facing answer and a validated **JSON Quote Invoice** (Pydantic)
9. Supports **LangSmith tracing** for full observability of every agent run
10. Includes an automated eval suite covering simple and complex scenarios

## Project Structure

```
week9_10/
├── config.py            # Central settings (model, discount tiers, policy cap)
├── schema.py            # QuoteInvoiceSchema - Pydantic model + validation
├── policy.py            # Discount cap enforcement
├── llm_client.py        # ChatGoogleGenerativeAI wrapper
├── tools.py             # The four @tool functions the agent can call
├── agent.py             # LangChain AgentExecutor + system prompt
├── service.py           # Cleanup layer + structured invoice builder
├── eval_agent.py        # Rate-limit-aware test suite
├── tool_tests.ipynb     # Jupyter notebook testing each tool in isolation
└── langsmith_setup.py   # Enables LangSmith tracing
```

---

<!-- # Interneers Lab - Backend in Python

Welcome to the **Interneers Lab 2026** Python backend! This serves as a minimal starter kit for learning and experimenting with:

- **Django** (Python)
- **MongoDB** (via Docker Compose)
- Development environment in **VSCode** (recommended)

**Important:** Use the **same email** you shared during onboarding when configuring Git and related tools. That ensures consistency across all internal systems.

---

## Table of Contents

1. [Prerequisites & Tooling](#prerequisites--tooling)
2. [Setting Up the Project](#setting-up-the-project)
3. [Running Services](#running-services)
   - [Backend: Django](#backend-django)
   - [Database: MongoDB via Docker Compose](#database-mongodb-via-docker-compose)
4. [Verification of Installation](#verification-of-installation)
5. [Development Workflow](#development-workflow)
   - [Recommended VSCode Extensions](#recommended-vscode-extensions)
   - [Making Changes & Verifying](#making-changes--verifying)
   - [Pushing Your First Change](#pushing-your-first-change)
6. [Making Your First Change](#making-your-first-change)
   - [Starter 0](#starter-0-changes)
   - [Starter 1](#starter-1-changes)
7. [Running Tests (Optional)](#running-tests-optional)
8. [Hot Reloading](#hot-reloading)
9. [MongoDB Connection](#mongodb-connection)
10. [Further Reading](#further-reading)
11. [Important Note on settings.py](#important-note-on-settingspy)

---

## Prerequisites & Tooling

These are the essential tools you need:

1. **Homebrew (macOS Only)**

   **Why?**

   Homebrew is a popular package manager for macOS, making it easy to install and update software (like Python, Docker, etc.).

   **Install**:

   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

```

```

2. **Python 3.14** (3.12 or higher required)

   **Why 3.14?**

   This is the recommended version for the module's Python-related tasks, ensuring consistency across projects.

   **Install or Upgrade**:
   - macOS (with Homebrew): `brew install python` or use [pyenv](https://github.com/pyenv/pyenv):
     ```bash
     brew install pyenv
     brew update && brew upgrade pyenv
     pyenv install 3.14.3
     ```
   - Windows: [Download from python.org](https://www.python.org/downloads/) (ensure it's 3.14)
   - Linux: Use your distro's package manager or pyenv

   **Verify**:

   ```bash
   python3 --version
   ```

   You should see something like `Python 3.14.x`.

   If you are getting an older version, you can either:
   - Use the full path: `~/.pyenv/versions/3.14.3/bin/python`
   - Or update your `.bashrc` / `.zshrc`:
     ```bash
     vim ~/.zshrc   # or any preferred editor of your choice
     alias python3="/path/to/python3.14"
     source ~/.zshrc # or ~/.bashrc
     ```

3. **virtualenv** or built-in `venv`

   **Why?**

   A virtual environment keeps project dependencies isolated from your system Python.

   **Install**
   - `pip3 install virtualenv` (if needed)
   - or use `python3 -m venv venv`

   **Verify**
   - Try to activate the venv using the following command:

     ```bash
     source venv/bin/activate         # macOS/Linux
     .\venv\Scripts\activate          # Windows
     ```

   - In most machines, your terminal prompt will be prefixed with something like `(venv)`.

   Check which Python is being used:
   - macOS/Linux:

     ```bash
     which python
     ```

     This should return a path inside the `venv/` directory (e.g., `.../backend/python/venv/bin/python`)

   - Windows:
     ```
     where python
     ```
     This should return a path inside `venv\Scripts\python.exe`.

4. **Docker** & **Docker Compose**

   **Why?**

   We use Docker to run MongoDB (and potentially other services) in containers, preventing "works on my machine" issues.

   **Install**
   - [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)
   - [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)

   **Verify**

   Verify version and successful installation with `docker --version` and `docker compose version`.

5. **API & MongoDB Tools**
   - **[Postman](https://www.postman.com/downloads/)**, **[Insomnia](https://insomnia.rest/download)**, or **[Paw](https://paw.cloud/client) (only for mac)** for API testing
   - **[MongoDB Compass](https://www.mongodb.com/try/download/compass)** or a **[VSCode MongoDB](https://code.visualstudio.com/docs/azure/mongodb)** extension

---

## Setting Up the Project

### Create a Python Virtual Environment

The python virtual env should be created inside the `backend/python` directory. Run the following commands:

```bash
cd backend/python
python3 -m venv venv
```

To activate the virtual environment:

```bash
# macOS/Linux
source venv/bin/activate
```

```Powershell
# on Windows Powershell:
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\activate
```

### Install Python Dependencies

```bash
pip install --upgrade pip
pip3 install -r requirements.txt
```

By default, **requirements.txt** includes:

- **Django** 6.0.2
- **pymongo** 4.16.0 (MongoDB driver)

**Check your `.gitignore`**
Make sure `venv/` and other temporary files aren't committed.

---

## Running Services

### Backend: Django

Navigate to the `backend/python` directory:

```bash
cd backend/python
```

Start the Django server on port `8001`:

```bash
python manage.py runserver 8001
```

Open [http://127.0.0.1:8001/hello/](http://127.0.0.1:8001/hello/) to see the **"Hello World"** endpoint.

---

### Database: MongoDB via Docker Compose

Inside `backend/python`, you'll find a `docker-compose.yaml`.

To start MongoDB via Docker Compose:

```bash
docker compose up -d
```

Verify with:

```bash
docker compose ps
```

MongoDB is now running on `localhost:27019`. Connect using `root` / `example` or update credentials as needed.

---

## Verification of Installation

- **Python**: `python3 --version` (should be 3.12+)
- **Django**: `python -c "import django; print(django.get_version())"` (should be 6.0.2)
- **Docker**: `docker --version`
- **Docker Compose**: `docker compose version`

Confirm that all meet the minimum version requirements.

---

## Development Workflow

### Recommended VSCode Extensions

- **Python (Microsoft)**
  Provides language server support, debugging, linting, and IntelliSense for Python code.

- **Django** (optional but helpful)
  Offers syntax highlighting and code snippets tailored for Django projects.

- **Docker**
  Allows you to visualize, manage, and interact with Docker containers and images directly in VSCode.

- _(Optional)_ **MongoDB for VSCode**
  Lets you connect to and browse your MongoDB databases, run queries, and view results without leaving VSCode.

---

### Making Your First Change

## Backend:

### Starter 0 changes:

1. Edit the `hello_world` function in `django_app/urls.py`.
2. Refresh your browser at [http://127.0.0.1:8001/hello/](http://127.0.0.1:8001/hello/).

### Starter 1 changes:

##### Creating and Testing a Simple "Hello, {name}" API (via Query Parameters)

This section explains how to create a Django endpoint that reads a `name` parameter from the **query string** (e.g., `/?name=Bob`).

---

#### 1. Define the View Function

Open `django_app/urls.py`. Below, we'll define a function that looks for a `name` query parameter in `request.GET`:

```python
# django_app/urls.py

from django.contrib import admin
from django.urls import path
from django.http import JsonResponse

def hello_name(request):
    """
    A simple view that returns 'Hello, {name}' in JSON format.
    Uses a query parameter named 'name'.
    """
    # Get 'name' from the query string, default to 'World' if missing
    name = request.GET.get("name", "World")
    return JsonResponse({"message": f"Hello, {name}!"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello_name),
    # Example usage: /hello/?name=Bob
    # returns {"message": "Hello, Bob!"}
]
```

---

#### 2. Run the Django Server

Activate your virtual environment (if not already active):

```bash
source venv/bin/activate         # macOS/Linux
.\venv\Scripts\activate          # Windows
```

Install dependencies (if you haven't):

```bash
cd backend/python  # if you are not inside backend/python already.
pip3 install -r requirements.txt
```

Start the server on port 8001:

```bash
python manage.py runserver 8001
```

You should see:

```
Starting development server at http://127.0.0.1:8001/
```

#### Test the Endpoint with Postman (or Insomnia/Paw)

Install a REST client like Postman (if you haven't already).

Create a new GET request.

Enter the endpoint, for example:

```
http://127.0.0.1:8001/hello/?name=Bob
```

Send the request. You should see a JSON response:

```json
{
  "message": "Hello, Bob!"
}
```

#### Congratulations! You wrote your first own API.

---

### Pushing Your First Change

1. **Stage and commit**:
   ```bash
   git add .
   git commit -m "Your descriptive commit message"
   ```
2. **Push to your forked repo (main branch by default):**
   ```bash
   git push origin main
   ```

---

## Running Tests (Optional)

### Django Tests

```bash
cd backend/python
python manage.py test
```

### Docker

```bash
docker compose ps
```

Note: This command displays the status of the containers, including whether they are running, their assigned ports, and their names, as defined in the docker-compose.yaml file. If you have set up a MongoDB server using Docker and connected it to your Django application, you can use this command to verify that the MongoDB container is running properly.

---

## Hot Reloading

Django's development server supports hot reloading out of the box. When you modify any Python file, the server automatically detects the change and restarts. Simply save your file and refresh the browser to see your changes.

---

## MongoDB Connection

MongoDB connections differ depending on your setup:

### Local Development

When running the project locally, MongoDB is exposed on port **27019**:

```
mongodb://root:example@localhost:27019/?authSource=admin
```

### Using Environment Variables

To ensure flexibility across environments, use environment variables for the MongoDB connection. For example:

#### Example `settings.py` (Django + pymongo):

```python
# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases
from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv()
MONGO_USER = os.getenv("MONGO_USER", "root")
MONGO_PASS = os.getenv("MONGO_PASS", "example")
MONGO_PORT = os.getenv("MONGO_PORT", "27019")
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")

client = MongoClient(
    f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/?authSource=admin"
)

DATABASES = {}
```

---

## Further Reading

- Django: https://docs.djangoproject.com/en/6.0/
- MongoDB: https://docs.mongodb.com/
- Docker Compose: https://docs.docker.com/compose/
- pymongo: https://pymongo.readthedocs.io/en/stable/

---

## Important Note on `settings.py`

- You should commit `settings.py` so the Django configuration is shared.
- However, never commit secrets (API keys, passwords) directly. Use environment variables or `.env` files (excluded via `.gitignore`).

---

## Common Commands Reference

```bash
# Virtual environment
python3 -m venv venv                        # Create virtual environment
source venv/bin/activate                     # Activate (macOS/Linux)
.\venv\Scripts\activate                      # Activate (Windows)
deactivate                                   # Deactivate

# Dependencies
pip install -r requirements.txt              # Install dependencies
pip freeze > requirements.txt                # Update requirements file

# Django
python manage.py runserver 8001              # Start dev server on port 8001
python manage.py test                        # Run tests

# Docker / MongoDB
docker compose up -d                         # Start MongoDB
docker compose down                          # Stop MongoDB
docker compose ps                            # List running containers
docker compose logs -f                       # View logs
```

```

``` -->
