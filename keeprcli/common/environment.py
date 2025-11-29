#!/usr/bin/env python3

import sys

import logging
logger = logging.getLogger("main")

min_version = (3, 10)  # 3.10 | major : 3
                       #      | minor : 10


def python_compatiblity() -> None:
    """Check if the Python version is compatible.

    This function checks whether the Python version of the environment where
    the program is running is equal to or greater than the minimum recommended
    version, "min_version". It compares the current version to the minimum
    version, saves the results.

    :rtype: None
    """

    python_version = sys.version_info

    min_version_str = ".".join(map(str, min_version))
    python_version_str = ".".join(map(str, python_version[:3]))

    logger.debug(f"Python minimal version : {min_version_str}")
    logger.debug(f"Current version of Python : {python_version_str}")

    logger.debug(f"Checking the required version : {min_version_str}")
    if python_version < min_version:
        exit(logger.critical(f"The version of the Python environment where the program is running is lower than the minimum recommended version. ({python_version_str} < {min_version_str})"))

    logger.info("The Python environment version is compatible.")

    return None
