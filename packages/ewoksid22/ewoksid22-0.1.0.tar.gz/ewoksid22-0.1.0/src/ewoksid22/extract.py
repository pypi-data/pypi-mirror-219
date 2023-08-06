import os
import shutil
import subprocess
from ewokscore import Task
from . import topas_extract
from . import dirutils


class ID22TopasExtract(
    Task,
    input_names=["filename", "inp_file"],
    optional_input_names=[
        "entries",
        "tth_min",
        "tth_max",
        "full_tth",
        "outdirs",
        "outprefix",
        "primary_outdir",
        "inp_step",
        "startp",
    ],
):
    def run(self):
        in_file = self.get_input_value("filename", None)

        scans = self.get_input_value("entries", None)
        if scans:
            scans = sorted({int(float(s)) for s in scans})
        assert len(scans) == 1, f"Extract only 1 scan ({scans})"
        tth_min = self.get_input_value("tth_min", None)
        tth_max = self.get_input_value("tth_max", None)
        full_tth = self.get_input_value("full_tth", False)

        outdirs = self.get_input_value("outdirs", dict())
        primary_outdir = self.get_input_value("primary_outdir", None)
        outdirs = dirutils.prepare_outdirs(outdirs, primary_outdir)

        out_file = os.path.splitext(os.path.basename(in_file))[0]
        if not self.missing_inputs.outprefix:
            out_file = self.inputs.outprefix + "_" + out_file
        out_file = out_file + "_calib"

        # TODO: use all outdirs
        rootpath = os.path.join(outdirs["primary"][1], out_file)
        savepath_xye = os.path.join(rootpath, "topas_extract")
        savepath_inp = os.path.join(rootpath, "topas_refine")
        os.makedirs(savepath_xye, exist_ok=True)
        os.makedirs(savepath_inp, exist_ok=True)

        topas_extract.run(
            in_file,
            out_file,
            scans=scans,
            savepath=savepath_xye,
            min_usr_tth=tth_min,
            max_usr_tth=tth_max,
            full_tth=full_tth,
        )

        scannr = scans[0]
        savepath_xye = os.path.relpath(savepath_xye, savepath_inp)
        xye_files = os.path.join(savepath_xye, out_file + f"_s{scannr}_MA")
        inp_file = self.inputs.inp_file
        inp_step = self.get_input_value("inp_step", 2)
        startp = self.get_input_value("startp", 31)

        inp_file_cp = os.path.join(savepath_inp, os.path.basename(inp_file))
        shutil.copyfile(inp_file, inp_file_cp)

        # Modify inp_file_cp and save xdds.inp
        args = [
            "gen_xdds_file",
            xye_files,
            os.path.basename(inp_file_cp),
            0,
            topas_extract.NUM_CHANNELS - 1,
            startp,
            topas_extract.X_HIGH,
            inp_step,
        ]
        args = list(map(str, args))

        proc = subprocess.Popen(
            args, stdout=subprocess.PIPE, cwd=os.path.dirname(inp_file_cp)
        )
        try:
            outs, errs = proc.communicate(timeout=120)
        except subprocess.TimeoutExpired:
            proc.kill()
            raise
        with open(os.path.join(savepath_inp, "xdds.inp"), "wb") as f:
            f.write(outs)
