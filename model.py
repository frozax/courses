#!/usr/bin/python2
# coding: utf-8

import json
import sys
import unidecode

SAVE_FILE = "save.json"
HTML_START = "<b><u>"
HTML_END = "</u></b>"

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

        # list of products without special caracters for auto_complete
        self.sorted_products_without_special_chars = [self.remove_special_chars(a) for a in self.sorted_products]

        # selected items
        self.selected_items = []

        # comment of items (saved apart from the list)
        # comments[item] = "comment"
        self.comments = {}

        self.load(SAVE_FILE)

    def remove_special_chars(self, text):
        return unidecode.unidecode(text)

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
            return False
        else:
            self.add_item(item)
            return True

    def add_item_to_shop_list_temporarily(self, item):
        self.sorted_products.insert(0, item)
        self.sorted_products_without_special_chars.insert(0, self.remove_special_chars(item))

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
                # check temp items
                for item in self.selected_items:
                    if not self.exists(item):
                        self.add_item_to_shop_list_temporarily(item)

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

    def compute_auto_complete_list(self, text):
        MAX_LIST_SIZE = 20
        t = self.remove_special_chars(text)
        if len(t) == 0:
            return []
        else:

            def htmlize(text, index, length):
                return text[:index] + HTML_START + text[index:index + length] + HTML_END + text[index + length:]

            # find all items starting with text
            l1 = []
            l2 = []
            for i, a in enumerate(self.sorted_products_without_special_chars):
                found = a.find(t)
                if found != -1:
                    if found == 0:
                        list_to_add_to = l1
                    else:
                        list_to_add_to = l2
                    list_to_add_to.append(htmlize(self.sorted_products[i], found, len(t)))

            l = l1[:MAX_LIST_SIZE]
            cur_len = len(l)
            if cur_len < MAX_LIST_SIZE:
                l.extend(l2[:MAX_LIST_SIZE-cur_len])

            return l

    def get_real_item_name_from_list_item(self, item):
        new_item = item.replace(HTML_START, "").replace(HTML_END, "")
        return new_item

    def exists(self, item):
        return item in self.sorted_products

    def generate_html_user_list(self):
        def get_aisle_from_product(item):
            for aisle in self.aisles:
                if item in aisle.get("products", []):
                    return aisle["name"]
            return None

        def enc(text):
            return text.encode('ascii', 'xmlcharrefreplace')

        html = u"<html><p style=\"font-family: Arial\">"
        prev_aisle = None
        for item in self.selected_items:
            aisle = get_aisle_from_product(item)
            if aisle != prev_aisle:
                html += u"<h2 style=\"font-size: small; font-family: arial; margin-bottom: 0px; margin-top: 3px;\">%s</h2>" % enc(aisle)
                prev_aisle = aisle
            html += u"<p style=\"font-size: small; font-family: arial; margin: 0px; margin-left: 10px;\">%s %s</p>" % (enc(item), enc(self.comments.get(item, u"")))

        html += u"</p></html>"

        return html