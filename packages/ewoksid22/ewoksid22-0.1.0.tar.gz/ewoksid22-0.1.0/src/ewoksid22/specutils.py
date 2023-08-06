import os


def saved_scan_numbers(filename):
    """Scans saved in the SPEC file.

    :param str filename:
    :param dict outdirs:
    :returns list(int):
    """
    saved = []
    if os.path.isfile(filename):
        with open(filename, "r") as f:
            for line in f:
                if "#S" in line:
                    saved.append(int(line.split()[1]))
    return saved
