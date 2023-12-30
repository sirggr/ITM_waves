import pysat

import pysatNASA

import datetime as dt

from pysatNASA.instruments.methods import de2

# Define date range to download data
start = dt.datetime(1983, 1, 1)
stop = dt.datetime(1983, 3, 15)

# Download data
nacs = pysat.Instrument('de2', 'nacs')
nacs.download(start, stop)
rpa = pysat.Instrument('de2', 'rpa')
rpa.download(start, stop)
lang = pysat.Instrument('de2', 'lang')
lang.download(start, stop)
