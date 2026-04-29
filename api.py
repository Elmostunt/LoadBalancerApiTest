from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pymysql
import os

app = FastAPI()

# =========================
# CONFIG (usa env vars idealmente)
# =========================
DB_HOST = os.getenv("DB_HOST", "TU_RDS_ENDPOINT")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Admin1234!")
DB_NAME = os.getenv("DB_NAME", "api_db")

# =========================
# MODELO
# =========================
class Usuario(BaseModel):
    nombre: str
    email: str
    edad: int

# =========================
# CONEXIÓN
# =========================
def get_connection():
    try:
        return pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error DB: {str(e)}")

# =========================
# HEALTHCHECK
# =========================
@app.get("/health")
def healthcheck():
    return {"status": "ok"}

# Hello World
@app.post("/hello")
def hello():
    return {
        "message": "Hello World 👋"
    }

# =========================
# INSERT USUARIO (ÚNICO ENDPOINT IMPORTANTE)
# =========================
@app.post("/usuarios")
def crear_usuario(usuario: Usuario):
    connection = get_connection()

    try:
        with connection:
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO usuarios (nombre, email, edad)
                VALUES (%s, %s, %s)
                """
                cursor.execute(sql, (usuario.nombre, usuario.email, usuario.edad))
            
            connection.commit()

        return {
            "message": "Usuario insertado en RDS",
            "data": usuario
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))