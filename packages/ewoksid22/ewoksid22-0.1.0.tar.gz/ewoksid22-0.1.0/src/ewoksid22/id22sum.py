"""Script for batch runs with id22sum and id22sumall:
processes powder diffraction data from a multianalyser instrument

Fortran source code: https://github.com/jonwright/id31sum

Written by Ola G. Grendal @ ID22 ESRF
"""

import os
import sys
import subprocess
import glob

import numpy
import h5py
import hdf5plugin  # noqa F401

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None


from . import specutils


def usage_msg(name=None):
    """Function for re-defining the usage-message when no and/or wrong input is given"""

    return """id22sumepy

[-h, for more help than given here]
    -i, start of, or full filename. Ex: ch5900_S1_ or ch5900_S1_RT_0001.dat
    -b, binsize. Ex: 0.002
[-int, True for interactive mode, default is False]
"""


def epilog_msg(name=None):
    """Function for re-defining the usage-message when no and/or wrong input is given"""
    return """
PRO TIP #1):
Put filename in quotes with * or ? for linux wildcard expansion.
Ex: -i \"hc4000_sample*_\"
"""


def generate_cmd(
    program,
    programdir,
    filename,
    binsize,
    first_scan,
    last_scan,
    lowtth,
    scaling,
    excludedetector,
    excludescan,
    zingit,
    advanced=None,
):
    """Fortran sum program command"""
    if programdir:
        program = os.path.join(programdir, program)
    cmd = [
        program,
        filename,
        binsize,
        "{}".format(first_scan),
        "{}".format(last_scan),
        "lowtth={}".format(lowtth),
    ]
    if scaling is None:
        cmd.append("scalmon")
    elif scaling.startswith("scal"):
        cmd.append("{}".format(scaling))
    if excludescan:
        cmd.append("es={}".format(excludescan))
    if excludedetector:
        cmd.append("ed={}".format(excludedetector))
    if zingit:
        cmd.append("ef={}.zin".format(os.path.basename(filename)))
    if advanced is not None:
        for i in advanced:
            cmd.append(i)
    return cmd


def generate_es(first_scan, last_scan, *args):
    """Exclude scan numbers: exclude from start, missing from spec file, interactive prompt"""
    scannrs = list()
    for numbers in args:
        if numbers:
            if isinstance(numbers, int):
                scannrs.append(numbers)
                continue
            if isinstance(numbers, str):
                numbers = numbers.split(",")
            scannrs += [int(i) for i in numbers]
    scannrs = [i for i in sorted(set(scannrs)) if i >= first_scan and i <= last_scan]
    if scannrs:
        return ",".join(list(map(str, scannrs)))
    return None


def yes_no(question):
    """Yes/no prompt. Returns True or False."""
    answers = ["n", "no", "y", "yes"]
    while True:
        try:
            answer = input(question)
        except ValueError:
            print("Sorry, I did not understand that!")
            continue
        answer = answer.lower()
        if answer not in answers:
            print("Your response must be [y]es or [n]o")
            continue
        else:
            break
    if answer.startswith("y"):
        return True
    else:
        return False


def new_bin(question):
    """Retrieve new binsize"""
    while True:
        try:
            answer = float(input(question))
            break
        except ValueError:
            print("Please type a valid number. Ex: 0.002")
            continue

    return str(answer)


def removed_scans(question):
    """Retrieve scans to be removed"""
    while True:
        answer = input(question)
        try:
            scannrs = [int(i) for i in answer.split(",")]
            break
        except ValueError:
            print("Please type a valid number or list of numbers. Ex: 2 or 1,2,5")
    return ",".join(map(str, scannrs))


def plot_xy(
    filename,
    first_scan,
    last_scan,
    es_scans,
    sum_single,
    sum_all,
    binsize=None,
    show=True,
):
    """Reads XY data and plots it"""
    if es_scans is None:
        exclude_scans = []
    else:
        exclude_scans = [int(x) for x in es_scans.split(",")]
    all_scans = list(range(first_scan, last_scan + 1))
    plot_scans = [x for x in all_scans if x not in exclude_scans]
    if sum_all:
        for i in plot_scans:
            xyfilename = "{}_{}.xye".format(os.path.splitext(filename)[0], i)
            data = numpy.loadtxt(xyfilename, usecols=(0, 1)).T
            plt.plot(data[0], data[1], label="Scan: {}".format(i))

    if sum_single:
        if binsize:
            xyfilename = "{}_b{}.xye".format(
                os.path.splitext(filename)[0], str(binsize).replace(".", "")
            )
        else:
            xyfilename = "{}.xye".format(os.path.splitext(filename)[0])
        data = numpy.loadtxt(xyfilename, usecols=(0, 1)).T
        plt.plot(data[0], data[1], label="Final pattern")

    plt.plot(
        [], [], " ", label="To continue press: Ctrl + w"
    )  # Simple hack for adding explanatory text to legend
    plt.legend()
    plt.xlim(data[0].min(), data[0].max())
    plt.title(str(filename))
    if show:
        plt.show()


def find_h5_files(user_str):
    all_files = []
    if any(element in user_str for element in ["*", "?", "["]):
        all_files = glob.glob(user_str + ".h5")
    else:
        basename = os.path.basename(user_str)
        dirname = os.path.dirname(user_str)
        if not dirname:
            dirname = "."
        for filename in os.listdir(dirname):
            if filename.startswith(basename) and filename.endswith(".h5"):
                all_files.append(os.path.join(dirname, filename))
    print("id22sumpy: Found {} files starting with {}".format(len(all_files), user_str))
    return all_files


def get_all_scans_h5(file_path):
    with h5py.File(file_path, "r") as h:
        all_scans = sorted(h.keys(), key=lambda x: float(x))
    return all_scans


def read_h5(file_path, entry="1.1"):
    """Read h5-file and returns dict with data"""
    print("id22sumpy: Reading data...")
    res = {}
    with h5py.File(file_path, "r") as h:
        res["I"] = numpy.nan_to_num(
            h["/{}/id22rebin/data/I_MA".format(entry)][()], nan=0
        )
        res["I_sum"] = h["/{}/id22rebin/data/I_sum".format(entry)][()]
        res["tth"] = h["/{}/id22rebin/data/2th".format(entry)][()]
        res["norm"] = h["/{}/id22rebin/data/norm".format(entry)][()]
    return res


def save_spec(file_path, data, monav, entry="1.1"):
    scannr = int(float(entry))
    header_1 = "#S {} hookscan \n".format(scannr)
    header_2 = "#N 28\n"
    header_3 = "#L  2_theta  MA0  MA1  MA2  MA3  MA4  MA5  MA6  MA7  MA8  MA9  MA10  MA11  MA12  Mon0  Mon1  Mon2  Mon3  Mon4  Mon5  Mon6  Mon7  Mon8  Mon9  Mon10  Mon11  Mon12  Monav"
    header = header_1 + header_2 + header_3
    fmt = "%3.8f" + 13 * " %i" + 14 * " %i"
    if not os.path.exists(file_path):
        dirname = os.path.dirname(file_path)
        if dirname:
            os.makedirs(dirname, exist_ok=True)
        with open(file_path, "wb+") as dat:
            numpy.savetxt(
                dat,
                numpy.c_[
                    data["tth"],
                    numpy.transpose(data["I_sum"]),
                    numpy.transpose(data["norm"]),
                    numpy.transpose(monav),
                ],
                header=header,
                comments="",
                fmt=fmt,
            )
    else:
        with open(file_path, "ab+") as dat:
            numpy.savetxt(
                dat,
                numpy.c_[
                    data["tth"],
                    numpy.transpose(data["I_sum"]),
                    numpy.transpose(data["norm"]),
                    numpy.transpose(monav),
                ],
                header="\n" + header,
                comments="",
                fmt=fmt,
            )
    print("id22sumpy: Saved scan {} to {}".format(scannr, file_path))
    return scannr


def execute_cmd(cmd, wd):
    cmd = list(map(str, cmd))
    print("\nid22sumpy: Execute " + " ".join(cmd))
    output = subprocess.check_output(cmd, universal_newlines=True, cwd=wd)
    if output:
        print(output)


def execute_sum(
    programdir,
    filename,
    binsize,
    first_scan,
    last_scan,
    lowtth,
    scaling,
    zingit,
    sum_single,
    sum_all,
    excludedetector,
    excludescan,
    outdir,
    advanced=None,
    interactive=0,
):
    """Execute id22sumalle and id22sume"""
    cmdfilename = os.path.abspath(filename)

    if sum_all:
        cmd = generate_cmd(
            "id22sumalle",
            programdir,
            cmdfilename,
            binsize,
            first_scan,
            last_scan,
            lowtth,
            scaling,
            excludedetector,
            excludescan,
            zingit,
            advanced=advanced,
        )
        execute_cmd(cmd, outdir)

    if sum_single:
        cmd = generate_cmd(
            "id22sume",
            programdir,
            cmdfilename,
            binsize,
            first_scan,
            last_scan,
            lowtth,
            scaling,
            excludedetector,
            excludescan,
            zingit,
            advanced=advanced,
        )
        execute_cmd(cmd, outdir)

    if interactive:
        plot_xy(filename, first_scan, last_scan, excludescan, sum_single, sum_all)


def run(
    filename,
    binsize,
    lowtth=0,
    scaling=None,
    entries=None,
    excludescan=None,
    excludedetector=None,
    interactive=0,
    sum_single=1,
    sum_all=1,
    zingit=0,
    advanced=tuple(),
    outdir=None,
    resbasename="temp.res",
    ascii_extension=".dat",
    programdir=None,
):
    if outdir is None:
        outdir = os.getcwd()
    resfile = os.path.join(outdir, resbasename)
    do_sum = sum_single or sum_all
    if do_sum and not os.path.isfile(resfile):
        raise RuntimeError("Cannot find {}".format(resfile))

    print("\nid22sumpy: processing file " + filename)

    if filename.endswith(ascii_extension):
        specfile = filename
        scan_numbers = specutils.saved_scan_numbers(specfile)
        if entries:
            scan_numbers = sorted(set(scan_numbers) - set(map(int, entries)))
    else:
        # Convert HDF5 to ASCII
        scans_h5 = get_all_scans_h5(filename)
        if not scans_h5:
            print("id22sumpy: No scans to process")
            return

        specfile = os.path.splitext(filename)[0] + ascii_extension
        specfile = os.path.join(outdir, os.path.basename(specfile))

        processed = specutils.saved_scan_numbers(specfile)

        scan_numbers = list()
        for entry in scans_h5:
            if not entry.endswith(".1"):
                continue
            if entries and entry not in entries:
                continue
            scannr = int(float(entry))
            if scannr in processed:
                continue
            data = read_h5(filename, entry)
            monav = numpy.mean(data["norm"], axis=0)
            save_spec(specfile, data, monav, entry)
            scan_numbers.append(scannr)

    if not scan_numbers:
        print("id22sumpy: No scans to process")
        return specfile

    first_scan = min(scan_numbers)
    last_scan = max(scan_numbers)
    missing_scans = sorted(set(range(first_scan, last_scan + 1)) - set(scan_numbers))
    gen_es = generate_es(first_scan, last_scan, excludescan, missing_scans)

    if zingit:
        program = "zingit"
        if programdir:
            program = os.path.join(programdir)
        cmd = [program, specfile, resbasename]
        execute_cmd(cmd, outdir)

    sbinsize = str(binsize)

    execute_sum(
        programdir,
        specfile,
        sbinsize,
        first_scan,
        last_scan,
        lowtth,
        scaling,
        zingit,
        sum_single,
        sum_all,
        excludedetector,
        gen_es,
        outdir,
        advanced=advanced,
        interactive=interactive,
    )

    while interactive and not yes_no(
        "Are you happy with selected binsize and scans[y/n]? "
    ):
        if yes_no("Do you want to change binsize[y/n]? "):
            sbinsize = new_bin(
                "Please type new binsize for {} [Ex:0.002]: ".format(specfile)
            )
        if yes_no("Do you want to exclude specific scans[y/n]? "):
            es_new = removed_scans(
                "Please type scan(s) to be removed from {} [Ex:2 or 1,2,5]: ".format(
                    specfile
                )
            )
            gen_es = generate_es(
                first_scan, last_scan, excludescan, missing_scans, es_new
            )

        execute_sum(
            programdir,
            specfile,
            sbinsize,
            first_scan,
            last_scan,
            lowtth,
            scaling,
            zingit,
            sum_single,
            sum_all,
            excludedetector,
            gen_es,
            outdir,
            interactive=interactive,
        )

    # Rename the sumall file to include the binsize
    xyfile = os.path.splitext(specfile)[0] + ".xye"
    if os.path.exists(xyfile):
        xybfile = os.path.splitext(xyfile)[0] + "_b{}.xye".format(
            sbinsize.replace(".", "")
        )
        os.rename(xyfile, xybfile)

    return specfile


def main(argv=None):
    import argparse
    from datetime import datetime

    if argv is None:
        argv = sys.argv

    starttime = datetime.now()

    parser = argparse.ArgumentParser(
        description="Script for processing of high resolution diffraction data using id22sume @ ID22, ESRF ",
        usage=usage_msg(),
        epilog=epilog_msg(),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-i",
        "--filename",
        type=str,
        required=True,
        help="Full filename of a .h5-file, or start of filename for processing all files with same starting filename. Ex: hc4000_sample1_",
    )
    parser.add_argument(
        "-b", "--binsize", type=str, required=True, help="Binsize. Ex: 0.002"
    )
    parser.add_argument(
        "-lowtth", "--lowtth", type=float, default=0, help="Set low tth. Default is 0."
    )
    parser.add_argument(
        "-scal",
        "--scaling",
        type=str,
        default=None,
        help="Pattern scaling options (default is option 1 with default value for XXX): 1) scalmon=XXX: for counts per XXX monitor counts (default = 100000) 2) scalpk: to scale highest peak to correct number of obs counts 3) scaltot: to make total number of counts in scan correct 4) no: for no pattern scaling",
    )
    parser.add_argument(
        "-es",
        "--excludescan",
        type=str,
        help="Scans to be excluded. Ex: 3 or 3,5,8. Default is none.",
    )
    parser.add_argument(
        "-ed",
        "--excludedetector",
        type=str,
        help="Detectors to be excluded. Ex: 3 or 3,5,8. Default is none.",
    )
    parser.add_argument(
        "-int",
        "--interactive",
        type=int,
        default=0,
        help="Set to 1 if you want plotting and the option to change binsize and/or selected scans for each .dat-file being processed. Default is not interactive mode.",
    )
    parser.add_argument(
        "-all",
        "--sum_all",
        type=int,
        default=1,
        help="Set to 0 if you do NOT want to do id22sumall. Default is to do id22sumall.",
    )
    parser.add_argument(
        "-single",
        "--sum_single",
        type=int,
        default=1,
        help="Set to 0 if you do NOT want to do id22sum. Default is to do id22sum.",
    )
    parser.add_argument(
        "-zin",
        "--zingit",
        type=int,
        default=0,
        help="Set 1 if you need to do zingit (looking for saturated pixels in data). Default is not to do it. !!SHOULD NOT BE NEEDED ANYMORE!!",
    )
    parser.add_argument(
        "-a",
        "--advanced",
        type=str,
        default=None,
        nargs="+",
        help="For using any of the id22sum options not directly supported with this python-script. Ex: hightth=120 zap=1 gsas. Type id22sum+Enter for full list of options.",
    )
    parser.add_argument(
        "--programdir",
        type=str,
        default=None,
        help="Directory of the fortran programs.",
    )

    args = parser.parse_args(argv[1:])

    programdir = args.programdir
    if not programdir and os.path.exists("/users/opid22/bin"):
        programdir = "/users/opid22/bin"

    all_h5_files = find_h5_files(args.filename)
    if not all_h5_files:
        print(
            "Did not find any files starting/matching with {}...".format(args.filename)
        )

    for filename in all_h5_files:
        run(
            filename,
            binsize=args.binsize,
            lowtth=args.lowtth,
            scaling=args.scaling,
            excludescan=args.excludescan,
            excludedetector=args.excludedetector,
            interactive=args.interactive,
            sum_single=args.sum_single,
            sum_all=args.sum_all,
            zingit=args.zingit,
            advanced=args.advanced,
            programdir=args.programdir,
        )

    print(
        "Finished! :) Time taken in hh:min:sec : {} ".format(datetime.now() - starttime)
    )


if __name__ == "__main__":
    sys.exit(main())
