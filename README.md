# Django Video Hosting

Учебный проект видеохостинга, реализованный на Django + Django REST Framework с использованием Docker и PostgreSQL.

---

## 📌 Описание

Проект предоставляет REST API для работы с видеоконтентом:

- создание и хранение видео
- загрузка файлов разных качеств (HD / FHD / UHD)
- система лайков
- управление пользователями
- административная панель Django

---

## ⚙️ Технологии

- Python 3.14
- Django
- Django REST Framework
- PostgreSQL
- Docker / Docker Compose
- UV (dependency manager)

---

## 🧱 Сущности

### Video
- владелец (User)
- название
- статус публикации
- количество лайков
- дата создания

### VideoFile
- файл видео
- качество (HD / FHD / UHD)
- связь с Video

### Like
- пользователь
- видео
- уникальность (1 пользователь = 1 лайк)

---

## 🚀 Запуск проекта

### 1. Клонировать репозиторий

```bash
git clone https://github.com/ChaRoodey/django_videohosting
cd django_videohosting
```

### 2. Создать .env
```bash
POSTGRES_DB=video_hosting_db
POSTGRES_USER=video_hosting_user
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
```

### 3. Запуск через Docker
```bash
docker compose up --build
```
### 📡 API

#### Базовый URL:

```bash
http://localhost:8000/api/
```

#### Примеры эндпоинтов:

- GET /v1/videos/ — список видео
- GET /v1/videos/{id}/ — детали видео
- POST /v1/videos/{id}/likes/ — поставить лайк
- GET /v1/videos/ids/ — список ID опубликованных видео
- GET /v1/videos/statistics-subquery/ — статистика через Subquery
- GET /v1/videos/statistics-group-by/ — статистика через GROUP BY

### 🧪 Тестовые данные

Есть management command:
```bash
uv run python manage.py generate_data
```
Генерирует пользователей(10k), видео(100k), лайки(rand 1-20 per video)