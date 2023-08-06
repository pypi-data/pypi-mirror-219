from ewmh import EWMH
from .win_exists import get_win_by_name


def win_get_process(win_name):
    ewmh = EWMH()
    w = get_win_by_name(win_name)
    if w:
        return ewmh.getWmPid(w['win'])
    return 0
