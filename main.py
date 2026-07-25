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


tasks = [
    {
        "id": 1,
        "title": "Learn FastAPI",
        "done": False
    },
    {
        "id": 2,
        "title": "Build CRUD API",
        "done": False
    },
    {
        "id": 3,
        "title": "Submit FlyRank assignment",
        "done": True
    }
]

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
    return tasks


@app.get("/tasks/{id}")
def get_task(id: int):

    for task in tasks:
        if task["id"] == id:
            return task

    raise HTTPException(
        status_code=404,
        detail={
            "error": f"Task {id} not found"
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

    new_task = {
        "id": len(tasks) + 1,
        "title": task.title,
        "done": False
    }

    tasks.append(new_task)

    return new_task


class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None


@app.put("/tasks/{id}")
def update_task(id: int, task: TaskUpdate):

    for existing_task in tasks:
        if existing_task["id"] == id:

            if task.title is None and task.done is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "error": "No update data provided"
                    }
                )

            if task.title is not None:
                if not task.title.strip():
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail={
                            "error": "Title cannot be empty"
                        }
                    )

                existing_task["title"] = task.title

            if task.done is not None:
                existing_task["done"] = task.done

            return existing_task

    raise HTTPException(
        status_code=404,
        detail={
            "error": f"Task {id} not found"
        }
    )


@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int):

    for index, task in enumerate(tasks):
        if task["id"] == id:
            tasks.pop(index)
            return

    raise HTTPException(
        status_code=404,
        detail={
            "error": f"Task {id} not found"
        }
    )