from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Tarefa, Base
from schemas import TarefaCreate, TarefaUpdate, TarefaBase

app = FastAPI()


@app.get("/tasks")#ok
async def get_tasks(db: Session = Depends(get_db)):
    tarefas = db.query(Tarefa).all()# Lista de dicionários
    return {"tasks": tarefas}


@app.post("/tasks")
async def create_task(task: TarefaCreate, db: Session = Depends(get_db)):
    nova_tarefa = Tarefa(tarefa=task.tarefa, feito=task.feito)
    db.add(nova_tarefa)
    db.commit()
    db.refresh(nova_tarefa)
    return {
        "message": f"Tarefa '{nova_tarefa.tarefa}' criada com sucesso!",
        "task": nova_tarefa
    }
    

@app.put("/tasks")
async def update_put_task(task: TarefaUpdate, db: Session = Depends(get_db)):
    if not task.id:
        raise HTTPException(status_code=400, detail="ID da tarefa é necessário")

    #Consulta para saber se a tarefa existe olhando o ID
    tarefa = db.query(Tarefa).filter(Tarefa.id == task.id).first() #Select
    
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")


    if task.feito is not None:
        tarefa.feito = task.feito #O que a pessoa manda na requisição
    
    db.commit()
    db.refresh(tarefa)

    return {"message": f"Tarefa {task.id} atualizada para '{tarefa.feito}'", "task": tarefa}



@app.patch("/tasks")
async def update_task(task: TarefaUpdate, db: Session = Depends(get_db)):
    tarefa = db.query(Tarefa).filter(Tarefa.id == task.id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    if task.tarefa is not None:
        tarefa.tarefa = task.tarefa
    if task.feito is not None:
        tarefa.feito = task.feito
    db.commit()
    db.refresh(tarefa)
    return {"message": f"Tarefa '{tarefa.tarefa}' atualizada com sucesso!"}


@app.delete("/tasks")
async def delete_task(task:TarefaBase, db: Session = Depends(get_db)):
    tarefa = db.query(Tarefa).filter(Tarefa.id == task.id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    db.delete(tarefa)
    db.commit()
    return {"message": f"Tarefa {task.id} removida com sucesso"}
