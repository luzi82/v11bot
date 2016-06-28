import pytz, datetime

def to_datetime(time64):
    time_str = datetime.datetime.fromtimestamp(time64)
    time_str = pytz.timezone('Asia/Tokyo').localize(time_str)
    time_str = time_str.isoformat()
    return time_str