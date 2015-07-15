#!/usr/bin/python2

import json

from ui import GUI

def product_text_text_changed(text):
    app.set_status(text, 0)

def product_text_enter_pressed(text):
    app.set_status(text, 0)

def get_products_list():
    return data.get_products_list()

def get_final_list():
    return [("desserts fr", ""),
            ("jambon", "2x4")]

class Data(object):
    def __init__(self):
        self.data = json.load(open("carrefour-vaulx.json"))

    def get_products_list(self):
        # return list of 3-tuples:
        #  text, selectable (or not), selected (or not)
        return [("75", False, False),
                ("roller", True, False),
                ("45", False, False),
                ("Torchon", True, True)]

data = Data()

app = GUI(
    {
        "product_text_enter_pressed": product_text_enter_pressed,
        "product_text_text_changed": product_text_text_changed,
        "get_products_list": get_products_list,
        "get_final_list": get_final_list
    })

def main():
    app.refresh()
    app.MainLoop()

if __name__ == '__main__':
    main()
