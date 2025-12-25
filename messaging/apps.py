from django.apps import AppConfig

class MessagingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "messaging"

    def ready(self):
        # import receivers so signals are connected
        from . import signals  # noqa: F401
