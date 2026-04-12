from fastapi import FastAPI, HTTPException
import asyncio  # Для асинхронных операций

app = FastAPI()

# Не лучшая практика - глобальная переменная для подключения, но для демо сойдет
connection_pool = None


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/slow_endpoint")
async def slow_endpoint():
    # Имитация медленной I/O-задачи (например, сетевой запрос)
    await asyncio.sleep(0.1)  # Асинхронная задержка, не блокирует event loop
    return {"message": "This was a slow request"}


@app.get("/high_cpu_endpoint")
async def high_cpu_endpoint():
    # Функция, которая нагружает ЦПУ
    def cpu_intensive_task():
        total = 0
        for i in range(10_000_000):
            total += i
        return total

    result = await asyncio.to_thread(
        cpu_intensive_task
    )  # Выполнение в отдельном потоке
    return {"message": f"CPU task completed with result: {result}"}


@app.get("/database_endpoint")
async def database_endpoint():
    # Имитация запроса к базе данных (I/O-задержка)
    await asyncio.sleep(0.05)  # Симуляция времени запроса к БД
    return {"message": "Database query result", "data": {"users": 100, "active": 50}}
