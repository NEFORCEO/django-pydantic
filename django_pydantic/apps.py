from __future__ import annotations

from django.apps import AppConfig

_MIDDLEWARE_PATH = "django_pydantic.middleware.PydanticValidationMiddleware"


class DjangoPydanticConfig(AppConfig):
    """AppConfig for django_pydantic.

    Automatically injects ``PydanticValidationMiddleware`` into
    ``settings.MIDDLEWARE`` at startup so the user does not have to add it
    manually. The middleware is appended at the end; if you need a specific
    position, add it manually and this code will skip the auto-injection.
    """

    name = "django_pydantic"
    label = "django_pydantic"
    default_auto_field = "django.db.models.BigAutoField"
    default = True

    def ready(self) -> None:
        self._inject_middleware()

    def _inject_middleware(self) -> None:
        """Append PydanticValidationMiddleware to MIDDLEWARE if not present."""
        from django.conf import settings

        if not hasattr(settings, "MIDDLEWARE"):
            return

        if _MIDDLEWARE_PATH in settings.MIDDLEWARE:
            return

        if isinstance(settings.MIDDLEWARE, list):
            settings.MIDDLEWARE.append(_MIDDLEWARE_PATH)
        elif isinstance(settings.MIDDLEWARE, tuple):
            settings.MIDDLEWARE = settings.MIDDLEWARE + (_MIDDLEWARE_PATH,)
