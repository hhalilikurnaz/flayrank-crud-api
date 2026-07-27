# Task API

## Project Overview

This project is a **FastAPI CRUD API** backed by **PostgreSQL**, with **Supabase Authentication** and **JWT-protected endpoints**. It supports local development and full-stack runs via **Docker Compose**.

You can manage tasks with standard CRUD operations, sign users up and in through Supabase Auth, and protect selected routes with Bearer access tokens.

## Architecture

```text
Client
  → FastAPI routes
  → Authentication layer
  → Supabase Auth
  → PostgreSQL repository
```

### Responsibilities

| File | Responsibility |
|------|----------------|
| `main.py` | Application entry point and router registration |
| `auth.py` | Signup, login, and logout endpoints |
| `supabase_client.py` | Supabase client connection |
| `auth_utils.py` | JWT token verification |
| `dependencies.py` | Reusable FastAPI authentication dependency (`get_current_user`) |
| `access.py` | Public and protected route handlers |
| `database.py` | PostgreSQL CRUD repository |

FastAPI routes stay separate from storage and auth verification. Switching auth or database details only requires changing the relevant layer.

## Environment Setup

Required variables:

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string |
| `SUPABASE_URL` | Supabase project URL |
| `SUPABASE_KEY` | Supabase anon / publishable key |

Also used by Docker Compose for the database service:

| Variable | Description |
|----------|-------------|
| `POSTGRES_USER` | PostgreSQL username |
| `POSTGRES_PASSWORD` | PostgreSQL password |
| `POSTGRES_DB` | PostgreSQL database name |

Create your local env file from the template:

```bash
cp .env.example .env
```

- **`.env`** — contains local secrets; **not** committed to Git
- **`.env.example`** — committed placeholders for required configuration

Example placeholders (from `.env.example`):

```env
DATABASE_URL=postgresql://postgres:dev@localhost:5432/tasks
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
```

## Installation

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the API (with PostgreSQL reachable and `.env` configured):

```bash
uvicorn main:app --reload
```

The API is available at:

```text
http://localhost:8000
```

## Docker

Start the application stack:

```bash
docker compose up
```

This starts PostgreSQL and the FastAPI app together. The API waits until the database is healthy, then serves traffic on port `8000`.

```text
http://localhost:8000
```

Run in the background:

```bash
docker compose up -d
```

Stop:

```bash
docker compose down
```

## Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/signup` | Register a user with email and password |
| POST | `/auth/login` | Sign in and receive a session / access token |
| POST | `/auth/logout` | Sign out via Supabase Auth (204 No Content) |

Signup / login body:

```json
{
  "email": "user@example.com",
  "password": "your-password"
}
```

## Protected Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/protected/profile` | Returns the authenticated user (`id`, `email`) |
| GET | `/protected/dashboard` | Dashboard payload for the authenticated user |

These endpoints require:

```http
Authorization: Bearer <access_token>
```

Obtain an access token from `/auth/login` (or `/auth/signup` when a session is returned), then send it on protected requests.

Public (no auth):

```text
GET /public/info
```

## Swagger Documentation

Open the interactive docs:

```text
http://localhost:8000/docs
```

1. Call `/auth/login` (or signup) to get an `access_token`.
2. Click the **Authorize** 🔒 button in Swagger UI.
3. Enter the Bearer access token (Swagger’s HTTP Bearer field; you typically paste the token value only).
4. Call protected endpoints such as `/protected/profile` and `/protected/dashboard`.

## API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/` | No | API information |
| GET | `/health` | No | Health check |
| GET | `/tasks` | No | List all tasks |
| GET | `/tasks/{id}` | No | Get a task by id |
| POST | `/tasks` | No | Create a task |
| PUT | `/tasks/{id}` | No | Update a task |
| DELETE | `/tasks/{id}` | No | Delete a task |
| GET | `/public/info` | No | Public sample endpoint |
| POST | `/auth/signup` | No | User signup |
| POST | `/auth/login` | No | User login |
| POST | `/auth/logout` | No | User logout |
| GET | `/protected/profile` | Bearer | Authenticated profile |
| GET | `/protected/dashboard` | Bearer | Authenticated dashboard |

## Database Schema

| Column | Type |
|--------|------|
| id | SERIAL PRIMARY KEY |
| title | TEXT NOT NULL |
| done | BOOLEAN NOT NULL |

## Project Structure

```text
.
├── main.py              # App entry + router registration
├── auth.py              # Signup / login / logout
├── supabase_client.py   # Supabase client
├── auth_utils.py        # JWT verification
├── dependencies.py      # get_current_user dependency
├── access.py            # Public / protected routes
├── database.py          # PostgreSQL repository
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```
