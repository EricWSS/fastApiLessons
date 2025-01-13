from pydantic import BaseModel, Field
from typing import Optional

class TarefaBase(BaseModel):
    id: Optional[int] = Field(None)
    tarefa: Optional[str] = Field(None)
    feito: Optional[bool] = Field(None)

class TarefaCreate(TarefaBase):
    tarefa: str 

class TarefaUpdate(TarefaBase):
    id: int 

class TarefaResponse(TarefaBase):
    id: int

    class Config:
        orm_mode = True
