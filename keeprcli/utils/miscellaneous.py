#!/user/bin/env python3

import os


def clear_screen() -> int:
    """clear_screen Clear the terminal screen.

    Clears the console output by using the appropriate system command
    depending on the operating system (``cls`` for Windows, ``clear`` for
    Unix/Linux/Mac).

    Returns:
        int -- The return code of the executed system command.
    """
    
    return os.system('cls' if os.name == 'nt' else 'clear') 
    