<div id="header" align="center">
  <img src="https://media.giphy.com/media/h408T6Y5GfmXBKW62l/giphy.gif" width="200"/>
</div>

<div id="badges" align="center">
  <a href="https://t.me/devil_on_the_wheel">
    <img src="https://img.shields.io/badge/telegram-26A5E4?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram Badge"/>
  </a>
  <a href="https://wa.me/+79117488008">
    <img src="https://img.shields.io/badge/whatsapp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" alt="Telegram Badge"/>
  </a>
  <a href="https://www.linkedin.com/in/igor526/">
    <img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn Badge"/>
  </a>
  <a href="igor-526@yandex.ru">
    <img src="https://img.shields.io/badge/email-orange?style=for-the-badge&logo=mail.ru&logoColor=white" alt="LinkedIn Badge"/>
  </a>
</div>

<div id="view_counter" align="center">
  <img src="https://komarev.com/ghpvc/?username=igor-526&color=blue&style=for-the-badge&label=Просмотры"/>
</div>

---

*Универсальный backend для организации работы конюшни*

## Основной функционал
- **Администрирование пользователей**
- **JWT авторизация**
- **Добавление | удаление | изменение лошадей**
- **Добавление | удаление | изменение родителей и детей лошадей**
- **Подробная документация**
- **Генерация рандомных лошадей**

## Технологический стек

| Тип       | Технологии                                             |
|-----------|--------------------------------------------------------|
| **Языки** | ![python](https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white) |
| **Backend** | [![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/) [![REST API](https://img.shields.io/badge/REST_API-FF6C37?style=for-the-badge&logo=fastapi&logoColor=white)](https://www.django-rest-framework.org/) |
| **База данных** | ![postgresql](https://img.shields.io/badge/postgresql-4169E1?style=for-the-badge&logo=postgresql&logoColor=white) |
| **Инфраструктура** | [![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/) [![Docker Compose](https://img.shields.io/badge/Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/) |
| **Стиль кода** | [![PEP8](https://img.shields.io/badge/PEP8-794013?style=for-the-badge)](https://www.docker.com/) |

## 🚀 Запуск проекта

### 1. Клонирование проекта
```bash
git clone https://github.com/igor-526/EqUniAPI
cd EqUniAPI
```

### 2. Настройка окружения

Создайте файл `.env` в корне проекта на основе примера `example.env`:

```ini
# ========================
# Настройки Django
# ========================
DJANGO_SETTINGS_MODULE='equestrian.settings'    # путь к настройкам
DJANGO_SECRET_KEY='django-insecure'             # Секретный ключ Django
DJANGO_DEBUG="1"                                # режим Debug ("" для production)
DJANGO_ALLOWED_HOST="*"                         # домен/IP
DB_HOST=eq_database                             # хост БД
DB_PORT=5432                                    # порт БД
GUNICORN_PORT=5050                              # порт для открытия Gunicorn

# ========================
# Настройки проекта
# ========================
ALLOW_DOCUMENTATION="1"                         # доступ к документации ("" для закрытия)
ACCESS_TOKEN_LIFETIME_HOURS=23                  # количество часов жизни access токена
REFRESH_TOKEN_LIFETIME_DAYS=30                  # количество дней жизни refresh токена

# ========================
# Настройки БД
# ========================
DB_DB=eq_development                            # Имя БД
DB_USER=eq_development                          # Имя пользователя
DB_PASSWORD=eq_development                      # Пароль БД
DB_PORT_FORWARD=5436                            # Порт для внешних подключений
```

### 4. Запуск
```bash
docker compose up -d
```

### 5. Создание пользователя
```bash
docker compose exec eq_django bash
uv run python manage.py createsuperuser

*Следуйте инструкциям

exit
```

### 6. Создание лошадей (при необходимости)
```bash
docker compose exec eq_django bash
uv run python manage.py generate_horse -c 100   # -c --count : количество фейковых лошадей
exit
```

## Документация API
Документация будет доступна при переходе на **{host}/doc/** после запуска проекта.

Проверьте параметр **ALLOW_DOCUMENTATION** в .env файле
