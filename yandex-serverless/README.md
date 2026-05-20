# Лабораторная работа 12. Yandex Serverless Applicatios

## Шаг 1. Установка SourceCraft Code Assistant для VS code

![alt text](./pics/sourceCraft.png)

![alt text](./pics/sourceCraft-site.png)

## Шаг 2. Установка MCP-плагин Yandex Cloud Toolkit а также Yandex Cloud Containers:

![alt text](./pics/toolkit.png)

![alt text](./pics/containers.png)

## Шаг 3. Создание файла main.py и requirements.txt

```python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/login")
def login():
    return {"author": "1155288"}


@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Лабораторная работа</title>
    </head>
    <body>
        <h1>Лабораторная работа: Yandex Serverless Applications</h1>

        <p>В ходе лабораторной работы был установлен и настроен SourceCraft Code Assistant в VS Code.</p>
        <p>Также были подключены MCP-серверы Yandex Cloud Toolkit и Yandex Cloud Containers.</p>
        <p>Для работы с облаком был установлен и настроен Yandex Cloud CLI.</p>
        <p>Разработано веб-приложение на FastAPI с маршрутом /login.</p>
        <p>Приложение подготовлено к развёртыванию в Yandex Serverless Containers.</p>
    </body>
    </html>
    """
```

## Шаг 4. Написание Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

## Шаг 5. Сборка проекта с помощью SourceCraft Assistant

https://bbaq5cb94tsg9aun9k5o.containers.yandexcloud.net/