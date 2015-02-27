#!/usr/bin/python

import wx 
import sys
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin
import wx.lib.scrolledpanel as scrolled
import sqlite3 as lite
import os

class AutoWidthListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT)
        ListCtrlAutoWidthMixin.__init__(self)
        

class Window(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        
        self.browseStatus = False
        self.InitUI()
        
    def InitUI(self):
        menubar = wx.MenuBar()
        file = wx.Menu()
        Report = wx.Menu()
        Help = wx.Menu()
        
        file.Append(101, '&open', 'Open a history file')
        file.AppendSeparator()
        quit = wx.MenuItem(file, 105, '&Quit\tCtrl+Q', 'Quit the Application')
        file.AppendItem(quit)
        Report.Append(201, 'Save report', 'Export info to pdf')
        Help.Append(301, 'About Software', '')
        menubar.Append(file, '&File')
        menubar.Append(Report, '&Report')
        menubar.Append(Help, '&Help')
        
        self.SetMenuBar(menubar)
        self.SetTitle('History Viewer')
        #self.Center()
        self.SetPosition((300, 130))
        self.SetSize((980, 580))
        self.SetMaxSize((980, 580))
        self.SetMinSize((980, 580))
        self.TreeUI()
        
        self.Bind(wx.EVT_MENU, self.OnQuit, id=105)
        self.Show(True)
    
    def TreeUI(self):
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.panel1 = wx.Panel(self, -1, (0, 0), (0, 0), style=wx.SUNKEN_BORDER)
        #self.panel2 = wx.Panel(self, -1, (0, 0), (825, 348), style=wx.SUNKEN_BORDER)
        
        self.panel2 = scrolled_panel = scrolled.ScrolledPanel(parent=self, id=-1, style=wx.SUNKEN_BORDER)
        self.panel2.SetPosition((152, 2))
        self.panel2.SetSize((825, 552))
        scrolled_panel.SetBackgroundColour(wx.BLACK)
        scrolled_panel.SetupScrolling()
        
        
        self.tree = wx.TreeCtrl(self.panel1, 1, wx.DefaultPosition, (-1, -1), wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS)
        root = self.tree.AddRoot('Browsers')
        firefox = self.tree.AppendItem(root, 'Firefox')
        chrome = self.tree.AppendItem(root, 'Google Chrome')
        self.tree.AppendItem(firefox, 'Url History')
        self.tree.AppendItem(firefox, 'Cookies')
        self.tree.AppendItem(firefox, 'Downloads')
        self.tree.AppendItem(firefox, 'Popular Sites')
        self.tree.AppendItem(firefox, 'Least Popular')
        
        self.tree.AppendItem(chrome, 'Url History')
        self.tree.AppendItem(chrome, 'Cookies')
        self.tree.AppendItem(chrome, 'Downloads')
        self.tree.AppendItem(chrome, 'Popular Sites')
        self.tree.AppendItem(chrome, 'Least popular')
        
        
        #============================================================
        #                 LISTCtrl
        #============================================================
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        
        self.list = AutoWidthListCtrl(self.panel2)
        self.list.InsertColumn(0, 'Hits', width=50)
        self.list.InsertColumn(1, 'Last Visited', width=180)
        self.list.InsertColumn(2, 'Url', width=140)
        
        hbox2.Add(self.list, 1, wx.EXPAND|wx.ALL)
        #============================================================
        #============================================================
        #                 STATUSBAR
        #============================================================
        self.StatusBar = self.CreateStatusBar()
        #=============================================================
        #============================================================
        #                 Binding
        #============================================================
        self.Bind(wx.EVT_MENU, self.onBrowse, id=101)
        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, id=1)
        #============================================================
        vbox.Add(self.tree, 1)
        hbox.Add(self.panel1, 1, wx.EXPAND)
        #hbox.Add(self.panel2, 1, wx.EXPAND)
        self.panel1.SetSizer(vbox)
        self.panel2.SetSizer(hbox2)
        self.SetSizer(hbox)
    
    def onBrowse(self, event):
        wildcard = "database (*.sqlite)|*.sqlite"
        dialog = wx.FileDialog(self, "Choose a File", defaultDir=os.getcwd(), defaultFile="*.sqlite", wildcard=wildcard, style=wx.OPEN)
        
        if dialog.ShowModal() == wx.ID_OK:
            self.filePath = dialog.GetPath() 
            self.browseStatus = True
            self.StatusBar.SetStatusText(self.filePath)
        dialog.Destroy()
        
    
    def OnSelChanged(self, event):
        item = event.GetItem()
        textItem = self.tree.GetItemText(item)
        
        if self.browseStatus:
            if textItem == "Url History":
                self.list.DeleteAllItems()
                data = self.databaseHistory(self.filePath)
                self.fillInData(self.filePath, data)
            if textItem == "Cookies":
                self.list.DeleteAllItems()
            if textItem == "Downloads":
                self.list.DeleteAllItems()
            if textItem == "Popular Sites":
                self.list.DeleteAllItems()
                data = self.databasePopular(self.filePath)
                self.fillInData(self.filePath, data)
            if textItem == "Least Popular":
                self.list.DeleteAllItems()
                data = self.databaseLessPopular(self.filePath)
                self.fillInData(self.filePath, data)
    
    def fillInData(self, filepath, data):
        for i in data:
            index = self.list.InsertStringItem(sys.maxint, str(i[0]))
            self.list.SetStringItem(index, 1, i[1].decode('utf8', 'ignore'))
            self.list.SetStringItem(index, 2, i[2].decode('utf8', 'ignore'))  
            
    
    def databaseLessPopular(self, filename):
        con = lite.connect(filename)
        cur = con.cursor()
        statement = "SELECT moz_places.visit_count, datetime(moz_historyvisits.visit_date/1000000, 'unixepoch', 'localtime'), moz_places.url FROM moz_places, moz_historyvisits WHERE moz_places.id = moz_historyvisits.place_id ORDER BY moz_places.visit_count ASC"
        cur.execute(statement)
        row = cur.fetchall()
        return row 
    
    def databasePopular(self, filename):
        con = lite.connect(filename)
        cur = con.cursor()
        statement = "SELECT moz_places.visit_count, datetime(moz_historyvisits.visit_date/1000000, 'unixepoch', 'localtime'), moz_places.url FROM moz_places, moz_historyvisits WHERE moz_places.id = moz_historyvisits.place_id ORDER BY moz_places.visit_count DESC"
        cur.execute(statement)
        row = cur.fetchall()
        return row  
                        
    def databaseHistory(self, filename):
        con = lite.connect(filename)
        cur = con.cursor()
        statement = "SELECT moz_places.visit_count, datetime(moz_historyvisits.visit_date/1000000, 'unixepoch', 'localtime'), moz_places.url FROM moz_places, moz_historyvisits WHERE moz_places.id = moz_historyvisits.place_id"
        cur.execute(statement)
        row = cur.fetchall()
        return row   
        
    def OnQuit(self, event):
        self.Close()

def main():
    app = wx.App()
    Window(None)
    app.MainLoop()

if __name__ == "__main__":
    main()