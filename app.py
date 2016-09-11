#!/usr/bin/python3

import json

from view import View
from controller import Controller
from model import Model

def main():
    import os
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    m = Model()
    v = View()
    c = Controller(m, v)

    v.MainLoop()

if __name__ == '__main__':
    main()
