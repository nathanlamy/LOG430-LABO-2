FROM python:3.11

WORKDIR /app

RUN apt-get update && apt-get install -y postgresql-client

COPY ./app /app/app
COPY ./web /app/web
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "web/app.py"]
