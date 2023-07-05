from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = "backend.core"
    verbose_name = "Core"

    def ready(self):
        try:
            import backend.core.signals  # noqa F401
        except ImportError:
            pass
