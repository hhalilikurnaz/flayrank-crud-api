from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import sqlite3


app = FastAPI()


DATABASE = "tasks.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def seed_tasks():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.executemany(
            """
            INSERT INTO tasks (title, done)
            VALUES (?, ?)
            """,
            [
                ("Learn FastAPI", False),
                ("Build CRUD API", False),
                ("Submit FlyRank assignment", True)
            ]
        )

        conn.commit()

    conn.close()


create_tables()
seed_tasks()


@app.get("/")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.get("/tasks")
def get_tasks():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


@app.get("/tasks/{id}")
def get_task(id: int):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (id,)
    )

    task = cursor.fetchone()

    conn.close()

    if task:
        return dict(task)

    raise HTTPException(
        status_code=404,
        detail={
            "error": "Task not found"
        }
    )


class TaskCreate(BaseModel):
    title: str


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):

    if not task.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "Title cannot be empty"
            }
        )

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO tasks (title, done)
        VALUES (?, ?)
        """,
        (task.title, False)
    )

    conn.commit()

    task_id = cursor.lastrowid

    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    )

    new_task = cursor.fetchone()

    conn.close()

    return dict(new_task)


class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None


@app.put("/tasks/{id}")
def update_task(id: int, task: TaskUpdate):

    if task.title is None and task.done is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "No update data provided"
            }
        )

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (id,)
    )

    existing_task = cursor.fetchone()

    if existing_task is None:
        conn.close()

        raise HTTPException(
            status_code=404,
            detail={
                "error": "Task not found"
            }
        )

    if task.title is not None:

        if not task.title.strip():
            conn.close()

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "Title cannot be empty"
                }
            )

        cursor.execute(
            """
            UPDATE tasks
            SET title = ?
            WHERE id = ?
            """,
            (task.title, id)
        )

    if task.done is not None:

        cursor.execute(
            """
            UPDATE tasks
            SET done = ?
            WHERE id = ?
            """,
            (task.done, id)
        )

    conn.commit()

    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (id,)
    )

    updated_task = cursor.fetchone()

    conn.close()

    return dict(updated_task)


@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (id,)
    )

    task = cursor.fetchone()

    if task is None:
        conn.close()

        raise HTTPException(
            status_code=404,
            detail={
                "error": "Task not found"
            }
        )

    cursor.execute(
        "DELETE FROM tasks WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return