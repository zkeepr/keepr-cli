#!/usr/bin/env python3

import platform
import re

import logging
logger = logging.getLogger("main")


def get_os_name():
    return platform.system()


def parse_version(version: str) -> tuple:
    return tuple(map(int, re.findall(r"\d+", version)))  # '10.0.19044' -> (10, 0, 19044)


def os_compatibility() -> None:
    """Check OS compatibility.

    This feature automatically detects the operating system (Windows,
    macOS/Darwin, or Linux), analyzes its version, and then compares it with
    the minimum recommended version. If the operating system or its version
    does not meet the minimum criteria, the program is terminated with a
    critical error message via the logger.

    :raises Exception: If the Darwin version is lower than the minimum
    required version or if the OS version is lower than the minimum
    required version.

    :rtype: None
    """

    os_name = get_os_name()
    os_release = platform.release()
    os_version = extract_kernel_version(os_release) if os_name == "Linux" else platform.version()

    logger.debug(f"Detected operating system: {os_name}")
    logger.debug(f"Detected release: {os_release}")
    logger.debug(f"Detected version: {os_version}")

    # Checking supported operating systems
    # Windows   : 10 21H2               : 10.0.19044
    # Darwin    : macOS 12 (Monterey)   : (12)
    # Linux     : 5.15.0-60-generic     : (5,15,0)
    supported_os = {"Windows": {"min_version": (10, 0, 19044), "patterns": os_version},
                    "Darwin": {"min_version": 21, "patterns": os_release},
                    "Linux": {"min_version": (5, 10), "patterns": os_release}}

    if os_name not in supported_os:
        exit(logger.critical(f"Unsupported operating system: {os_name}"))

    # Checking supported the OS version
    os_info = supported_os[os_name]
    os_version_tuple = parse_version(os_info["patterns"])

    logger.debug(f"Minimum required version for {os_name}: {os_info["min_version"]}")

    try:
        if os_name == "Darwin":
            if os_version_tuple[0] < os_info["min_version"]:
                raise Exception()
        elif os_version_tuple < os_info["min_version"]:
            raise Exception()
    except Exception:
        exit(logger.critical(f"Minimum required version for {os_name} is {os_info["min_version"]}, but you have {os_version_tuple}"))

    logger.info(f"Operating system: {os_name} {os_version} ({os_release})")

    return None


def extract_kernel_version(os_release: str) -> str:
    """Extracts the kernel version from the os_release string.

    :param os_release: The original OS release string.
    :type os_release: str

    :return: The extracted version in the format X.Y.Z or X.Y.
    :rtype: str
    """

    # Find the first instance of the version in X.Y.Z or X.Y format.
    match = re.search(r'\d+\.\d+(\.\d+)?', os_release)
    if match:
        kernel_version = match.group(0)
        logger.debug(f"Extracted kernel version: {kernel_version}")
        return kernel_version
    else:
        logger.error(f"Could not extract kernel version from: {os_release}")
        return os_release  # Return the original version if no correspondence is found
