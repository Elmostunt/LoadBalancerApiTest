# LoadBalancerApiTest
api de muestra para desplegar en maquinas virtuales

correr con uvicorn

🚀 API básica (Hello World + Healthcheck en /)
📁 archivo: main.py
from fastapi import FastAPI

app = FastAPI()

# Healthcheck en "/"
@app.get("/")
def healthcheck():
    return {
        "status": "ok",
        "message": "API funcionando correctamente 🚀"
    }

# Endpoint Hello World
@app.get("/hello")
def hello():
    return {
        "message": "Hello World 👋"
    }
▶️ Cómo ejecutarla

Ya que tú usas uvicorn:

uvicorn main:app --reload


🌐 Probar endpoints
Healthcheck:
http://localhost:8000/
Hello World:
http://localhost:8000/hello
🧪 Bonus (útil para clases / demos)

FastAPI te levanta docs automáticamente:

Swagger:
http://localhost:8000/docs