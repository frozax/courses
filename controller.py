#!/usr/bin/python2

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

    def shop_list_clicked(self, item):
        self.model.shop_list_item_toggle(item)
        self.refresh_both_lists()