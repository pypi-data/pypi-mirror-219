from ewokscore import Task
from .h5_to_spec import convert_h5


class ID22H5ToSpec(
    Task,
    input_names=["filename"],
    optional_input_names=[
        "entries",
        "outdirs",
        "primary_outdir",
        "outprefix",
        "retry_timeout",
        "rebin_filename",
        "ascii_extension",
    ],
    output_names=["outfile"],
):
    def run(self):
        entries = self.get_input_value("entries", None)
        outdirs = self.get_input_value("outdirs", None)
        primary_outdir = self.get_input_value("primary_outdir", None)
        retry_timeout = self.get_input_value("retry_timeout", 10)
        rebin_filename = self.get_input_value("rebin_filename", None)
        ascii_extension = self.get_input_value("ascii_extension", ".dat")

        self.outputs.outfile = convert_h5(
            self.inputs.filename,
            self.inputs.outprefix,
            entries=entries,
            outdirs=outdirs,
            primary_outdir=primary_outdir,
            retry_timeout=retry_timeout,
            rebin_filename=rebin_filename,
            ascii_extension=ascii_extension,
        )
