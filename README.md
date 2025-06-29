# Задание на экзамен (Вариант 2: "Блог-платформа")

## Описание проекта и его функционала
"Блог платформа" - веб API для реализации функций блога-платформы.
Позволяет просматривать статьи и информацию о них, оставлять лайки и комментарии под статьями, а также создавать статьи авторам.
## Используемые технологии и их версии
  Основные технологии: FastAPI, SqlAlchemy, Pydantic. Полный список используемые библиотек можно найти в файле api/requirements.txt.
## Инструкция по запуску
> Все действия по запуску должны происходить в терминале. Перед запуском необходимо перейти в папку **api**, через терминал:
> ```cd api```

**1. Создание виртуального окружения**
```
py -m venv venv
```
**2. Активация виртуального окружения**
```
venv/Scripts/activate
```
**3. Установка библиотек**
```
pip install -r requirements.txt
```
**4. Посев**
```
py seed.py
```
**5. Запуск**
```
fastapi dev
```
**6. Тестирование**

Перейдите по адресу `http://127.0.0.1:8000/docs` в браузере. Откроется интерфейс Swagger для удобного тестирования.
## Описание API
Тип API - REST API. Все эндпоинты API задокументировани при помощи Swagger. Чтобы перейти к документации пройдите по адресу `http://127.0.0.1:8000/docs` запустив проект.
## Описание валидации к ключевым эндпоинтам
Все схемы данных и их валидация описаны в документации Swagger.
Все маршруты, изменяющие данные, защищены через JWT авторизацию.
## Описание ролей пользователей и их прав
Роли:
- Читатель (reader) - просмотр статей, оставление лайков и комментариев.
- Автор (author) - создание статей, те же действия что может делать Читатель
- Админ (admin) - управление всеми сущностями
Посев содержит пользователей всех ролей (таблица ниже).

Username | Пароль | Роль
--- | --- | ---
user1 | 123 | reader
user2 | 234 | author
user3 | 345 | admin

Чтобы авторизоваться используйте эндпоинт авторизации `/api/token` в документации Swagger и введите данные авторизации.

Токен действителен в течении 200 минут.
## Контакты

Ермолин Артем, студент НТИ (филиал УРФУ), группы Т-323901-НТ.

Email: `artem.ermolin04@mail.ru`
