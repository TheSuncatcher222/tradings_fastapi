# Tradings FastAPI

Web-сервис для развертки своего маркетплейса с блекджеком и всем остальным.

___

### ВВЕДЕНИЕ

Tradings - это веб-приложение, которое является серверной частью маркетплейса. Оно позволяет регистрироваться одновременно и как покупатель, и как продавец. Таким образом размываются рамки между условными Avi** и Ozo**, и получается нечно единое, прекрасное и удобное.

___

### ОПИСАНИЕ

Миссия Tradings - предоставить максимально удобный и доступный сервис как для покупателей, так и для продавцов, максимально размывая границы между этими ролями.

Для покупателей:
- ⚡️ быстрое оформление заказа
- 🕑 регистрация заявок 24/7
- 🔄 возможность просмотра и повтора заказов в несколько кликов
- 🫶 забота

Для продавцов:
- 💷 прозрачное ценообразования
- 🚦 автоматическое оформление заказа
- 📊 емкая статистика заказов, охватывающая каждый их аспект
- 📅 управление скидками, рассылками
- 🌎 продажи по всему миру

___

### ТЕХНОЛОГИИ

CleanPRO разработан с использованием следующих технологий:

- [Python] (v.3.11) - целевой язык программирования backend
- [FastAPI] (v.0.109) - высокоуровневый асинхронный веб-фреймворк
- [Alembic] (v.1.13) - инструмент для миграций базы данных для SQLAlchemy
- [SQLAlchemy] (v.2.0) - SQL ORM реляционный преобразователь объектов
- [PostgreSQL] (v.13.10) - объектно-реляционная база данных
- [Celery] (v.5.3) - распределенная очередь задач
- [Redis] (v.5.0) - резидентная система управления NoSQL базами данных, брокер сообщений Celery
- [Uvicorn] (v.0.27) - Python ASGI HTTP-сервер для UNIX
- [Nginx] - HTTP-сервер и обратный прокси-сервер
- [Docker] (v.24.0) - инструмент для автоматизирования процессов разработки, доставки и запуска приложений в контейнерах

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Celery](https://a11ybadges.com/badge?logo=celery)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

___

### РАЗВЕРТКА

✅ Загрузить актуальную версию проекта

```
git clone git@github.com:TheSuncatcher222/tradings_fastapi.git
```

✅ Перейти в папку app

```
cd app
```

✅ Создать файл переменных окружения из примера

```
cp .env.example .env
```

✅ Изменить переменные окружения (если необходимо)
```
(на примере редактора Nano)
nano .env
```

✅ Перейти в корневую папку backend
```
cd ..
```

✅ Запустить Docker (убедитесь, что `docker daemon` запущен в системе!)

```
docker-compose up --build
```

✅ Проверить доступность проекта на `localhost:80`

```
http://localhost:8000/
```

___

### ЛИЦЕНЗИЯ

MIT

**Ура, халява!**

[Python]: <https://www.python.org/>
[FastAPI]: <https://fastapi.tiangolo.com/>
[Alembic]: <https://alembic.sqlalchemy.org/en/latest/>
[SQLAlchemy]: <https://www.sqlalchemy.org/>
[PostgreSQL]: <https://www.postgresql.org/>
[Celery]: <https://docs.celeryq.dev/en/stable/>
[Redis]: <https://redis.io/>
[PyJWT]: <https://pyjwt.readthedocs.io/en/latest/>
[Uvicorn]: <https://www.uvicorn.org/>
[Nginx]: <https://nginx.org/en/>
[Docker]: <https://www.docker.com/>
