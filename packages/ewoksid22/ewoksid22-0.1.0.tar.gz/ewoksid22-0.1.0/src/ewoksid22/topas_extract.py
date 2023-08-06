"""
Written by Ola G. Grendal @ ID22 ESRF
"""

import os
import sys
import numpy as np
import h5py
import bisect
from concurrent.futures import ProcessPoolExecutor as Pool


X_LOW = 0
X_HIGH = 511
NUM_CHANNELS = 13
ROIS = [i for i in range(NUM_CHANNELS)]
ROWS = [i for i in range(X_LOW, X_HIGH + 1)]

# TODO check for sorted/non-unique tth. !!Chop data fixed when data is not unique!!


def minmax_tth(min_usr_tth, max_usr_tth, tth_min, tth_max):
    # Takes in the user set min/max tth, and min/max of scans, and return min/max tth for data to to exported to xye-files
    print(f"tth min - max is: {tth_min} - {tth_max}")
    print(
        f"Widest range possible for MA06 with all detectors: {tth_min+12} - {tth_max-12}"
    )
    print(f"Your selection for MA06 is: {min_usr_tth} - {max_usr_tth}")

    if min_usr_tth is None and max_usr_tth is None:
        print(
            f"Your MA06 range is set to the widest possible: {tth_min+12}-{tth_max-12}"
        )
        return tth_min + 12, tth_max - 12
    elif min_usr_tth is None and max_usr_tth is not None:
        print("Your MA06 range is {tth_min+12} - {min(max_usr_tth, tth_max)}")
        return tth_min + 12, min(max_usr_tth, tth_max)
    elif min_usr_tth is not None and max_usr_tth is None:
        print(f"Your MA06 range is: {max(min_usr_tth, tth_min)} - {tth_max-12}")
        return max(min_usr_tth, tth_min), tth_max - 12
    else:
        print(
            f"Your MA06 range is: {max(min_usr_tth, tth_min)} - {min(max_usr_tth, tth_max)}"
        )
        return max(min_usr_tth, tth_min), min(max_usr_tth, tth_max)


def set_savepath(savepath):
    # Returns a string with the path to where to save the output images
    if savepath is None:
        return str("./")
    else:
        os.makedirs(savepath, exist_ok=True)
        return savepath


def set_filename(scan, in_file, out_file):
    # Returns a list of filename-strings
    if out_file is None:
        file_name_base = str(in_file.split("/")[-1].split(".")[0])
    else:
        file_name_base = out_file
    out_file_name_base = file_name_base + "_s{}_".format(scan)
    return out_file_name_base


def read_h5(scan, in_file):
    # Read h5-file and returns dict with info
    print(f"Reading data from scan {scan} of {in_file}...")
    res = {}
    with h5py.File(in_file, "r") as h:
        res["roicol"] = h["/{}.1/measurement/eiger_roi_collection".format(scan)][()]
        res["tth"] = h["/{}.1/measurement/tth".format(scan)][()]
        res["mon"] = h["/{}.1/measurement/mon".format(scan)][()]
        res["xs"] = h["/{}.1/instrument/eiger_roi_collection/selection/x".format(scan)][
            ()
        ]  # FIX
        res["ys"] = h["/{}.1/instrument/eiger_roi_collection/selection/y".format(scan)][
            ()
        ]  # FIX
    return res


def get_tth_indexes(tth_minMA06, tth_maxMA06, tth):
    # Find the tth subranges for the detectors assuming a nominal offset of 2-deg, and the corresponding indexes
    sub_ranges_tth = {}
    sub_ranges_idx = {}
    for i in range(NUM_CHANNELS):
        tth_low = tth_minMA06 + (6 - i) * 2
        tth_high = tth_maxMA06 + (6 - i) * 2
        idx_low = bisect.bisect_left(tth, tth_low)
        idx_high = bisect.bisect_left(tth, tth_high)
        sub_ranges_tth[f"MA{i:02d}"] = [tth_low, tth_high]
        sub_ranges_idx[f"MA{i:02d}"] = [idx_low, idx_high]
    # print(sub_ranges_tth, sub_ranges_idx)
    return sub_ranges_idx


def set_scans(scans, ex_scans):
    if isinstance(scans, int):
        all_scans = [scans]
    elif len(scans) == 1:
        all_scans = scans
    elif len(scans) == 2:
        all_scans = [x for x in range(scans[0], scans[1] + 1)]
        if ex_scans is not None:
            all_scans = [x for x in all_scans if x not in ex_scans]
    elif len(scans) >= 3:
        all_scans = [x for x in scans]
        if ex_scans is not None:
            all_scans = [x for x in all_scans if x not in ex_scans]
    else:
        all_scans = tuple()
    assert all_scans, "no scans to process"
    print("Converting the following scan(s): ", end="")
    print(*all_scans, sep=", ")
    return all_scans


# def check_tth(tth):
# 	is_sorted = np.all(tth[:-1] <= tth[1:])
# 	if is_sorted is False:
# 		print('!!tth is not a sorted array!!')
# 	tth_set = set(tth)
# 	if len(tth_set) == len(tth):
# 		all_unique = True
# 		chop = None
# 	else:
# 		all_unique = False
# 		chop = len(tth) - len(tth_set)
# 		print('!!tth does not only contain unique values!!')
# 	return is_sorted, all_unique, chop


def run(
    in_file,
    out_file,
    scans=(1,),
    savepath=None,
    ex_scans=None,
    min_usr_tth=None,
    max_usr_tth=None,
    full_tth=False,
):
    # Saves data from roi_collection to .xye-files
    save_data_path = set_savepath(savepath)
    all_scans = set_scans(scans, ex_scans)
    fmt = ("%3.8f", "%i", "%i")
    for scan in all_scans:
        data = read_h5(scan, in_file)
        out_filename = set_filename(scan, in_file, out_file)

        # is_sorted, all_unique, chop = check_tth(data['tth'])
        # if all_unique is False:
        # 	data['tth'] = data['tth'][chop:]
        # 	data['mon'] = data['mon'][chop:]
        # 	data['roicol'] = data['roicol'][chop:]

        sorted_xs = sorted(set(data["xs"]))
        nfiles = len(data["xs"])

        print(f"Extract scan {scan} from file {in_file} ...")

        if full_tth:
            with Pool() as pool:
                for i in range(nfiles):
                    channel = sorted_xs.index(data["xs"][i])
                    suffix = "MA{}_c{}.xye".format(channel, data["ys"][i])
                    filenamei = os.path.join(save_data_path, out_filename + suffix)
                    datai = np.c_[data["tth"], data["roicol"][:, i], data["mon"]]
                    pool.submit(np.savetxt, filenamei, datai, fmt=fmt)
        else:
            tth_min = round(data["tth"][0])
            tth_max = round(data["tth"][-1])
            tth_minMA06, tth_maxMA06 = minmax_tth(
                min_usr_tth, max_usr_tth, tth_min, tth_max
            )
            ranges_idx = get_tth_indexes(tth_minMA06, tth_maxMA06, data["tth"])

            with Pool() as pool:
                for i in range(nfiles):
                    channel = sorted_xs.index(data["xs"][i])
                    low_idx = ranges_idx[f"MA{channel:02d}"][0]
                    high_idx = ranges_idx[f"MA{channel:02d}"][1]
                    suffix = "MA{}_c{}.xye".format(channel, data["ys"][i])
                    filenamei = os.path.join(save_data_path, out_filename + suffix)
                    datai = np.c_[
                        data["tth"][low_idx:high_idx],
                        data["roicol"][low_idx:high_idx, i],
                        data["mon"][low_idx:high_idx],
                    ]
                    pool.submit(np.savetxt, filenamei, datai, fmt=("%3.8f", "%i", "%i"))

        print(f"Saved {nfiles} xye files")


def main(argv=None):
    import argparse
    from datetime import datetime

    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser(
        description="Script for exporting xye-files for TOPAS from roi collection @ ID22, ESRF"
    )
    parser.add_argument(
        "-in",
        "--in_file",
        type=str,
        required=True,
        help="Filepath to h5-file including filename",
    )

    parser.add_argument(
        "-s",
        "--scans",
        type=int,
        default=1,
        nargs="+",
        help="Scan number(s) of scan(s) to convert. Default is scan 1.1. Ex: 2 or 1 10 or 2 3 5",
    )

    parser.add_argument(
        "-es",
        "--ex_scans",
        type=int,
        default=None,
        nargs="+",
        help="Scan number(s) of scan(s) to exclude. Default is none. Ex: 2 or 2 3 5",
    )

    parser.add_argument(
        "-l_tth",
        "--tth_min",
        type=float,
        default=None,
        help="Lowest tth to include (MA6). Default is lowest possible (scan_start + 12).",
    )
    parser.add_argument(
        "-h_tth",
        "--tth_max",
        type=float,
        default=None,
        help="Highest tth to include (MA6). Default is highest possible (scan_end - 12).",
    )
    parser.add_argument(
        "-full_tth",
        "--full_tth",
        type=int,
        default=0,
        help="Set 1 to use all data/full tth-range. Default is 0.",
    )

    parser.add_argument(
        "-o",
        "--savepath",
        type=str,
        default=None,
        help="Full path to where you want to save your data. By default data is saved in the current directory: ./",
    )

    parser.add_argument(
        "-f",
        "--out_file",
        type=str,
        default=None,
        help="Filename. Ex: LaB6_35keV --> LaB6_35keV_sx_MAy_z.xye. If not given filename of h5-file is used --> h5filename_sx_MAy_z.xye.",
    )

    # parser.add_argument('-is', '--includescan', type=int, nargs='+', default=None, help='If used alone list of the only scans to be included. If used with -sts and/or -ens it will include scans outside the given range. Ex: 2 3 5 10')

    args = parser.parse_args(argv[1:])

    time_start_TOT = datetime.now()
    run(
        args.in_file,
        args.out_file,
        scans=args.scans,
        savepath=args.savepath,
        ex_scans=args.ex_scans,
        min_usr_tth=args.tth_min,
        max_usr_tth=args.tth_max,
        full_tth=bool(args.full_tth),
    )
    print("Time total: {}".format(datetime.now() - time_start_TOT))


if __name__ == "__main__":
    sys.exit(main())
