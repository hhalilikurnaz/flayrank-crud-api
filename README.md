# Task API

A simple CRUD API built with FastAPI and SQLite.

## Features

- Health check endpoint
- Create tasks
- Read tasks
- Update tasks
- Delete tasks
- SQLite database persistence
- Automatic Swagger documentation

## Database

This project uses SQLite as the database.

SQLite was chosen because it is lightweight, does not require a separate database server, and stores all data in a single file. This makes it simple to set up and suitable for small applications and development environments.

The database file:

```text
tasks.db
```

The application automatically creates the database file and the `tasks` table when it starts.

### Tasks Table Schema

| Column | Type |
|--------|------|
| id | INTEGER PRIMARY KEY |
| title | TEXT |
| done | BOOLEAN |

## Running Locally

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment:

macOS / Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install fastapi uvicorn
```

Start the application:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

## Example SQL Queries

List all tasks:

```sql
SELECT * FROM tasks;
```

Show completed tasks:

```sql
SELECT * FROM tasks WHERE done = 1;
```

Count all tasks:

```sql
SELECT COUNT(*) FROM tasks;
```

Mark all tasks as completed:

```sql
UPDATE tasks SET done = 1;
```

Delete completed tasks:

```sql
DELETE FROM tasks WHERE done = 1;
```

## SQLite Database Screenshot

Database inspection was performed using DB Browser for SQLite..

(Add your DB Browser screenshot here)

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /tasks | Get all tasks |
| GET | /tasks/{id} | Get a single task |
| POST | /tasks | Create a new task |
| PUT | /tasks/{id} | Update a task |
| DELETE | /tasks/{id} | Delete a task |