#!/usr/bin/env python

import wx

class Window(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        
        self.InitUI()
        self.picturePath = None
        self.PhotoMaxSize = 400
        
    def InitUI(self):
        #=================================================
        img = wx.EmptyImage(350, 350)
        #==================================================
        
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        toolbar = wx.ToolBar(self)
        toolbar.AddLabelTool(1, '', wx.Bitmap('topen.png'))
        toolbar.AddSeparator()
        toolbar.AddSeparator()
        qtool = toolbar.AddLabelTool(wx.ID_ANY, '', wx.Bitmap('tclose.png'))
        toolbar.AddSeparator()
        toolbar.AddSeparator()
        toolbar.AddLabelTool(2, '', wx.Bitmap('tabout.png'))
        toolbar.Realize()
        vbox.Add(toolbar, 0, wx.EXPAND)
        
        #====================================================
        #     PANEL
        #====================================================
        self.panel = wx.Panel(self, -1, (25, 85), (350, 350), style=wx.SUNKEN_BORDER)
        self.imageCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY, wx.BitmapFromImage(img))
        self.panel.SetBackgroundColour(wx.BLACK)
        
        #====================================================
        #     Sliders
        #====================================================
        #                             def min max
        slider = wx.Slider(self, -1, 50, 1, 100, pos=(80, 450), size=(250, -1), style=wx.SL_AUTOTICKS)
        slider.SetTickFreq(5, 1)
        
        
        self.Bind(wx.EVT_TOOL, self.OnBrowse, id=1)
        self.Bind(wx.EVT_TOOL, self.OnAboutBox, id=2)
        self.Bind(wx.EVT_TOOL, self.OnQuit, qtool)
        self.SetSizer(vbox)
        
        self.SetSize((1250, 750))
        self.SetTitle('Project Luna')
        self.Center()
        self.Show(True)
        
    
    def OnAboutBox(self, e):
        description = """Luna forensic is a unix based forensic tool that include inbuilt
        features for extracting metadata from files.
        """
        licence = """Luna forensic is covered by the free software license which is Apache
        2 license read more on it
        """
        info = wx.AboutDialogInfo()
        
        info.SetIcon(wx.Icon('gnu.png', wx.BITMAP_TYPE_PNG))
        info.SetName('Luna Forensics')
        info.SetVersion('1.0')
        info.SetDescription(description)
        info.SetCopyright('(C) 2015 - 2017 Brian Gichohi')
        info.SetLicence(licence)
        info.AddDeveloper('Brian Gichohi')
        wx.AboutBox(info)
    
    def OnBrowse(self, event):
        #wildcard = "JPEG files (*.jpg) | *.jpg"
        dialog = wx.FileDialog(None, "Choose a File", "*.*", style=wx.OPEN)
        
        if dialog.ShowModal() == wx.ID_OK:
            self.picturePath = dialog.GetPath() 
        dialog.Destroy()
        self.onView()
    
    def onView(self):
        filePath = self.picturePath
        img = wx.Image(filePath, wx.BITMAP_TYPE_ANY)
        
        #scaling the image preserving aspect ratio
        W = img.GetWidth()
        H = img.GetHeight()
        if W > H:
            NewW = self.PhotoMaxSize 
            NewH = self.PhotoMaxSize * H / W
        else:
            NewH = self.PhotoMaxSize
            NewW = self.PhotoMaxSize * W / H
        img = img.Scale(NewW, NewH)
        
        self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
        self.panel.Refresh()
        
    def OnQuit(self, e):
        self.Close()

def main():
    app = wx.App()
    Window(None)
    app.MainLoop()


if __name__ == "__main__":
    main()