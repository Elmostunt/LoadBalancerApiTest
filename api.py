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
@app.get("/hello")
def hello():
    return {
        "message": "Hello World 👋"
    }

# POST - Crear usuario
@app.post("/usuarios")
def crear_usuario(usuario: Usuario):
    return {
        "message": "Usuario creado correctamente",
        "data": usuario
    }