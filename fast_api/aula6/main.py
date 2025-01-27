from fastapi import FastAPI
from routers import users, tasks
from db.database import Base, engine
from middlewares.rbac import rbac_middleware

from slowapi.middleware import SlowAPIMiddleware
from config.limiter import limiter  

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.middleware("http")(rbac_middleware)



app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)




# Inclui os routers
app.include_router(users.router)
app.include_router(tasks.router)
