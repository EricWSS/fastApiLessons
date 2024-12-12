from fastapi import FastAPI
from models import Task

app = FastAPI()

tasks = []

@app.get("/tasks")
async def get_tasks():
    return {"tasks": tasks}

@app.post("/tasks")
async def create_task(task: Task):
    tasks.append(task)
    return {"message": "Tarefa adicionada", "task": task}

@app.put("/tasks/{task_id}")
async def update_task(task_id: int, updated_task: Task):
    for task in tasks:
        if task.id == task_id:
            task.title = updated_task.title
            task.legenda = updated_task.legenda
            task.is_completed = updated_task.is_completed
            return {"message": "Tarefa atualizada", "task": task}
    return {"error": "Tarefa não encontrada"}

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    global tasks
    tasks = [task for task in tasks if task.id != task_id]
    return {"message": "Tarefa removida"}
