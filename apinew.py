from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pymysql

app = FastAPI()

# =========================
# MODELO
# =========================
class Usuario(BaseModel):
    nombre: str
    email: str

# =========================
# CONEXIÓN
# =========================
def get_connection():
    return pymysql.connect(
        host="localhost",
        user="appuser",
        password="App1234!",
        database="api_db",
        cursorclass=pymysql.cursors.DictCursor
    )

# =========================
# HEALTHCHECK
# =========================
@app.get("/health")
def health():
    return {"status": "ok"}

# =========================
# INSERT USUARIO
# =========================
@app.post("/usuarios")
def crear_usuario(usuario: Usuario):
    connection = get_connection()

    try:
        with connection:
            with connection.cursor() as cursor:
                sql = "INSERT INTO usuarios (nombre, email) VALUES (%s, %s)"
                cursor.execute(sql, (usuario.nombre, usuario.email))
            connection.commit()

        return {
            "message": "Usuario insertado",
            "data": usuario
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))