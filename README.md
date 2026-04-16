# LoadBalancerApiTest
api de muestra para desplegar en maquinas virtuales

correr con uvicorn

🚀 API básica (Hello World + Healthcheck en /health)
@app.get("/health")
def healthcheck():

# Endpoint Hello World
@app.get("/hello")

▶️ Cómo ejecutarla

uvicorn api:app --reload

🌐 Probar endpoints
Healthcheck:
http://localhost:8000/health
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