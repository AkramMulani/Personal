"""
    This script is experimental and for educational purpose
    please do not use it for wrong purposes
    @author:    Akram Mulani
"""
import threading

import command_line
import gui_interface


def print_hi(name):
    print(f'Hi, {name}')


if __name__ == '__main__':
    print_hi('PyCharm')
    # command_line.init()
    gui_interface.start()
