def get_minutes_from_td(timedelta):
    return timedelta.days * 1440 + timedelta.seconds/60


def get_total_minutes(time_period):
    switch = {
        'minute': 1,
        'hour': 60,
        'day': 1440,
        'week': 10080,
        'month': 43800,
        'year': 525600
    }

    return switch.get(time_period)
