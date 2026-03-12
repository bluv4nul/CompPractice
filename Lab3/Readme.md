# Отправка запросов

api - api.weather.gov

## Netcat

команда - ncat --ssl api.weather.gov 443

### GET

Запрос:
```
GET /points/39.7456,-97.0892 HTTP/1.1
Host: api.weather.gov
User-Agent: test
```

Ответ сервера:
![alt text](image.png)
И еще много информации


### POST

Запрос:
```
POST / HTTP/1.1
Host: api.weather.gov
User-Agent: test
Content-Length: 0
```
Ответ сервера:
![alt text](image-1.png)

## Curl

### GET

```
curl -v https://api.weather.gov/points/39.7456,-97.0892
```

![alt text](image-2.png)

### POST

```
curl -v https://api.weather.gov/points/39.7456,-97.0892 -d "123"
```

![alt text](image-3.png)

## Postman + API Центробанк

![alt text](image-4.png)

## Чат

![alt text](image-5.png)