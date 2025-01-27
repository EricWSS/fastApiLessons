from sqlalchemy import Column, Integer, String, Boolean
from db.database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "ew_usuarios"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String(50), nullable=False, default="user")
