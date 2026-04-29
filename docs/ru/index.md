<p align="center">
  <img src="https://raw.githubusercontent.com/NEFORCEO/django-pydantic/master/docs/static/logo.svg" alt="django-pydantic-client" width="520">
</p>

# django-pydantic-client

**django-pydantic-client** позволяет заменить ручной парсинг запросов на Pydantic-модели. Передай Django `HttpRequest` напрямую в схему — получи валидированный типизированный объект или автоматический HTTP 422, если данные невалидны.

## Возможности

- **Одна строка** — `data = MySchema(request)`
- **Автоматические ответы об ошибках** — middleware конвертирует `ValidationError` в `422 JSON`
- **Умное слияние данных** — GET-параметры + POST/JSON тело + kwargs URL — всё в одном объекте
- **Нулевая конфигурация** — middleware устанавливается автоматически через `INSTALLED_APPS`
- **Весь Pydantic v2** — валидаторы, `Field()`, кастомные типы, `model_config`

## Требования

| Зависимость | Версия |
|-------------|--------|
| Python      | ≥ 3.10 |
| Django      | ≥ 4.2  |
| Pydantic    | ≥ 2.0  |

## Установка

```bash
pip install django-pydantic-client
```

```python title="settings.py"
INSTALLED_APPS = [
    ...
    "django_pydantic",
]
```

Всё. Готово к использованию.

## Что дальше

- [**Туториал → Первые шаги**](tutorial/first-steps.md) — создай первую валидированную вьюху
- [**Туториал → Схема запроса**](tutorial/request-schema.md) — как работает `RequestModel` изнутри
- [**API Справочник**](reference/request-model.md) — полный справочник `RequestModel`
