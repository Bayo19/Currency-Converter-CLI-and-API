FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/app"

COPY common /app/src


CMD ["uvicorn", "app.src.API.main:app", "--host", "0.0.0.0", "--port", "80"]
