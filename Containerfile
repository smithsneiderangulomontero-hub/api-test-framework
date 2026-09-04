FROM python:3.12-slim

WORKDIR /app

# Copiamos solo requirements.txt primero (no requirements-dev.txt: la imagen
# de producción/SUT no necesita pytest, black, ruff...). Esto también
# aprovecha la cache de capas de Podman: si el código cambia pero las
# dependencias no, no se reinstalan.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

EXPOSE 8000

# --host 0.0.0.0 es obligatorio: sin esto, uvicorn solo escucha en
# localhost DENTRO del contenedor y el mapeo de puertos (-p) no llega.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
