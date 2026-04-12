from aiohttp import web
import asyncio

# Не лучшая практика - глобальная переменная для подключения, но для демо сойдет
connection_pool = None


async def read_root(request):
    return web.json_response({"Hello": "World"})


async def slow_endpoint(request):
    # Имитация медленной I/O-задачи (например, сетевой запрос)
    await asyncio.sleep(0.1)  # Асинхронная задержка
    return web.json_response({"message": "This was a slow request"})


async def high_cpu_endpoint(request):
    # Функция, которая нагружает ЦПУ
    def cpu_intensive_task():
        total = 0
        for i in range(10_000_000):
            total += i
        return total

    result = await asyncio.to_thread(
        cpu_intensive_task
    )  # Выполнение в отдельном потоке
    return web.json_response({"message": f"CPU task completed with result: {result}"})


async def database_endpoint(request):
    # Имитация запроса к базе данных (I/O-задержка)
    await asyncio.sleep(0.05)  # Симуляция времени запроса к БД
    return web.json_response(
        {"message": "Database query result", "data": {"users": 100, "active": 50}}
    )


app = web.Application()
app.router.add_get("/", read_root)
app.router.add_get("/slow_endpoint", slow_endpoint)
app.router.add_get("/high_cpu_endpoint", high_cpu_endpoint)
app.router.add_get("/database_endpoint", database_endpoint)

if __name__ == "__main__":
    web.run_app(app, host="127.0.0.1", port=8000)
