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
