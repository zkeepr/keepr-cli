#!/user/bin/env python3

import datetime
import calendar
import platform

from __init__ import __version__
from common.miscellaneous import clear_screen

current_time = datetime.datetime.now()


class KeeprCLI:
    def __init__(self, parameters):
        self.version = __version__
        self.ftime = {
            'year': current_time.year,
            'month': calendar.month_abbr[current_time.month],
            'day': current_time.day,
            'hour': current_time.hour,
            'minute': current_time.minute,
            'second': current_time.second
        }
        self.args = parameters[2]
        self.os = platform.system()

        clear_screen()

        print(f"Keepr-CLI v{self.version} ({self.ftime['month']} {self.ftime['day']} {self.ftime['year']}, {self.ftime['hour']}:{self.ftime['minute']}:"
              f"{self.ftime['second']}){" [DEBUG]" if self.args.debug else ""} on {self.os}\n"
              "Type \"help\", \"credits\", \"copyright\", \"license\" for more information.")

        
