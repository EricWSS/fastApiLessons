from pydantic import BaseModel

class Task(BaseModel):
    id: int
    legenda: str 
    is_completed: bool = False
