from django.apps import AppConfig
from .scheduler import init_schedulers


class CoreConfig(AppConfig):
    name = 'controlr.core'

    def ready(self):
        import os
        if os.environ.get('RUN_MAIN'):
            init_schedulers()
