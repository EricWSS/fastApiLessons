from pydantic import BaseModel
from typing import Optional

class Tarefa(BaseModel):
    id:Optional[int]
    task:Optional[str] = ''
    feito: Optional[bool] = None  # Campo feito ainda é opcional

    class Config:
        orm_mode = True

