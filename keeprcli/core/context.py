#!/usr/bin/env python3

from pathlib import Path
from argparse import ArgumentParser, Namespace


class Context:
    def __init__(self, version: str, os: str, parameters: list[Path | ArgumentParser | Namespace]) -> None:
        self.version = version
        self.os = os
        self.keepr_path_default = parameters[0]
        self.parser = parameters[1]
        self.args = parameters[2]
