#!/usr/bin/env python3

class BasePyPIxzException(Exception):
    """Base exception for PyPIxz"""

    def __init__(self, *args, details = None):
        """Initialize the exception with optional additional arguments"""

        self.details = details
        super().__init__(*args)


# Exception for package management and package installation
class PackageError(BasePyPIxzException):
    """Exception raised when a package cannot be installed"""

class PackageInstallationError(PackageError):
    """Exception raised when a package cannot be installed"""

class MissingRequirementsFileError(PackageError):
    """Exception raised when a requirements file is missing"""
