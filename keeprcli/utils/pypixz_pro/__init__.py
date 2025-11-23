#!/usr/bin/env python3

""" PyPIxz-PRO 
Module to manage your dependencies.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A fork of PyPixz.

PyPIxz module to manage your dependencies in a simple and efficient way while maintaining guaranteed security.
Basic usage:
    import pypixz_pro as ppxz_pro

    ppxz_pro.install_requirements("requirements.txt")
    
:copyright: (c) 2025 YourLabXYZ.
:license: MIT, see LICENSE for more details.
"""

__all__ = [
    "install_requirements",
    "install_modules"
]


from .__version__ import (
    __title__,
    __description__,
    __url__,
    __version__,
    __author__,
    __license__,
    __copyright__
)

from .scripts.install import install_requirements, install_modules
