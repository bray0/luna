#!/usr/bin/env python

import wx
import os
import sys
from lib import checkhash
from lib import checkproperties
from lib import metainfo
from lib import CSVManager
import wx.lib.scrolledpanel as scrolled
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin

class AutoWidthListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT)
        ListCtrlAutoWidthMixin.__init__(self)
        
class Window(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        
        self.InitUI()
        self.picturePath = None
        self.globalList = [[]]
        self.PhotoMaxSize = 400
        
    def InitUI(self):
        #=================================================
        img = wx.EmptyImage(350, 250)
        #==================================================
        self.md5Hash = ''
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        toolbar = wx.ToolBar(self)
        toolbar.AddLabelTool(1, '', wx.Bitmap('images/topen.png'))
        toolbar.AddSeparator()
        toolbar.AddSeparator()
        qtool = toolbar.AddLabelTool(wx.ID_ANY, '', wx.Bitmap('images/tclose.png'))
        toolbar.AddSeparator()
        toolbar.AddSeparator()
        toolbar.AddLabelTool(2, '', wx.Bitmap('images/tabout.png'))
        toolbar.Realize()
        vbox.Add(toolbar, 0, wx.EXPAND)
        
        #====================================================
        #     PANEL
        #====================================================
        font = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        mainFont = wx.Font(20, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        
        self.panel = wx.Panel(self, -1, (120, 130), (350, 250), style=wx.SUNKEN_BORDER)
        self.panel2 = wx.Panel(self, -1, (25, 400), (584, 348), style=wx.SUNKEN_BORDER)
        #self.panel3 = wx.Panel(self, -1, (610, 60), (635, 690), style=wx.SUNKEN_BORDER)
        #self.panel3.SetBackgroundColour(wx.WHITE)
        
        self.panel3 = scrolled_panel = scrolled.ScrolledPanel(parent=self, id=-1, style=wx.SUNKEN_BORDER)
        self.panel3.SetPosition((610, 60))
        self.panel3.SetSize((635, 690))
        scrolled_panel.SetBackgroundColour(wx.WHITE)
        scrolled_panel.SetupScrolling()
        
        #================================================================
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        
        self.list = AutoWidthListCtrl(self.panel3)
        self.list.InsertColumn(0, 'MetaInfo', width=260)
        self.list.InsertColumn(1, 'Result', width=150)
        
        hbox.Add(self.list, 1, wx.EXPAND)
        self.panel3.SetSizer(hbox)
        #================================================================
        self.panel2.SetBackgroundColour(wx.WHITE)
        
        self.imageCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY, wx.BitmapFromImage(img))
        self.panel.SetBackgroundColour(wx.BLACK)
        self.panel.SetBackgroundColour(wx.WHITE)
        heading = wx.StaticText(self.panel2, label='File Properties', pos=(160, 5))
        heading2 = wx.StaticText(self.panel2, label='MAC Times', pos=(160, 150))
        MainHeading = wx.StaticText(self, label='PREVIEW', pos=(240, 80))
        MainHeading.SetFont(mainFont)
        
        wx.StaticLine(self, pos=(140, 115), size=(300, 1))
        wx.StaticLine(self, pos=(140, 115), size=(300, 1))
        wx.StaticLine(self, pos=(140, 115), size=(300, 1))
        wx.StaticLine(self, pos=(140, 115), size=(300, 1))
        wx.StaticLine(self, pos=(140, 115), size=(300, 1))
        wx.StaticLine(self, pos=(140, 115), size=(300, 1))
        
        self.vn = wx.StaticLine(self, pos=(30, 150), style=wx.LI_VERTICAL)
        self.vn2 = wx.StaticLine(self, pos=(580, 150), style=wx.LI_VERTICAL)
        
        self.vn.SetSize((2, 200))
        self.vn2.SetSize((2, 200))
        
        
        wx.StaticLine(self.panel2, pos=(60, 40), size=(300, 1))
        wx.StaticLine(self.panel2, pos=(60, 180), size=(300, 1))
        heading.SetFont(font)
        heading2.SetFont(font)
        
        #=====================================================
        #    STATIC TEXT
        #=====================================================
        wx.StaticText(self.panel2, label='MD5:', pos=(20, 60))
        wx.StaticText(self.panel2, label='SHA1:', pos=(20, 80))
        wx.StaticText(self.panel2, label='SHA256:', pos=(20, 100))
        
        self.md5text = wx.StaticText(self.panel2, label='-', pos=(100, 60))
        self.sha1Text = wx.StaticText(self.panel2, label='-', pos=(100, 80))
        self.sha256Text = wx.StaticText(self.panel2, label='-', pos=(100, 100))
        
        self.mtime = wx.StaticText(self.panel2, label='-', pos=(160, 200))
        self.atime = wx.StaticText(self.panel2, label='-', pos=(160, 220))
        self.ctime = wx.StaticText(self.panel2, label='-', pos=(160, 240))
        
        wx.StaticText(self.panel2, label='Modified Time:', pos=(20, 200))
        wx.StaticText(self.panel2, label='Accessed Time:', pos=(20, 220))
        wx.StaticText(self.panel2, label='Creation Time:', pos=(20, 240))
        wx.StaticText(self.panel2, label='File Size:', pos=(20, 300))
        
        
        self.fSize = wx.StaticText(self.panel2, label='-', pos=(120, 300))
        
                
        #=======================================================
        #   statusbus
        #=======================================================
        self.StatusBar = self.CreateStatusBar()
        
        self.Bind(wx.EVT_TOOL, self.OnBrowse, id=1)
        self.Bind(wx.EVT_TOOL, self.OnAboutBox, id=2)
        self.Bind(wx.EVT_TOOL, self.OnQuit, qtool)
        self.SetSizer(vbox)
        
        self.SetSize((1250, 800))
        self.SetTitle('Project Luna')
        self.Center()
        self.Show(True)
    
    def fillTable(self):
        for i in self.globalList:
            index = self.list.InsertStringItem(sys.maxint, i[0])
            self.list.SetStringItem(index, 1, i[1].decode('utf8', 'ignore'))
        
    def getExif(self, fileName):
        data = metainfo.get_exif(fileName)
        newlist = metainfo.dataToList(data)
        return newlist
    
                
    def OnAboutBox(self, e):
        description = """Luna forensic is a unix based forensic tool that include inbuilt
        features for extracting metadata from files.
        """
        licence = """Luna forensic is covered by the free software license which is Apache
        2 license read more on it
        """
        info = wx.AboutDialogInfo()
        
        info.SetIcon(wx.Icon('images/gnu.png', wx.BITMAP_TYPE_PNG))
        info.SetName('Luna Forensics')
        info.SetVersion('1.0')
        info.SetDescription(description)
        info.SetCopyright('(C) 2015 - 2017 Brian Gichohi')
        info.SetLicence(licence)
        info.AddDeveloper('Brian Gichohi')
        wx.AboutBox(info)
    
    def OnBrowse(self, event):
        wildcard = "pictures (*.jpg,*.png)|*.jpg;*.png"
        dialog = wx.FileDialog(self, "Choose a File", defaultDir=os.getcwd(), defaultFile="*.jpg/*.png", wildcard=wildcard, style=wx.OPEN)
        
        if dialog.ShowModal() == wx.ID_OK:
            self.picturePath = dialog.GetPath() 
            self.StatusBar.SetStatusText(self.picturePath)
        dialog.Destroy()
        self.onView()
        self.calculateChecksum()
        self.displayMtimes()
        self.displaySize()
        self.list.DeleteAllItems()
        self.globalList = self.getExif(self.picturePath)
        self.fillTable()
        
    def calculateChecksum(self):
        filepath = self.picturePath
        self.md5Hash = checkhash.md5sum(filepath)
        self.shaHash = checkhash.sha1sum(filepath)
        self.sha256hash = checkhash.sha256sum(filepath)
        
        self.md5text.SetLabel(self.md5Hash)
        self.sha1Text.SetLabel(self.shaHash)
        self.sha256Text.SetLabel(self.sha256hash)
        
    def displaySize(self):
        filepath = self.picturePath
        self.ftext = checkproperties.getFsize(filepath)
        self.ftext = str(self.ftext) + ' Bytes'
        
        self.fSize.SetLabel(self.ftext)
        
        
    def displayMtimes(self):
        filepath = self.picturePath
        self.mtext = checkproperties.getMtime(filepath)
        self.atext = checkproperties.getAtime(filepath)
        self.ctext = checkproperties.getCtime(filepath)
        
        self.mtime.SetLabel(self.mtext)
        self.atime.SetLabel(self.atext)
        self.ctime.SetLabel(self.ctext)
        
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
        self.panel2.Refresh()
        self.panel3.Refresh()
        
    def OnQuit(self, e):
        self.Close()

def main():
    app = wx.App()
    Window(None)
    app.MainLoop()


if __name__ == "__main__":
    main()