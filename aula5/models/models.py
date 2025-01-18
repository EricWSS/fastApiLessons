from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Tarefa(Base):
    __tablename__ = "ew_tarefas"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tarefa = Column(String(255), nullable=True)
    feito = Column(Boolean, default=False)