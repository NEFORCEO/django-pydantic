# API Справочник

| Символ | Описание |
|--------|---------|
| [`RequestModel`](request-model.md) | Базовый класс для Pydantic-моделей с валидацией запроса |
| `PydanticValidationMiddleware` | Автоустанавливаемый middleware; конвертирует `ValidationError` → 422 |
| `extract_data(request, **extra)` | Хелпер, строящий словарь данных из запроса |
