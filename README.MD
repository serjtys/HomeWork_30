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
- **Веб-сервер**: Nginx

## 🚀 Запуск с Docker Compose

### Предварительные требования
- Docker
- Docker Compose

### Быстрый старт

1. **Клонируйте репозиторий и перейдите в папку проекта**

```bash
https://github.com/serjtys/HomeWork_30.git
``` 

2. **Настройте переменные окружения:**

```bash
cp .env.example .env
``` 

3. **Отредактируйте .env файл, указав:**

    SECRET_KEY - Секретный ключ Django

    DB_NAME, DB_USER, DB_PASSWORD - Данные для PostgreSQL

    REDIS_URL - Адрес Redis

    STRIPE_API_KEY - Ключи Stripe API

    ALLOWED_HOSTS - Домены для доступа (через запятую)

4. **Запустите все сервисы:**

```bash
docker compose up -d --build
```    

5. **Выполните миграции и создайте суперпользователя:**

```bash
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py createsuperuser
```

6. **Соберите статические файлы:**

```bash
docker compose exec backend python manage.py collectstatic --noinput
```

### 📊 Проверка работоспособности

    Главная страница: http://localhost

    Админ-панель: http://localhost/admin

    API документация: http://localhost/swagger/

    Redoc документация: http://localhost/redoc/

### Проверка сервисов:

```bash
# Статус всех контейнеров
docker compose ps

# Логи приложения
docker compose logs backend -f

# Логи Nginx
docker compose logs nginx -f

# Проверка базы данных
docker compose exec db psql -U ${DB_USER} -d ${DB_NAME} -c "SELECT version();"

# Проверка Redis
docker compose exec redis redis-cli ping

# Проверка Celery
docker compose logs celery -f
```

###🏗 Архитектура Docker

#Сервисы:

    backend - Django приложение

    db - PostgreSQL база данных

    redis - Redis для кэширования и Celery

    celery - Celery worker для фоновых задач

    celery_beat - Celery beat для периодических задач

    nginx - Веб-сервер и reverse proxy


###🔧 Управление

#Docker команды

```bash

# Запуск
docker compose up -d --build

# Остановка
docker compose down

# Остановка с удалением volumes
docker compose down -v

# Просмотр логов
docker compose logs -f [service_name]

# Выполнение команд в контейнере
docker compose exec backend python manage.py [command]

# Пересборка конкретного сервиса
docker compose build backend
```

#Django команды

```bash

# Миграции
docker compose exec backend python manage.py makemigrations
docker compose exec backend python manage.py migrate

# Создание суперпользователя
docker compose exec backend python manage.py createsuperuser

# Сбор статики
docker compose exec backend python manage.py collectstatic --noinput

# Запуск тестов
docker compose exec backend python manage.py test
```

### 💻 Локальная разработка (без Docker)

1. **Активируйте виртуальное окружение:**

```bash

python -m venv venv
source venv/bin/activate
```
2. **Установите зависимости:**

```bash

pip install -r requirements.txt
```
3. **Настройте базу данных PostgreSQL и Redis**

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


### 🔄 CI/CD Pipeline

#GitHub Actions Workflow

**При пуше в ветки develop или homework-35.2 автоматически запускается:**

    Тестирование - запуск unit-тестов Django

    Сборка Docker - проверка сборки всех образов

    Деплой - автоматический деплой на сервер через Docker Compose

#Настройка Secrets в GitHub

**Для работы CI/CD необходимо добавить в настройках репозитория:**

    SERVER_IP - IP адрес сервера

    SSH_USER - пользователь для SSH (например, ubuntu)

    SSH_KEY - приватный SSH ключ для доступа к серверу

    DJANGO_SECRET_KEY - секретный ключ Django

    DJANGO_DEBUG - False для продакшена

    DJANGO_ALLOWED_HOSTS - домен или IP сервера


###🚀 Деплой на сервер
#Настройка сервера (Ubuntu 20.04+)

**Обновление системы и установка Docker:**

```bash

sudo apt update && sudo apt upgrade -y
sudo apt install -y docker.io docker-compose-v2 git
sudo systemctl enable docker
sudo systemctl start docker
```
    
**Настройка firewall:**

```bash

sudo ufw allow OpenSSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable
```

**Добавление пользователя в группу docker:**

```bash

sudo usermod -aG docker $USER
# Перелогиньтесь или выполните:
newgrp docker
```

**Автоматический деплой через GitHub Actions**

При пуше в ветку develop:

    Запускаются тесты

    Собираются Docker образы

    Происходит деплой на сервер через SSH

    На сервере выполняются команды:
```bash
git pull origin develop
docker compose down
docker compose up -d --build
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py collectstatic --noinput
```

#Ручной деплой на сервер

    Клонирование репозитория:

```bash

git clone https://github.com/your-username/your-repo.git /home/ubuntu/app
cd /home/ubuntu/app
```
    Настройка переменных окружения:

```bash

cp .env.example .env
nano .env  # Отредактируйте настройки
```
    Запуск приложения:

```bash

docker compose up -d --build
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py collectstatic --noinput
docker compose exec backend python manage.py createsuperuser
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

### 🌐Деплой

Приложение развернуто по адресу: http://51.250.20.114:8000

## Инструкция по настройке сервера:
1. Создать ВМ в Яндекс Облаке
2. Установить Docker и Docker Compose
3. Настроить firewall (открыть порты 80, 443, 22)
4. Добавить SSH-ключ в настройки ВМ

### Инструкция по деплою:
1. При пуше в ветку develop запускается GitHub Actions workflow
2. Проходят автоматические тесты и сборка Docker образов
3. После успешных проверок происходит деплой на сервер через Docker Compose
4. Приложение автоматически перезапускается в контейнерах