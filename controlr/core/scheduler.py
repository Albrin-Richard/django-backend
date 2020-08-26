from apscheduler.schedulers.background import BackgroundScheduler

timer_sched = BackgroundScheduler(daemon=True)
schedule_sched = BackgroundScheduler(daemon=True)

timer_sched.add_jobstore(
    'redis',
    jobs_key='controlr.timer.jobs',
    run_times_key='controlr.timer.run_times'
)

schedule_sched.add_jobstore(
    'redis',
    jobs_key='controlr.schedule.jobs',
    run_times_key='controlr.schedule.run_times'
)


def init_schedulers():
    print('Schedulers started')
    timer_sched.start()
    schedule_sched.start()
