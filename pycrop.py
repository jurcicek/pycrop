#!//usr/bin/python
# -*-  coding: UTF-8 -*-

##################################################################################################
WXVER = '2.6'
##################################################################################################

# Becasue of deployment by PY2EXE we have to comment out this section.

"""
import wxversion
if wxversion.checkInstalled(WXVER):
    wxversion.select(WXVER)
else:
    import sys, wx, webbrowser
    app = wx.PySimpleApp()
    wx.MessageBox("The requested version of wxPython is not installed.\n\n"
                  "Please install version %s" % WXVER,
                  "wxPython Version Error")
    app.MainLoop()
    webbrowser.open("http://wxPython.org/")
    sys.exit()
"""
    
import xml.dom.minidom, getopt, sys
import wx

import mainframe
#import config 

class PyCrop(wx.App):
    def OnInit(self):
        #load config        
        
        frame = mainframe.MainFrame(None, -1, "Photo Ya Crop - " + imageFileName, imageFileName)
        frame.Center()
        frame.Maximize()
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

###################################################################################################
###################################################################################################

def usage():
    print("""
    Usage:   pycrop [options] file
    
    Description:
             This program crops images. You can either pass a concrete image as
             an argument or the program will process all images from the current 
             directory.
             
             The program uses the tool "convert" from ImageMagic (http://www.imagemagick.org).
             
    Options: 
             -h         : print this help message and exit
             -v         : produce verbose output
             --image    : image file
             
    Keyboard control:
            down        : move the selection down
            up          : move the selection up
            left        : move the selection left
            right       : move the selection right
            +           : zoom in by 5% 
            -           : zoom out by 5% 
            Ctrl +      : zoom in by 1%
            Ctrl -      : zoom out by 1%
            Alt +       : zoom in by 25%
            Alt -       : zoom out by 25%
            Del         : change between landscape and portrait orientation
            Home        : move forward in the list of the preset side ratios 
            End         : move backward in the list of the preset side ratios 
            Enter       : crop the selected image
             """)

###################################################################################################
###################################################################################################

try:
    opts, args = getopt.gnu_getopt(sys.argv[1:], "hv", 
        ["image="])
         
except getopt.GetoptError, exc:
    print("ERROR: " + exc.msg)
    usage()
    sys.exit(2)

imageFileName = "test.jpg"

for o, a in opts:
    if o == "-h":
        usage()
        sys.exit()
    elif o == "-v":
        verbose = True
    elif o == "--image":
        imageFileName = a


app = PyCrop(0)    # Create an instance of the application class
app.MainLoop()     # Tell it to start processing events
