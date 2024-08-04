from django.apps import AppConfig


class ImageAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "image_app"

    def ready(self):
        import image_app.signals  # noqa: F401
