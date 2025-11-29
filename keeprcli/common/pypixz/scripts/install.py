#!/usr/bin/env python3

from typing import Optional
import logging
import sys
import subprocess
from pathlib import Path

from ..exceptions import (
    PackageInstallationError,
    MissingRequirementsFileError,
    PackageError
)


def _build_requirement(package: str, version: Optional[str], version_range: Optional[str]) -> str:
    requirement = package  # Latest version installed by default
    if version:
        return f"{package}=={version}"
    elif version_range:
        return f"{package}{version_range}"  # e.g. "package>=1.2.0" or "package!=2.0.0"

    return requirement


def install_package(package: str, version: Optional[str] = None, version_range: Optional[str] = None, logger: Optional[str | logging.Logger] = None) -> bool:
    """Install a specified Python package with optional version,
    version range, and logging.

    This function installs a Python package from PyPI, supporting exact
    versions, version ranges, or installing the latest available version.
    It supports logging for debugging and handles various installation and
    dependency errors.

    :param package: The name of the package to install.
    :type package: str
    :param version: A specific version to install.
    :type version: Optional[str]
    :param version_range: A version range specifier.
    :type version_range: Optional[str]
    :param logger: Logger instance used for logging during installation.
    :type logger: Optional[logging.Logger]

    :raises PackageInstallationError: If installation fails due to system
    issues, dependency problems, or invalid version constraints.

    :return: True if the package was installed successfully.
    :rtype: bool
    """

    logger = logging.getLogger(logger) if isinstance(logger, str) else logging

    # Build the package specifier with version or version range
    try:
        requirement = _build_requirement(package, version, version_range)
    except Exception as error:
        raise PackageInstallationError(logger.error(f"Invalid module specification: {error}")) from error

    logger.debug(f"Preparing to install requirement: {requirement}")

    # Build pip command
    command = [
        sys.executable,
        "-m",
        "pip",
        "install",
        requirement,
        "--disable-pip-version-check",  # avoid noisy warnings
        "--no-input",  # prevent hanging
    ]

    logger.debug(f"Executing pip command: {' '.join(command)}")

    try:
        result = subprocess.run(
            command,
            check=True,  # Raises CalledProcessError if the command fails
            capture_output=True,  # Captures stdout and stderr for debugging/logging
            text=True  # Decodes stdout/stderr as text
        )

        logger.info(f"Package '{package}' installed successfully.")
        if result.stdout:
            logger.debug("Pip output:\n%s", result.stdout)

        return True

    except subprocess.CalledProcessError as error:
        error_msg = error.stderr or "Unknown installation error."
        logger.error("Pip installation failed: %s", error_msg)
        raise PackageInstallationError(f"Failed to install package '{package}': {error_msg}") from error

    except OSError as system_error:
        logger.error("System error during installation: %s", system_error)
        raise PackageInstallationError(f"System failure during installation of '{package}': {system_error}") from system_error


def install_requirements(path: str = "requirements.txt", logger: Optional[str | logging.Logger] = None) -> bool:
    """Install Python packages listed in a requirements file.

    This function reads a `requirements.txt` file and installs all listed
    dependencies via pip. It validates the file's existence, logs installation
    details, and raises structured exceptions on errors.

    :param path: Path to the requirements file.
    :type path: str
    :param logger: Logger instance or logger name to use for output.
    :type logger: Optional[str | logging.Logger]

    :raises MissingRequirementsFileError: If the requirements file does not exist.
    :raises PackageInstallationError: If pip fails to install dependencies.
    :raises PackageError: On OS-level errors during pip execution.

    :return: True if installation completed successfully.
    :rtype: bool
    """

    logger = logging.getLogger(logger) if isinstance(logger, str) else logging  # Resolve logger
    file_path = Path(path).resolve()  # Resolve path safely

    logger.debug(f"Resolved requirements path: {file_path}")

    # Check if the file exists and is valid
    if not file_path.is_file():
        message = f"Requirements file not found: {file_path}"
        logger.error(message)
        raise MissingRequirementsFileError(message)

    logger.info(f"Installing package from: {file_path.name}")

    # Build pip command
    command = [
        sys.executable,
        "-m",
        "pip",
        "install",
        "-r",
        str(file_path),
        "--disable-pip-version-check",  # avoid noisy warnings
        "--no-input",  # prevent hanging
    ]

    logger.debug(f"Executing pip command: {' '.join(command)}")

    try:
        result = subprocess.run(
            command,
            check=True,  # Raises CalledProcessError if the command fails
            capture_output=True,  # Captures stdout and stderr for debugging/logging
            text=True  # Decodes stdout/stderr as text
        )

        logger.info("All dependencies installed successfully.")
        if result.stdout:
            logger.debug("Pip output:\n%s", result.stdout)

        return True

    except subprocess.CalledProcessError as error:
        stderr = error.stderr or "Unknown error from pip."
        logger.error("pip installation failed: %s", stderr)
        raise PackageInstallationError(f"pip failed to install requirements: {stderr}") from error

    except OSError as os_error:
        logger.error("OS-level installation error: %s", os_error)
        raise PackageError(f"OS error during pip execution: {os_error}") from os_error
