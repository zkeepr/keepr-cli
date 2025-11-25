#!/usr/bin/env python3

import shutil


def center(text: str = "") -> None:
    """center Center the provided text in the terminal.

    This function takes a multi-line string as input and centers each line
    within the current terminal width. It calculates the necessary padding
    for each line to be centrally aligned and prints it accordingly.

    Keyword Arguments:
        text {str} -- The text to be centered, which can span multiple lines. (default: {""})
    """
    
    lines = text.split('\n')
    terminal_width, _ = shutil.get_terminal_size()
    
    for line in lines:
        padding = (terminal_width - len(line)) // 2
        print(" " * padding + line)
    