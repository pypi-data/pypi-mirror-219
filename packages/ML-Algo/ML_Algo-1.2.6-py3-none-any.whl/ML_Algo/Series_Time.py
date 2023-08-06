from datetime import datetime, timedelta

def get_previous_weekday_dates():
    current_date = datetime.now().date()
    weekday = current_date.weekday()

    previous_dates = []
    i = 1
    while len(previous_dates) < 3:
        delta = timedelta(days=i)
        previous_date = current_date - delta
        if previous_date.weekday() == weekday:
            previous_dates.append(previous_date.strftime("%d-%m-%Y"))
        i += 1

    # Inserting today's date at index 0
    today_date = current_date.strftime("%d-%m-%Y")
    previous_dates.insert(0, today_date)

    return previous_dates

def calculate_completed_intervals(n):
    current_time = datetime.now().time()
    total_minutes = current_time.hour * 60 + current_time.minute
    completed_intervals = total_minutes // n

    return completed_intervals