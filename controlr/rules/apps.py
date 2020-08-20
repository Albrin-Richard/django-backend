from django.apps import AppConfig

from apscheduler.schedulers.background import BackgroundScheduler

timer_schedule = BackgroundScheduler(daemon=True)
schedule_schedule = BackgroundScheduler(daemon=True)


def init_schedulers():
    print('Schedulers started')
    timer_schedule.start()
    schedule_schedule.start()


class RulesConfig(AppConfig):
    name = 'controlr.rules'

    def ready(self):
        init_schedulers()
