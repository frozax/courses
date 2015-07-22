# encoding: utf8

import wx
import wx.lib.scrolledpanel as scrolled
from TextCtrlAutoComplete import TextCtrlAutoComplete

class SampleWindow(wx.PyWindow):
    """
    A simple window that is used as sizer items in the tests below to
    show how the various sizers work.
    """
    def __init__(self, parent, text, pos=wx.DefaultPosition, size=wx.DefaultSize):
        wx.PyWindow.__init__(self, parent, -1,
                             #style=wx.RAISED_BORDER
                             #style=wx.SUNKEN_BORDER
                             style=wx.SIMPLE_BORDER
                             )
        self.text = text
        if size != wx.DefaultSize:
            self.bestsize = size
        else:
            self.bestsize = (80,25)
        self.SetSize(self.GetBestSize())

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)

    def OnPaint(self, evt):
        sz = self.GetSize()
        dc = wx.PaintDC(self)
        w,h = dc.GetTextExtent(self.text)
        dc.Clear()
        dc.DrawText(self.text, (sz.width-w)/2, (sz.height-h)/2)

    def OnSize(self, evt):
        self.Refresh()

    def DoGetBestSize(self):
        return self.bestsize

class ShopList(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        # horiz sizer full of vert sizers
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.sizer)
        #self.SetBackgroundColour((127, 127, 255))

        #btn = wx.Button(self, label="toto")
        #self.sizer.Add(btn, 1, wx.EXPAND)

        self.click_callback = None
        self.header_font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)

    def set_callback(self, cbk):
        self.click_callback = cbk

    def click_product(self, event):
        eo = event.GetEventObject()
        text = eo.GetLabel()
        self.click_callback(text)

    def set_data(self, data):
        self.sizer.Clear(True)
        max_y_size = self.GetSize()[1]
        #remaining_size_x, init_remaining_size_y = self.parent.GetSize()
        nb_items_vertically = 50
        remaining_y = nb_items_vertically
        cur_sizer = wx.BoxSizer(wx.VERTICAL)

        # add all products
        for product, type_ in data:
            if type_ == "spacer":
                ctrl = wx.StaticText(self, label=" ")
            else:
                style = wx.ALIGN_RIGHT
                ctrl = wx.StaticText(self, label=product, style=style, size=(130, -1))
                if "product" in type_:
                    ctrl.Bind(wx.EVT_LEFT_DOWN, self.click_product)
                    if "selected" in type_:
                        ctrl.SetForegroundColour((0, 180, 0))
                elif type_ == "aisle-name":
                    ctrl.SetFont(self.header_font)

            remaining_y -= 1
            if remaining_y == 0:
                # sizer virtically full, add it
                self.sizer.Add(cur_sizer, 0, wx.EXPAND)
                remaining_y = nb_items_vertically
                cur_sizer = wx.BoxSizer(wx.VERTICAL)

            cur_sizer.Add(ctrl, 0)

        # add the last sizer
        if cur_sizer:
            self.sizer.Add(cur_sizer, 0, wx.EXPAND)

        self.parent.Layout()


class UserList(scrolled.ScrolledPanel):
    def __init__(self, parent):
        scrolled.ScrolledPanel.__init__(self, parent)
        self.parent = parent
        #self.SetBackgroundColour((128, 255, 128))
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        self.set_data({})
        self.SetupScrolling(scroll_x=False)
        self.comment_entered = None
        self.item_clicked_cbk = None

    def set_callbacks(self, comment_entered, item_clicked):
        self.comment_entered_cbk = comment_entered
        self.item_clicked_cbk = item_clicked

    def _add_line(self, val, comment):
        horiz_sizer = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(self, label=val)
        text.Bind(wx.EVT_LEFT_DOWN, lambda evt: self.item_clicked_cbk(text.GetLabel()))
        horiz_sizer.Add(text, proportion=1)
        if comment is not None:
            comment_ctrl = wx.TextCtrl(self, value=comment, size=(40, -1))
            comment_ctrl.Bind(wx.EVT_TEXT,
                lambda evt: self.comment_entered_cbk(val, comment_ctrl.GetValue()))
            horiz_sizer.Add(comment_ctrl, proportion=0)
        self.sizer.Add(horiz_sizer, flag=wx.EXPAND)

    def set_data(self, data):
        self.sizer.Clear(True)
        if len(data) == 0:
            self._add_line("", None)
        else:
            for val, comment in data:
                self._add_line(val, comment)

        self.parent.Layout()
        self.Layout()

class Frame(wx.Frame):

    def __init__(self, title):
        wx.Frame.__init__(self, None, title=title)

        self.new_list_cbk = None

        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour((255, 128, 128))
        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # left side: product list and search box
        self.left_side = wx.BoxSizer(wx.VERTICAL)
        self.shop_list = ShopList(self.panel)

        self.left_side.Add(self.shop_list, 1, wx.EXPAND)
        self.enter_product = TextCtrlAutoComplete(self.panel)
        self.left_side.Add(self.enter_product, 0, wx.EXPAND)

        self.main_sizer.Add(self.left_side, 1, wx.EXPAND|wx.ALL, 4)

        self.right_side = wx.BoxSizer(wx.VERTICAL)
        self.user_list = UserList(self.panel)
        self.right_side.Add(self.user_list, 1, wx.EXPAND)
        # add something to sort
        user_list_sort_sizer = wx.BoxSizer(wx.HORIZONTAL)
        user_list_sort_sizer.Add(wx.StaticText(self.panel, 0, "Tri:"), 0, wx.EXPAND)
        self.user_list_sort = wx.ComboBox(self.panel, choices=["alphabétique", "magasin"], style=wx.CB_READONLY)
        user_list_sort_sizer.Add(self.user_list_sort, 1, wx.EXPAND)
        self.right_side.Add(user_list_sort_sizer, 0, wx.EXPAND)

        self.main_sizer.Add(self.right_side, 0, wx.EXPAND|wx.TOP|wx.BOTTOM|wx.RIGHT, 4)

        self.panel.SetSizer(self.main_sizer)
        self.main_sizer.Fit(self.panel)

        self.CreateStatusBar()
        self.tool_bar = self.CreateToolBar()
        tsize = (24, 24)
        self.tool_bar.SetToolBitmapSize(tsize)
        new_bmp = wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, tsize)
        new_tool = self.tool_bar.AddLabelTool(0, "new", new_bmp)
        def yes_no(event):
            dlg = wx.MessageDialog(self.panel, "Effacer la liste?", "Effacer la liste?", wx.YES_NO | wx.ICON_QUESTION)
            result = dlg.ShowModal() == wx.ID_YES
            dlg.Destroy()
            if result:
                self.new_list_cbk()
        self.Bind(wx.EVT_TOOL, yes_no, new_tool)
        print_bmp = wx.ArtProvider.GetBitmap(wx.ART_PRINT, wx.ART_TOOLBAR, tsize)
        self.tool_bar.AddLabelTool(1, "print", print_bmp)
        self.tool_bar.Realize()


class View(wx.App):
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
        #self.frame.search_ctrl.Bind(wx.EVT_TEXT,
        #                             lambda evt: controller.product_text_text_changed(self.product_text.GetValue()))
        #self.frame.search_ctrl.Bind(wx.EVT_TEXT_ENTER,
        #                             lambda evt: controller.product_text_enter_pressed(self.product_text.GetValue()))
        #self.frame.print_btn.Bind(wx.EVT_BUTTON,
        #                          lambda evt: controller.print_pressed())
        self.frame.shop_list.set_callback(controller.shop_list_clicked)
        self.frame.user_list.set_callbacks(controller.user_list_comment_entered,
                                           controller.user_list_clicked)

        self.frame.new_list_cbk = controller.new_list
        self.frame.Bind(wx.EVT_CLOSE, self.exit)
        self.frame.enter_product.SetEntryCallback(controller.enter_product_text_entered)
        self.exit_cbk = controller.exit

    def exit(self, event):
        self.exit_cbk()
        self.frame.Destroy()

    def msg_box(self, text):
        dlg = wx.MessageDialog(self.frame, text, "Message Box", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def set_user_list_sort(self, sort_type):
        pass
