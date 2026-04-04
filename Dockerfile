# Usamos una imagen de Python oficial y ligera
FROM python:3.10-slim

# Instalamos dependencias del sistema necesarias para compilar el driver de MariaDB
RUN apt-get update && apt-get install -y \
    gcc \
    libmariadb-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Definimos el directorio donde vivirá el código dentro del contenedor
WORKDIR /app

# Copiamos primero los requerimientos para aprovechar el sistema de capas de Docker (caché)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el contenido de tu proyecto al contenedor
COPY . .

# El puerto por defecto que usa Flask
EXPOSE 5000

# Comando para iniciar la aplicación en modo desarrollo
CMD ["python", "run.py"]