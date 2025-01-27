
from fastapi import Request, HTTPException
from jwt import decode, InvalidTokenError

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

async def auth_middleware(request: Request, call_next):
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        try:
            payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            # Armazena user e role no state para ser usado depois
            request.state.user = {
                "id": payload.get("sub"),
                "role": payload.get("role")
            }
        except InvalidTokenError:
            raise HTTPException(status_code=403, detail="Token inválido")
    
    return await call_next(request)
