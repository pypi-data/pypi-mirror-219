import pyautogui as pa
from time import *
from random import *

screen_width, screen_height = pa.size()


def win_go():
    pa.press('win')


def taskmenager_go():
    pa.hotkey('ctrl', 'shift', 'esc')


def file_go():
    pa.hotkey('ctrl', 'n')


def window_hover():
    pa.hotkey('alt', 'space')


def taskbarapps_hover():
    pa.hotkey('ctrl', 't')


def run_go():
    pa.hotkey('win', 'r')


def rotatescreen_go():
    direction = choice(['up', 'down', 'right', 'left'])
    pa.hotkey('altright', direction)


def filemenager_go():
    pa.hotkey('win', 'e')


def opentaskbarapps_go():
    pa.hotkey('win', f'{round(randint(1,9))}')


def starting():
    sleep(2)
    pa.hotkey('win', 'r')
    sleep(0.1)
    pa.write('cmd')
    sleep(0.1)
    pa.press('enter')
    sleep(0.3)
    pa.press('f11')
    sleep(0.3)
    pa.write('color a')
    sleep(0.3)
    pa.press('enter')
    sleep(0.2)
    pa.write('Ready..', interval=0.55)
    sleep(1)
    for i in range(8):
        pa.press('backspace')
        sleep(0.12)
    sleep(1)
    pa.write('die...', interval=0.3)
    sleep(2)
    for i in range(19):
        pa.press('backspace')
    sleep(0.9)
    pa.write('dir/s', interval=0.2)
    pa.press('enter')
    sleep(17)
    pa.hotkey('ctrl', 'c')
    sleep(0.5)
    pa.hotkey('alt', 'f4')
    sleep(0.5)

    while True:
        my_list = [win_go, taskmenager_go, file_go, window_hover, taskbarapps_hover,
                   run_go,  rotatescreen_go, filemenager_go, opentaskbarapps_go]
        choice(my_list)()
        choice(my_list)()
        pa.moveTo(randint(1, screen_width), randint(
            1, screen_height), duration=0.01)
        pa.doubleClick()


if __name__ == '__main__':
    starting()

# amine_was_here
