#!/usr/bin/python2

import json

import wx

class Model(object):
    def __init__(self):
        # list of aisles
        self.shop = json.load(open("carrefour-vaulx.json"))

        # selected items
        self.selected_items = ["desserts fr", "jambon"]

        # comment of items (saved apart from the list)
        # comments[item] = "comment"
        self.comments = {}

    def get_user_list(self):
        return [(a, self.comments.get(a, "")) for a in self.selected_items]

    def get_shop_list(self):
        # return list of 3-tuples:
        #  text, selectable (or not), selected (or not)
        return [("75", False, False),
                ("roller", True, False),
                ("45", False, False),
                ("Torchon", True, True)]

    def shop_list_item_toggle(self, item):
        if item in self.selected_items:
            self.selected_items.remove(item)
        else:
            self.selected_items.append(item)

