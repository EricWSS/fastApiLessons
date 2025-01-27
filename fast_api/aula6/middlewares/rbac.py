# middlewares/rbac.py
from fastapi import Request, HTTPException
import jwt
from auth.jwt_handler import SECRET_KEY

IGNORED_PATHS = ["/login", "/register"]
ALGORITHM = "HS256"

async def rbac_middleware(request: Request, call_next):
    if request.url.path in IGNORED_PATHS:
        return await call_next(request)

    auth_header = request.headers.get("Authorization")
    print("Auth header:", auth_header)  # Log
    
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Token não fornecido")

    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("Payload do token:", payload)  # Log
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Token inválido")

    role = payload.get("role")
    print("Role no payload:", role)  # Log
    
    if not role:
        raise HTTPException(status_code=403, detail="Role não fornecida")
    
    return await call_next(request)
