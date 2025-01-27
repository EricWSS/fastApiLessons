from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from auth.jwt_handler import create_access_token
from auth.dependencies import get_current_user
from db.database import get_db
from models.user import  Base, User
from models.tasks import Tarefa
from schemas.tasks import TarefaBase,TarefaUpdate,TarefaCreate,TarefaResponse
from schemas.users import UserBase, UserCreate, UserLogin, UserResponse
from passlib.context import CryptContext

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Função para criptografar a senha
def hash_password(password: str):
    return pwd_context.hash(password)

def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Verifica se o email já está cadastrado
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email já registrado")

    # Cria o novo usuário
    hashed_password = hash_password(user.password)
    
    new_user = User(name=user.name, email=user.email, password=hashed_password)
    

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Usuário criado com sucesso!", "user": new_user}

@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Verifica se o email já está cadastrado
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email já registrado")

    # Cria o novo usuário
    hashed_password = hash_password(user.password)
    new_user = User(name=user.name, email=user.email, password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Usuário criado com sucesso!", "user": new_user}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    # Verifica se o email já está cadastrado
    db_user = db.query(User).filter(User.email == user.email).first()
    
    if not db_user or not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(db_user.id)})
    return {"access_token": token, "token_type": "bearer"}
