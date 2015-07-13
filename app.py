#!/usr/bin/python2

import wx

from ui import GUI, ID_TEXTCTRL_ENTER_PRODUCT

def toto(event):
    print "TOTO"

def main():
    app = GUI()
    app.Bind(wx.EVT_TEXT_ENTER, toto, id=ID_TEXTCTRL_ENTER_PRODUCT)
    app.MainLoop()

if __name__ == '__main__':
    main()
