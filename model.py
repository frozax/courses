#!/usr/bin/python2

import json

class Model(object):
    def __init__(self):
        # list of aisles
        self.shop = json.load(open("carrefour-vaulx.json"))
        #self.shop = json.load(open("simple-shop.json"))

        # selected items
        self.selected_items = ["desserts fr", "jambon", "roller", "melon", "tomate"]

        # comment of items (saved apart from the list)
        # comments[item] = "comment"
        self.comments = {}

    def get_user_list(self):
        return [(a, self.comments.get(a, "")) for a in self.selected_items]

    def clear_user_list(self):
        self.selected_items = []

    def get_shop_list(self):
        # return list of 3-tuples:
        #  text, selectable (or not), selected (or not)
        ret = []
        for aisle in self.shop["rayons"]:
            if "name" in aisle and "products" in aisle:
                ret.append((aisle["name"], "aisle-name"))
                for p in aisle["products"]:
                    ret.append((p, "product" if p not in self.selected_items else "selected-product"))
                ret.append(("", "spacer"))
        return ret

    def shop_list_item_toggle(self, item):
        if item in self.selected_items:
            self.selected_items.remove(item)
        else:
            self.selected_items.append(item)

    def user_list_remove_item(self, item):
        if item in self.selected_items:
            self.selected_items.remove(item)

    def update_product_comment(self, item, comment):
        self.comments[item] = comment

    def DBG_add_product_in_first_aisle(self):
        self.shop["rayons"][0]["products"].append("to")