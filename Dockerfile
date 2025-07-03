FROM python:3.11-slim

# Evitar prompts interactivos al instalar
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Instala dependencias del sistema mínimas
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copia archivos de proyecto
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Puerto interno (opcional)
EXPOSE 5002

CMD ["python", "app.py"]
