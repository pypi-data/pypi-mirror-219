from ewmh import EWMH
from Xlib.error import BadWindow
import subprocess
import re


def win_exists(win_name):
    if get_win_by_name(win_name):
        return True
    return False


def get_win_by_name(win_name):
    ewmh = EWMH()

    # get every displayed windows
    wins = ewmh.getClientList()

    for win in wins:
        try:
            name = win.get_wm_name()
        except BadWindow:
            continue
        if hasattr(win, 'id'):
            wm_id = win.id
        else:
            continue
        if not name:
            name = get_window_name(wm_id)

        if name == win_name:
            return {'name': name, 'win': win}
    return False


def get_window_name(win_id):
    p = subprocess.run(f'xprop -id {win_id}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = p.stdout.decode('utf-8')

    for line in out.splitlines():
        if match := re.match(r'WM_NAME\(.+\) = "(.+)"', line):
            return match.group(1)
