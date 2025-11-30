#!/usr/bin/env python3

from pathlib import Path
from argparse import ArgumentParser, Namespace
import datetime
import calendar

from .context import Context
from common.miscellaneous import clear_screen


class KeeprApp:
    def __init__(self, app_version: str, operating_system: str, parameters: list[Path | ArgumentParser | Namespace]) -> None:
        self.context = Context(app_version, operating_system, parameters)
        clear_screen()
        self.header()

    def header(self) -> None:
        ftime = datetime.datetime.now()
        month = calendar.month_abbr[ftime.month]

        print(f"Keepr-CLI {self.context.version} "
              f"({month} {ftime.day} {ftime.year}, {ftime.hour}:{ftime.minute}:{ftime.second}) "
              f"{"[DEBUG] " if self.context.args.debug else ""}on {self.context.os}")
        print('Type "help", "about", "credits", "license" or "copyright" for more information.')

