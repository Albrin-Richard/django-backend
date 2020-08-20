from django.apps import AppConfig

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime


class CoreConfig(AppConfig):
    name = 'controlr.core'
