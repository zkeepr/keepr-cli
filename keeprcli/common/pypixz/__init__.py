#!/usr/bin/env python3

""" PyPIxz

PyPIxz module to manage your dependencies in a simple and efficient way while
maintaining guaranteed security.

Basic usage:
    import pypixz
    pypixz.install_package("pypixz", version_range='>=2.0')

    pypixz.install_requirements("requirements.txt")

:copyright: (c) 2025 ZKeepr
:license: MIT, see LICENSE for more details.
"""

__all__ = [
    "install_package",
    "install_requirements"
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

from .scripts.install import install_package, install_requirements
from .exceptions import *
