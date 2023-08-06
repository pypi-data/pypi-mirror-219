from pathlib import Path

try:
    from importlib import resources
except ImportError:
    import importlib_resources as resources


def program_path(program: str) -> Path:
    with resources.path(__name__, program) as path:
        return path


def main(argv=None):
    import sys
    import argparse

    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser(description="Full path of the binary")
    parser.add_argument("name", type=str, help="Binary name")

    args = parser.parse_args(argv[1:])
    print(program_path(args.name))
