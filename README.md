## Установка

git clone <репозиторий>
cd barter_system
virtualenv virt
cd virt/Scripts/activate
pip install -r requirements.txt

В базе данных уже есть два пользователя
1. Логин:admin Пароль:admin
2. Логин:test Пароль:test12345678

## Миграции и запуск сервера

python manage.py makemigrations
python manage.py migrate
python manage.py runserver

### HTML-интерфейс
`/` — список объявлений
`/create/` — создание объявления
`/proposal/` — создание предложения
`/proposals/` - список предложений

### REST API
`/api/ads/` — API для объявлений
`/api/proposals/` — API для предложений обмена
`/api-token-auth/` — получение токена с помощью 'POST'

## Технологии
Django 4+
Django REST Framework
SQLite
