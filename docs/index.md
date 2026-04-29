---
hide:
  - navigation
  - toc
---

<div class="dp-hero">
  <div class="dp-badge-row">
    <span class="dp-badge dp-badge-django">Django 4.2+</span>
    <span class="dp-badge dp-badge-pydantic">Pydantic v2</span>
    <span class="dp-badge dp-badge-python">Python 3.10+</span>
  </div>

  <div class="dp-wordmark">
    <svg class="dp-wordmark-icon" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect width="48" height="48" rx="12" fill="#44B78B"/>
      <path d="M14 24 C14 18 18 14 24 14 C30 14 34 18 34 24 C34 30 30 34 24 34" stroke="white" stroke-width="3" stroke-linecap="round"/>
      <circle cx="24" cy="24" r="3" fill="white"/>
      <path d="M24 34 L20 30 M24 34 L28 30" stroke="white" stroke-width="2.5" stroke-linecap="round"/>
    </svg>
    <span class="dp-wordmark-text">django-pydantic</span>
  </div>

  <p class="dp-tagline">
    Skip the serializer. Validate Django requests<br>with Pydantic models — one line, zero boilerplate.
  </p>
  <div class="dp-install">
    <span class="dp-install-prompt">$</span>
    <span class="dp-install-cmd">pip install django-pydantic</span>
  </div>
  <div class="dp-buttons">
    <a href="en/tutorial/first-steps/" class="dp-btn dp-btn-primary">Get Started</a>
    <a href="ru/tutorial/first-steps/" class="dp-btn dp-btn-secondary">Начать на русском</a>
    <a href="en/reference/request-model/" class="dp-btn dp-btn-ghost">API Reference</a>
  </div>
</div>

<div class="dp-features">

  <div class="dp-feature">
    <div class="dp-feature-icon">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
      </svg>
    </div>
    <h3>One-line validation</h3>
    <p>Pass the Django request directly to your Pydantic model. No manual parsing, no <code>request.data</code>, no boilerplate.</p>
  </div>

  <div class="dp-feature">
    <div class="dp-feature-icon">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
        <path d="M9 12l2 2 4-4"/>
      </svg>
    </div>
    <h3>Automatic 422 errors</h3>
    <p>Validation failures return structured JSON error responses automatically. No try/except needed in your views.</p>
  </div>

  <div class="dp-feature">
    <div class="dp-feature-icon">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="3"/>
        <path d="M19.07 4.93a10 10 0 0 1 0 14.14M4.93 4.93a10 10 0 0 0 0 14.14"/>
        <path d="M12 1v3M12 20v3M4.22 4.22l2.12 2.12M17.66 17.66l2.12 2.12M1 12h3M20 12h3M4.22 19.78l2.12-2.12M17.66 6.34l2.12-2.12"/>
      </svg>
    </div>
    <h3>Zero configuration</h3>
    <p>Add <code>django_pydantic</code> to <code>INSTALLED_APPS</code>. The middleware registers itself. Nothing else required.</p>
  </div>

  <div class="dp-feature">
    <div class="dp-feature-icon">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="16 18 22 12 16 6"/>
        <polyline points="8 6 2 12 8 18"/>
      </svg>
    </div>
    <h3>Full Pydantic v2 power</h3>
    <p>All validators, <code>Field()</code> constraints, <code>model_config</code>, computed fields, and custom types work as-is.</p>
  </div>

  <div class="dp-feature">
    <div class="dp-feature-icon">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="18" cy="18" r="3"/>
        <circle cx="6" cy="6" r="3"/>
        <circle cx="6" cy="18" r="3"/>
        <path d="M6 9v6M18 15V9A6 6 0 0 0 12 3H9"/>
      </svg>
    </div>
    <h3>Merges all data sources</h3>
    <p>GET params, POST form data, JSON body, and URL path parameters — merged transparently into one validated object.</p>
  </div>

  <div class="dp-feature">
    <div class="dp-feature-icon">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <polygon points="12 2 2 7 12 12 22 7 12 2"/>
        <polyline points="2 17 12 22 22 17"/>
        <polyline points="2 12 12 17 22 12"/>
      </svg>
    </div>
    <h3>Works with CBVs too</h3>
    <p>Fully compatible with Django class-based views and Django REST Framework. Drop it into any existing project.</p>
  </div>

</div>

## The idea in 30 seconds

<div class="dp-compare">
  <div class="dp-compare-col dp-compare-old">
    <div class="dp-compare-header">
      <svg class="dp-compare-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M18 6L6 18M6 6l12 12"/></svg>
      Without django-pydantic
    </div>

```python
def signup(request):
    import json
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "bad json"}, status=400)

    username = body.get("username")
    email    = body.get("email")
    age      = body.get("age")

    if not username:
        return JsonResponse({"error": "username required"}, status=400)
    if not email or "@" not in email:
        return JsonResponse({"error": "bad email"}, status=400)
    if not isinstance(age, int) or age < 0:
        return JsonResponse({"error": "bad age"}, status=400)

    # finally do something useful
```

  </div>
  <div class="dp-compare-col dp-compare-new">
    <div class="dp-compare-header">
      <svg class="dp-compare-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg>
      With django-pydantic
    </div>

```python
# schema.py
from pydantic import EmailStr, Field
from django_pydantic import RequestModel

class SignupSchema(RequestModel):
    username: str
    email: EmailStr
    age: int = Field(ge=0)

# views.py
def signup(request):
    data = SignupSchema(request)
    # data.username, data.email, data.age
    # all validated, typed, ready to use
```

  </div>
</div>

## Quick example

=== "schema.py"

    ```python
    from pydantic import BaseModel, EmailStr, Field
    from django_pydantic import RequestModel

    class SignupSchema(RequestModel):
        username: str = Field(min_length=3, max_length=32)
        email: EmailStr
        age: int = Field(ge=18)
    ```

=== "views.py"

    ```python
    from django.http import JsonResponse
    from .schema import SignupSchema

    def signup(request):
        data = SignupSchema(request)  # (1)!
        # User.objects.create(...)
        return JsonResponse({"username": data.username})
    ```

    1.  Accepts JSON body, POST form data, or GET query params.
        Returns HTTP **422** with structured errors on failure — automatically.

=== "Error response"

    ```json
    {
      "detail": [
        {
          "type": "missing",
          "loc": ["username"],
          "msg": "Field required"
        },
        {
          "type": "value_error",
          "loc": ["email"],
          "msg": "value is not a valid email address"
        }
      ]
    }
    ```

=== "settings.py"

    ```python
    INSTALLED_APPS = [
        ...
        "django_pydantic",  # that's all
    ]
    ```
