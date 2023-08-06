from .win_exists import get_win_by_name
from ewmh import EWMH


def get_win_geometry(name):
    ewmh = EWMH()

    win = get_win_by_name(name)
    if win:
        win = win['win']
    else:
        print(f'Cannot find {name} window')
        return [0] * 4
    geom = win.get_geometry()
    # print(f'{geom=}')
    (x, y, w, h) = (geom.x, geom.y, geom.width, geom.height)
    while True:
        parent = win.query_tree().parent
        pgeom = parent.get_geometry()
        x += pgeom.x
        y += pgeom.y
        if parent.id == ewmh.root.id:
            break
        win = parent
    # print(f'{x=}, {y=}')
    return x, y, w, h
