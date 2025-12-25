from django.apps import AppConfig

class AdminPanelConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "admin_panel"

    def ready(self):
        # ensure any imports that register signals can run here later
        pass
