import wx
import os
from frame import *
from panel import *

class MyApp(wx.App):
	def OnInit(self):
		window = MyFrame('chat0.0')
		panel = MyPanel(window)
		window.Show(True)
		self.SetTopWindow(window)
		return True
app = MyApp()
app.MainLoop()
