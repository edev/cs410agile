from .input_handler import read_user_input
from actions import  put_file_onto_remote_server

import pysftp

# ===================
# SECTION: Controller
# ===================


def main_loop(sftp: pysftp.Connection) -> int:
    """Main controller loop. Asks the user for input, attempts to decipher
    user input, and invoke the appropriate actions with the desired arguments.
    """

    # Catch disconnects & no connection errors.
    try:
        # Main control loop.
        while True:

            # First, we take in a command sequence from the user.
            try:
                tokens = read_user_input()
            except EOFError:
                # EOF received. User wants to close the program.
                print("\nConnection closed.")
                sftp.close()
                return 0

            # ==========================
            # LIST OF SUPPORTED ACTIONS: add new actions as elif clauses.
            # ==========================

            # Blank line. Ignore.
            if len(tokens) == 0:
                continue
            elif len(tokens) == 1 and tokens[0] == "ls":
                # Barebones remote "ls" support to let us write meaningful
                # tests of the basic skeleton.
                # TODO Replace this action handler when implementing remote ls.
                sftp.listdir(".")
            elif len(tokens) == 2 and tokens[0] == "put":
                put_file_onto_remote_server.put(sftp, tokens[1])
            else:
                print("That command is not recognized.")

    except AttributeError as e:
        if "open_session" in str(e):
            # The connection has been severed or a command was attempted
            # while no connection was active.
            print("The connection was closed unexpectedly.")
            return -1
        else:
            raise
