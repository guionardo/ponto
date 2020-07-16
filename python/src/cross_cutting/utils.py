from datetime import datetime, timedelta


def now_as_timedelta() -> timedelta:
    return timedelta(hours=datetime.now().hour,
                     minutes=datetime.now().minute)
