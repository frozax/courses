#!/usr/bin/python2

import json

from view import View
from controller import Controller
from model import Model

def main():
    m = Model()
    v = View()
    c = Controller(m, v)

    v.MainLoop()

if __name__ == '__main__':
    main()
