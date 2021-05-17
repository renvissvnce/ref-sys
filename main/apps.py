from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'


class AuthenticationConfig(AppConfig):
    name = 'authentication'
