from pydantic import BaseModel
from typing import Optional

class Tarefa(BaseModel):
    id:Optional[int] = None
    task:Optional[str] = ''
    feito: Optional[bool] = None  

    class Config:
        orm_mode = True

