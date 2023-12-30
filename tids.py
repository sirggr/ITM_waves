# -*- coding: utf-8 -*-
"""Quick and simple view of TIDS in DE2 data."""

import matplotlib.pyplot as plt
import numpy as np
import pysat
from funcs import calculate_delta
from manual_sorting import manual_sort


def plot_orbits(doy: int, user_examine: bool, path: str):
    orbit_info = {'index': 'OrbitNumber', 'kind': 'orbit'}

    lang = pysat.Instrument('de2', 'lang', use_header=True, strict_time_flag=False, orbit_info=orbit_info)
    lang.custom_attach(calculate_delta, kwargs={'labels': ['plasmaDensity'], 'normalize': True})

    nacs = pysat.Instrument('de2', 'nacs', use_header=True, strict_time_flag=False, orbit_info=orbit_info)
    nacs.custom_attach(calculate_delta, kwargs={'labels': ['O_density', 'N2_density', 'Ar_density'], 'normalize': True})

    rpa = pysat.Instrument('de2', 'rpa', use_header=True, strict_time_flag=False)
    rpa.custom_attach(calculate_delta, kwargs={'labels': ['ionDensity'], 'normalize': True})
    rpa.custom_attach(calculate_delta, kwargs={'labels': ['x', 'y', 'z'], 'normalize': False})
    lang.load(1983, doy)
    rpa.load(1983, doy)
    nacs.load(1983, doy)

    orbits = np.unique(lang['OrbitNumber'])
    plt.close('all')
    for orbit in orbits:
        # Choose orbit number and low altitudes
        ind = (nacs['OrbitNumber'] == orbit) * (nacs['alt'] < 400)
        if sum(ind) > 100:
            t0 = nacs.index[ind][0]
            t1 = nacs.index[ind][-1]

            fig = plt.figure(figsize=[14, 6])
            plt.plot(lang['delta_plasmaDensity_norm'][t0:t1], '--',
                     label='LANG: delta Ne')
            plt.plot(rpa['delta_ionDensity_norm'][t0:t1], '--',
                     label='RPA: delta Ni')
            plt.plot(nacs['delta_O_density_norm'][t0:t1], label='NACS: delta O')
            plt.plot(nacs['delta_N2_density_norm'][t0:t1], label='NACS: delta N2')
            # plt.plot(nacs['delta_Ar_density_norm'][t0:t1], label='NACS: delta Ar')
            plt.legend()
            plt.grid()
            plt.ylim([-0.5, 0.5])

            plt.ylabel('Relative change (normalized)')
            plt.title('DE2 -- {:}/{:}/{:} -- Orbit {:}'.format(t0.date().year,
                                                               t0.date().month,
                                                               t0.date().day,
                                                               orbit))
            if user_examine:
                img_src = path + "\\" + str(t0.date().year) + "_" + str(doy) + "_" + str(orbit) + "_" + "plot.jpg"
                plt.savefig(img_src)
                manual_sort(source=img_src)
            else:
                plt.show()





