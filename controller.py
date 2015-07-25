#!/usr/bin/python2
# encoding: utf-8

import os
import webbrowser

class Controller(object):
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.setup_controller(self)
        self.refresh_both_lists()

    def refresh_both_lists(self):
        self.view.refresh_user_list(self.model.get_user_list())
        self.view.refresh_shop_list(self.model.get_shop_list())

    def print_pressed(self):
        self.view.set_status("print pressed")
        self.model.DBG_add_product_in_first_aisle()
        self.refresh_both_lists()

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
        l = self.model.compute_auto_complete_list(text)
        self.view.frame.enter_product.SetChoices(l)

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
        print type(html)
        f.write(html.encode("utf-8"))
        f.close()
        webbrowser.open("file://%s" % fname)

    def save(self):
        self.model.save()