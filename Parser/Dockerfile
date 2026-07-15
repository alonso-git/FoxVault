FROM python:3.11-slim

# Le decimos a Docker en qué carpeta de su sistema interno vamos a trabajar
WORKDIR /app

# Copiamos SOLO el archivo de dependencias primero (truco para caché de Docker)
COPY requirements.txt .

# Instalamos las dependencias GLOBALMENTE en el contenedor (sin venv)
RUN pip install --no-cache-dir -r requirements.txt

# Ahora copiamos todo tu código (main.py, models.py, etc.)
COPY . .

# Exponemos el puerto para que sepamos por dónde habla la app
EXPOSE 8000

# El comando que arranca tu FastAPI (Ojo: 0.0.0.0 es crucial en Docker)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]