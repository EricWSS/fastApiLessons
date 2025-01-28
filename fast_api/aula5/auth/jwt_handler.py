from datetime import datetime, timedelta
import jwt
# from jwt.exceptions import ExpiredSignatureError, InvalidTokenError,ExpiredSignatureError, InvalidSignatureError, DecodeError
from typing import Dict
from fastapi import Depends, HTTPException, Header, status
from db.database import get_db
from sqlalchemy.orm import Session
from models.user import User
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "your_secret_key"  # A chave secreta   
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Função para criar o token de acesso
def create_access_token(data: dict):
    payload = data.copy()
    expire = datetime.now() + timedelta(hours=30)  
    payload.update({"exp": expire})
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


# Função para verificar o token
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
            )
        return {"id": user_id}  # Retorne o ID do usuário
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
        )
    
    