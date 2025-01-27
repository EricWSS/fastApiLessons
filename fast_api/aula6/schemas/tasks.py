from pydantic import BaseModel
from typing import Optional

class TarefaDelete(BaseModel):
    id:int


class TarefaBase(BaseModel):
    id: Optional[int]
    tarefa: Optional[str]
    feito: Optional[bool] 
    usuario_id: Optional[int]


class TarefaCreate(BaseModel):
    tarefa: str
    feito: bool


class TarefaUpdate(BaseModel):
    
    id: int
    tarefa: Optional[str] = None
    feito: Optional[bool] = None


class TarefaResponse(BaseModel):
    #Equivalente a um 'select'
    id: int
    tarefa: str
    feito: bool
    usuario_id: int

    class Config:
        orm_mode = True

