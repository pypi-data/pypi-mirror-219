from pyKey import pressKey, releaseKey, press, sendSequence, showKeys
import re


def send(keys_str: str, sec_per_key=0.05):
    keys = []
    if matches := re.findall(r'{(\w+)}', keys_str):
        for match in matches:
            if match == 'BACKSPACE':
                match = 'BKSP'
            keys.append(match.upper())
    else:
        keys = [x for x in keys_str]

    for key in keys:
        if key == ' ':
            key = 'SPACEBAR'
        elif key == '~':
            key = 'TILDE'
        press(key, sec=sec_per_key)
