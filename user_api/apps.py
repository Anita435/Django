from django.apps import AppConfig


class AppApiConfig(AppConfig):
    name = 'user_api'

    verbose_name = "User"

    def ready(self):
        try:
            from .signals import log_user_logged_in_failed, log_user_logged_in_success
        except ImportError as e:
            print(e)
