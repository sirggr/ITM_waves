import pysat

import pysatNASA

from pysatNASA.instruments.methods import de2

# Define params in dt.datetime format
def download_range(start, stop):
    

    # Download data
    nacs = pysat.Instrument('de2', 'nacs')
    nacs.download(start, stop)
    rpa = pysat.Instrument('de2', 'rpa')
    rpa.download(start, stop)
    lang = pysat.Instrument('de2', 'lang')
    lang.download(start, stop)
