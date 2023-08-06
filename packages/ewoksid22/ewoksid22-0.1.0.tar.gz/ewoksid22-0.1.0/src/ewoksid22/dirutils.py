import os
import shutil
import socket
import subprocess
from typing import Dict, Optional, Tuple, Iterator

HOST_NAME = socket.gethostname()

PARSED_OUTDIR = Tuple[Optional[str], str]
PARSED_OUTDIRS = Dict[str, PARSED_OUTDIR]


def prepare_outdirs(outdirs: Dict[str, str], primary_outdir: str) -> PARSED_OUTDIRS:
    """
    :param outdirs: maps names to local directories (/users/opid22/data1/)
                    or remote directories (opid22@diffract22new:/users/opid22/data1/)
    :param primary_outdir:
    """
    if outdirs is None:
        outdirs = dict()
    else:
        outdirs = dict(outdirs)
    if primary_outdir:
        for key in _outdir_key_generator():
            if key not in outdirs:
                break
        outdirs[key] = primary_outdir
    outdirs = {name: parse_outdir(dirname) for name, dirname in outdirs.items()}
    if "primary" not in outdirs:
        return dict()
    userhost, _ = outdirs["primary"]
    if userhost:
        raise ValueError("The primary output directory should be a local directory")
    return outdirs


def _outdir_key_generator() -> Iterator[str]:
    yield "primary"
    yield "processed"
    i = 0
    while True:
        i += 1
        yield f"processed{i}"


def parse_outdir(dirname: str) -> PARSED_OUTDIR:
    err_msg = f"malformed directory name '{dirname}'"
    if dirname.count(":") > 1:
        raise ValueError(err_msg)
    parts = dirname.split(":")
    if len(parts) not in (1, 2):
        raise ValueError(err_msg)
    if len(parts) == 1:
        return None, dirname
    userhost, dirname = parts
    if userhost.endswith(HOST_NAME):
        return None, dirname
    return userhost, dirname


def copy_file(filename: str, outdirs: PARSED_OUTDIRS) -> None:
    """Copy file from the primary output directory to the others."""
    if not outdirs:
        return
    local_filename = primary_file(filename, outdirs)
    filename = os.path.basename(local_filename)
    for name, (userhost, dirname) in outdirs.items():
        if name == "primary":
            continue
        remote_filename = os.path.join(dirname, filename)
        if userhost:
            cmd = ["scp", "-q", local_filename, f"{userhost}:'{remote_filename}'"]
            output = subprocess.check_output(cmd)
            if output:
                print(output)
        else:
            dirname = os.path.dirname(remote_filename)
            if dirname:
                os.makedirs(dirname, exist_ok=True)
            shutil.copyfile(local_filename, remote_filename)


def copy_file_to_primary(filename: str, outdirs: PARSED_OUTDIRS) -> None:
    """Copy file to the primary output directory."""
    shutil.copyfile(filename, primary_file(filename, outdirs))


def primary_file(filename: str, outdirs: PARSED_OUTDIRS) -> str:
    if not outdirs:
        return
    filename = os.path.basename(filename)
    return os.path.join(outdirs["primary"][1], filename)
