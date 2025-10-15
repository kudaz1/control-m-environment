# Dockerfile para desplegar la API Control-M

FROM python:3.9-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivo de requisitos
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY api_control_m.py .

# Exponer el puerto 5000
EXPOSE 5000

# Comando para ejecutar la aplicación con gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "api_control_m:app"]


