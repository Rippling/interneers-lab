# Intern Bootcamp 2025

Welcome to the **Rippling Intern Bootcamp 2025** repository! This serves as a minimal starter kit for learning and experimenting with:
- **Django** (Python)
- **Next.js** (React)
- **MongoDB** (via Docker Compose)
- Development environment in **VSCode** (recommended)

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Prerequisites & Tooling](#prerequisites--tooling)
3. [Setting Up the Project](#setting-up-the-project)
4. [Running Services](#running-services)
   - [Backend: Django](#backend-django)
   - [Frontend: Next.js](#frontend-nextjs)
   - [Database: MongoDB via Docker Compose](#database-mongodb-via-docker-compose)
5. [Verification of Installation](#verification-of-installation)
6. [Development Workflow](#development-workflow)
   - [Recommended VSCode Extensions](#recommended-vscode-extensions)
   - [Making Changes & Verifying](#making-changes--verifying)
   - [Pushing Your First Change](#pushing-your-first-change)
7. [Running Tests (Optional)](#running-tests-optional)
8. [Further Reading](#further-reading)

---

## Getting Started

### 1. Setting up Git and the Repo

1. **Install Git** (if not already):
   - **macOS**: [Homebrew](https://brew.sh/) users can run `brew install git`.
   - **Windows**: Use [Git for Windows](https://gitforwindows.org/).
   - **Linux**: Install via your distro’s package manager, e.g., `sudo apt-get install git` (Ubuntu/Debian).

2. **Configure Git** with your name and email:
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
3. **Fork** the Rippling/intern-bootcamp-2025(you should have access to this repo) repository on GitHub.
4. **Clone** your forked repo:
    ```
    git clone git@github.com:<YourUsername>/intern-bootcamp-2025.git
    cd intern-bootcamp-2025
    ```

## Prerequisites & Tooling

These are the essential tools you need:

1. **Python 3**  
   - Check via `python3 --version`  
   - On macOS (with Homebrew): `brew install python3`  
   - [Windows Install Guide](https://www.python.org/downloads/)

2. **virtualenv** or built-in `venv`  
   - `pip install virtualenv` (if needed)  
   - or use `python3 -m venv venv`

3. **Docker** & **Docker Compose**  
   - [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)  
   - [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)  
   - Verify with `docker --version` and `docker compose version`

4. **Node.js** & **Yarn**  
   - [Node.js Downloads](https://nodejs.org/en/download/)  
   - [Yarn Install Docs](https://classic.yarnpkg.com/lang/en/docs/install/)  
   - Check with `node --version` and `yarn --version`

5. *(Optional)* **Homebrew** (macOS)  
   - ```bash
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
     ```

6. *(Optional)* **API & MongoDB Tools**  
   - **Postman**, **Insomnia**, or **Paw** for API testing  
   - **MongoDB Compass** or a **VSCode MongoDB** extension

## Setting Up the Project

### Create a Python Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate   # macOS/Linux or, 
# on Windows:
.\venv\Scripts\activate
```

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

By default, **requirements.txt** includes:
- **Django**
- **pymongo** (MongoDB driver)

### Install Frontend Dependencies (if you have a Next.js project)

```bash
cd frontend
yarn install
cd ..
```

**Check your `.gitignore`**  
Make sure `venv/` and other temporary files aren’t committed.

---

## Running Services

### Backend: Django

If your Django project is in `bootcamp_backend/`, navigate there:

```bash
cd bootcamp_backend
```

Start the Django server on a port less likely to conflict (e.g., `8001`):

```bash
python manage.py runserver 8001
```

Open [http://127.0.0.1:8001/hello/](http://127.0.0.1:8001/hello/) to see the **"Hello World"** endpoint.

---

### Frontend: Next.js

If your Next.js app is in `frontend/`, navigate to it:

```bash
cd frontend
yarn dev --port 3001
```

The app should be accessible at [http://localhost:3001](http://localhost:3001).

If you haven’t created a Next.js project yet, you can do so with:

```bash
yarn create next-app frontend
```

---

### Database: MongoDB via Docker Compose

In the project root, you’ll find (or create) a `docker-compose.yaml`. For example:

```yaml
version: '3.8'

services:
  mongodb:
    image: mongo:latest
    container_name: intern_bootcamp_mongodb
    ports:
      - '27018:27017'
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: example
    volumes:
      - mongodb_data:/data/db

volumes:
  mongodb_data:
```

To start MongoDB via Docker Compose:

```bash
docker compose up -d
```

Verify with:

```bash
docker compose ps
```

MongoDB is now running on `localhost:27018`. Connect using `root` / `example` or update credentials as needed.

---

## Verification of Installation

- **Python**: `python3 --version`
- **Docker**: `docker --version`
- **Docker Compose**: `docker compose version`
- **Node**: `node --version`
- **Yarn**: `yarn --version`

Confirm that all meet any minimum version requirements.

---

## Development Workflow

### Recommended VSCode Extensions

- **Python** (Microsoft)
- **Django** (optional but helpful)
- **ESLint** (JavaScript/TypeScript linting)
- **Prettier** (optional, for code formatting)
- **Docker** (to visualize/manage containers)
- *(Optional)* **MongoDB for VSCode**

---

### Making Changes & Verifying

#### Backend (Django):
1. Edit the `hello_world` function in `urls.py` (or your views).
2. Refresh your browser at [http://127.0.0.1:8001/hello/](http://127.0.0.1:8001/hello/).

#### Frontend (Next.js):
1. Edit a component in `pages/index.js`.
2. Save and see the changes immediately at [http://localhost:3001](http://localhost:3001).

---

### Pushing Your First Change

1. **Stage and commit**:
   ```bash
   git add .
   git commit -m "Your descriptive commit message"
2. **Push to your forked repo (main branch by default):**
    ```
    git push origin main
    ```

---

## Running Tests (Optional)

### Django Tests

```
cd bootcamp_backend
python manage.py test
```

### Next.js Tests

```
cd frontend
yarn test
```

### Docker
```
docker compose ps
```

---

## Further Reading

- Django: https://docs.djangoproject.com/en/3.2/
- Next.js: https://nextjs.org/docs
- MongoDB: https://docs.mongodb.com/
- Docker Compose: https://docs.docker.com/compose/

---


## Important Note on `settings.py`:
- You should commit settings.py so the Django configuration is shared.
- However, never commit secrets (API keys, passwords) directly. Use environment variables or .env files (excluded via .gitignore).

---






