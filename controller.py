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
        self.model.DBG_add_product_in_first_aisle()
        self.refresh_both_lists()

    def shop_list_clicked(self, item):
        self.model.shop_list_item_toggle(item)
        self.refresh_both_lists()

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