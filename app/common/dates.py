from datetime import datetime, timedelta


def first_day_of_current_month():
    today = datetime.today()
    return today.replace(day=1)


def first_day_of_next_month():
    next_month = datetime.today().replace(day=28) + timedelta(days=4)
    return next_month.replace(day=1)
