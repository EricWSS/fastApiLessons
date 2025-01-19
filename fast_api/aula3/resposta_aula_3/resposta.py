from fastapi import FastAPI
from models import Tarefa
from conector import BancoDeDados


app = FastAPI()

banco = BancoDeDados()

@app.get("/tasks") #Trazer dados do banco
async def get_tasks():# select
    banco.conectar()
    banco.criar_cursor()
    query = "SELECT * FROM ew_tarefas;"
    banco.cursor.execute(query)
    resultados = banco.cursor.fetchall() # Lista de tuplas
    banco.fechar_conexao()
    return {"tasks":[d for d in resultados]}  # Lista de listas

@app.post("/tasks")
async def create_task(task: Tarefa):
    banco.conectar()
    banco.criar_cursor()
    query = "INSERT INTO ew_tarefas (tarefa, feito) VALUES (%s, %s);" #Placeholder (evitar SQL-Injection)
    banco.cursor.execute(query, (task.task, task.feito))
    banco.commit()
    banco.fechar_conexao()
    
    return {"message": f"Tarefa '{task.task}' criada com sucesso!"}

@app.patch("/tasks")
async def update_patch_task(task: Tarefa):
    banco.conectar()
    banco.criar_cursor()
    query = "UPDATE ew_tarefas SET tarefa = %s WHERE id = %s;"
    banco.cursor.execute(query, (task.task, task.id))
    banco.commit()
    banco.fechar_conexao()
    return {"message": f"Tarefa '{task}' atualizada com sucesso!"}

@app.put("/tasks")
async def update_put_task(task: Tarefa):
    banco.conectar()
    banco.criar_cursor()
    query = "UPDATE ew_tarefas SET feito = %s WHERE id = %s;"    
    banco.cursor.execute(query, (task.feito, task.id))
    banco.connection.commit()
    banco.fechar_conexao()
    return {"message": f"Tarefa {task.id} atualizada para '{task.feito}'"}

@app.delete("/tasks")
async def delete_task(task: Tarefa):
    banco.conectar()
    banco.criar_cursor() 
    query = "DELETE FROM ew_tarefas WHERE id = %s;"   
    banco.cursor.execute(query, (task.id,))
    banco.connection.commit()
    banco.fechar_conexao()  
    
    return {"message": f"Tarefa {task.id} removida com sucesso"}

