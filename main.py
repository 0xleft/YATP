import screeninfo

import sys
from core.util import *
from core.yatp import YATP

if os.name != 'nt':
    sys.exit('This program only works on Windows')

if __name__ == '__main__':
    # get monitor dimensions
    monitor_info = screeninfo.get_monitors()[0]
    monitor_width = monitor_info.width
    monitor_height = monitor_info.height

    YATP(int(monitor_width / 2), int(monitor_height / 2))