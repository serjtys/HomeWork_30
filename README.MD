# Online Education Platform

Django REST Framework приложение для онлайн-обучения с курсами, уроками, платежами через Stripe и системой подписок.

## 📋 Основные функции

- **Управление курсами и уроками** - создание, редактирование, просмотр
- **Система подписок** - подписка/отписка на обновления курсов
- **Платежная система** - интеграция с Stripe для оплаты курсов
- **JWT аутентификация** - безопасный вход по email
- **Роли пользователей** - владельцы, модераторы, обычные пользователи
- **Уведомления** - автоматические уведомления при обновлении курсов
- **Фоновые задачи** - Celery для обработки фоновых процессов
- **Периодические задачи** - Celery Beat для регулярных уведомлений

## 🛠 Технологии

- **Backend**: Django 4.2, Django REST Framework
- **База данных**: PostgreSQL
- **Кэширование**: Redis
- **Асинхронные задачи**: Celery, Celery Beat
- **Платежи**: Stripe API
- **Документация API**: Swagger/DRF-YASG
- **Аутентификация**: JWT Tokens
- **Контейнеризация**: Docker, Docker Compose

## 🚀 Запуск с Docker Compose

### Предварительные требования
- Docker
- Docker Compose

### Быстрый старт

1. **Клонируйте репозиторий и перейдите в папку проекта**

2. **Настройте переменные окружения:**
```bash
cp .env.example .env
``` 

Отредактируйте .env файл, указав:

    *Секретный ключ Django*

    Данные для PostgreSQL

    Ключи Stripe API

    Настройки email

    Запустите все сервисы:
```bash
docker compose up -d --build

    Создайте суперпользователя:
```
bash

docker compose exec backend python manage.py createsuperuser

### 📊 Проверка работоспособности

    Главная страница: http://localhost:8000

    Админ-панель: http://localhost:8000/admin

    API документация: http://localhost:8000/swagger/

    Redoc документация: http://localhost:8000/redoc/

### Проверка сервисов:

```bash
# Статус всех контейнеров
docker compose ps

# Логи приложения
docker compose logs backend -f

# Проверка базы данных
docker compose exec db psql -U your-database-user -d your-database-name -c "SELECT version();"

# Проверка Redis
docker compose exec redis redis-cli ping

# Проверка Celery
docker compose logs celery -f
```

### 💻 Локальная разработка (без Docker)

# Активируйте виртуальное окружение:

```bash

python -m venv venv
source venv/bin/activate
```
# Установите зависимости:

```bash

pip install -r requirements.txt
```
# Настройте базу данных PostgreSQL и Redis

    Примените миграции:

```bash

python manage.py migrate
```

    Создайте суперпользователя:

```bash

python manage.py createsuperuser
```

    Запустите сервер:

```bash

python manage.py runserver
```

    Запустите Celery worker (в отдельном терминале):

```bash

celery -A config worker --loglevel=info
```

    Запустите Celery beat (в отдельном терминале):

```bash

celery -A config beat --loglevel=info
```

### 📚 API Endpoints
# Аутентификация

    POST /api/users/register/ - Регистрация пользователя

    POST /api/users/token/ - Получение JWT токена

# Пользователи

    GET /api/users/ - Список пользователей

    GET/PUT/PATCH /api/users/{id}/ - Профиль пользователя

# Курсы

    GET /api/courses/ - Список курсов

    POST /api/courses/ - Создание курса (только владельцы)

    GET/PUT/PATCH /api/courses/{id}/ - Детали курса

    DELETE /api/courses/{id}/ - Удаление курса (только владельцы)

# Уроки

    GET /api/lessons/ - Список уроков

    POST /api/lessons/ - Создание урока (только владельцы)

    GET/PUT/PATCH /api/lessons/{id}/ - Детали урока

    DELETE /api/lessons/{id}/ - Удаление урока (только владельцы)

# Подписки

    POST /api/subscriptions/ - Подписка/отписка на курс

# Платежи

    POST /api/payments/create/ - Создание платежной сессии Stripe

    GET /api/payment/success/ - Страница успешной оплаты

    GET /api/payment/cancel/ - Страница отмены оплаты

## 🗄 Модели данных
# Пользователи (User)

    Email (уникальный), телефон, город, аватар

    Кастомный менеджер пользователей

# Курсы (Course)

    Название, описание, превью, цена

    Владелец, даты создания/обновления

# Уроки (Lesson)

    Название, описание, превью, ссылка на видео

    Привязка к курсу, владелец

# Подписки (Subscription)

    Связь пользователь-курс

    Автоматические уведомления при обновлениях

# Платежи (Payment)

    Интеграция с Stripe

    История транзакций

### 🔧 Управление
## Docker команды
```bash

# Запуск
docker compose up -d --build

# Остановка
docker compose down

# Просмотр логов
docker compose logs -f [service_name]

# Выполнение команд в контейнере
docker compose exec backend python manage.py [command]
```

## Django команды
```bash

# Миграции
python manage.py makemigrations
python manage.py migrate

# Создание суперпользователя
python manage.py createsuperuser

# Сбор статики
python manage.py collectstatic

# Запуск тестов
python manage.py test
```

### 📝 Примечания

    Для работы платежей нужны действительные ключи Stripe

    Email уведомления настроены для вывода в консоль (для тестирования)

    Модераторы могут редактировать все курсы, но не создавать/удалять

    Владельцы имеют полный контроль над своими курсами и уроками

### 🐛 Поиск проблем

# Если возникают проблемы с запуском:

    Проверьте что все переменные в .env заполнены правильно

    Убедитесь что порты 8000, 5432, 6379 свободны

    Проверьте логи: docker compose logs -f

    Убедитесь что Docker запущен: docker --version

## 🚀 Инструкция по деплою

### Настройка сервера (Ubuntu 20.04+)

1. **Обновление системы:**
```bash
sudo apt update && sudo apt upgrade -y
```
    Установка базовых пакетов:

```bash

sudo apt install -y python3-pip python3-venv nginx postgresql postgresql-contrib redis-server git
```
    Настройка PostgreSQL:

```bash

sudo -u postgres psql -c "CREATE DATABASE myapp_db;"
sudo -u postgres psql -c "CREATE USER myapp_user WITH PASSWORD 'your_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE myapp_db TO myapp_user;"
```
    Настройка firewall:

```bash

sudo ufw allow 'OpenSSH'
sudo ufw allow 'Nginx Full'
sudo ufw enable
```
Настройка GitHub Actions

    Добавьте secrets в репозитории:

    SERVER_IP - IP вашего сервера

    SSH_USER - пользователь для подключения (например, ubuntu)

    SSH_KEY - приватный SSH-ключ

    DJANGO_SECRET_KEY - секретный ключ Django

    DJANGO_DEBUG - False

    DJANGO_ALLOWED_HOSTS - ваш IP или домен

    При пуше в ветку develop автоматически:

    Запускаются тесты

    Происходит деплой на сервер

    Приложение перезапускается

Проверка работоспособности

После деплоя приложение доступно по IP сервера:
```bash

curl http://your-server-ip
```
Логи и мониторинг

Просмотр логов приложения:
```bash

sudo journalctl -u myapp -f
```
Просмотр логов Nginx:
```bash

sudo tail -f /var/log/nginx/error.log
```
Статус сервисов:
```bash

sudo systemctl status myapp
sudo systemctl status nginx
sudo systemctl status redis
```

## Деплой

Приложение развернуто по адресу: http://51.250.20.114:8000

### Инструкция по настройке сервера:
1. Создать ВМ в Яндекс Облаке
2. Установить Python, nginx, настроить firewall
3. Настроить systemd сервис для автоматического запуска
4. Добавить SSH-ключ в настройки ВМ

### Инструкция по деплою:
1. При пуше в ветку develop запускается GitHub Actions workflow
2. Проходят автоматические тесты
3. После успешных тестов происходит деплой на сервер
4. Приложение автоматически перезапускается