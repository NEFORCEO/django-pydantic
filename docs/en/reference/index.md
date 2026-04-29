# API Reference

| Symbol | Description |
|--------|-------------|
| [`RequestModel`](request-model.md) | Base class for request-validated Pydantic models |
| `PydanticValidationMiddleware` | Auto-installed middleware; converts `ValidationError` → 422 |
| `extract_data(request, **extra)` | Helper that builds the data dict from a request |
