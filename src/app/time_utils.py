from machine import Pin
import ntptime
import utime as time
from .ds1302 import DS1302


def time_set():
    ntptime.settime()
    now = time.time() + 19800
    t = time.localtime(now)
    year, month, mday, hour, minute, second, weekday, yearday  = t
    ds = DS1302(Pin(5),Pin(18),Pin(19))
    ds.date_time([year, month, mday, weekday, hour, minute, second])

def time_get():
    ds = DS1302(Pin(5),Pin(18),Pin(19))
    return ds



