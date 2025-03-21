# Usa una imagen de Python
FROM python:3.9

# Define el directorio de trabajo
WORKDIR /app

# Copia los archivos al contenedor
COPY requirements.txt ./
COPY main.py ./

# Instala las dependencias
RUN pip install -r requirements.txt

# Expone el puerto
EXPOSE 8080

# Comando para ejecutar la app usando gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "main:app"]
