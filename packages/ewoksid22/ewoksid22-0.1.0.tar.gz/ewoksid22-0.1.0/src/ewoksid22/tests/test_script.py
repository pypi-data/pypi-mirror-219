import subprocess
import pytest
from ..bin import program_path


@pytest.mark.parametrize("program", ["id22sume", "id22sumalle"])
def test_binary(program):
    cmd = program_path(program)
    subprocess.check_output([str(cmd)])


@pytest.mark.parametrize("program", ["id22sumepy"])
def test_console_script(program):
    subprocess.check_output([program, "--help"])
