
'''

wxPython Custom Widget Collection 20060207
Written By: Edward Flick (eddy -=at=- cdf-imaging -=dot=- com)
            Michele Petrazzo (michele -=dot=- petrazzo -=at=- unipex -=dot=- it)
            Will Sadkin (wsadkin-=at=- nameconnector -=dot=- com)
Copyright 2006 (c) CDF Inc. ( http://www.cdf-imaging.com )
Contributed to the wxPython project under the wxPython project's license.

Modified by Francois Guibert (www.frozax.com)

'''

import locale, wx, sys

import  wx.lib.mixins.listctrl  as  listmix

class myListCtrl_(wx.SimpleHtmlListBox, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID=-1, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.SimpleHtmlListBox.__init__(self, parent=parent, id=ID, pos=pos, size=size, style=style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)

    def DeleteAllItems(self):
        self.Clear()

    def InsertColumn(self, idx, value):
        pass

    def SetStringItem(self, idx, col_val):
        pass

class myListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID=-1, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)

class TextCtrlAutoComplete(wx.TextCtrl, listmix.ColumnSorterMixin):

    def __init__(self, parent, colNames=None, choices=None,
                 dropDownClick=True,
                 hideOnNoMatch=True,
                 selectCallback=None, entryCallback=None, matchFunction=None,
                 **therest):
        '''
        Constructor works just like wx.TextCtrl except you can pass in a
        list of choices.  You can also change the choice list at any time
        by calling setChoices.
        '''

        if therest.has_key('style'):
            therest['style'] = wx.TE_PROCESS_ENTER | therest['style']
        else:
            therest['style'] = wx.TE_PROCESS_ENTER

        wx.TextCtrl.__init__(self, parent, **therest)

        #Some variables
        self._dropDownClick = dropDownClick
        self._colNames = colNames
        self._choices = choices
        self._lastinsertionpoint = 0
        self._hideOnNoMatch = hideOnNoMatch
        self._selectCallback = selectCallback
        self._entryCallback = entryCallback
        self._matchFunction = matchFunction

        self._screenheight = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_Y)

        #sort variable needed by listmix
        self.itemDataMap = dict()

        #Load and sort data
        if not self._choices:
            raise ValueError, "Pass me choices"

        #widgets
        self.dropdown = wx.PopupWindow(self)

        #Control the style
        flags = wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_SORT_ASCENDING | wx.LC_NO_HEADER

        #Create the list and bind the events
        self.dropdownlistbox = myListCtrl(self.dropdown, style=flags,
                                          pos=wx.Point(0, 0))

        #initialize the parent
        # TODO CHECK SIMPLIFICATION
        ln = 1
        #else: ln = len(choices)
        listmix.ColumnSorterMixin.__init__(self, ln)

        #load the data
        self.SetChoices(choices)

        gp = self
        while gp != None:
            gp.Bind(wx.EVT_MOVE, self.onControlChanged, gp)
            gp.Bind(wx.EVT_SIZE, self.onControlChanged, gp)
            gp = gp.GetParent()

        self.Bind(wx.EVT_KILL_FOCUS, self.onControlChanged, self)
        self.Bind(wx.EVT_TEXT, self.onEnteredText, self)
        self.Bind(wx.EVT_KEY_DOWN, self.onKeyDown, self)

        #If need drop down on left click
        if dropDownClick:
            self.Bind(wx.EVT_LEFT_DOWN, self.onClickToggleDown, self)
            self.Bind(wx.EVT_LEFT_UP, self.onClickToggleUp, self)

        self.dropdown.Bind(wx.EVT_LISTBOX, self.onListItemSelected, self.dropdownlistbox)
        self.dropdownlistbox.Bind(wx.EVT_LEFT_DOWN, self.onListClick)
        self.dropdownlistbox.Bind(wx.EVT_LEFT_DCLICK, self.onListDClick)

        self._ascending = True

    def GetListCtrl(self):
        return self.dropdownlistbox

    # -- event methods
    def onListClick(self, evt):
        toSel, flag = self.dropdownlistbox.HitTest(evt.GetPosition())
        #no values on poition, return
        if toSel == -1:
            return
        self.dropdownlistbox.Select(toSel)

    def onListDClick(self, evt):
        self._setValueFromSelected()

    def onEnteredText(self, event):
        text = event.GetString()

        if self._entryCallback:
            self._entryCallback()

        if not text:
            # control is empty; hide dropdown if shown:
            if self.dropdown.IsShown():
                self._showDropDown(False)
            event.Skip()
            return

        found = False
        choices = self._choices

        for numCh, choice in enumerate(choices):
            if self._matchFunction and self._matchFunction(text, choice):
                found = True
            elif choice.lower().startswith(text.lower()):
                found = True
            if found:
                self._showDropDown(True)
                item = self.dropdownlistbox.GetItem(numCh)
                toSel = item.GetId()
                self.dropdownlistbox.Select(toSel)
                break

        if not found:
            self.dropdownlistbox.Select(self.dropdownlistbox.GetFirstSelected(), False)
            if self._hideOnNoMatch:
                self._showDropDown(False)

        self._listItemVisible()

        event.Skip()

    def onKeyDown(self, event):
        """ Do some work when the user press on the keys:
            up and down: move the cursor
            left and right: move the search
        """
        skip = True
        sel = self.dropdownlistbox.GetFirstSelected()
        visible = self.dropdown.IsShown()

        KC = event.GetKeyCode()
        if KC == wx.WXK_DOWN:
            if sel < (self.dropdownlistbox.GetItemCount() - 1):
                self.dropdownlistbox.Select(sel+1)
                self._listItemVisible()
            self._showDropDown()
            skip = False
        elif KC == wx.WXK_UP:
            if sel > 0:
                self.dropdownlistbox.Select(sel - 1)
                self._listItemVisible()
            self._showDropDown()
            skip = False

        if visible:
            if event.GetKeyCode() == wx.WXK_RETURN:
                self._setValueFromSelected()
                skip = False
            if event.GetKeyCode() == wx.WXK_ESCAPE:
                self._showDropDown(False)
                skip = False
        if skip:
            event.Skip()

    def onListItemSelected(self, event):
        self._setValueFromSelected()
        event.Skip()

    def onClickToggleDown(self, event):
        self._lastinsertionpoint = self.GetInsertionPoint()
        event.Skip()

    def onClickToggleUp(self, event):
        if self.GetInsertionPoint() == self._lastinsertionpoint:
            self._showDropDown(not self.dropdown.IsShown())
        event.Skip()

    def onControlChanged(self, event):
        self._showDropDown(False)
        event.Skip()

    def SetChoices(self, choices):
        '''
        Sets the choices available in the popup wx.ListBox.
        The items will be sorted case insensitively.
        '''
        self._choices = choices
        self._multiChoices = None
        flags = wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_SORT_ASCENDING | wx.LC_NO_HEADER
        self.dropdownlistbox.SetWindowStyleFlag(flags)

        if not isinstance(choices, list):
            self._choices = [x for x in choices]

        #prevent errors on "old" systems
        if sys.version.startswith("2.3"):
            self._choices.sort(lambda x, y: cmp(x.lower(), y.lower()))
        else:
            self._choices.sort(key=lambda x: locale.strxfrm(x).lower())

        self._updateDataList(self._choices)

        self.dropdownlistbox.InsertColumn(0, "")

        for num, colVal in enumerate(self._choices):
            index = self.dropdownlistbox.InsertStringItem(sys.maxint, colVal, -1)
            self.dropdownlistbox.SetStringItem(index, 0, colVal)
            self.dropdownlistbox.SetItemData(index, num)

        self._setListSize()

    def GetChoices(self):
        if self._choices:
            return self._choices
        else:
            return self._multiChoices

    def SetSelectCallback(self, cb=None):
        self._selectCallback = cb

    def SetEntryCallback(self, cb=None):
        self._entryCallback = cb

    def SetMatchFunction(self, mf=None):
        self._matchFunction = mf


    #-- Internal methods
    def _setValueFromSelected(self):
        '''
        Sets the wx.TextCtrl value from the selected wx.ListCtrl item.
        Will do nothing if no item is selected in the wx.ListCtrl.
        '''
        sel = self.dropdownlistbox.GetFirstSelected()
        if sel > -1:
            itemtext = self.dropdownlistbox.GetItem(sel, 0).GetText()
            if self._selectCallback:
                dd = self.dropdownlistbox
                values = [dd.GetItem(sel, 0).GetText()]
                self._selectCallback(values)

            self.SetValue(itemtext)
            self.SetInsertionPointEnd()
            self.SetSelection(-1, -1)
            self._showDropDown(False)


    def _showDropDown(self, show=True):
        '''
        Either display the drop down list (show = True) or hide it (show = False).
        '''
        if show:
            size = self.dropdown.GetSize()
            width, height = self.GetSizeTuple()
            x, y = self.ClientToScreenXY(0, height)
            if size.GetWidth() != width:
                size.SetWidth(width)
                self.dropdown.SetSize(size)
                self.dropdownlistbox.SetSize(self.dropdown.GetClientSize())
            if (y + size.GetHeight()) < self._screenheight:
                self.dropdown.SetPosition(wx.Point(x, y))
            else:
                self.dropdown.SetPosition(wx.Point(x, y - height - size.GetHeight()))
        self.dropdown.Show(show)

    def _listItemVisible(self):
        '''
        Moves the selected item to the top of the list ensuring it is always visible.
        '''
        toSel = self.dropdownlistbox.GetFirstSelected()
        if toSel == -1:
            return
        self.dropdownlistbox.EnsureVisible(toSel)

    def _updateDataList(self, choices):
        #delete, if need, all the previous data
        self.dropdownlistbox.DeleteAllItems()

        #and update the dict
        if choices:
            for numVal, data in enumerate(choices):
                self.itemDataMap[numVal] = data
        else:
            numVal = 0
        self.SetColumnCount(numVal)

    def _setListSize(self):
        if self._multiChoices:
            choices = self._multiChoices
        else:
            choices = self._choices

        longest = 0
        for choice in choices:
            longest = max(len(choice), longest)

        longest += 3
        itemcount = min(len(choices), 7) + 2
        charheight = self.dropdownlistbox.GetCharHeight()
        charwidth = self.dropdownlistbox.GetCharWidth()
        self.popupsize = wx.Size(charwidth * longest, charheight * itemcount)
        self.dropdownlistbox.SetSize(self.popupsize)
        self.dropdown.SetClientSize(self.popupsize)
