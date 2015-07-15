#!/usr/bin/python2

import wx

from ui import GUI

def product_text_text_changed(text):
    app.set_status(text, 0)

def product_text_enter_pressed(text):
    app.set_status(text, 0)

app = GUI(
    {
        "product_text_enter_pressed": product_text_enter_pressed,
        "product_text_text_changed": product_text_text_changed
    })

def main():
    app.MainLoop()

if __name__ == '__main__':
    main()
