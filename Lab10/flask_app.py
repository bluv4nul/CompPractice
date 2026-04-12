from flask import Flask
import time
import threading

app = Flask(__name__)

# Не лучшая практика - глобальная переменная для подключения, но для демо сойдет
connection_pool = None


@app.route("/")
def read_root():
    return {"Hello": "World"}


@app.route("/slow_endpoint")
def slow_endpoint():
    # Имитация медленной I/O-задачи (например, сетевой запрос)
    time.sleep(0.1)  # Синхронная задержка
    return {"message": "This was a slow request"}


@app.route("/high_cpu_endpoint")
def high_cpu_endpoint():
    # Функция, которая нагружает ЦПУ
    def cpu_intensive_task():
        total = 0
        for i in range(10_000_000):
            total += i
        return total

    result = cpu_intensive_task()  # Выполнение в том же потоке (блокирует)
    return {"message": f"CPU task completed with result: {result}"}


@app.route("/database_endpoint")
def database_endpoint():
    # Имитация запроса к базе данных (I/O-задержка)
    time.sleep(0.05)  # Симуляция времени запроса к БД
    return {"message": "Database query result", "data": {"users": 100, "active": 50}}


if __name__ == "__main__":
    app.run(debug=True)
