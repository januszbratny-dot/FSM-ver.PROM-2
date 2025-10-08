from datetime import datetime

def get_time_range(day, start_time, end_time):
    date = datetime.combine(day, start_time)
    end = datetime.combine(day, end_time)
    return date, end
