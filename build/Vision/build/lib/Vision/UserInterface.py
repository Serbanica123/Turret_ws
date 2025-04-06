
import sys
sys.path.append('/home/alex/anaconda3/envs/Turret3.10/lib/python3.10/site-packages')

import numpy as np
import wx
import wx.xrc
import gettext
_ = gettext.gettext

class cameraFeedFrame ( wx.Frame ):
    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 1920,1080 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.SetBackgroundColour( wx.Colour( 65, 59, 59 ) )

        mainSizer = wx.BoxSizer( wx.HORIZONTAL )
        feedSizer = wx.BoxSizer( wx.VERTICAL )

        self.cameraFeed = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 1280,720 ), 0 )
        feedSizer.Add( self.cameraFeed, 0, 0, 5 )

        mainSizer.Add( feedSizer, 1, 0, 5 )

        controlSizer = wx.BoxSizer( wx.VERTICAL )

        self.programTypeDisplay = wx.StaticText( self, wx.ID_ANY, _(u"Select Program: "), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.programTypeDisplay.Wrap( -1 )

        self.programTypeDisplay.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )

        controlSizer.Add( self.programTypeDisplay, 0, wx.ALL, 5 )

        programSelectionChoices = [ _(u"Aim") ]
        self.programSelection = wx.ComboBox( self, wx.ID_ANY, _(u"Aim"), wx.DefaultPosition, wx.DefaultSize, programSelectionChoices, 0 )
        self.programSelection.SetSelection( 1 )
        controlSizer.Add( self.programSelection, 0, wx.EXPAND, 5 )

        mainSizer.Add( controlSizer, 1, wx.EXPAND, 5 )

        self.SetSizer( mainSizer )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.cameraFeed.Bind( wx.EVT_LEFT_DOWN, self.onFeedClick )


    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def onFeedClick( self, event ):
        x,y=event.GetPosition()
        print(x)
        print(y)
        print(self.transformation([x,y,0,1], xOffset=60))
        


    def setFeed(self, img):
        h,w=img.shape[:2]

        image = wx.Image(w,h)
        image.SetData(img) 
        bitmap = wx.Bitmap(image)  
        self.cameraFeed.SetBitmap(bitmap)  
        self.cameraFeed.Refresh()

    def transformation(self, point,xOffset=0, yOffset=0, zOffset=0, thetaX=0, thetaY=0, thetaZ=0):
        point=np.array(point)
        thetaX=np.radians(thetaX)
        thetaY=np.radians(thetaY)
        thetaZ=np.radians(thetaZ)

        rX=np.array([[1,0,0],[0, np.cos(thetaX), -np.sin(thetaX)],[0, np.sin(thetaX), np.cos(thetaX)]])
        rY=np.array([[np.cos(thetaY), 0, np.sin(thetaY)],[0,1,0],[-np.sin(thetaY), 0, np.cos(thetaY)]])
        rZ=np.array([[np.cos(thetaZ),-np.sin(thetaZ), 0],[np.sin(thetaZ),np.cos(thetaZ),0],[0,0,1]])
        R=rZ@rY@rX
        M = np.array([
            [R[0, 0], R[0, 1], R[0, 2], xOffset],
            [R[1, 0], R[1, 1], R[1, 2], yOffset],
            [R[2, 0], R[2, 1], R[2, 2], zOffset],
            [0, 0, 0, 1]])
        return M@point



class MainTurretApp(wx.App):
    def __init__(self):
        super().__init__()
        self.cameraFrame = cameraFeedFrame(None)
        self.cameraFrame.Show(True)

    def setCameraFrameFeed(self, img):
        self.cameraFrame.setFeed(img)