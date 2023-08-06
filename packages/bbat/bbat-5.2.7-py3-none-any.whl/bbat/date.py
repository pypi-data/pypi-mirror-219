import time
import datetime

def time_to_str(timestamp=None, format="%Y-%m-%d %H:%M:%S"):
    '''
    Args 
        f - %Y-%m-%d %H:%M:%S 格式化时间
    '''
    if timestamp:
        ts = datetime.datetime.fromtimestamp(timestamp)
    else:
        ts = datetime.datetime.now()
    formatted = ts.strftime(format)
    return formatted

def str_to_time(date, format="%Y-%m-%d %H:%M:%S"):
    '''
    Args:
        str_date - 字符时间
        f - 默认 %Y-%m-%d %H:%M:%S '''
    return datetime.datetime.strptime(date, format)


def timestamp():
    return time.time()

def date_diff(fmt='%Y-%m-%d %H:%M:%S', start_date=None, **kwargs):
    """
    Args:
        start_date: datetime.datetime.today()
        days: float = ...,
        seconds: float = ...,
        microseconds: float = ...,
        milliseconds: float = ...,
        minutes: float = ...,
        hours: float = ...,
        weeks
    """
    if start_date is None:
        start_date = datetime.datetime.now()

    if isinstance(start_date, (str, int)):
        start_date = datetime.datetime.strptime(str(start_date), fmt)

    date = start_date - datetime.timedelta(**kwargs)
    return date.strftime(fmt)