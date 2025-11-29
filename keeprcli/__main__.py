#!/usr/bin/env python3

""" Keepr-ClI

Keepr makes it easy to manage all your development projects, in a simple and
secure way. The project is developed primarily in Python.

-------------------------------------------
This version of Keepr is command line only.
"""

import argparse
from argparse import ArgumentParser, Namespace
from pathlib import Path
import logging
try:  # 2.7+
    from logging.config import dictConfig
except ImportError as error:
    raise ImportError(f"Unable to import the module needed for logging. Check that your Python version is 2.7 or later.\n\n{error}")
logger = logging.getLogger('main')

from __init__ import __version__
from common.pypixz import install_package, install_requirements, PackageInstallationError
from common._os import os_compatibility
from common.environment import python_compatiblity

try:
    import yaml
except ModuleNotFoundError as error:
    if input("The pyyaml ​​package is not installed, would you like to try installing it automatically?\n[y] / [n] : ").lower() == 'y':
        try:
            install_package(package='pyyaml', logger=logger)
            exit("'pyyaml' has been successfully installed, please restart Keepr-CLI.")
        except PackageInstallationError as error:
            exit("Please try installing 'pyyaml' manually.")
    else:
        exit(1)


def get_keepr_path() -> Path:
    current_file = Path(__file__).resolve()
    keepr_path_default = current_file.parent
    
    return keepr_path_default


def argparse_setup() -> tuple[ArgumentParser, Namespace]:
    """Configures the argparse module.

    This function create and configuration and `argparse.ArgumentParser` object
    to manage the program's launch arguments.

    :return: An tuple containing the parsed arguments.
    :rtype: tuple[ArgumentParser, Namespace]
    """
    
    parser = argparse.ArgumentParser(description=f"Keepr-CLI - v{__version__}")
    parser.add_argument('-v', '--version', action='version', version=f'Keepr-CLI - v{__version__}')
    parser.add_argument('--skip-check', nargs='+', choices=['os', 'env', 'pip', 'all'], help="pass the program launch checks")
    parser.add_argument('--debug', action='store_true', help="enable debug output")
    args = parser.parse_args()
    
    return parser, args


def logging_setup(args: Namespace) -> None:
    """Configure the logging system based on the passed arguments.

    This function initializes and adapts the behavior of the main logger based
    on the options and information provided.

    :param args: The parsed command line arguments.
    :type args: Namespace

    :rtype: None
    """
    
    if args.debug:
        logger.setLevel(logging.DEBUG)

    for handler in logger.handlers:
        if getattr(handler, "baseFilename", "").endswith("debug.log"):
            handler.addFilter(lambda record: record.levelno == logging.DEBUG)
    return None


def technology_checks(args: Namespace, parser: ArgumentParser, requirements: str) -> bool:
    """Checks the compatibility of the execution environment based on the
    provided command-line options.

    This function runs a series of checks (operating system, Python
    environment, required packages) unless pecific checks have been explicitly
    excluded using the `--skip-check` argument.
    The order and logic of all checks are defined in an internal dictionary,
    allowing centralized and maintainable control over compatibility tests.

    Arguments:
    args {argparse.Namespace} -- The parsed command line arguments.
    parser {argparse.Namespace} -- The parser instance used to raise argument-related errors, especially when invalid values are passed to `--skip-check`.

    Returns:
    bool -- Returns True only when the user explicitly passes `--skip-check all`, meaning that no compatibility checks are executed.
    Otherwise, the function returns True and simply runs the required checks.

    """

    verifications = {
        "os": {
            "name": "operating system",
            "function": lambda: os_compatibility()
        },
        "env": {
            "name": "environment",
            "function": lambda: python_compatiblity()
        },
        "pip": {
            "name": "packages",
            "function": lambda: install_requirements(requirements, logger)
        }
    }
    
    verification_passed = args.skip_check or []
    if "all" in verification_passed:
        if verification_passed and (len(verification_passed) > 1 or verification_passed[0] != "all"):
            parser.error("The 'all' argument must be the first and only choice after '--skip-check'.")
        return True
    
    for object, data in verifications.items():
        if object not in verification_passed:
            logger.debug(f"Running {data['name']} compatibility check...")
            data['function']()
        else:
            logger.warning(f"Skipping {data['name']} compatibility check.")

    return True


def initialize() -> list[Path | ArgumentParser | Namespace]:
    keepr_path_default = get_keepr_path()
    parser, args = argparse_setup()
    
    logging_config_path = f"{keepr_path_default}/cache/logs/logging_config.yaml"
    with open(logging_config_path, 'r') as file:
        logging_config = yaml.safe_load(file)
    dictConfig(logging_config)
    logging_setup(args)
    
    requirements = f"{keepr_path_default.parent}/requirements.txt"
    technology_checks(args, parser, requirements)
    
    return [keepr_path_default, parser, args]

if __name__ == '__main__':
    parameters = initialize()
    
    from runtime.keeprcli import KeeprCLI
    KeeprCLI(parameters)
    