from fastapi import FastAPI

app = FastAPI()

# Healthcheck en "/"
@app.get("/health")
def healthcheck():
    return {
        "status": "ok"
    }

# Endpoint Hello World
@app.get("/hello")
def hello():
    return {
        "message": "Hello World 👋"
    }