from ewokscore import Task
from silx.io.h5py_utils import retry, File, safe_top_level_names
from silx.utils.retry import RetryError


@retry(retry_period=0.5)
def wait_scans_finished(filename, entries=None):
    if not entries:
        entries = safe_top_level_names(filename)
    with File(filename, mode="r") as fh:
        for entry in entries:
            if "end_time" not in fh[entry]:
                raise RetryError
            print(f"Scan {entry} is finished")


class WaitScansFinished(
    Task,
    input_names=["filename"],
    optional_input_names=[
        "entries",
        "retry_timeout",
    ],
    output_names=["filename", "entries"],
):
    def run(self):
        if self.inputs.entries:
            retry_timeout = self.get_input_value("retry_timeout", 10)
            print(f"Wait: {self.inputs.filename} ({self.inputs.entries})")
            wait_scans_finished(
                self.inputs.filename,
                entries=self.inputs.entries,
                retry_timeout=retry_timeout,
            )
        self.outputs.filename = self.inputs.filename
        self.outputs.entries = self.get_input_value("entries", None)
