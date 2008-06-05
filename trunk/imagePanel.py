 # -*-  coding: UTF-8 -*-
 
import os, wx, commands

MOVE_STEP = 0.05
SCALE_STEP = 0.05
FINE_SCALE = 0.2

class ImagePanel(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id, style = wx.WANTS_CHARS)
        
        self.image = None  # wxPython image
        self.sizeList = ((10.0,15.0), (13.0,18.0), (15.0, 21.0), (20.0,30.0), (30.0,45.0), (320, 240))
        self.sizeIndex = 0
        self.sizeRotation = 1
        self.siSize = (0,0)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_CHAR, self.OnChar)

        self.SetBackgroundColour('black')

    def LoadImage(self, imageFileName):
        self.imageFileName = imageFileName
        self.image = wx.Image(imageFileName)
        self.imSize = self.image.GetSize()

        self.SetRSize()
        self.rCenter = [0, 0]
        self.rZoom = 0.6
        
        self.Refresh(True)

    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        
        if self.image:
            dcSize = dc.GetSize()
            self.dcSize = dcSize 
            
            # process the image
           
            wRatio = float(dcSize[0]) / self.imSize[0]
            hRatio = float(dcSize[1]) / self.imSize[1]
            
            # scale the image, but keap the ratio
            if wRatio > hRatio:
                scl = hRatio
            else:
                scl = wRatio
            
            self.siScale = scl
            scaledSize = (self.imSize[0]*scl, self.imSize[1]*scl)
            
            if self.siSize != scaledSize:
                # scale image only if there is a change of the target size 
                self.sImage = self.image.Scale(scaledSize[0], scaledSize[1])
                
            # center the image
            topLeft = ((dcSize[0] - scaledSize[0])/2, (dcSize[1] - scaledSize[1])/2)
            
            # print the image
            self.siSize = scaledSize
            self.siTopLeft = topLeft

            dc.DrawBitmapPoint(self.sImage.ConvertToBitmap(), topLeft)

            self.AssertRectangle(scaledSize)

            # process the rectangle
            wRatio = float(scaledSize[0]) / self.rSize[0]
            hRatio = float(scaledSize[1]) / self.rSize[1]

            # scale the retangle, but keap the ratio and the zoom
            if wRatio > hRatio:
                scl = hRatio*self.rZoom
            else:
                scl = wRatio*self.rZoom
                
            scaledSize = (self.rSize[0]*scl, self.rSize[1]*scl)
            scaledCenter = ((self.rCenter[0] + 1)*dcSize[0]/2, (self.rCenter[1] + 1)*dcSize[1]/2)
            
            # place the rectangle
            topLeft = (scaledCenter[0] - scaledSize[0]/2, scaledCenter[1] - scaledSize[1]/2)
            self.srSize = scaledSize
            self.srTopLeft = topLeft

            # print the retangle
            dc.SetBrush(wx.Brush('white', wx.TRANSPARENT))
            
            dc.SetPen(wx.Pen('red', 1))
            dc.DrawRectanglePointSize(topLeft, scaledSize)
            
            dc.SetPen(wx.Pen('black', 1))
            dc.DrawRectangle(topLeft[0] - 1, topLeft[1] - 1, scaledSize[0] + 2, scaledSize[1] + 2)
            dc.DrawRectangle(topLeft[0] + 1, topLeft[1] + 1, scaledSize[0] - 2, scaledSize[1] - 2)
            
            # print the crop ratio
            str = "%d x %d" % (self.sizeList[self.sizeIndex][0], self.sizeList[self.sizeIndex][1])
            
            fnt = wx.FFontFromPixelSize((scaledSize[0] / 5,scaledSize[0] / 5), wx.FONTFAMILY_DEFAULT)
            dc.SetFont(fnt)
            strSize = dc.GetTextExtent(str)
            dc.SetTextForeground('red')
            dc.DrawText(str, scaledCenter[0] - strSize[0]/2, scaledCenter[1] - strSize[1]/2)


    def OnChar(self, event):
        kc = event.GetKeyCode() 
        
        # print kc
        
        if kc < 200:
            kcc = chr(kc).upper()
        else:
            kcc = ""
            
        if event.ControlDown():
            fine = FINE_SCALE
        elif event.AltDown():
            fine = 1/FINE_SCALE
        else:
            fine = 1.0
        
        if kc == wx.WXK_LEFT:
            self.rCenter[0] -= MOVE_STEP*fine
        elif kc == wx.WXK_RIGHT:
            self.rCenter[0] += MOVE_STEP*fine
        elif kc == wx.WXK_UP:
            self.rCenter[1] -= MOVE_STEP*fine
        elif kc == wx.WXK_DOWN:
            self.rCenter[1] += MOVE_STEP*fine
        elif kc == wx.WXK_DELETE:
            if self.sizeRotation:
                self.sizeRotation = 0
                self.rZoom *= float(self.imSize[0]) / self.imSize[1]
            else:
                self.sizeRotation = 1
                self.rZoom *= float(self.imSize[1]) / self.imSize[0]
            self.SetRSize()

        elif kc == wx.WXK_END:
            # retotate forward in list of ratios
            self.sizeIndex += 1
            if self.sizeIndex == len(self.sizeList):
                self.sizeIndex = 0
            self.SetRSize()
        
        elif kc == wx.WXK_HOME:
            # retotate back in list of ratios
            self.sizeIndex -= 1
            if self.sizeIndex == -1:
                self.sizeIndex = len(self.sizeList) - 1
            self.SetRSize()
        
        elif kc == wx.WXK_RETURN:
            # crop image
            self.CropImage()
            pass
            
        elif kcc == '+':
            self.rZoom *= 1 + SCALE_STEP*fine
        elif kcc == '-':
            self.rZoom /= 1 + SCALE_STEP*fine
        else:
            event.Skip()

        self.Refresh(True)
        
    def AssertRectangle(self, x):
        if self.rZoom >= 1:
            self.rZoom = 1.0
            if self.sizeRotation:
                self.rCenter[0] = 0.0
            else:
                self.rCenter[1] = 0.0
        elif self.rZoom < 0.1:
            self.rZoom = 0.1
        
        if self.rCenter[0] > 1:
            self.rCenter[0] = 1
        elif self.rCenter[0] < -1:
            self.rCenter[0] = - 1
        elif self.rCenter[1] > 1:
            self.rCenter[1] = 1
        elif self.rCenter[1] < -1:
            self.rCenter[1] = - 1
        
    def SetRSize(self):
        self.rSize = self.sizeList[self.sizeIndex]
        
        if self.sizeRotation:
            self.rSize = (self.rSize[1], self.rSize[0])
            
    def CropImage(self):
        self.srSize
        self.srTopLeft
        
        self.siSize
        self.siTopLeft

        cropTopLeft = (self.srTopLeft[0] - self.siTopLeft[0], self.srTopLeft[1] - self.siTopLeft[1])
        
        # transform cropTopLeft to original numbers
        cropTopLeft = (cropTopLeft[0]/self.siScale, cropTopLeft[1]/self.siScale)
        cropSize = (self.srSize[0]/self.siScale, self.srSize[1]/self.siScale)
        
        if cropTopLeft[0] < 0 or cropTopLeft[1] < 0:
            wx.MessageBox("The cropping area has to be in the photo.", "Photo Ya Crop")
        elif cropTopLeft[0] + cropSize[0] > self.imSize[0] or cropTopLeft[1] + cropSize[1] > self.imSize[1]:
            wx.MessageBox("The cropping area has to be in the photo.", "Photo Ya Crop")
        
        # save cropImage
        str = "crop.%dx%d.jpg" % (self.sizeList[self.sizeIndex][0], self.sizeList[self.sizeIndex][1])
        
#        print cropSize
#        print cropTopLeft
        
#        print('convert %s -crop %dx%d+%d+%d -quality 94 %s' % \
#            (self.imageFileName, \
#            cropSize[0], cropSize[1], \
#            cropTopLeft[0], cropTopLeft[1], \
#            self.imageFileName[:-3] + str))

        commands.getoutput('convert %s -crop %dx%d+%d+%d -quality 94 %s' % \
            (self.imageFileName, \
            cropSize[0], cropSize[1], \
            cropTopLeft[0], cropTopLeft[1], \
            self.imageFileName[:-3] + str))
