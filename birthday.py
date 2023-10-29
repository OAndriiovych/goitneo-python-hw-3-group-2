from datetime import datetime, timedelta
from collections import defaultdict


def get_birthdays_per_week(date):
    now = datetime.now()
    next_monday = now + timedelta(7 - now.weekday())
    next_sunday = next_monday + timedelta(6)

    return [i for i in date if next_monday <= get_next_bd(i["birthday"]) <= next_sunday]


def get_next_bd(bd: datetime):
    now = datetime.now()
    year = now.year
    if now.month == 12 and bd.month == 1:
        year = now.year + 1
    return datetime(year, bd.month, bd.day)


def print_birthdays_per_week(date):
    users_with_new_year = [{
        "birthday": get_next_bd(x["birthday"].date),
        "name": k}
        for k, x in date.items() if x["birthday"] is not None]

    now = datetime.now()
    next_monday = now + timedelta(7 - now.weekday())
    next_sunday = next_monday + timedelta(6)
    users_with_bd_on_the_next_week = {u["name"]: u["birthday"].strftime('%A')
                                      for u in users_with_new_year if
                                      next_monday <= u["birthday"] <= next_sunday}

    grouped_users_by_day = defaultdict(list)
    for key, val in users_with_bd_on_the_next_week.items():
        if val == "Sunday" or val == "Saturday":
            val = "Monday"
        grouped_users_by_day[val].append(key)

    for x, y in grouped_users_by_day.items():
        print(x + ": " + ", ".join(y))
