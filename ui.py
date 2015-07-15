import wx


class FinalList(wx.BoxSizer):
    def __init__(self, parent):
        wx.BoxSizer.__init__(self, wx.VERTICAL)
        self.parent = parent

    def refresh(self, data):
        data = [("desserts fr", ""),
                ("jambon", "2x4")]

        self.DeleteWindows()

        for val, comment in data:
            horiz_sizer = wx.BoxSizer(wx.HORIZONTAL)
            horiz_sizer.Add(wx.StaticText(self.parent, label=val))
            horiz_sizer.Add(wx.TextCtrl(self.parent, value=comment))
            self.Add(horiz_sizer)

        self.Layout()

class Frame(wx.Frame):

    def product_text_text_changed(self, event):
        text = event.GetEventObject().GetValue()
        text2 = self.product_text.GetValue()
        print "ta", text, "ta", text2
        auto_completion_list = self.callbacks["product_text_text_changed"](text)

    def product_text_enter_pressed(self, event):
        text = event.GetEventObject().GetValue()
        self.callbacks["product_text_enter_pressed"](text)

    def __init__(self, title, callbacks):
        self.callbacks = callbacks
        wx.Frame.__init__(self, None, title=title)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        right_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(left_sizer)
        main_sizer.Add(right_sizer)
        self.SetSizer(main_sizer)

        # left side: list and input box
        self.product_text = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.product_text.SetHint("Entre un produit")
        self.product_text.Bind(wx.EVT_TEXT, self.product_text_text_changed)
        self.product_text.Bind(wx.EVT_TEXT_ENTER, self.product_text_enter_pressed)
        left_sizer.Add(self.product_text)

        # right side: list itself (with comments), and print button
        final_list = FinalList(self)
        final_list.refresh({})
        right_sizer.Add(final_list)

        print_btn = wx.Button(self, -1, "Imprimer")
        right_sizer.Add(print_btn)

        self.CreateStatusBar()


class GUI(wx.App):
    def __init__(self, callbacks):
        self.callbacks = callbacks
        wx.App.__init__(self)

    def OnInit(self):
        self.frame = Frame("Liste de Courses Creator", self.callbacks)
        self.frame.Show(True)
        self.frame.Centre()
        return True

    def set_status(self, status, ith):
        self.frame.GetStatusBar().SetStatusText(status, ith)
