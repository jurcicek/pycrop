 # -*-  coding: UTF-8 -*-
import xml.dom.minidom
import codecs, platform
import datetime
import os, wx, re, glob, wx.lib.layoutf
import wx.lib.dialogs, wx.lib.layoutf, wx.lib.scrolledpanel

import imagePanel 

class MainFrame(wx.Frame):
    def __init__(
        self, parent, ID, title, imageFileName, 
        pos=wx.DefaultPosition,
        size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE
        ):
        wx.Frame.__init__(self, parent, ID, title, pos, size, style)        

        # image
        self.iPanel = imagePanel.ImagePanel(self, -1)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.iPanel, 1, wx.TOP | wx.BOTTOM | wx.ALL | wx.EXPAND)               

        self.iPanel.LoadImage(imageFileName)
        self.iPanel.SetFocus()
        sizer.Fit(self)
        self.SetSizer(sizer)      
        self.Fit()
        
