from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()

class Tarefa(Base): # tabela mestre para todas as 'tarefas'
    __tablename__ = "ew_tarefas"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tarefa = Column(String(255), nullable=True)
    feito = Column(Boolean, default=False)
    usuario_id = Column(Integer)

