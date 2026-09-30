# Interneers Lab - Backend in Golang

Welcome to the **Interneers Lab 2026** Golang backend! This serves as a minimal starter kit for learning and experimenting with:
- **Golang** (Go)
- **MongoDB** (via Docker Compose)
- Development environment in **VSCode** (recommended)

**Important:** Use the **same email** you shared during onboarding when configuring Git and related tools. That ensures consistency across all internal systems.


---

## Table of Contents

1. [Prerequisites & Tooling](#prerequisites--tooling)
2. [Setting Up the Project](#setting-up-the-project)
3. [Running Services](#running-services)
   - [Backend: Go](#backend-go)
   - [Database: MongoDB via Docker Compose](#database-mongodb-via-docker-compose)
4. [Verification of Installation](#verification-of-installation)
5. [Development Workflow](#development-workflow)
   - [Making Changes & Verifying](#making-changes--verifying)
   - [Pushing Your First Change](#pushing-your-first-change)
6. [Running Tests](#running-tests)
7. [Docker Command Reference](#docker-command-reference)
8. [Further Reading](#further-reading)
9. [Common Commands Reference](#common-commands-reference)

---

## Prerequisites & Tooling

These are the essential tools you need:

1. **Golang 1.23.6**

   **Why?**

   The project uses Go for the backend. Use the VSCode extension for the best experience: [Reference](https://code.visualstudio.com/docs/languages/go)

2. **MongoDB 7.0.0**

   **Why?**

   The backend uses MongoDB as the database.

   You don't need to install it separately; it is included in the docker compose file. You can download MongoDB Compass from [here](https://www.mongodb.com/try/download/compass) and connect to the database using the connection string provided in the docker compose file.

3. **Docker & Docker Compose**

   **Why?**

   We use Docker to run MongoDB (and potentially other services) in containers. The project also exposes the App via Docker.

   **Install**

   You can download Docker Desktop from [here](https://www.docker.com/products/docker-desktop/) and install it.

4. **Git**

   **Why?**

   Required for version control and pushing your changes.

   **Install**

   You can setup Git using this [guide](https://docs.github.com/en/get-started/quickstart/set-up-git). Optionally you may install the GitHub CLI for a better experience: [Reference](https://cli.github.com/)

---

## Setting Up the Project

The project has a simple Golang backend with a MongoDB database. Currently a hello world API is implemented.

Run the following commands to setup the project:

```bash
make setup
make build-and-run
```

> **Note:** `make setup` is only needed once; it loads all the dependencies and sets up the environment variables.

---

## Running Services

### Backend: Go

After running `make build-and-run`, the Go backend is running. You can test the API in a new terminal (see [Making Changes & Verifying](#making-changes--verifying)).

---

### Database: MongoDB via Docker Compose

Inside `backend/go`, you'll find a `docker-compose.yml`. After running `make setup`, set unique values for `MONGO_USER` and `MONGO_PASSWORD` in the ignored `.env.local` file. Then start MongoDB with:

```bash
docker compose --env-file .env.local up -d
```

You can test the Mongo connection with the following command:

```bash
make mongo-login
```

Or connect to Mongo directly using a UI tool like MongoDB Compass.

MongoDB is bound to `127.0.0.1`, so it is not reachable from other machines. If you previously started MongoDB without authentication, recreate the local volume after setting credentials:

```bash
docker compose --env-file .env.local down -v
docker compose --env-file .env.local up -d
```

This deletes any data stored in the local development volume.

---

## Verification of Installation

- **Go**: `go version` (should be 1.23.6 or compatible)
- **Docker**: `docker --version`
- **Docker Compose**: `docker compose version`

Confirm that all meet the minimum version requirements.

---

## Development Workflow

### Making Changes & Verifying

In a new terminal, run the following command to test the API:

```bash
make test
```

You can also test the API with a name:

```bash
make welcome "John Doe"
```

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

## Running Tests

```bash
make test
```

---

## Docker Command Reference

The project uses Docker and Docker Compose to run the application and the database. The project also exposes the App via Docker.

To see the logs you can run the following command:

```bash
docker compose --env-file .env.local logs -f
```

To stop you can run the following command:

```bash
docker compose --env-file .env.local down
```

---

## Further Reading

- Go: https://go.dev/doc/
- MongoDB: https://www.mongodb.com/docs/
- Docker Compose: https://docs.docker.com/compose/
- VSCode Go extension: https://code.visualstudio.com/docs/languages/go

---

## Common Commands Reference

```bash
# Setup (once)
make setup                                # Load dependencies and set up environment variables
make build-and-run                        # Build and run the application

# Testing
make test                                 # Run tests
make welcome "John Doe"                   # Test API with a name

# Docker / MongoDB
docker compose --env-file .env.local up -d   # Start application and database
docker compose --env-file .env.local down    # Stop containers
docker compose --env-file .env.local ps      # List running containers
docker compose --env-file .env.local logs -f # View logs
make mongo-login                            # Test MongoDB connection
```
