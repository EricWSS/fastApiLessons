from fastapi import FastAPI, Request
from models import Task


app = FastAPI()

banco_de_dados = []

@app.get("/tasks")
async def get_tasks():# select
    #estabelecer conexão
    #estabelexer cursor 
    #...
    return {"tasks":[d for d in banco_de_dados]} 

@app.post("/tasks")
async def create_task(task: Task):
    #estabelecer conexão
    #estabelexer cursor 
    #...
    banco_de_dados.append(task.task)
    #.close()
    
    return {"message": f"Tarefa '{task.task}' criada com sucesso!"}

# @app.post("/tasks")
# async def create_task(request: Request):
#     body = await request.json()  
#     task = body.get("task") 
#     banco_de_dados.append(task)
#     return {"message": f"Tarefa '{task}' criada com sucesso!"}

@app.put("/tasks/{task_id}")
#estabelecer conexão
    #estabelexer cursor 
    #...
async def update_task(task_id: int, task: str):

    return {"message": f"Tarefa {task_id} atualizada para '{task}'"}

@app.delete("/tasks/{task_id}")
#estabelecer conexão
    #estabelexer cursor 
    #...
async def delete_task(task_id: int):
    
    return {"message": f"Tarefa {task_id} removida com sucesso"}

