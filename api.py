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