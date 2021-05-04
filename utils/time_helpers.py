from datetime import datetime
# pytz = python time zone
import pytz


def utc_now():
    return datetime.now().replace(tzinfo=pytz.utc)