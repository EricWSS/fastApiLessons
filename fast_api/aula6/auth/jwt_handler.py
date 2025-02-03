from datetime import datetime, timedelta
import jwt
from typing import Dict
from fastapi import Depends, HTTPException, status
from db.database import get_db
from sqlalchemy.orm import Session
from models.user import User
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "your_secret_key"  # A chave secreta
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Função para criar o token de acesso
def create_access_token(data: dict): # Não fiz nada novo
    payload = data.copy()
    expire = datetime.now() + timedelta(hours=30)  # Token expira em 30 horas
    payload.update({"exp": expire})
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

# Função para verificar o token
def verify_token(token: str = Depends(oauth2_scheme)):
    
    try:
        payload:dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        role: str = payload.get("role") # Novidade
        if user_id is None or role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido ou role não fornecida",
            )
        return {"id": user_id, "role": role}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expirado")
    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Erro ao decodificar token")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

