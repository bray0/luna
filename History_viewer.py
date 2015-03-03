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
        self.SetSize((980, 598))
        self.SetMaxSize((980, 598))
        self.SetMinSize((980, 598))
        self.TreeUI()
        
        self.Bind(wx.EVT_MENU, self.OnQuit, id=105)
        self.Show(True)
    
    def TreeUI(self):
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.panel1 = wx.Panel(self, -1, (0, 0), (0, 0), style=wx.SUNKEN_BORDER)
        #self.panel2 = wx.Panel(self, -1, (0, 0), (825, 348), style=wx.SUNKEN_BORDER)
        
        
        
        self.tree = wx.TreeCtrl(self.panel1, 1, wx.DefaultPosition, (-1, -1), wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS)
        root = self.tree.AddRoot('Browsers')
        firefox = self.tree.AppendItem(root, 'Firefox')
        chrome = self.tree.AppendItem(root, 'Google Chrome')
        self.tree.AppendItem(firefox, 'F History')
        self.tree.AppendItem(firefox, 'F Cookies')
        self.tree.AppendItem(firefox, 'F Downloads')
        self.tree.AppendItem(firefox, 'F High Hits')
        self.tree.AppendItem(firefox, 'F Low Hits')
        
        self.tree.AppendItem(chrome, 'G History')
        self.tree.AppendItem(chrome, 'G Cookies')
        self.tree.AppendItem(chrome, 'G Downloads')
        self.tree.AppendItem(chrome, 'G High Hits')
        self.tree.AppendItem(chrome, 'G Low Hits')
        
        
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
        self.SetSizer(hbox)
    
    def selfListCtrl(self):
        self.panel2 = scrolled_panel = scrolled.ScrolledPanel(parent=self, id=-1, style=wx.SUNKEN_BORDER)
        self.panel2.SetPosition((152, 2))
        self.panel2.SetSize((825, 552))
        scrolled_panel.SetBackgroundColour(wx.WHITE)
        scrolled_panel.SetupScrolling()
        
        #============================================================
        #                 LISTCtrl
        #============================================================
        self.hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        
        self.list = AutoWidthListCtrl(self.panel2)
        self.list.InsertColumn(0, 'Hits', width=50)
        self.list.InsertColumn(1, 'Last Visited', width=180)
        self.list.InsertColumn(2, 'Url', width=140)
        
        self.list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.selectedItem)
        
        self.hbox2.Add(self.list, 1, wx.EXPAND|wx.ALL)
        
        self.panel2.SetSizer(self.hbox2)
    
    def selfListCtrl2(self):
        self.panel2 = scrolled_panel = scrolled.ScrolledPanel(parent=self, id=-1, style=wx.SUNKEN_BORDER)
        self.panel2.SetPosition((152, 2))
        self.panel2.SetSize((825, 552))
        scrolled_panel.SetBackgroundColour(wx.WHITE)
        scrolled_panel.SetupScrolling()
        
        #============================================================
        #                 LISTCtrl
        #============================================================
        self.hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        ##################################
        #     Creating new columns
        ##################################
        self.list = AutoWidthListCtrl(self.panel2)
        self.list.InsertColumn(0, 'Start Time', width=160)
        self.list.InsertColumn(1, 'Recived Bytes', width=120)
        self.list.InsertColumn(2, 'Total Bytes', width=120)
        self.list.InsertColumn(3, 'Target Path', width=200)
        self.list.InsertColumn(4, 'Source URL', width=200 )
                
        self.list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.selectedItemDown)
        
        self.hbox2.Add(self.list, 1, wx.EXPAND|wx.ALL)
        
        self.panel2.SetSizer(self.hbox2)
    
    def selfListCookieCtrl(self):
        self.panel2 = scrolled_panel = scrolled.ScrolledPanel(parent=self, id=-1, style=wx.SUNKEN_BORDER)
        self.panel2.SetPosition((152, 2))
        self.panel2.SetSize((825, 552))
        scrolled_panel.SetBackgroundColour(wx.WHITE)
        scrolled_panel.SetupScrolling()
        
        #============================================================
        #                 LISTCtrl
        #============================================================
        self.hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        ##################################
        #     Creating new columns
        ##################################
        self.list = AutoWidthListCtrl(self.panel2)
        self.list.InsertColumn(0, 'Creation Date', width=160)
        self.list.InsertColumn(1, 'Url Host', width=180)
        self.list.InsertColumn(2, 'Expiry Date', width=160)
        self.list.InsertColumn(3, 'Is Secure?', width=80)
        self.list.InsertColumn(4, 'Is HttpOnly?', width=80 )
        self.list.InsertColumn(5, 'Last Access', width=160 )
        
        self.hbox2.Add(self.list, 1, wx.EXPAND|wx.ALL)
        
        self.panel2.SetSizer(self.hbox2)
        
    def selectedItemDown(self, event):
        currentItem = event.m_itemIndex  
        rowItem = self.myRowDict[currentItem]
        self.StatusBar.SetStatusText('LOCATION PATH: => '+ rowItem[3])
    
    def selectedItem(self, event):
        currentItem = event.m_itemIndex  
        rowItem = self.myRowDict[currentItem]
        self.StatusBar.SetStatusText(rowItem[2])
        
    def onBrowse(self, event):
        wildcard = "database (*.sqlite, *.*)|*.sqlite;*.*"
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
            if textItem == "F History":
                self.selfListCtrl()
                filename = self.filePath.split('/')[-1]
                if filename == "places.sqlite":
                    data = self.databaseHistory(self.filePath)
                    self.fillInData(self.filePath, data)
            if textItem == "F Cookies":
                self.selfListCookieCtrl()
                filename = self.filePath.split('/')[-1]
                if filename == 'cookies.sqlite':
                    data = self.firefoxCookies(self.filePath)
                    self.fillinCookies(self.filePath, data)
            if textItem == "F Downloads":
                self.list.DeleteAllItems()
            if textItem == "F High Hits":
                self.selfListCtrl()
                filename = self.filePath.split('/')[-1]
                if filename == "places.sqlite":
                    data = self.databasePopular(self.filePath)
                    self.fillInData(self.filePath, data)
            if textItem == "F Low Hits":
                self.selfListCtrl()
                filename = self.filePath.split('/')[-1]
                if filename == "places.sqlite":
                    data = self.databaseLessPopular(self.filePath)
                    self.fillInData(self.filePath, data)
            if textItem == "G History":
                self.selfListCtrl()
                
                filename = self.filePath.split('/')[-1]
                if filename == 'history':
                    data = self.googleHistory(self.filePath)
                    self.fillInData(self.filePath, data)
                    
            if textItem == "G High Hits":
                self.selfListCtrl()
                filename = self.filePath.split('/')[-1]
                if filename == 'history':
                    data = self.googleHighHits(self.filePath)
                    self.fillInData(self.filePath, data)
            if textItem == "G Low Hits":
                self.selfListCtrl()
                filename = self.filePath.split('/')[-1]
                if filename == 'history':
                    data = self.googleLowHits(self.filePath)
                    self.fillInData(self.filePath, data)
            if textItem == "G Downloads":
                self.selfListCtrl2()
                filename = self.filePath.split('/')[-1]
                if filename == 'history':
                    data = self.googleDownloads(self.filePath)
                    self.fillInDownloads(self.filePath, data)
            if textItem == "G Cookies":
                self.selfListCookieCtrl()
                filename = self.filePath.split('/')[-1]
                if filename == 'Cookies':
                    data = self.googleCookies(self.filePath)
                    self.fillinCookies(self.filePath, data)
    
    def fillInData(self, filepath, data):
        self.myRowDict = {}
        for i in data:
            index = self.list.InsertStringItem(sys.maxint, str(i[0]))
            self.list.SetStringItem(index, 1, i[1].decode('utf8', 'ignore'))
            self.list.SetStringItem(index, 2, i[2].decode('utf8', 'ignore'))
            self.myRowDict[index] = i  
    def bytes2Human(self, digits):
        answer = None
        if str(digits).isdigit():
            if digits >= 1024:
                answer = "%.1fKB" % (digits / float(1024))
            if digits >= 1048576:
                answer = "%.1fMB" % (digits / float(1048576))
            if digits >= 1073741824:
                answer = "%.1fGB" % (digits / float(1073741824))

        return str(answer)
    
    def boolean2Human(self, state):
        answer = None
        if state == 1:
            answer = 'Yes'
        else:
            answer = 'No'
        
        return str(answer)
    
    def fillinCookies(self, filepath, data):
        self.myRowDict = {}
        
        for i in data:
            index = self.list.InsertStringItem(sys.maxint, str(i[0])) #creation date
            self.list.SetStringItem(index, 1, i[1].decode('utf8', 'ignore')) #url host
            self.list.SetStringItem(index, 2, str(i[2])) #expiry date
            self.list.SetStringItem(index, 3, label=self.boolean2Human(i[3])) #is secure
            self.list.SetStringItem(index, 4, label=self.boolean2Human([4])) #is httponly
            self.list.SetStringItem(index, 5, str(i[5])) #last access
            self.myRowDict[index] = i 
            
    def fillInDownloads(self, filepath, data):
        self.myRowDict = {}
        
        for i in data:
            index = self.list.InsertStringItem(sys.maxint, str(i[0]))
            self.list.SetStringItem(index, 1, label=self.bytes2Human(i[1]))
            self.list.SetStringItem(index, 2, label=self.bytes2Human(i[2]))
            self.list.SetStringItem(index, 3, i[3].decode('utf8', 'ignore'))
            self.list.SetStringItem(index, 4, i[4].decode('utf8', 'ignore'))
            self.myRowDict[index] = i 
            
    def googleLowHits(self, filename):
        con = lite.connect(filename)
        cur = con.cursor()
        statement = 'SELECT urls.visit_count, datetime(((visits.visit_time/1000000)-11644473600), "unixepoch"), urls.url FROM urls, visits WHERE urls.id = visits.url ORDER BY urls.visit_count ASC'
        cur.execute(statement)
        row = cur.fetchall()
        return row 
    
    def googleHighHits(self, filename):
        con = lite.connect(filename)
        cur = con.cursor()
        statement = 'SELECT urls.visit_count, datetime(((visits.visit_time/1000000)-11644473600), "unixepoch"), urls.url FROM urls, visits WHERE urls.id = visits.url ORDER BY urls.visit_count DESC'
        cur.execute(statement)
        row = cur.fetchall()
        return row 
    
    def firefoxCookies(self, filename):
        con = lite.connect(filename)
        cur = con.cursor()
        statement = 'SELECT datetime(creationTime/1000000, "unixepoch"), baseDomain, datetime(expiry/1000000, "unixepoch"), isSecure, isHttpOnly, datetime(lastAccessed/1000000, "unixepoch") FROM moz_cookies'
        cur.execute(statement)
        row = cur.fetchall()
        return row
    def googleCookies(self, filename):
        con = lite.connect(filename)
        cur = con.cursor()
        statement = 'SELECT datetime(((cookies.creation_utc/1000000)-11644473600), "unixepoch"), cookies.host_key, datetime(((cookies.expires_utc/1000000)-11644473600), "unixepoch"), cookies.secure, cookies.httponly, datetime(((cookies.last_access_utc/1000000)-11644473600), "unixepoch") FROM cookies'
        cur.execute(statement)
        row = cur.fetchall()
        return row
    
    def googleDownloads(self, filename):
        con = lite.connect(filename)
        cur = con.cursor()
        statement = 'SELECT datetime(((downloads.start_time/1000000)-11644473600), "unixepoch"), downloads.received_bytes, downloads.total_bytes, downloads.target_path, downloads_url_chains.url FROM downloads, downloads_url_chains WHERE downloads.id = downloads_url_chains.id'
        cur.execute(statement)
        row = cur.fetchall()
        return row 
    
    def googleHistory(self, filename):
        con = lite.connect(filename)
        cur = con.cursor()
        statement = 'SELECT urls.visit_count, datetime(((visits.visit_time/1000000)-11644473600), "unixepoch"), urls.url FROM urls, visits WHERE urls.id = visits.url'
        cur.execute(statement)
        row = cur.fetchall()
        return row 
    
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