# Task API

## Project Overview

This is a FastAPI CRUD API that stores tasks in PostgreSQL. It provides endpoints to create, read, update, and delete tasks. Database connection settings are managed through environment variables.

## Architecture

The application separates HTTP routing from database operations.

- **`main.py`** — Contains FastAPI routes, request validation with Pydantic, and HTTP error handling. Routes do not execute SQL queries directly.
- **`database.py`** — Contains the PostgreSQL repository layer. It manages database connections, table creation, seeding, and all CRUD SQL operations using `psycopg`.

The storage layer is isolated from the API layer. Switching from one storage solution to another only requires changing the repository layer, without rewriting routes.

```text
Client → FastAPI Routes (main.py) → Repository Layer (database.py) → PostgreSQL
```

## Features

- Health check endpoint
- Full CRUD operations for tasks
- PostgreSQL persistence
- Environment-based configuration
- Docker Compose support
- Automatic Swagger documentation

## Prerequisites

- Docker and Docker Compose
- Python 3.12+ (for local development)

---

# Environment Configuration

Create your local environment file:

```bash
cp .env.example .env
```

Environment variables:

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string |
| `POSTGRES_USER` | PostgreSQL username |
| `POSTGRES_PASSWORD` | PostgreSQL password |
| `POSTGRES_DB` | PostgreSQL database name |

Example:

```env
DATABASE_URL=postgresql://postgres:dev@localhost:5432/tasks
POSTGRES_USER=postgres
POSTGRES_PASSWORD=dev
POSTGRES_DB=tasks
```

The `.env` file is ignored by Git and should not contain committed secrets.

The repository includes `.env.example` as a template.

---

# Running with Docker Compose

Start the complete application stack:

```bash
docker compose up
```

Docker Compose starts two services:

## PostgreSQL Database

- Uses PostgreSQL 16
- Stores data in a persistent Docker volume
- Performs a health check before the API starts

## FastAPI Application

- Built from the project Dockerfile
- Runs with Uvicorn
- Connects to PostgreSQL through the Compose network

API:

```
http://localhost:8000
```

Swagger documentation:

```
http://localhost:8000/docs
```

Run in background:

```bash
docker compose up -d
```

Stop containers:

```bash
docker compose down
```

---

# Persistence Test

Database persistence was verified using the following steps:

1. Start the application stack:

```bash
docker compose up
```

2. Create a new task using the API.

Example:

```json
{
  "title": "Persistence test"
}
```

3. Stop the containers:

```bash
docker compose down
```

4. Start the stack again:

```bash
docker compose up
```

5. Request the tasks list again:

```
GET /tasks
```

The previously created task is still available.

This confirms that PostgreSQL data survives container restarts because the database uses a Docker volume.

---

# Running Locally

Create and activate a virtual environment:

```bash
python -m venv .venv

source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the API:

```bash
uvicorn main:app --reload
```

---

# Database Schema

The `tasks` table:

| Column | Type |
|---|---|
| id | SERIAL PRIMARY KEY |
| title | TEXT NOT NULL |
| done | BOOLEAN NOT NULL |

---

# API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API information |
| GET | `/health` | Health check |
| GET | `/tasks` | List all tasks |
| GET | `/tasks/{id}` | Get a task by id |
| POST | `/tasks` | Create a task |
| PUT | `/tasks/{id}` | Update a task |
| DELETE | `/tasks/{id}` | Delete a task |

---

# Example Requests

## Create Task

```bash
curl -X POST http://localhost:8000/tasks \
-H "Content-Type: application/json" \
-d '{"title":"Write documentation"}'
```

## List Tasks

```bash
curl http://localhost:8000/tasks
```

## Update Task

```bash
curl -X PUT http://localhost:8000/tasks/1 \
-H "Content-Type: application/json" \
-d '{"done":true}'
```

## Delete Task

```bash
curl -X DELETE http://localhost:8000/tasks/1
```

---

# Project Structure

```text
.
├── main.py
├── database.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```