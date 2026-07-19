import asyncio

from typing_extensions import Literal
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()
tasks_db = []

@app.get("/")
async def starting():
    return {"message":"Welcome! go to /docs"}

class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    status: Literal["started", "doing", "on-going", "completed", "on-review"] = "started"
    
@app.post("/tasks")
async def create_task(Task:TaskCreate):

    await asyncio.sleep(0.5)
    new_id = len(tasks_db) + 1

    new_tasks = {
        "id": new_id,
        "title": Task.title,
        "description": Task.description,
        "status": Task.status
    }

    tasks_db.append(new_tasks)
    return new_tasks


@app.get("/tasks")
async def show_task():
    return tasks_db

@app.get("/tasks/{task_id}")
async def get_taskid(task_id:int):
    for task in tasks_db:
        if task["id"] == task_id:
            return task
        
    raise HTTPException(status_code= 404, message="Task Not Found")

@app.delete("/tasks/{task_id}")
async def delete_task(task_id:int):
    await asyncio.sleep(0.5)
    for tasks in tasks_db:
        if tasks["id"] == task_id:
            tasks_db.remove(tasks)
            return {"message": "Task Delelted successfully"}
    
    raise HTTPException(status_code=404, detail="Task not found")


@app.put("/tasks/{task_id}")
async def update_task(task_id:int, updated_task:TaskCreate):
    for task in tasks_db:
        if task["id"] == task_id:
            task["title"] = updated_task.title
            task["description"] = updated_task.description
            return task
        
    raise HTTPException(status_code=404, detail="Task not found")