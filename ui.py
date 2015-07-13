import wx
import wx.grid as wxgrid

ID_TEXTCTRL_ENTER_PRODUCT = 1

class FinalList(wx.Panel):
    def __init__(self, parent, id_):
        wx.Panel.__init__(self, parent, id_)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.Add(self.sizer)

    def refresh(self, data):
        data = {("desserts fr", ""),
                ("jambon", "2x4")}

        self.sizer.DeleteWindows()

        for val, comment in data:
            horiz_sizer = wx.BoxSizer(wx.HORIZONTAL)
            horiz_sizer.Add(wx.StaticText(self.GetParent(), label=val))
            horiz_sizer.Add(wx.StaticText(self.GetParent(), label=comment))
            self.sizer.Add(horiz_sizer)

        self.Layout()

class Frame(wx.Frame):
    def __init__(self, parent, id_, title="Liste de Courses Creator"):
        wx.Frame.__init__(self, parent, id_, title, wx.DefaultPosition)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        right_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(left_sizer)
        main_sizer.Add(right_sizer)
        self.SetSizer(main_sizer)

        # left side: list and input box
        input_box = wx.TextCtrl(self, ID_TEXTCTRL_ENTER_PRODUCT, "Entre un produit", style=wx.TE_PROCESS_ENTER)
        left_sizer.Add(input_box)

        # right side: list itself (with comments), and print button
        final_list = wxgrid.Grid(self)
        final_list.CreateGrid(20, 2)
        final_list.SetRowLabelSize(0)
        final_list.SetColLabelSize(0)
        right_sizer.Add(final_list)

        print_btn = wx.Button(self, -1, "Imprimer")
        right_sizer.Add(print_btn)

class GUI(wx.App):
    def OnInit(self):
        frame = Frame(None, -2)
        frame.Show(True)
        frame.Centre()
        return True
