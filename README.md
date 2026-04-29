Aquí tienes el **README completo integrado**, con:

* Orden correcto paso a paso
* Corrección de **Security Group del Load Balancer (asociación incluida)**
* Anexo de **Auto Scaling + pruebas de carga**
* Todo en un solo documento listo para usar en clase

---

# 🚀 LoadBalancerApiTest

API de ejemplo en **FastAPI** para desplegar en múltiples EC2 detrás de un **Load Balancer (ALB)**.

---

# 📌 PASO A PASO

---

# 🏗️ 1. Arquitectura

-La idea es que desde internet podamos accder a nuestras aplicaciones por medio del Load Balancer

```text
Internet
   ↓
Load Balancer (puerto 80)
   ↓
EC2 (puerto 8000)
```

---

# 🔐 2. Configuración de Seguridad

# Crear grupos de Seguridad .-

## Security Group del Load Balancer

**Este grupo se asociará al momento de crear el Load Balancer**

| Tipo | Puerto | Origen    |
| ---- | ------ | --------- |
| HTTP | 80     | 0.0.0.0/0 |

---

## Security Group de EC2

**Este grupo se asociará en la plantilla de creación de instancias EC2**

| Tipo       | Puerto | Origen               |
| ---------- | ------ | -------------------- |
| SSH        | 22     | TU_IP                |
| Custom TCP | 8000   | SG del Load Balancer |

---

# 🖥️ 3. Crear plantilla de creación de instancias EC2

Usar Maquinas Gratuitas

Dejar como Grupo de seguridad el creado anteriormente

Crear 2 o mas maquinas virtuales

---

# ⚙️ 4. Load Balancer (ALB) Configuraciones

## Listener

* HTTP : 80

## Security Group del Load Balancer

* Al momento de crear el Load Balancer, **asociar el Security Group del Load Balancer**
* Este grupo debe permitir:

| Tipo | Puerto | Origen    |
| ---- | ------ | --------- |
| HTTP | 80     | 0.0.0.0/0 |

---

## Forward

* Target Group / Grupo de desino

Crear Grupo de destino

* Asociar Maquinas Virtales creadas con plantilla de ejecucion

---

# 🎯 5. Target Group

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

# 🛠️ 6. Preparar EC2 (Amazon Linux)

```bash
#!/bin/bash
sudo dnf update -y
sudo dnf install git -y
sudo dnf install python3 -y
sudo dnf install pip -y
sudo dnf install mariadb105 -y
pip install fastapi
pip install "uvicorn[standard]"
pip install gunicorn
pip install pymysql
git clone https://github.com/Elmostunt/LoadBalancerApiTest.git
cd LoadBalancerApiTest
gunicorn -w 3 -k uvicorn.workers.UvicornWorker api:app -b 0.0.0.0:8000

```


---

# 📦 7. Clonar proyecto

```bash
git clone https://github.com/Elmostunt/LoadBalancerApiTest.git
cd LoadBalancerApiTest
```

---

# 🧩 8. Conociendo la API

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

# ▶️ 9. Ejecución local

```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```









---

# ⚙️ 10. Ejecutar API en EC2 (FORMA CORRECTA)

```bash
gunicorn -w 3 -k uvicorn.workers.UvicornWorker api:app -b 0.0.0.0:8000
```

---

# 🌐 11. Probar endpoints

* Healthcheck:
  [http://localhost:8000/health](http://localhost:8000/health)
  http://<DNS>:8000/health

* Hello:
  [http://localhost:8000/hello](http://localhost:8000/hello)
  http://<DNS>:8000/hello

* Swagger:
  [http://localhost:8000/docs](http://localhost:8000/docs)

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

---

# 📈 ANEXO A: Auto Scaling (Escalamiento Automático)

## 🎯 Objetivo

Permitir que las EC2:

* Se creen automáticamente cuando aumenta la carga
* Se eliminen automáticamente cuando baja la carga

---

## 🏗️ 1. Requisito previo

* Load Balancer funcionando
* Target Group creado
* Template de EC2 creado

---

## ⚙️ 2. Crear Auto Scaling Group (ASG)

Ir a AWS → Auto Scaling Groups → Create Auto Scaling Group

### 2.1 Seleccionar plantilla

* Usar la plantilla creada

---

### 2.2 Configurar grupo

* Nombre: `asg-api-test`
* VPC: misma del Load Balancer
* Subnets: al menos 2

---

### 2.3 Asociar al Load Balancer

* Attach to existing load balancer
* Seleccionar Target Group

---

### 2.4 Tamaño del grupo

| Parámetro        | Valor |
| ---------------- | ----- |
| Desired capacity | 2     |
| Minimum          | 2     |
| Maximum          | 4     |

---

## 📊 3. Políticas de escalamiento

Tipo: Target Tracking

* Métrica: CPU
* Target: 60%

---

## ❤️ 4. Health Check

* EC2 + ELB

---

# 🧪 ANEXO B: Pruebas de Carga

## 🎯 Objetivo

* Validar escalamiento
* Simular tráfico real

---



## 🛠️ 1. Herramienta

### Apache JMeter

![Image](https://images.openai.com/static-rsc-4/IbV_hLMCdIj3xAyy_mnjTtBw-560LH2iSGIPraPqbhI1W87O-gbholx-vA5MpBnN7_JEKYCh7aLF6us-bKZL_eCKbrRBAQ7Nb-inaev5iIZHNHY4ba-n4bQ5PkhIpTg51SDDXuXllcjF-VLFi08B7xY21fQARNHxdH6l9YJZJu3wLQNyEkrabJVNLKMUHtB7?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/skYHX4D8P_QoVBoi-OvmUjAdBRt8D7myNeoRieBe2hx-H09cDSKpjAZ0V6HKBSTcBaB5b38QRTXA6OhAIsgpz0LwirOR9trzuCsDUmXV89VV0MPd8jn7Obn2y-7wWQfID1m4-lMwDOtGUEXCvXCyy6zzCijU7odaO9-T7cUmjmGF9IWjJNmV0c2X3K3ruUjV?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/i_EmR1MApnVVdy9a9yTHOossbqRlS414hr401Yt4fZlQ93-skAhhNRsIEd-y0p3kXjeiH2KQEWNPHufLUZeFKHXzRrBLCpT33U2g7ZnylSioLeTPtm_I0Gp1_gX9_tz8_8V8dyDUXRXONsADrmRM6ciXLNgEIMX5HlFwdXnDagvyMW6DczjvkvOrYg9GoxWO?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/iMv6jR-cBDa9Vo-CWQToHkId6uMc1rEUd3plPGL-3xUHVxvU30hquN-qi8h0hT46_F6Z2j90jJ_LisgKDQYuamIYaeiBmEbw54VhtWZSGcwOUlOA58OJW_QAr4YFyRPmTUpFEbDZEVcB4r4n5y0Cmv9z6OKDc72lTb5KBRQl_V0i7rkcKoBSj8trRvY7FAfc?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/imQOYi8wfJ4pZN1RQGWVuTeoPPEYhqKKwvebhBwGs0c5TvHcwuOZs-bAtXzZbR9fPrdynx1nJhq62W6Nr6Ia5774aSzfQHzW0vZA5iXD9rrIOgp3pcWJdTuwYc-3HmJkyW6-6Z58R-heUGvucFCC_gwZh1y9AEv7X0kuPLMhUEoo722rApghIX2PK_djuDq0?purpose=fullsize)

---

## ⚙️ 2. Configuración

* Usuarios: 100–500
* Ramp-up: 10s
* URL:

```
http://<LOAD_BALANCER_DNS>/hello
```

---

## 🚀 3. Ejecutar prueba

Genera carga sobre EC2

---

## 📊 4. Monitoreo

* EC2
* Auto Scaling
* CloudWatch

---

## 🔥 5. Validación esperada

* Se crean nuevas instancias
* No se cae el sistema
* LB distribuye tráfico

---

## 🧠 6. Prueba manual

```bash
for i in {1..1000}; do curl http://<LOAD_BALANCER_DNS>/hello & done
```

---

# 🎯 ANEXO C: Validación final

## ✔️ Deben demostrar

* Acceso por Load Balancer
* Múltiples EC2 activas
* Escalamiento automático
* Endpoint `/health` operativo

---

## ❓ Preguntas de defensa

1. ¿Por qué usar Auto Scaling?
2. ¿Qué métrica escala?
3. ¿Qué hace el Load Balancer?
4. ¿Qué pasa si una instancia falla?
5. ¿Por qué múltiples subredes?
6. Diferencia entre alta disponibilidad y escalabilidad

---
# Detalles sobre escalado automático 

🧠 Politica de Escalado Automático ¿Qué significa esto?

Básicamente le estás diciendo a AWS:

👉 “Mantén la CPU de mis instancias alrededor de X% automáticamente”

En tu caso:

Métrica: Utilización promedio de CPU
Valor de destino: 90%
⚙️ ¿Cómo funciona en la práctica?

AWS va a hacer esto automáticamente:

🔼 Si la CPU sube de 90%

👉 Agrega más instancias (scale out)

🔽 Si la CPU baja de 90%

👉 Elimina instancias (scale in)

📊 Ejemplo real (para que lo uses en clase)

Supongamos que tienes:

2 instancias EC2
CPU promedio = 95%

🔥 AWS detecta que está sobre 90% →
➡️ Lanza una nueva instancia (ahora tienes 3)

Luego:

CPU baja a 40%

🧊 AWS detecta que sobra capacidad →
➡️ Elimina instancias (quizás vuelve a 2)

⏱️ ¿Qué es “Preparación de la instancia (300 segundos)”?

👉 Es el tiempo que AWS espera antes de evaluar si la nueva instancia ya está lista.

300 segundos = 5 minutos
Sirve para evitar que escale demasiado rápido mientras la instancia aún está iniciando
⚠️ Ojo con ese 90% (importante)

Te digo directo:

👉 90% es MUY alto para producción

¿Por qué?

Vas a escalar tarde
Los usuarios pueden sentir lentitud antes de que escale

💡 Recomendado normalmente:

50% – 70% para apps web



Perfecto, tomé tu README base y le agregué lo que te falta para clase: **RDS + conexión desde Python + ejemplo real guardando usuario + scripts SQL**. Te lo dejo ordenado y listo para pegar como continuación del tutorial 👇

---

# 🔥 EXTENSIÓN — Integración con RDS (Base de Datos)

Basado en el tutorial original , ahora vamos a llevarlo a nivel **full backend real**:

👉 API + Load Balancer + Auto Scaling + Base de Datos (RDS)

---

# 🗄️ 14. Crear Base de Datos en RDS (MySQL)

## ⚙️ Paso a paso

1. Ir a **AWS → RDS → Create database**

2. Configuración:

* Engine: **MySQL**
* Version: default
* Template: **Free tier**
* DB Instance Identifier:
  `db-api-test`
* Master username:
  `admin`
* Password:
  `Admin1234!`

---

## 🌐 Conectividad

IMPORTANTE:

* VPC: misma del EC2
* Public access: **YES (solo para pruebas)**
* Security Group: crear uno nuevo

---

## 🔐 Security Group RDS

Agregar regla:

| Tipo  | Puerto | Origen    |
| ----- | ------ | --------- |
| MySQL | 3306   | SG de EC2 |

👉 NO usar 0.0.0.0/0 en producción

---

# 🧱 15. Script SQL (crear tabla)

Conéctate desde EC2:

```bash
sudo dnf install mariadb105 -y
mysql -h <RDS_ENDPOINT> -u admin -p
```

Luego ejecutar:

```sql
CREATE DATABASE api_db;

USE api_db;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    email VARCHAR(100),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

# 🐍 16. Instalar driver MySQL en EC2

```bash
pip install pymysql
```

---

# 🔌 17. Conexión Python a RDS

Editar tu `api.py`:

```python
from fastapi import FastAPI
import pymysql

app = FastAPI()

def get_connection():
    return pymysql.connect(
        host="TU_RDS_ENDPOINT",
        user="admin",
        password="Admin1234!",
        database="api_db",
        cursorclass=pymysql.cursors.DictCursor
    )
```

---

# ➕ 18. Endpoint para guardar usuario

```python
@app.post("/usuarios")
def crear_usuario(nombre: str, email: str):
    connection = get_connection()
    
    with connection:
        with connection.cursor() as cursor:
            sql = "INSERT INTO usuarios (nombre, email) VALUES (%s, %s)"
            cursor.execute(sql, (nombre, email))
        
        connection.commit()
    
    return {
        "message": "Usuario creado correctamente"
    }
```

---

# 📥 19. Endpoint para listar usuarios

```python
@app.get("/usuarios")
def listar_usuarios():
    connection = get_connection()
    
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM usuarios")
            result = cursor.fetchall()
    
    return result
```

---

# 🚀 20. Probar desde navegador / Postman

### Crear usuario:

```
POST http://<LOAD_BALANCER_DNS>/usuarios?nombre=Juan&email=juan@test.com
```

### Listar:

```
GET http://<LOAD_BALANCER_DNS>/usuarios
```

---

# 🧠 21. Flujo completo (para explicar en clase)

```text
Cliente
  ↓
Load Balancer (80)
  ↓
EC2 (FastAPI)
  ↓
RDS (MySQL)
```

---

# ⚠️ Buenas prácticas (dilo en la defensa)

* No hardcodear credenciales → usar variables de entorno
* No abrir RDS a internet
* Usar IAM + Secrets Manager (pro nivel)
* Manejar excepciones en conexión
* Usar pool de conexiones (nivel intermedio-avanzado)

---

# 🧪 BONUS (sube el nivel de la evaluación)

Pídeles esto a los alumnos:

👉 Validar:

* Inserción en DB
* Lectura desde múltiples instancias EC2
* Persistencia (aunque mueran instancias)

👉 Pregunta clave:

> ¿Por qué RDS no se cae aunque EC2 escale?

---

# 💥 Resultado final que logras con esto

Ahora tu laboratorio tiene:

✅ API real
✅ Load Balancer
✅ Auto Scaling
✅ Base de datos persistente
✅ Backend completo estilo producción
