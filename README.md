# 🚀 LoadBalancerApiTest

API de ejemplo en **FastAPI** para desplegar en múltiples EC2 detrás de un **Load Balancer (ALB)**.

---

# 🧩 1. API

Endpoints disponibles:

```python
@app.get("/health")
def healthcheck():
    return {"status": "ok"}

@app.get("/hello")
def hello():
    return {"message": "Hello World"}
```

---

# ▶️ 2. Ejecución local

```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

---

# 🌐 3. Probar endpoints

* Healthcheck:
  [http://localhost:8000/health](http://localhost:8000/health)

* Hello:
  [http://localhost:8000/hello](http://localhost:8000/hello)

* Swagger:
  [http://localhost:8000/docs](http://localhost:8000/docs)

---

# 🖥️ 4. Preparar EC2 (Amazon Linux)

```bash
sudo dnf update -y
sudo dnf install git -y
sudo dnf install python3 -y

pip3 install fastapi
pip3 install "uvicorn[standard]"
pip3 install gunicorn
```

---

# 📦 5. Clonar proyecto

```bash
git clone https://github.com/Elmostunt/LoadBalancerApiTest.git
cd LoadBalancerApiTest
```

---

# ⚙️ 6. Ejecutar API en EC2 (FORMA CORRECTA)

```bash
gunicorn -w 3 -k uvicorn.workers.UvicornWorker api:app -b 0.0.0.0:8000
```

---

# ❌ MALAS PRÁCTICAS (evitar)

```bash
uvicorn api:app --host localhost --port 8000   # ❌ no accesible desde LB
uvicorn api:app --port 80                      # ❌ innecesario + sudo
```

---

# 🏗️ 7. Arquitectura

```text
Internet
   ↓
Load Balancer (puerto 80)
   ↓
EC2 (puerto 8000)
```

---

# 🔐 8. Configuración de Seguridad

## Security Group del Load Balancer

| Tipo | Puerto | Origen    |
| ---- | ------ | --------- |
| HTTP | 80     | 0.0.0.0/0 |

---

## Security Group de EC2

| Tipo       | Puerto | Origen               |
| ---------- | ------ | -------------------- |
| SSH        | 22     | TU_IP                |
| Custom TCP | 8000   | SG del Load Balancer |

---

# ⚙️ 9. Load Balancer (ALB)

## Listener

* HTTP : 80

## Forward

* Target Group

---

# 🎯 10. Target Group

## Configuración

| Parámetro   | Valor    |
| ----------- | -------- |
| Protocol    | HTTP     |
| Port        | 8000     |
| Target type | Instance |

---

## Health Check

| Parámetro    | Valor        |
| ------------ | ------------ |
| Path         | `/health`    |
| Protocol     | HTTP         |
| Port         | traffic port |
| Success code | 200          |

---

# 🚨 11. Errores comunes

### ❌ Mezclar puertos

* EC2 en 8000 pero TG en 80

### ❌ Usar localhost

* LB no puede conectarse

### ❌ Abrir EC2 al mundo

```text
8000 → 0.0.0.0/0
```

### ❌ Editar reglas en vez de recrearlas

* AWS no permite cambiar de IP → SG

---

# 🧪 12. Validación

Dentro de la EC2:

```bash
curl http://localhost:8000/health
```

Desde navegador:

```text
http://<LOAD_BALANCER_DNS>/health
```

---

# 🧠 13. Resumen clave

* La API corre en **8000**
* El Load Balancer recibe en **80**
* Solo el LB puede acceder a la EC2
* `/health` es usado para validación
