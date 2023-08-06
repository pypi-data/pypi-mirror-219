"""
Contextual Value Shifter - A Python module that implements a contextual "shift" function. 
"""

import inspect
import subprocess

class ContextualActions():
    """
    Defines the contextual actions for ctxvalue-shifter.
    """
    def __init__(self):
        warning_msg = """WARNING: This class isn't supposed to be used directly.
        Use `cxvshifter.shift()`."""
        caller_module = inspect.getmodule(inspect.currentframe().f_back)
        module_name = caller_module.__name__ if caller_module else '<unknown>'
        if module_name != '__main__':
            print(warning_msg)

    def stdout(self, data):
        """
        Prints to stdout.

        Used if `destination` is `'stdout'`.
        """
        print(data)

    def exec(self, cmd):
        """
        Runs a command.

        Used if `destination` is `'exec'`.
        """
        # If cmd isn't str, that probably isn't good
        if not isinstance(cmd, str):
            raise TypeError("'exec' specified, but `origin` is not a string.")
        subprocess.run(cmd, shell=True, check=True)

    def filec(self, data, filename):
        """
        Writes a file.

        Used if `destination` is `'file'`.
        """
        if filename is None:
            raise ValueError("Missing 'file' parameter.")

        with open(filename, 'w', encoding="UTF-8") as file:
            file.write(str(data))

    def assign(self, origin, destination):
        """
        Assigns a variable.

        Used if `destination` is not a special value.
        """
        globals()[destination] = origin

def shift(origin, destination, filename=None):
    """
    Shifts the value of `origin` to the specified `destination`.

    `destination` options:
    - `'stdout'`: Prints `origin` to standard output.
    - `'exec'`: Executes `origin` as a command using subprocess.
    - `'file'`: Writes `origin` to a file.
    - `'return'`: Returns `origin`.

    If `destination` is `'return'`, shift returns `origin`.

    Otherwise, shift returns `None`.
    """

    # We make sure destination is str, to prevent abuse
    # and to make sure they're doing it right
    if not isinstance(destination, str):
        raise TypeError("`destination` is not string.")

    action = ContextualActions()

    if destination == 'stdout':
        action.stdout(origin)
    elif destination == 'exec':
        action.exec(origin)
    elif destination == 'file':
        action.filec(origin, filename)
    elif destination == 'return':
        return origin
    else:
        action.assign(origin, destination)

    return None
