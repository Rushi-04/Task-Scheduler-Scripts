from datetime import datetime, timedelta


def today_yymmdd():
    return datetime.now().strftime("%y%m%d")


WEEKDAY_MAP = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6
}


def is_task_due(schedule):
    """
    Returns (True/False, reason)
    """

    now = datetime.now()
    today_idx = now.weekday()

    days = schedule["days"]
    time_str = schedule["time"]

    #  Day check
    if "daily" not in days:
        valid_days = [WEEKDAY_MAP[d.lower()] for d in days]
        if today_idx not in valid_days:
            return False, "Today is not a scheduled day"

    #  Time check (+1 hour rule)
    task_time = datetime.strptime(time_str, "%H:%M").time()
    scheduled_dt = now.replace(
        hour=task_time.hour,
        minute=task_time.minute,
        second=0,
        microsecond=0
    )

    if now < scheduled_dt + timedelta(hours=1):
        return False, "Scheduled time + 1 hour not reached"

    return True, "Task is due"
