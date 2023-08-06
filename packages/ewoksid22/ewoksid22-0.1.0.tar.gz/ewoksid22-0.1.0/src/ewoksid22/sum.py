import os
import shutil
from ewokscore import Task
from .id22sum import run
from . import dirutils


class ID22Sum(
    Task,
    input_names=["filename", "binsize"],
    optional_input_names=[
        "entries",
        "lowtth",
        "scaling",
        "sum_single",
        "sum_all",
        "advanced",
        "resfile",
        "outdirs",
        "primary_outdir",
        "outprefix",
        "raw_filename",
        "ascii_extension",
    ],
    output_names=["outfile"],
):
    def run(self):
        # TODO: only outdirs["primary"] is used

        options = {
            "filename": self.inputs.filename,
            "entries": self.inputs.entries,
            "binsize": self.inputs.binsize,
            "lowtth": self.get_input_value("lowtth", 0),
            "scaling": self.get_input_value("scaling", None),
            "sum_single": self.get_input_value("sum_single", 1),
            "sum_all": self.get_input_value("sum_all", 1),
            "advanced": self.get_input_value("advanced", None),
            "ascii_extension": self.get_input_value("ascii_extension", ".dat"),
        }
        do_sum = options["sum_single"] or options["sum_all"]
        if not do_sum:
            self.outputs.outfile = None
            return

        if self.missing_inputs.raw_filename:
            primary_outdir = None
        else:
            primary_outdir = self.get_input_value("primary_outdir", None)

        outdirs = self.get_input_value("outdirs", dict())
        outdirs = dirutils.prepare_outdirs(outdirs, primary_outdir)

        # Save results in a subdirectory
        if do_sum:
            prefix = os.path.splitext(os.path.basename(self.inputs.filename))[0]
            outdirs_fortran = dict()
            for name, (userhost, dirname) in outdirs.items():
                sbinsize = str(options["binsize"]).replace(".", "")
                subdirname = f"{prefix}_b{sbinsize}"
                if not self.missing_inputs.outprefix:
                    subdirname = self.inputs.outprefix + "_" + subdirname
                dirname = os.path.join(dirname, subdirname)
                outdirs_fortran[name] = userhost, dirname
            options["outdir"] = outdirs_fortran["primary"][1]
        else:
            options["outdir"] = outdirs["primary"][1]

        if do_sum and not self.missing_inputs.resfile:
            # The fortran rebin program will be executed in outdir.
            # It needs the file res-file in that directory.
            resbasename = os.path.basename(self.inputs.resfile)
            options["resbasename"] = resbasename
            resfile = dirutils.primary_file(resbasename, outdirs_fortran)
            dirname = os.path.dirname(resfile)
            if dirname:
                os.makedirs(dirname, exist_ok=True)
            shutil.copyfile(self.inputs.resfile, resfile)

        print(f"Result will be saved in: {options['outdir']}")

        self.outputs.outfile = run(**options)
