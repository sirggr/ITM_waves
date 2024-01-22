# -*- coding: utf-8 -*-
"""Quick and simple view of TIDS in DE2 data."""

import matplotlib.pyplot as plt
import numpy as np
import pysat
from funcs import calculate_delta


def plot_doy(doy: int, classify: bool, train: bool):
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
    if classify:
        img_id = doy - 1
        label_list = []
        id_list = []
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
            if classify:
                label_list.append(classify_image(train=train, img_id=img_id))
                id_list.append(img_id)
                img_id += 1
            else:
                plt.show()
    if classify:
        return [label_list, id_list]


def classify_image(train: bool, img_id: int):
    img_name = str(img_id) + ".jpg"
    if train:
        img_path = 'train/' + img_name
    else:
        img_path = 'test/' + img_name
    plt.show()
    label = input('Enter 1 if the image contains waves, 0 otherwise: ')
    if label != 0 & label != 1:
        print("Invalid input")
        return classify_image()
    plt.savefig(img_path)
    print("Image saved as " + img_path)
    return label







