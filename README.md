# lms-django

**lms-django** — это web-платформа для управления обучающими курсами и пользователями, написанная на Django.

## Функционал

- Кастомная модель пользователя (`users.User`)
- Приложение для курсов и уроков (`materials`)
- Админ-панель
- Совместимость с Django 4.x / 5.x

## Требования

- Python 3.10+
- pip
- Django 4 или выше (указано в requirements.txt)
- Virtualenv (рекомендуется)

## Быстрый запуск

1. **Клонируйте репозиторий:**
    bash
    git clone https://github.com/ваш-юзернейм/lms-django.git
    cd lms-django


2. **Создайте и активируйте виртуальное окружение:**
    bash
    python3 -m venv venv
    source venv/bin/activate


3. **Установите зависимости:**
    bash
    pip install -r requirements.txt


4. **Примените миграции:**
    bash
    python manage.py migrate


5. **Создайте суперпользователя:**
    bash
    python manage.py createsuperuser


6. **Запустите сервер:**
    bash
    python manage.py runserver


7. **Зайдите в админку:**
    Откройте http://127.0.0.1:8000/admin/ в браузере.

## Структура проекта

\`\`\`
lms-django/
│
├── lms/              # Конфигурация проекта
├── users/            # Приложение пользователей (кастомная модель User)
├── materials/        # Приложение: курсы и уроки
├── manage.py
├── requirements.txt
└── README.md
\`\`\`

## ENV Переменные

В файле `.env` (или в settings.py) убедитесь, что настроены переменные:
- \`SECRET_KEY\`
- \`DEBUG\`
- \`DATABASES\`

## Полезные команды

- **Создать новое приложение:**  
  \`python manage.py startapp <appname>\`
- **Создать миграции:**  
  \`python manage.py makemigrations\`
- **Применить миграции:**  
  \`python manage.py migrate\`
- **Создать суперпользователя:**  
  \`python manage.py createsuperuser\`

## Лицензия

MIT (или ваша)