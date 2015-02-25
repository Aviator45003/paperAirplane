# Draw us a pretty window for the pretty teenagers.
# We will need 2 classes and a function.
# 1 is our wxFrame class.
#   Important simply to define what our window looks like.
# Then we need a thread to run this window.
#   That's actually a function.
# Finally, we have a thread that updates the counter variable on the window.
#   That must be another thread because the window hogs the thread.

import Queue
import threading
import logging
import getpass
import getuser
import wx
import time

# Just a constant we can pop on a queue and kill threads with.
EXIT_CODE = -0xDEADBEEF

# Class 1.
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
        ''' If we could edit self.pageCount, this shows the change'''
        self.modify(value=self.pageCount)

    def modify(self, value='45003'):
        '''Modify the shown value.'''
        self.pageCount = value;
        self.displayCount.SetLabel(value)

def update_visual_count(page_display, queue):
    '''Update tracker. Wait for queue update, then process. A thread.'''
    while True:
        elem = queue.get() # Block until there is an element.
        if elem == EXIT_CODE: # In event of exit code passed to us
            break;
        # wx.CallAfter is thread-safe and uses the GUI thread to execute calls.
        wx.CallAfter(page_display.modify, elem)
        queue.task_done() # In case someone wants to (How polite!) join() the queue
    wx.CallAfter(page_display.Close)
    return 0


def run_window(update_queue):
    '''Set up our window thread and a messaging thread and let them die nicely'''
    app = wx.App(False)  # Create a new app, don't redirect stdout/stderr to GUI
    mainWindow = PageDisplay()
    # wxPython calls Window the base class from which visual objects are derived
    # A FRAME is what we luddites call a window
    # Obvious, isn't it?
    windowThread = threading.Thread(target=app.MainLoop) # Start to handle events.
    updateThread = threading.Thread(
                        target=update_visual_count,
                        args=(mainWindow, update_queue)
                    ) # And updates are possible.

    windowThread.start()
    updateThread.start()
    windowThread.join() # After the window quits...
    update_queue.put(EXIT_CODE) #Pop in a nice exit code.
    updateThread.join()

# Start in debug mode
if __name__ == "__main__":
    q = Queue.Queue()
    thread = threading.Thread(target=run_window, args=(q,))
    thread.start()
    for i in reversed(xrange(0,45003)):
        if thread.isAlive(): # Otherwise we are doing nothing.
            time.sleep(0.0001)
            print(i)
            q.put(str(i))
    time.sleep(10)
    q.put(EXIT_CODE)
    thread.join()
