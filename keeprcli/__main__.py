#!/usr/bin/env python3

""" Keepr-CLI

Keeper makes it easy to manage all your development projects, in a simple and
secure way. The project is developed primarily in Python.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This version of Keepr is command line only.
"""

import argparse
from pathlib import Path
import logging
try:  # 2.7+
    from logging.config import dictConfig
except ImportError as error:
    raise ImportError(f"Unable to import the module needed for logging. Check that your Python version is 2.7 or later.\n{error}")
logger = logging.getLogger('main')

from __init__ import __version__
from utils.pypixz_pro import install_modules, install_requirements

try:
    import yaml
except ModuleNotFoundError:
    install_modules(module='pyyaml', logger='main')
    import yaml


def get_keepr_path() -> str:
    current_file = Path(__file__).resolve()
    keepr_path_default = current_file.parent
    
    return keepr_path_default


def argparse_setup() -> argparse.Namespace:
    """argparse_setup Configures the argparse module.

    This function create and configuration an `argparse.ArgumentParser` object
    to manage the program's launch arguments.

    Returns:
        argparse.Namespace -- An object containing the parsed arguments.
    """
    
    parser = argparse.ArgumentParser(description=f"Keepr-CLI - v{__version__}")
    parser.add_argument('-v', '--version', action='version', version=f"Keepr-CLI - v{__version__}")
    parser.add_argument('--debug', action='store_true', help="enable debug output")
    args = parser.parse_args()
    
    return parser, args


def logging_setup(args: argparse.Namespace) -> logging.Logger:
    """logging_setup Configure the logging system based on the passed arguments.

    This function initializes and adapts the behavior of the main logger based
    on the options and information provided.

    Arguments:
        args {argparse.Namespace} -- The parsed command line arguments.

    Returns:
        logging.Logger -- The configured logger instance.
    """
    
    if args.debug:
        logger.setLevel(logging.DEBUG)
    
    for handler in logger.handlers:
        if getattr(handler, 'basefileName', '').endswith('debug.log'):
            handler.addFilter(lambda record: record.levelno == logger.DEBUG)
    return logger


def initialize() -> None:
    keepr_path_default = get_keepr_path()
    parser, args = argparse_setup()
    
    logging_config_path = f"{keepr_path_default}/configurations/logging.yaml"
    with open(logging_config_path, 'r') as file:
        configuration_file = yaml.safe_load(file)
        dictConfig(configuration_file)
    
    logger = logging_setup(args=args)
    
    return None
    

if __name__ == '__main__':
    initialize()
    