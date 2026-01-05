# Todo List API

REST API для управления задачами (Todo List) с аутентификацией через OAuth2/OpenID Connect.

## Публикация

- **API**: https://todo-api-production-f779.up.railway.app/docs
- **SSO (OAuth2 провайдер)**: https://server-production-5c965.up.railway.app

## Тестовые пользователи

Для тестирования API можно использовать следующие тестовые учетные записи:

| Логин | Пароль |
|-------|--------|
| `test` | `Altatestuser1!` |
| `test-1` | `Altatestuser1!` |

## Требования

- Python 3.12+
- PostgreSQL 15+
- pip

## Установка

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd web-api
```

### 2. Создание виртуального окружения

```bash
python -m venv venv
```

### 3. Активация виртуального окружения

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Установка зависимостей

```bash
make install
```

или

```bash
pip install -r requirements.txt
```

### 5. Настройка переменных окружения

Создайте файл `.env` в корне проекта на основе `.env.example`:

```bash
cp .env.example .env
```

Откройте файл `.env` и настройте переменные окружения:

```env
# База данных
TODO_DB_URL=postgresql://user:password@localhost:5432/todo_db

# OAuth2/OpenID Connect
AUTH_URL=https://server-production-5c965.up.railway.app
```

Пример для локальной разработки:
```env
TODO_DB_URL=postgresql://postgres:postgres@localhost:5432/todo_db
AUTH_URL=https://server-production-5c965.up.railway.app
```

## Запуск приложения

### Применение миграций

Перед первым запуском примените миграции базы данных:

```bash
make update
```

или

```bash
alembic upgrade head
```

### Запуск сервера

```bash
make run
```

или

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Приложение будет доступно по адресу: `http://localhost:8000`

## Аутентификация

API использует OAuth2/OpenID Connect с PKCE (Proof Key for Code Exchange).

### Получение токена через Swagger UI

1. Откройте Swagger UI: `http://localhost:8000/docs`
2. Нажмите кнопку **"Authorize"**
3. Введите `client_id` (если требуется)
4. Выполните авторизацию через OAuth2 провайдер
5. После успешной авторизации токен будет автоматически добавлен в заголовки запросов

### Использование токена

Добавьте заголовок в запросы:

```
Authorization: Bearer <your_access_token>
```

## Миграции базы данных

### Создание новой миграции

```bash
make migrate MESSAGE="описание изменений"
```

или

```bash
alembic revision --autogenerate -m "описание изменений"
```

### Применение миграций

```bash
make update
```

или

```bash
alembic upgrade head
```

### Откат миграции

```bash
make downgrade
```

или

```bash
alembic downgrade -1
```

## Доступные команды

- `make install` - установить зависимости
- `make run` - запустить API локально
- `make migrate MESSAGE="..."` - создать миграцию
- `make update` - применить миграции
- `make downgrade` - откатить миграцию
- `make build` - собрать Docker образы
- `make up` - запустить контейнеры
- `make down` - остановить контейнеры
- `make logs` - показать логи контейнеров
- `make help` - показать все доступные команды

## Структура проекта

```
web-api/
├── app/
│   ├── core/           # Основные модули (settings, security, handlers)
│   ├── entities/       # Модели базы данных
│   ├── features/       # Функциональные модули (todo)
│   └── main.py         # Точка входа приложения
├── alembicl/           # Миграции Alembic
├── requirements.txt    # Зависимости Python
├── Makefile           # Команды для разработки
└── README.md          # Документация
```

## Разработка

### Локальная разработка

1. Убедитесь, что PostgreSQL запущен и доступен
2. Создайте базу данных: `CREATE DATABASE todo_db;`
3. Создайте файл `.env` на основе `.env.example` и настройте `TODO_DB_URL`
4. Примените миграции: `make update`
5. Запустите сервер: `make run`

## Лицензия

Проект создан в учебных целях, но буду рад помощи и коллективной разработке!
