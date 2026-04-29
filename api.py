from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Modelo de entrada
class Usuario(BaseModel):
    nombre: str
    email: str
    edad: int

# Healthcheck
@app.get("/health")
def healthcheck():
    return {
        "status": "ok"
    }

# Hello World
@app.post("/hello")
def hello():
    return {
        "message": "Hello World 👋"
    }
