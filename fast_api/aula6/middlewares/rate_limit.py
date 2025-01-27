from slowapi.errors import RateLimitExceeded
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request
from starlette.responses import JSONResponse

limiter = Limiter(key_func=get_remote_address)

async def rate_limit_middleware(request: Request, call_next):
    try:
        limiter.check(request)
    except RateLimitExceeded:
        return JSONResponse(
            status_code=429,
            content={"detail": "Muitas requisições. Tente novamente mais tarde."}
        )
    response = await call_next(request)
    return response
