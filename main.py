from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

from access import protected_router, public_router
from auth import router as auth_router
from database import (
    create_tables,
    seed_tasks,
    get_all_tasks,
    get_task_by_id,
    create_task as create_task_db,
    update_task as update_task_db,
    delete_task as delete_task_db
)


app = FastAPI()
app.include_router(auth_router)
app.include_router(public_router)
app.include_router(protected_router)


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

    return get_all_tasks()


@app.get("/tasks/{id}")
def get_task(id: int):

    task = get_task_by_id(id)

    if task:
        return task

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

    return create_task_db(task.title)


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

    if task.title is not None and not task.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "Title cannot be empty"
            }
        )

    updated_task = update_task_db(id, title=task.title, done=task.done)

    if updated_task is None:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "Task not found"
            }
        )

    return updated_task


@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int):

    deleted = delete_task_db(id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "Task not found"
            }
        )
