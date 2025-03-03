# Tradings FastAPI

Web-сервис для развертки своего маркетплейса с блекджеком и всем остальным.

___

### ВВЕДЕНИЕ

Tradings - это веб-приложение, которое является серверной частью маркетплейса. Оно позволяет регистрироваться одновременно и как покупатель, и как продавец. Таким образом размываются рамки между условными Avi** и Ozo**, и получается нечто универсальное, прекрасное и удобное.

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

Tradings разработан с использованием следующих технологий:

- [Python] (v.3.12) - целевой язык программирования backend
- [FastAPI] (v.0.111) - высокоуровневый асинхронный веб-фреймворк
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

1) Склонировать репозиторий

```
git clone git@github.com:TheSuncatcher222/tradings_fastapi.git
```

2) Создать .env файл по шаблону

```
cp app/src/config/.env.example app/src/config/.env
```

[опционально] настроить .env согласно комментариям

```
nano app/src/config/.env
```

3) Запустить Docker Compose сборку (убедитесь, что `docker daemon` запущен в системе!)

- prod build:

```
git checkout main
docker compose -f docker/docker-compose.yml --env-file app/src/config/.env up -d
```

4) Проверить доступность API по ссылке на документацию:

```
http://localhost:8000/api/v1/swagger/
```

### РАЗРАБОТКА

❗️ ВНИМАНИЕ: некоторые библиотеки проекта не поддерживают Python выше 12 версии❗️

1) Перейти в корень проекта (где находится README.md) и выполнить команды (на примере Windows):

```
py -3.12 -m venv .venv &&
source .venv/scripts/activate &&
python -m pip install --upgrade pip &&
pip install -r app/requirements.txt &&
pre-commit install
```

2) Подключение к БД:

- Перейти в PG Admin:

```
http://localhost:5050/browser/
```

- Использовать логин и пароль из .env:

```
PGADMIN_DEFAULT_EMAIL=admin@email.com
PGADMIN_DEFAULT_PASSWORD=admin
```

- Нажать "Servers" (ПКМ) -> "Register" -> "Server..."

```
"Name" = "tradings"
"Host name/address" = "tradings-postgresql" (DB_HOST в .env)
"Username" = "db_user" (POSTGRES_USER в .env)
"Password" = "db_pass" (POSTGRES_PASSWORD в .env)
"Save password?" = "yes"
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
