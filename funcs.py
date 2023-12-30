"""Functions to support tid tracker."""


def calculate_delta(inst, labels, normalize=False):
    """Calculate the deltas for a list of labels.

    Parameters
    ----------
    inst : pysat.Instrument()
        The instrument to attach this function to.
    labels : listlike
        list of labels to calculate delta for
    """

    for label in labels:
        mean_label = '_'.join(('mean', label))
        delta_label = '_'.join(('delta', label))
        norm_label = '_'.join(('delta', label, 'norm'))

        inst[mean_label] = inst[label].rolling(window=60, center=True).mean()
        inst[delta_label] = inst[label] - inst[mean_label]

        if normalize:
            inst[norm_label] = inst[delta_label] / inst[mean_label]

    return
