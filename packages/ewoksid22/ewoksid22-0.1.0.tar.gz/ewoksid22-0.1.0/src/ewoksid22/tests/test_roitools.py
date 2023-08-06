import numpy
import random
from .. import roitools


def test_unscramble_roi_collection():
    x = [1, 2, 3]
    y = [4, 5, 6, 7]
    n = len(x) * len(y)
    mot = numpy.random.random(n)
    motfixed = numpy.random.random(n + 1)
    mca = numpy.random.random((3, n))
    mcafixed = numpy.random.random((3, n + 1))
    scalarfixed = 10

    data1 = {
        "x": numpy.repeat(x, len(y)),
        "y": numpy.tile(y, len(x)),
        "mot": mot,
        "motfixed": motfixed,
        "mca": mca,
        "mcafixed": mcafixed,
        "scalarfixed": scalarfixed,
    }

    idx = list(range(n))
    random.shuffle(idx)
    data2 = {k: v[..., idx] if "fixed" not in k else v for k, v in data1.items()}

    data3 = roitools.unscramble_roi_collection(data2, ["x", "y"])

    data1 = {k: v.tolist() if "scalar" not in k else v for k, v in data1.items()}
    data3 = {k: v.tolist() if "scalar" not in k else v for k, v in data3.items()}
    assert data1 == data3
