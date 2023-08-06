import subprocess
from x11_automation import get_win_by_name


def win_activate(win_name):
    win = get_win_by_name(win_name)
    if win and hasattr(win['win'], 'id'):
        wm_id = win['win'].id
    else:
        wm_id = 0
    subprocess.run(f'xdotool windowactivate $(  xdotool search --name "{win_name}" )',
                   shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if wm_id > 0:
        subprocess.run(f'xdotool windowactivate {wm_id}', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
