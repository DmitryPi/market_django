from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = "backend.users"
    verbose_name = "Пользователи"

    def ready(self):
        try:
            import backend.users.signals  # noqa F401
        except ImportError:
            pass
