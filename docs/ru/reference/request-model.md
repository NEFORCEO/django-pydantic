# RequestModel

```python
from django_pydantic import RequestModel
```

Подкласс `pydantic.BaseModel`, который можно создать напрямую из Django `HttpRequest`.

---

## Класс: RequestModel

**Наследует:** `pydantic.BaseModel`

### Создание объекта

#### `MySchema(request, **kwargs)`

```python
data = MySchema(request)
data = MySchema(request, pk=pk)   # объединить с URL kwargs
```

**Параметры:**

| Параметр | Тип | Описание |
|----------|-----|---------|
| `request` | `django.http.HttpRequest` | Текущий запрос. Данные извлекаются автоматически. |
| `**kwargs` | `Any` | Дополнительные пары ключ-значение с наивысшим приоритетом (path-параметры URL). |

**Возвращает:** Валидированный экземпляр `MySchema`.

**Бросает:** `pydantic.ValidationError` при ошибке валидации. Автоустановленный middleware конвертирует это в HTTP 422.

---

#### `MySchema(field=value, ...)`

Стандартное создание объекта Pydantic по-прежнему работает:

```python
data = MySchema(username="alice", email="alice@example.com")
```

---

### Классовые методы

#### `MySchema._extract(request, **kwargs) → dict`

Переопредели этот classmethod для кастомизации способа извлечения данных из запроса. По умолчанию вызывает `django_pydantic.request.extract_data`.

```python
class MySchema(RequestModel):
    @classmethod
    def _extract(cls, request, **extra):
        from django_pydantic.request import extract_data
        data = extract_data(request, **extra)
        data["user_id"] = request.user.pk   # инжектируем доп. поля
        return data
```

---

### Унаследовано от BaseModel

Все стандартные методы Pydantic доступны:

| Метод | Описание |
|-------|---------|
| `model_dump(**kw)` | Сериализация в `dict` |
| `model_dump_json(**kw)` | Сериализация в JSON-строку |
| `model_copy(**kw)` | Копия с опциональным переопределением полей |
| `model_fields_set` | Множество явно переданных полей |
| `model_validate(data)` | Классовый метод — валидировать из dict |
| `model_json_schema()` | Вернуть JSON Schema dict |

---

## Функция: extract_data

```python
from django_pydantic.request import extract_data
```

```python
def extract_data(request: HttpRequest, **extra: Any) -> dict
```

Строит плоский `dict` из Django `HttpRequest` путём объединения:

1. GET query parameters (`request.GET`)
2. JSON тело (при `Content-Type: application/json`)  
   — ИЛИ — POST form data (для не-GET/HEAD/OPTIONS/DELETE)
3. `**extra` keyword-аргументы (наивысший приоритет)

**Параметры:**

| Параметр | Тип | Описание |
|----------|-----|---------|
| `request` | `HttpRequest` | Объект Django-запроса |
| `**extra` | `Any` | Доп. поля, объединяемые последними (например, path-параметры URL) |

**Возвращает:** `dict`, готовый для `pydantic.BaseModel.model_validate`.

---

## Класс: PydanticValidationMiddleware

```python
from django_pydantic.middleware import PydanticValidationMiddleware
```

Django middleware, перехватывающий `pydantic.ValidationError` при обработке запроса и возвращающий структурированный 422 JSON-ответ.

**Устанавливается автоматически**, когда `django_pydantic` есть в `INSTALLED_APPS`. Добавлять вручную в `settings.MIDDLEWARE` не нужно.

### Формат ответа

```json
{
  "detail": [
    {
      "type":  "string",
      "loc":   ["field_name"],
      "msg":   "string",
      "input": "any"
    }
  ]
}
```

### Ручная установка

Если нужно контролировать порядок middleware — добавь явно, и авто-вставка пропустится:

```python title="settings.py"
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django_pydantic.middleware.PydanticValidationMiddleware",  # (1)!
    ...
]
```

1. django-pydantic-client проверяет наличие и пропускает авто-вставку.
