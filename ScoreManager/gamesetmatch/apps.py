from django.apps import AppConfig


class GamesetmatchConfig(AppConfig):
    name = 'gamesetmatch'

    def ready(self):
        import gamesetmatch.signals