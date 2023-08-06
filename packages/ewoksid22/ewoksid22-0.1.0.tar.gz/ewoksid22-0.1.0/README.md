# ewoksid22

Data processing workflows for ID22

## Getting started

Example of using the command line scripts directly (needs access to `/data/id22/inhouse/`):

```bash
./examples/rebinsum.sh
```

Example of defining and executing an HDF5 to SPEC conversion workflow (needs access to `/data/id22/inhouse/`):

```bash
ewoks execute examples/convert.json
```

Example of defining and executing a ROI collection rebin+sum workflow (needs access to `/data/id22/inhouse/`):

```bash
ewoks execute examples/rebinsum.json
```

## Installation

```bash
pip install multianalyzer@git+https://github.com/kif/multianalyzer.git@main
pip install ewoksid22
```

The following command line scripts are installed:

* `id22sumepy`: python wrapper for `id22sume` and `id22sumalle`
* `id22sume`: fortran program
* `id22sumalle`: fortran program
* `zingit`: awk program

## Documentation

https://ewoksid22.readthedocs.io/
