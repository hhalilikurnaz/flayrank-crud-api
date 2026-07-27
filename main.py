from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

from database import (
    create_tables,
    seed_tasks,
    get_all_tasks,
    get_task_by_id
)


app = FastAPI()


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

    raise HTTPException(
        status_code=501,
        detail="Not implemented yet"
    )


class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None


@app.put("/tasks/{id}")
def update_task(id: int, task: TaskUpdate):

    raise HTTPException(
        status_code=501,
        detail="Not implemented yet"
    )


@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int):

    raise HTTPException(
        status_code=501,
        detail="Not implemented yet"
    )