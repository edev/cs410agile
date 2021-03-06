from actions import put_file_onto_remote_server
from app.controller import main_loop
import pysftp
from tests.test_helpers import mock_input

# Arbitrary string that we'll print inside mock_put()
# and check for in our tests.
SUCCESS_STRING = "mock_put CALLED"

# The fake filename to pass in.
FILENAME = "filename"


def mock_put(sftp:pysftp.Connection, filename: str):
    """A fake put() function that checks the arguments and prints a string we
    can check for, to verify that the function was called.
    """

    assert isinstance(sftp, pysftp.Connection)
    assert filename == FILENAME
    print(SUCCESS_STRING)


def test_put_file_invokes_put_function(capsys, monkeypatch, sftp):
    """Tests that writing 'put file' calls the put action and passes 'file'
    as the filename.
    """

    # Replace put_file_onto_remote_server.put with our mocked function
    monkeypatch.setattr(put_file_onto_remote_server, "put", mock_put)

    # Pass in a valid input
    with mock_input("put " + FILENAME):
        main_loop(sftp)

    assert SUCCESS_STRING in capsys.readouterr().out


def test_invalid_commands_do_not_invoke_put_function(capsys, sftp):
    """Tests that writing invalid commands doesn't invoke the put action."""

    # See tests/integration/test_close.py for details.
    with mock_input("putty"):
        main_loop(sftp)
        assert "not recognized" in capsys.readouterr().out
