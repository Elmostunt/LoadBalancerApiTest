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

uvicorn api:app --reload


🌐 Probar endpoints
Healthcheck:
http://localhost:8000/
Hello World:
http://localhost:8000/hello
🧪 Bonus (útil para clases / demos)

FastAPI te levanta docs automáticamente:

Swagger:
http://localhost:8000/docs


PREPARAR MAQUINA 
sudo dnf update

sudo dnf install git

sudo dnf install python3

sudo dnf install pip

sudo pip install fastapi 

sudo pip install "uvicorn[standard]"   

git clone https://github.com/Elmostunt/LoadBalancerApiTest.git

cd LoadBalancerApiTest

sudo uvicorn api:app --host 0.0.0.0 --port 80

uvicorn api:app --host localhost --port 80