#!/usr/bin/python2
# encoding: utf-8

import os
import webbrowser

class Controller(object):
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.setup_controller(self)
        self.view.setup_shop_list(self.model.get_shop_list())
        self.refresh_both_lists()

    def update_shop_list_colors(self, autocomplete_items=None):
        self.view.update_shop_list_colors(self.model.get_shop_list_details(autocomplete_items))

    def refresh_both_lists(self):
        self.view.refresh_user_list(self.model.get_user_list())
        self.update_shop_list_colors()

    def shop_list_clicked(self, item):
        selected = self.model.shop_list_item_toggle(item)
        self.view.refresh_user_list(self.model.get_user_list())
        return selected

    def user_list_comment_entered(self, item, comment):
        self.model.update_product_comment(item, comment)

    def user_list_clicked(self, item):
        self.model.user_list_remove_item(item)
        self.refresh_both_lists()

    def new_list(self):
        self.model.clear_user_list()
        self.refresh_both_lists()

    def exit(self):
        # app is exited
        self.model.save()

    def enter_product_text_entered(self, text):
        html_list, item_list = self.model.compute_auto_complete_list(text)
        self.view.frame.enter_product.SetChoices(html_list)
        self.update_shop_list_colors(item_list)

    def enter_product_enter_pressed(self, text):
        self.add_item_to_user_list(text)
        self.refresh_both_lists()
        self.view.frame.enter_product.select_all()

    def add_item_to_user_list(self, item):
        if not self.model.exists(item):
            if self.view.msg_box_yesno(u"Ajouter %s à la liste?" % item):
                self.model.add_item_to_shop_list_temporarily(item)
            else:
                return None
        self.model.add_item(item)

    def enter_product_item_selected_from_list(self, item):
        real_item_name = self.model.get_real_item_name_from_list_item(item)
        self.add_item_to_user_list(real_item_name)
        self.refresh_both_lists()
        return real_item_name

    def print_pressed(self):
        # gen html
        html = self.model.generate_html_user_list()
        #with tempfile.TemporaryDirectory() as d:
        d = "/tmp"
        fname = os.path.join(d, "list.html")
        f = open(fname, "w")
        f.write(html.encode("utf-8"))
        f.close()
        webbrowser.open("file://%s" % fname)

    def save(self):
        self.model.save()
