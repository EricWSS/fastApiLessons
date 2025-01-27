from fastapi import FastAPI
from routers import users, tasks
from db.database import Base, engine
from auth.jwt_handler import create_access_token

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(tasks.router)
# app.include_router(users.router, prefix="/users", tags=["Users"]) 
# app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
