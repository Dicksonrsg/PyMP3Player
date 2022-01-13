import os
from tkinter.ttk import Style
import wx
import wx.media
import wx.lib.buttons as buttons

dirName = os.path.dirname(os.path.abspath(__file__))
bitmapDir = os.path.join(dirName, 'bitmaps')

class MediaPanel(wx.Panel):
    """"""
    
    def __init__(self, parent):
        """Constructor"""
        self.frame = parent
        self.currentVolume = 50
        self.createMenu()
        self.layoutControls()
        
        sp = wx.StandardPaths.Get()
        self.currentFolder = sp.GetDocumentsDir()
        
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onTimer)
        self.timer.Start(100)
    
    def layoutControls(self):
        """Create and layout the wdigets"""
        
        try:
            self.mediaPlayer = wx.media.MediaCtrl(self, style = wx.SIMPLE_BORDER)
        except NotImplementedError:
            self.Destroy()
            raise
    
        #Create playback slider
        self.playbackSlider = wx.Slider(self, size = wx.DefaultSize)
        self.Bind(wx.EVT_SLIDER, self.onSeek, self.playbackSlider)
        
        self.volumeCTRL = wx.Slider(self, style = wx.SL_VERTICAL|wx.SL_INVERSE)
        self.volumeCTRL.SetRange(0, 100)
        self.volumeCTRL.SetValue(self.currentVolume)
        self.volumeCTRL.Bind(wx.EVT_SLIDER, self.onSetVolume)
        
        #Create sizers
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        audioSizer = self.buildAudioBar()
        
        #layout widgets
        mainSizer.Add(self.playbackSlider, 1, wx.ALL|wx.EXPAND, 5)
        hSizer.Add(audioSizer, 0, wx.ALL|wx.CENTER, 5)
        hSizer.Add(self.volumeCTRL, 0, wx.ALL, 5)
        mainSizer.Add(hSizer)
        
        self.SetSizer(mainSizer)
        self.Layout()