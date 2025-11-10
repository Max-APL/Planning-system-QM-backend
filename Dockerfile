# Imagen base de Python
FROM python:3.11

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código del backend
COPY . .

# Exponer el puerto 8000 (FastAPI)
EXPOSE 8000

# Comando para iniciar FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
