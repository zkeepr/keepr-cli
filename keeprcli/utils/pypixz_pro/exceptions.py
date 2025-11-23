#!/usr/bin/env python3

class BasePyPIxzProException(Exception):
    """Base exception for PyPIxz-PRO."""
    
    def __init__(self, *args, details: None = None):
        """Initialize the exception with optional additional arguments."""
        
        self.details = details
        super().__init__(*args)
        

# Exception for dependency management and package installation
class DependencyError(BasePyPIxzProException):
    """Exception raised when a dependency cannot be installed."""
    
class MissingRequirementsFileError(DependencyError):
    """Exception raised when a requirements file is missing."""
    
class ModuleInstallationError(DependencyError):
    """Exception raised when a module cannot be installed."""
    