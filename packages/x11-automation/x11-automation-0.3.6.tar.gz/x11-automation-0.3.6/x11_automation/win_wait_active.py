from ewmh import EWMH
from .win_exists import get_win_by_name, get_window_name
import time


def win_wait_active(win_name, timeout=-1):
    ewmh = EWMH()
    w = get_win_by_name(win_name)
    if not w:
        return False
    while True:
        active_win = ewmh.getActiveWindow()
        active_win_name = get_window_name(active_win.id)
        if active_win_name == w['name']:
            return True

        if timeout == 0:
            return False
        timeout -= 1
        time.sleep(1)
