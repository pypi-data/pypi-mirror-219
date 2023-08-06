import numpy


def unscramble_roi_collection(data, keys):
    """Sort the dictionary of numpy arrays on the keys"""
    if not keys:
        return data
    lst = [data[key] for key in keys]
    idx = list(range(len(lst[0])))
    *_, idx = zip(*sorted(zip(*lst, idx)))
    idx = list(idx)
    return {k: _apply_index(v, idx) for k, v in data.items()}


def _apply_index(v, idx):
    v = numpy.asarray(v)
    if v.ndim == 0 or v.shape[-1] != len(idx):
        return v
    return v[..., idx]
