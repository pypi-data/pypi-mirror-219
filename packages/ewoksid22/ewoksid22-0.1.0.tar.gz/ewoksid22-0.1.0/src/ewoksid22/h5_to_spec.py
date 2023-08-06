"""Convert an HDF5 file to a SPEC .dat file
"""

import os
import io
import datetime
import logging

import numpy
from scipy.interpolate import interp1d
from silx.io.h5py_utils import retry, File

from . import dirutils
from . import specutils

logger = logging.getLogger(__name__)


def convert_h5(
    raw_filename,
    outprefix=None,
    entries=None,
    outdirs=None,
    primary_outdir=None,
    retry_timeout=10,
    rebin_filename=None,
    ascii_extension=".dat",
):
    """
    :param str raw_filename: full path of the Nexus file
    :param str outprefix: something unique to the proposal/session
    :param list entries: for example ["1.1", "1.2", ...]
    :param dict outdirs:
    :param str primary_outdir:
    :param str rebin_filename: full path of the id22rebin file
    :returns str: primary spec output file
    """
    raw_filename = os.path.abspath(raw_filename)
    outdirs = dirutils.prepare_outdirs(outdirs, primary_outdir)
    if "primary" not in outdirs:
        logger.warning("No primary output directory: not saving anything")
        return

    if entries:
        names = {}
        for name in entries:
            scannr = int(name.split(".")[0])
            names.setdefault(scannr, []).append(name)
    else:
        names = get_scan_names(raw_filename, retry_timeout=retry_timeout)
    if not names:
        logger.warning("no scans to convert")
        return

    # Save SPEC header when no scans have been saved yet
    if rebin_filename:
        spec_filename = rebin_filename
    else:
        spec_filename = raw_filename
    spec_filename = (
        os.path.splitext(os.path.basename(spec_filename))[0] + ascii_extension
    )
    if outprefix:
        spec_filename = outprefix + "_" + spec_filename
    has_new_data = False

    saved = saved_scan_numbers(spec_filename, outdirs)
    if not saved:
        first_scan = sorted(names.items())[0][1][0]
        start_time = get_start_time(
            raw_filename, first_scan, retry_timeout=retry_timeout
        )
        specdata = create_spec_header(raw_filename, start_time=start_time)
        has_new_data |= bool(specdata)
        add_to_specfile(spec_filename, specdata, outdirs)

    # Save scans
    first_error = None
    for scannr, subscans in sorted(names.items()):
        if scannr in saved:
            # fscan already saved
            continue
        if len(subscans) != 2:
            # incomplete fscan
            continue
        # fscan with 2 complete subscans
        subscan1, subscan2 = subscans
        try:
            specdata = read_fscan_data(
                raw_filename,
                subscan1,
                subscan2,
                rebin_filename=rebin_filename,
                retry_timeout=retry_timeout,
            )
        except Exception as e:
            if first_error is None:
                first_error = e
            continue
        has_new_data |= bool(specdata)
        add_to_specfile(spec_filename, specdata, outdirs)

    if has_new_data:
        dirutils.copy_file(spec_filename, outdirs)

    if first_error is not None:
        raise first_error

    return dirutils.primary_file(spec_filename, outdirs)


@retry(retry_period=0.5, retry_timeout=10)
def get_scan_names(filename, title=None):
    """Get the subscan names for all scans in the Nexus file

    :param str filename:
    :param str title:id22
    :returns dict: scannr(int)->subscan_names(list)
    """
    with File(filename, mode="r") as h5file:
        names = list(h5file["/"])

        def include(name):
            try:
                scan = h5file[name]
            except Exception as e:
                logger.warning(
                    "cannot read scan " + repr(name) + " (cause: " + str(e) + ")"
                )
                return False
            if "end_time" not in scan:
                return False
            if "measurement" not in scan:
                return False
            if title:
                stitle = str_from_dataset(scan["title"])
                if not any(s in stitle for s in ["fscan", "f2scan"]):
                    return False
            return True

        scans = dict()
        for name in names:
            if include(name):
                scannr = int(float(name))
                scans.setdefault(scannr, []).append(name)

        return scans


def saved_scan_numbers(filename, outdirs):
    """Scans saved in the SPEC file.

    :param str filename:
    :param dict outdirs:
    :returns list(int):
    """
    local_filename = dirutils.primary_file(filename, outdirs)
    return specutils.saved_scan_numbers(local_filename)


def add_to_specfile(spec_filename, specdata, outdirs):
    """
    :param str spec_filename:
    :param list(2-tuple) specdata:
    :param dict outdirs:
    """
    if not outdirs:
        return
    local_filename = dirutils.primary_file(spec_filename, outdirs)
    dirname = os.path.dirname(local_filename)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    for mode, lines in specdata:
        with open(local_filename, mode) as f:
            f.writelines(lines)


MOTOR_NAMES = [
    ["tth", "om", "manom", "mantth", "mantr", "Dh", "Dhd"],
    ["Dhm", "Dhu", "spinp", "bluspin", "t1h", "t1h1", "t1h2", "t1x"],
    ["t1y", "t1rz", "t1trans", "robtran", "s3vg", "s3vo", "s3hg", "s3ho"],
    ["s4vg", "s4vo", "s4hg", "s4ho", "u26b", "chi"],
    ["d2dtran", "Dy", "Dyu", "Dyd", "Drx", "Dry"],
    ["mos", "rst", "rsg", "redtrans"],
    ["xtrans", "ytrans", "ztrans", "gasspin", "DET_Z", "DET_X", "DET_Y", "DET_RZ"],
]


def create_spec_header(filename, start_time=None):
    """
    :param str filename:
    :returns list(2-tuple):
    """
    specdata = []
    lines = []
    specdata.append(("w", lines))

    if not start_time:
        start_time = datetime.datetime.now().astimezone().isoformat()
    lines.append("#F " + '"' + filename + '"' + "\n")
    lines.append("#D " + start_time + "\n")
    lines.append("#C exp  User = opid22" + "\n")
    lines.append("" + "\n")
    for i, names in enumerate(MOTOR_NAMES):
        lines.append("#o{} ".format(i) + " ".join(names) + "\n")
    lines.append("\n")
    return specdata


@retry(retry_period=0.5, retry_timeout=10)
def get_start_time(filename, scan):
    """
    :param str filename:
    :param str scan:
    :returns str:
    """
    with File(filename, mode="r") as h5file:
        return str_from_dataset(h5file[scan]["start_time"])


@retry(retry_period=0.5, retry_timeout=10)
def read_fscan_data(raw_filename, subscan1, subscan2, rebin_filename=None):
    """
    :param str raw_filename:
    :param str subscan1:
    :param str subscan2:
    :param str rebin_filename:
    :returns list(2-tuple):
    """
    with File(raw_filename, mode="r") as h5file:
        gsubscan1 = h5file[subscan1]
        gsubscan2 = h5file[subscan2]
        if rebin_filename:
            with File(rebin_filename, mode="r") as h5filerebin:
                try:
                    rebinscan = h5filerebin[subscan1]
                except KeyError:
                    return list()
                return _read_fscan_data(gsubscan1, gsubscan2, rebinscan=rebinscan)
        else:
            return _read_fscan_data(gsubscan1, gsubscan2)


def _read_fscan_data(subscan1, subscan2, rebinscan=None):
    """
    :param h5py.Group subscan1:
    :param h5py.Group subscan2:
    :param h5py.Group rebinscan:
    :returns list(2-tuple):
    """
    specdata = []

    fast_data = subscan1["measurement"]
    slow_data = subscan2["measurement"]
    if rebinscan is None:
        rebin_data = None
    else:
        rebin_data = rebinscan["id22rebin/data"]

    fscan_params = subscan1["instrument/fscan_parameters"]
    positioners_start = subscan1["instrument/positioners_start"]
    try:
        machine = subscan1["instrument/machine"]
    except KeyError:
        machine = {}
    try:
        robot = subscan1["instrument/robot"]
    except KeyError:
        robot = {}

    # Scan parameters
    scannr = subscan1.name[1:].split(".")[0]
    start_time = str_from_dataset(subscan1["start_time"])
    start_pos = float(fscan_params["start_pos"][()])
    step = float(fscan_params["step_size"][()])
    no_scan_points = float(fscan_params["npoints"][()])
    acq_time = float(fscan_params["acq_time"][()])
    end_pos = "{:.2f}".format(start_pos + step * no_scan_points)
    deg_per_min = "{:.2f}".format(step / acq_time * 60)

    # Scan header
    lines = []
    specdata.append(("a", lines))

    lines.append(
        "#S  "
        + scannr
        + "  hookscan "
        + str_from_dataset(fscan_params["motor"])
        + " "
        + read_position(fscan_params, "start_pos", "{:.2f}")
        + " "
        + end_pos
        + " "
        + deg_per_min
        + " "
        + read_position(fscan_params, "acq_time", "{:.5f}", modif=lambda x: x * 1000)
        + " "
        + "\n"
    )
    lines.append("#D " + start_time + "\n")
    lines.append(
        "#T " + read_position(fscan_params, "acq_time", "{:.5f}") + " (Seconds)\n"
    )
    lines.append("#Q \n")

    for i, names in enumerate(MOTOR_NAMES):
        positions = " ".join(
            [read_position(positioners_start, name, "{:.4f}") for name in names]
        )
        lines.append("#P{} ".format(i) + positions + "\n")

    lines.append("#UMI0    Current     AutoM      Shutter      U26B_GAP     \n")
    lines.append(
        "#UMI1"
        + " "
        + read_position(machine, "current", "{:.4f}")
        + " "
        + str_from_dataset(machine.get("automatic_mode"))
        + " "
        + str_from_dataset(machine.get("front_end"))
        + " "
        + read_position(positioners_start, "u26b", "{:.4f}")
        + "\n"
    )

    lines.append(
        "#UMI2"
        + " Refill in "
        + str_from_dataset(machine.get("refill_countdown"))
        + " sec,"
        + " Fill Mode: "
        + str_from_dataset(machine.get("mode"))
        + ","
        + " Op. Message: "
        + str_from_dataset(machine.get("message"))
        + "\n"
    )

    lines.append(
        "#CR"
        + " Last robot sample loaded: "
        + str_from_dataset(robot.get("sample_label"))
        + "\n"
    )

    # Slow counters
    slow_ctrs_spec = [
        "blowerT",
        "Cryostream",
        "Cryostat",
        "Press_in",
        "Press_out",
        "monin",
        "bmon",
    ]
    slow_ctrs_fmt = ["%4.3f", "%4.3f", "%4.3f", "%7.4f", "%7.4f", "%.5e", "%.5e"]
    slow_ctrs_h5 = [
        ("blower_in", False),
        ("ox700", False),
        ("ls340_A", False),
        ("pace_in", False),
        ("pace_press", False),
        ("monin", False),
        ("bmon", False),
    ]
    nslow_ctrs = len(slow_ctrs_spec)
    npts_slow = min_npts_ctrs(slow_data, slow_ctrs_h5)

    # Fast counters
    if "eiger" in fast_data:
        prefix = "eiger_roi"
        nchannels = 13
    else:
        prefix = "ma"
        nchannels = 9
    if rebin_data is None:
        fast_ctrs_spec = (
            ["2_theta"]
            + ["MA{}".format(i) for i in range(nchannels)]
            + ["Monitor", "Epoch", "Omega"]
        )
        fast_ctrs_fmt = ["%3.8f"] + ["%i"] * nchannels + ["%i", "%15.8f", "%3.8f"]
        fast_ctrs_h5 = (
            ["tth"]
            + [prefix + str(i) for i in range(nchannels)]
            + ["mon", "epoch_trig", "om"]
        )
    else:
        fast_ctrs_spec = ["Epoch", "Omega"]
        fast_ctrs_fmt = ["%3.8f"] * len(fast_ctrs_spec)
        fast_ctrs_h5 = ["epoch_trig", "om"]
    not_required = ["om"]
    fast_ctrs_h5 = [(name, name not in not_required) for name in fast_ctrs_h5]
    nfast_ctrs = len(fast_ctrs_spec)
    npts_fast = min_npts_ctrs(fast_data, fast_ctrs_h5)

    # Rebin counters
    if rebin_data is None:
        rebin_ctrs_h5 = []
        rebin_ctrs_spec = []
        rebin_ctrs_fmt = []
        rebin_ctrs_h5 = []
    else:
        rebin_ctrs_h5 = ["2th", "I_sum", "norm"]
        rebin_ctrs_spec = ["2_theta"] + [
            f"{name}{i}"
            for name in ["MA", "Mon"]
            for i in list(range(nchannels)) + ["av"]
        ]
        rebin_ctrs_fmt = (
            ["%3.8f"] + ["%i"] * nchannels + ["%3.8f"] + ["%i"] * nchannels + ["%3.8f"]
        )
        rebin_ctrs_h5 = [(name, True) for name in rebin_ctrs_h5]
    nrebin_ctrs = len(rebin_ctrs_spec)
    npts_rebin = min_npts_ctrs(rebin_data, rebin_ctrs_h5)

    # Prepare data
    if npts_rebin:
        nrows = npts_rebin
    else:
        nrows = npts_fast
    ncols = nrebin_ctrs + nfast_ctrs + nslow_ctrs
    data = numpy.zeros((nrows, ncols))
    ctrs_spec = rebin_ctrs_spec + fast_ctrs_spec + slow_ctrs_spec
    ctrs_fmt = rebin_ctrs_fmt + fast_ctrs_fmt + slow_ctrs_fmt
    rebinoff = 0
    fastoff = nrebin_ctrs
    slowoff = nrebin_ctrs + nfast_ctrs

    # Read rebin data
    off = rebinoff
    for i, idata in read_ctrs(rebin_data, rebin_ctrs_h5, npts_rebin):
        if idata.ndim == 2:
            idata = idata.T
            nadd = idata.shape[-1]
            data[:, off : off + nadd] = idata
            off += nadd
            data[:, off] = numpy.mean(idata, axis=1)
            off += 1
        else:
            data[:, off] = idata
            off += 1

    # Read fast data + interpolate at rebinned 2-theta
    if npts_rebin:
        xnew = list(read_ctrs(rebin_data, [("2th", True)], npts_rebin))[0][-1]
        xold = list(read_ctrs(fast_data, [("tth", True)], npts_fast))[0][-1]
        for i, idata in read_ctrs(fast_data, fast_ctrs_h5, npts_fast):
            func = interp1d(xold, idata, kind="nearest", fill_value="extrapolate")
            try:
                data[:, fastoff + i] = func(xnew)
            except Exception:
                pass
    else:
        for i, idata in read_ctrs(fast_data, fast_ctrs_h5, npts_fast):
            data[:, fastoff + i] = idata

    # Read slow data + interpolate at fast epoch
    xold = list(read_ctrs(slow_data, [("epoch", True)], npts_slow))[0][-1]
    xnew = data[:, ctrs_spec.index("Epoch")]
    for i, idata in read_ctrs(slow_data, slow_ctrs_h5, npts_slow):
        func = interp1d(xold, idata, kind="nearest", fill_value="extrapolate")
        try:
            data[:, slowoff + i] = func(xnew)
        except Exception:
            pass

    # Scan data header
    lines = []
    specdata.append(("a", lines))
    lines.append("#N {}\n".format(ncols))
    lines.append("#L  " + "  ".join(ctrs_spec) + "\n")

    # Scan data
    lines = []
    specdata.append(("ab", lines))
    f = io.BytesIO()
    numpy.savetxt(f, data, delimiter=" ", fmt=" ".join(ctrs_fmt))
    lines.append(f.getbuffer())
    lines.append(b"\n")

    return specdata


def read_ctrs(group, ctrs, npts):
    """Read datasets

    :param h5py.Group group:
    :param list(2-tuple) ctrs:
    :param int npts:
    :yield numpy.ndarray:
    """
    for i, (name, must_exist) in enumerate(ctrs):
        try:
            dset = group[name]
        except KeyError:
            if must_exist:
                raise
        else:
            try:
                data = dset[:npts]
            except Exception as e:
                logger.warning(
                    "skip counter data " + repr(name) + " (cause: " + str(e) + ")"
                )
            else:
                if not len(data):
                    logger.warning("no data in " + repr(name))
                    continue
                yield i, data


def min_npts_ctrs(group, ctrs):
    """Smallest number of points of a group of datasets.

    :param h5py.Group group:
    :param list(2-tuple) ctrs:
    :returns int:
    """
    if not ctrs:
        return 0
    npts = []
    for name, must_exist in ctrs:
        try:
            dset = group[name]
        except KeyError:
            if must_exist:
                raise
        else:
            npts.append(dset.shape[-1])
    return min(npts)


def str_from_dataset(dataset):
    """Read dataset as a string

    :param h5py.Dataset dataset:
    :returns str:
    """
    if isinstance(dataset, str):
        return dataset
    if dataset is None:
        return "UNKNOWN"
    try:
        return dataset.asstr()[()]
    except (AttributeError, TypeError):
        return str(dataset[()])


def read_position(grp, key, fmt, modif=None):
    """Read a motor position from grp[key], return "-999" when missing.

    :param h5py.Group grp:
    :param str key:
    :param callable or None modif:
    :returns str:
    """
    if key in grp:
        pos = grp[key][()]
        if pos == "*DIS*":
            return str(-999)
        try:
            num = float(fmt.format(pos))
        except Exception as e:
            raise RuntimeError("Error in formatting motor position " + repr(key)) from e
        if modif:
            num = modif(num)
        return str(num)
    return str(-999)
