# Запуск приложения в Docker
- Собрать образ:
```
docker compose build
```
- Выполнить команду:
```
docker compose up -d
```
- Документация XML сервиса доступна по адресу: http://localhost:8000/openapi/swagger

# Используемые технологии
- Python 3.12
- Flask
- Flask OpenAPI3
- SQLite
- SQLAlchemy
- Docker

# Описание
- XML сервис реализует JSON API для необходимых функций
- Добавлена OpenAPI Swagger документация
- Все эндпоинты имеют описание схем запросов, ответов и статус кодов
- Запросы и ответы валидируются Pydantic
- Проект упакован в Докер контейнер
- Код использует аннотации типов (mypy --strict)
