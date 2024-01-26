from scipy import fftpack
import pandas as pd
from tids import series_lists


def compare_attributes(year: int, doy: int, attr1: str, attr2: str):
    list1 = series_lists(year=year, doy=doy, attr=attr1)
    list2 = series_lists(year=year, doy=doy, attr=attr2)
    if len(list1) != len(list2):
        raise ValueError
    for i in range(len(list1)):
        series1 = list1[i].values
        series2 = list2[i].values
        f1 = fftpack.fftfreq(len(series1))
        f2 = fftpack.fftfreq(len(series2))

        # Calculate the phase shifts
        phase_shifts = np.angle(f1) - np.angle(f2)

        # Detect antiparallel waves (180 degree phase shift)
        antiparallel = np.isclose(phase_shifts, np.pi, atol=0.01)  # adjust tolerance as needed

        print("Antiparallel waves detected at indices:", np.where(antiparallel))
