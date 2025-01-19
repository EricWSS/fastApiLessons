from pydantic import BaseModel, Field
from typing import Optional

class TarefaBase(BaseModel):
    id: Optional[int] = None
    tarefa: Optional[str] = ''   #Field(None)
    feito: Optional[bool] = None

class TarefaCreate(TarefaBase):
    tarefa: str 

class TarefaUpdate(TarefaBase):
    id: int 

class TarefaResponse(TarefaBase):
    id: int

    class Config:
        orm_mode = True
