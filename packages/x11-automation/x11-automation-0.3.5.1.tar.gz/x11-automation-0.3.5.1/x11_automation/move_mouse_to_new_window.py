import cv2
import numpy as np
import mouse


def move_mouse_to_new_window(scr_empty, scr_window):
    scr1 = cv2.imread(scr_empty, cv2.IMREAD_GRAYSCALE)
    scr2 = cv2.imread(scr_window, cv2.IMREAD_GRAYSCALE)

    # 1) Check if 2 images are equals
    if scr1.shape == scr2.shape:
        # print("The images have same size and channels")
        difference = np.subtract(scr2, scr1)
        if cv2.countNonZero(difference) == 0:
            print('Same images')
            return
    else:
        print('Shape not match')
        return

    # cv2.imwrite('difference.png', difference)
    coords = np.argwhere(difference > 0)
    # print(coords)
    px, py = np.inf, np.inf
    split_coords = []
    temp_block = []
    for coord in coords:
        y, x = coord
        # print(f'{x=}, {y=}')
        if y > py + 1:
            # print(f'more {y}, {py}+1')
            split_coords.append(temp_block)
            temp_block = []
        temp_block.append([x, y])
        py = y
    split_coords.append(temp_block)
    # print(split_coords)
    for c in split_coords:
        # print(len(c))
        if len(c) > 100000:
            x, y = c[len(c)//2]
            mouse.move(x, y, duration=1)
            break
