import wx
class MyFrame(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, None, title=title, size=(400,600))

        fileMenu = wx.Menu()

        # wx.ID_ABOUT and wx.ID_EXIT are standard ids provided by wxWidgets.
        menuAbout = fileMenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        menuExit = fileMenu.Append(wx.ID_EXIT,"&Exit"," Terminate the program")
        menuOpenFile = fileMenu.Append(wx.ID_OPEN,"&Open"," Open a file")

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu,"&File") # Adding the "filemenu" to the MenuBar

        self.SetMenuBar(menuBar)

        # Set events.
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        #self.Bind(wx.EVT_MENU, self.OnOpen, menuOpenFile)

        self.CreateStatusBar() # A StatusBar in the bottom of the window


    def OnAbout(self,e):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        dlg = wx.MessageDialog( self, "chat", "About chat", wx.OK)
        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished.

    def OnExit(self,e):
        self.Close(True)# Close the frame.