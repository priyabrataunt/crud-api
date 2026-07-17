from fastapi import FastAPI, HTTPException  # type: ignore
from pydantic import BaseModel
from typing import Literal

app = FastAPI()
tasks_db = []

@app.get("/")
async def read_root():
    return {"message": "Welcome to the app!"}

class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    status: Literal["started", "on-going", "completed", "some-other-day", "need_review"] = "started"

@app.post("/tasks")
async def create_task(task:TaskCreate):
    new_id = len(tasks_db) + 1

    new_tasks = {
        "id": new_id,
        "title": task.title,
        "description": task.description,
        "status": task.status 
    }

    tasks_db.append(new_tasks)
    return new_tasks

@app.get("/tasks")
async def get_tasks():
    return tasks_db

@app.get("/tasks/{task_id}")
async def getTask(task_id:int):
    for task in tasks_db:
        if task["id"] == task_id:
            return task

    raise HTTPException(status_code= 404, detail= "Task Not Found")


@app.delete("/tasks/{task_id}")
async def delete_task(task_id:int):
    for task in tasks_db:
        if task["id"] == task_id:
            tasks_db.remove(task)
            return {"message":"Task deleted successfully"}

    raise HTTPException(status_code= 404, detail="Task Not Found")


@app.put("/tasks/{task_id}")
async def update_task(task_id:int, updated_data:TaskCreate):
    for task in tasks_db:
        if task["id"] == task_id:
            task["title"] = updated_data.title
            task["description"] = updated_data.description
            task["status"] = updated_data.status
            return task
        
    raise HTTPException(status_code=404, detail="Task Not Found")