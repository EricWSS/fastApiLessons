from fastapi import FastAPI
from routers import users, tasks
from db.database import Base, engine
from middlewares.rbac import rbac_middleware

from slowapi.middleware import SlowAPIMiddleware
from config.limiter import limiter  


app = FastAPI() # Intanciei a classe do fastapi
Base.metadata.create_all(bind=engine) # Instanciando banco de dados


app.middleware("http")(rbac_middleware) # Verifique todas as rotas
app.state.limiter = limiter # Limitando a quantidade de requisicoes
app.add_middleware(SlowAPIMiddleware) # Limitando a quantidade de requisicoes

# Inclui os routers
app.include_router(users.router)
app.include_router(tasks.router)
