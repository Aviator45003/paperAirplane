# Draw us a pretty window for the pretty teenagers.
import logging
import getpass
import getuser
import wx
import time

class PageDisplay(wx.Frame):
    ''' For showing page count, username, and a link to the server page. '''
    def __init__(self, parent=None, user=getuser.lookup_username(), title='Balance for _USER_'):
        title = title.replace('_USER_', user)
        # Initial
        wx.Frame.__init__(self, parent, title=title, size=(200,100))
        self.panel = wx.Panel(self)

        # Sizer setup
        self.sizer = wx.GridBagSizer(vgap=5, hgap=2)

        # Page count setup
        self.pageCount = 45003
        self.displayCount = wx.StaticText(
                    self.panel, label='45003'
                )
        font = wx.Font(
                    pointSize=30, style=wx.FONTSTYLE_NORMAL,
                    family=wx.FONTFAMILY_ROMAN, weight=wx.FONTWEIGHT_BOLD
                )
        self.displayCount.SetFont(font)
        # Add to sizer
        self.sizer.Add(
                    self.displayCount, pos=(1,1),
                    flag = wx.EXPAND | wx.ALIGN_RIGHT,
                    span = wx.GBSpan(rowspan=1, colspan=2)
                )

        # Hyperlink to Be
        url = 'http://beryllium:9191/user?username='+user
        self.detailsLink = wx.HyperlinkCtrl(
                    self.panel, url=url, label='Details...'
                )
        # Add to sizer
        self.sizer.Add(
                    self.detailsLink, pos=(2,3),
                    flag = wx.EXPAND | wx.ALIGN_RIGHT,
                    span = wx.GBSpan(rowspan=1, colspan=1)
                )

        # Run
        self.panel.SetSizer(self.sizer)
        self.Show(True) # Yes, I want to show you off to THE WORLD!

    def update_count(self):
        self.modify(value=self.pageCount)

    def modify(self, event, value='45003'):
        self.pageCount = value;
        self.displayCount.SetLabel(value)

def RunGui():
    app = wx.App(False)  # Create a new app, don't redirect stdout/stderr to GUI
    mainWindow = PageDisplay()
    # wxPython calls Window the base class from which visual objects are derived
    # A FRAME is what we luddites call a window
    # Obvious, isn't it?
    app.MainLoop() # Start to handle events.

if __name__ == "__main__":
    RunGui()
