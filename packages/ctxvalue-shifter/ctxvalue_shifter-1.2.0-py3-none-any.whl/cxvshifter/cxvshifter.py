"""
Contextual Value Shifter - A Python module that implements a contextual "shift" function. 
"""

import subprocess

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
    if destination is not str:
        raise TypeError("`destination` is not string.")

    if destination == 'stdout':
        print(origin)

    elif destination == 'exec':
        # If origin isn't str, that probably isn't good
        if origin is not str:
            raise TypeError("'exec' specified, but `origin` is not a string.")

        subprocess.run(origin, shell=True, check=True)

    elif destination == 'file':
        if filename is None:
            raise ValueError("Missing 'file' parameter.")

        with open(filename, 'w', encoding="UTF-8") as file:
            file.write(str(origin))

    elif destination == 'return':
        return origin

    else:
        globals()[destination] = origin

    return None
