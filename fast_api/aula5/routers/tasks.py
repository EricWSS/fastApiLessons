#NEW
from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import select , text
from db.database import get_db
from models.tasks import Tarefa, Base
from models.user import User
from schemas.tasks import TarefaCreate, TarefaUpdate, TarefaDelete, TarefaResponse
from schemas.users import UserBase
from auth.dependencies import verify_token , get_current_user

router = APIRouter()

@router.get("/tasks", response_model=list[TarefaResponse])
async def get_tasks(
    user: dict = Depends(get_current_user), # Verificando o token
    db: Session = Depends(get_db) # Conectanto ao banco de dados.
):
    # Busca as tarefas no banco
    # tarefas = db.query(Tarefa).filter(Tarefa.usuario_id ==user['id']).all() # Consulta por todas as tarefas do usuário.
    
    tarefas_query = text( # Consulta SQL Crua
        f"""select 
            t.id ,
            t.tarefa ,
            t.feito ,
            t.usuario_id ,
            u.name as "nome_usuario"
        from ew_tarefas as t
        left join ew_usuarios as u on u.id = t.usuario_id
        where t.usuario_id = :usuario_id;"""
    )

    result: list = db.execute(tarefas_query,{"usuario_id": user["id"]}).fetchall() # Lista de tuplas

    if result is None:
        raise HTTPException(status_code=404, detail="Nenhuma tarefa encontrada.")
    
    tarefas = [ # List comprehension
        {
            "id": row.id,
            "tarefa": row.tarefa,
            "feito": row.feito,
            "usuario_id": row.usuario_id,
            "nome_usuario": row.nome_usuario,
        }
        for row in result
    ]

    # Retorna as tarefas como uma lista de dicionários serializáveis
    # return {"dados":tarefas, 'user_id':user['id']}
    return tarefas


# Rota para criar uma nova tarefa
@router.post("/tasks", response_model=TarefaCreate)
async def create_task(
    task: TarefaCreate,  # validação do pacote (JSON)
    user: dict = Depends(get_current_user), # Verificando o token
    db: Session = Depends(get_db) # Acesso ao banco
):
    
    # Criação da nova tarefa, associando ao usuário logado (usuario_id vem do token)
    nova_tarefa = Tarefa(tarefa=task.tarefa, feito=task.feito, usuario_id=user['id'])
    
    # Adiciona a tarefa no banco de dados
    db.add(nova_tarefa)
    db.commit()
    db.refresh(nova_tarefa)
    
    # Retorna a resposta com os dados da tarefa criada
    return TarefaCreate(tarefa=nova_tarefa.tarefa, feito=nova_tarefa.feito, usuario_id=nova_tarefa.usuario_id)


# # Rota para atualizar a tarefa (PUT)
@router.put("/tasks")
async def update_put_task(
    task: TarefaUpdate, 
    user: User = Depends(verify_token), 
    db: Session = Depends(get_db)
):  
    """Atualizar apenas o status da tarefa (feito ou não feito)"""
    if not task.id:
        raise HTTPException(status_code=400, detail="ID da tarefa é necessário")

    tarefa = db.query(Tarefa).filter(Tarefa.id == task.id).first()
    
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    if task.feito is not None:
        tarefa.feito = task.feito
    
    db.commit()
    db.refresh(tarefa)

    return {"message": f"Tarefa {task.id} atualizada para '{tarefa.feito}'", "task": tarefa}

# Rota para atualizar a tarefa (PATCH)
@router.patch("/tasks")
async def update_task(
    task: TarefaUpdate, # Validação dos dados com pydantic
    user: User = Depends(verify_token), # Verificando o token
    db: Session = Depends(get_db) # Acesso ao banco
):
    """Atualizar apenas o texto da tarefa"""
    tarefa = db.query(Tarefa).filter(Tarefa.id == task.id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    if task.tarefa is not None:
        tarefa.tarefa = task.tarefa
    
    db.commit()
    db.refresh(tarefa)
    return {"message": f"Tarefa '{tarefa.tarefa}' atualizada com sucesso!"}

# Rota para excluir a tarefa
@router.delete("/tasks")
async def delete_task(
    task: TarefaDelete, 
    user: User = Depends(verify_token), 
    db: Session = Depends(get_db)
):  
    tarefa = db.query(Tarefa).filter(Tarefa.id == task.id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    db.delete(tarefa)
    db.commit()
    return {"message": f"Tarefa {task.id} removida com sucesso"}