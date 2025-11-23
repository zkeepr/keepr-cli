#!/usr/bin/env python3

import os
import logging
import subprocess
import sys

from ..exceptions import (
    MissingRequirementsFileError,
    ModuleInstallationError,
    DependencyError
)


def install_requirements(path: str = "requirements.txt", logger: str = "main"):
    """install_requirements Install required Python packages from a requirements file.

    This function enables the installation of Python package dependencies defined in a requirements file. 
    It first checks the file's existence before validating if all required packages are already installed. 
    If some packages aren't installed, it executes `pip` to install the missing dependencies. 
    The function includes optional logging features to record status, success, or error messages.

    Keyword Arguments:
        path {str} -- The path to the requirements file. (default: {"requirements"})
        logger {str} -- Choose the logger used (default: {"main"})

    Raises:
        MissingRequirementsFileError: If the specified requirements file does not exist or cannot be accessed.
        ModuleInstallationError: If an error occurs during the module installation using pip.
        DependencyError: If an OS-level error occurs during the installation process.
    """
    
    absolute_path = os.path.abspath(path)
    logger = logging.getLogger(logger)
    
    # Check if the file exists and is valid
    if not os.path.isfile(absolute_path):
        raise MissingRequirementsFileError(logger.error(f"The {path} file was not found."))
    
    try:
        # Run the pip install -r requirements.txt command
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", absolute_path],
            check=True,  # Raises CalledProcessError if the command fails
            capture_output=True,  # Captures stdout and stderr for debugging/logging
            text=True  # Decodes stdout/stderr as text
        )
        
        logger.info("Successfully installed dependencies.")
        logger.debug("Command output:\n%s", result.stdout)
    
    except subprocess.CalledProcessError as error:
        raise ModuleInstallationError(logger.error(f"An error occurred while installing dependencies:\n{error.stderr or 'Unknown error'}")) from error
    except OSError as os_error:
        raise DependencyError(logger.error(f"OS error occurred during installation: {os_error}")) from os_error
    

def install_modules(module: str, version: str = None, version_range: str = None, logger: str = "main") -> bool:
    """install_modules Install a specified Python module with optional version, version range, and logging.

    This function allows for installing a Python module from PyPI, with the option to specify a specific version, version range, or using the latest available version. 
    It supports logging for debugging purposes and handles various error scenarios like dependency issues or installation failure.

    Arguments:
        module {str} -- The name of the module to be installed.

    Keyword Arguments:
        version {str} -- The specific version of the module to be installed. Defaults to None. (default: {None})
        version_range {str} -- A version range specifier if a specific range of versions is needed. (default: {None})
        logger {str} -- Choose the logger used (default: {"main"})

    Raises:
        ModuleInstallationError: Raised when the module installation fails due to system issues, dependency issues, or other reasons.
        ModuleInstallationError: Raised when the requested version or version range is incompatible or not available on PyPI.

    Returns:
        bool -- True if the module was installed successfully.
    """
    
    # Format the package with a version or version range
    if version:
        package_specifier = f"{module}=={version}"
    elif version_range:
        package_specifier = f"{module}{version_range}"  # e.g. "module>=1.2.0, !=2.0.0"
    else:
        package_specifier = module  # Latest version installed by default
        
    try:

        # Pip command with specifier
        command = [
            sys.executable, "-m", "pip", "install", package_specifier
        ]

        # Call pip install
        result = subprocess.run(
            command,
            check=True,  # Raises CalledProcessError if the command fails
            capture_output=True,  # Captures stdout and stderr for debugging/logging
            text=True  # Decodes stdout/stderr as text
        )

        logger.info(f"Module {module} successfully installed.")
        logger.debug("Command output:\n%s", result.stdout)

    except subprocess.CalledProcessError as error:
        raise ModuleInstallationError(logger.error(f"An error occurred while installing the module {module}:\n{error.stderr or 'Unknown error'}")) from error
    except (OSError, DependencyError) as dep_error:
        raise ModuleInstallationError(logger.error(f"System or dependency error for the module {module}: {dep_error}")) from dep_error
    
    return True
