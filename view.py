import wx

class ShopList(wx.BoxSizer):
    def __init__(self, parent):
        wx.BoxSizer.__init__(self, wx.VERTICAL)
        self.parent = parent
        self.click_callback = None

    def set_callback(self, cbk):
        self.click_callback = cbk

    def click_product(self, event):
        eo = event.GetEventObject()
        text = eo.GetLabel()
        self.click_callback(text)

    def set_data(self, data):
        self.DeleteWindows()
        for text, selectable, selected in data:
            st = wx.StaticText(self.parent, label=text)
            if selectable:
                st.Bind(wx.EVT_LEFT_DOWN, self.click_product)
            self.Add(st)

        self.parent.Fit()


class UserList(wx.BoxSizer):
    def __init__(self, parent):
        wx.BoxSizer.__init__(self, wx.VERTICAL)
        self.parent = parent

    def set_data(self, data):
        self.DeleteWindows()

        for val, comment in data:
            horiz_sizer = wx.BoxSizer(wx.HORIZONTAL)
            horiz_sizer.Add(wx.StaticText(self.parent, label=val))
            horiz_sizer.Add(wx.TextCtrl(self.parent, value=comment))
            self.Add(horiz_sizer)

        self.parent.Fit()

class Frame(wx.Frame):

    def __init__(self, title):
        wx.Frame.__init__(self, None, title=title)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        right_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(left_sizer)
        main_sizer.Add(right_sizer)
        self.SetSizer(main_sizer)

        # right side: list itself (with comments), and print button
        self.user_list = UserList(self)
        right_sizer.Add(self.user_list)

        # left side: list and input box
        self.shop_list = ShopList(self)
        left_sizer.Add(self.shop_list)

        self.product_text = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.product_text.SetHint("Entre un produit")
        left_sizer.Add(self.product_text)

        self.print_btn = wx.Button(self, -1, "Imprimer")
        right_sizer.Add(self.print_btn)

        self.CreateStatusBar()


class View(wx.App):
    def __init__(self):
        # create app
        wx.App.__init__(self)

    def OnInit(self):
        self.frame = Frame("Liste de Courses Creator")
        self.frame.Show(True)
        self.frame.Centre()
        return True

    def set_status(self, status):
        self.frame.GetStatusBar().SetStatusText(status)

    def refresh_user_list(self, l):
        self.frame.user_list.set_data(l)

    def refresh_shop_list(self, l):
        self.frame.shop_list.set_data(l)

    def setup_controller(self, controller):
        # set up callbacks for user interactions
        self.frame.product_text.Bind(wx.EVT_TEXT,
                                     lambda evt: controller.product_text_text_changed(self.product_text.GetValue()))
        self.frame.product_text.Bind(wx.EVT_TEXT_ENTER,
                                     lambda evt: controller.product_text_enter_pressed(self.product_text.GetValue()))
        self.frame.print_btn.Bind(wx.EVT_BUTTON,
                                  lambda evt: controller.print_pressed())
        self.frame.shop_list.set_callback(controller.shop_list_clicked)

    def msg_box(self, text):
        dlg = wx.MessageDialog(self.frame, text, "Message Box", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
