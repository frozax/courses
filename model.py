#!/usr/bin/python2

import json
import sys

SAVE_FILE = "save.json"

class Model(object):
    def __init__(self):
        # list of aisles
        self.shop = json.load(open("carrefour-vaulx.json"))
        self.aisles = self.shop["rayons"]
        self.orders = self.shop["orders"][0]
        self.order = self.orders["order"]
        aisles_used = [a["name"] for a in self.aisles]
        assert len(set(self.order)) == len(self.order)
        assert len(set(aisles_used)) == len(aisles_used)
        missing_aisles = set(aisles_used) - set(self.order)
        if len(missing_aisles) > 0:
            print "Missing aisles in order: %s" % str(missing_aisles)
            sys.exit(1)

        # sort shop accord to self.order
        self.aisles.sort(key=lambda aisle: self.order.index(aisle["name"]))
        # create products sorted by aisle
        self.sorted_products = []
        for aisle in self.aisles:
            self.sorted_products.extend(aisle.get("products", []))

        # selected items
        self.selected_items = []

        # comment of items (saved apart from the list)
        # comments[item] = "comment"
        self.comments = {}

        self.load(SAVE_FILE)

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
            self.add_item(item)

    def add_item(self, item):
        self.selected_items.append(item)
        self.selected_items.sort(key=lambda product: self.sorted_products.index(product))

    def user_list_remove_item(self, item):
        if item in self.selected_items:
            self.selected_items.remove(item)

    def update_product_comment(self, item, comment):
        self.comments[item] = comment

    def load(self, filename):
        try:
            with open(filename, "r") as f:
                loaded = json.load(f)
                self.comments = loaded["comments"]
                self.selected_items = loaded["selected_items"]
        except IOError:
            pass
        # comments
        # current list

    def save(self, filename=SAVE_FILE):
        with open(filename, "w") as f:
            to_save = {"comments": self.comments, "selected_items": self.selected_items}
            json.dump(to_save, f)

    def DBG_add_product_in_first_aisle(self):
        self.shop["rayons"][0]["products"].append("to")