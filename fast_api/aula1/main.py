from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Hello, {name}!"}

@app.get("/dobro/{numero}")
async def double(numero: int):
    return {"message": f"o dobro é: {numero*2}"}

@app.get("/somar")
async def somar(a: int, b: int):
    return {"resultado": a + b}