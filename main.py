import datetime as dt
from download_data import download_range

start = dt.datetime(1983, 1, 1)
stop = dt.datetime(1983, 3, 15)
download_range(start, stop)

