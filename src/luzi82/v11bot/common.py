import pytz, datetime
from dateutil import tz

def to_datetime(time64):
    time_str = datetime.datetime.fromtimestamp(time64)
#    time_str = pytz.timezone('Asia/Tokyo').localize(time_str)
    time_str = time_str.replace(tzinfo=tz.tzlocal())
    time_str = time_str.astimezone(pytz.timezone('Asia/Tokyo'))
    time_str = time_str.isoformat()
    return time_str

def to_datetime_short(time64):
    time_str = datetime.datetime.fromtimestamp(time64)
#    time_str = pytz.timezone('Asia/Tokyo').localize(time_str)
    time_str = time_str.replace(tzinfo=tz.tzlocal())
    time_str = time_str.astimezone(pytz.timezone('Asia/Tokyo'))
    time_str = time_str.strftime('%m-%d %H:%M')
    return time_str

if __name__ == '__main__':
    print (to_datetime(0))
    print (to_datetime_short(0))
    import iso8601
    start_time = '2016-06-15T00:00:00+09:00'
    start_time = iso8601.parse_date(start_time).timestamp()
    print (to_datetime(start_time))
