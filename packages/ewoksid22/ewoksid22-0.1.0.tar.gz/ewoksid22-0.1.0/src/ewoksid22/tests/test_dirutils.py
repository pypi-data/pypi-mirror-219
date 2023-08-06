import pytest
import socket
from .. import dirutils


def test_prepare_outdirs():
    primary_outdir = None
    outdirs = dict()

    result = dirutils.prepare_outdirs(outdirs, primary_outdir)
    assert result == dict()

    primary_outdir = "/users/opid22/inhouse/id222207/id22/20220701/processed"
    result = dirutils.prepare_outdirs(outdirs, primary_outdir)
    expected = {
        "primary": (
            None,
            "/users/opid22/inhouse/id222207/id22/20220701/processed",
        )
    }
    assert result == expected

    outdirs = {
        "primary": "opid22@diffract22new:/users/opid22/data1/",
        "secondary": "opid22@diffract22new:/users/opid22/data1/",
    }
    with pytest.raises(ValueError):
        dirutils.prepare_outdirs(outdirs, primary_outdir)

    outdirs = {
        "primary": f"opid22@{socket.gethostname()}:/users/opid22/data1/",
        "secondary": "opid22@diffract22new:/users/opid22/data1/",
    }
    result = dirutils.prepare_outdirs(outdirs, primary_outdir)
    expected = {
        "primary": (None, "/users/opid22/data1/"),
        "secondary": ("opid22@diffract22new", "/users/opid22/data1/"),
        "processed": (
            None,
            "/users/opid22/inhouse/id222207/id22/20220701/processed",
        ),
    }
    assert result == expected
