import wx
from bs4 import BeautifulSoup
import requests

def add_user(user_name):
    """docstring for add_user"""
    open('gamertags.txt', 'a').write(user_name+'\n')

def remove_user(user_name):
    f = open('gamertags.txt','r')
    lines = f.readlines()
    f.close()
    f = open('gamertags.txt','w')
    for line in lines:
        if line != user_name + '\n':
            f.write(line)

def is_online(gamertag):
    """docstring for is_online"""
    url = 'http://live.xbox.com/en-GB/Profile?gamertag=' + gamertag
    page = requests.get(url, verify=False)
    data = page.text.encode('utf-8')
    soup = BeautifulSoup(data)
    cont = soup.find('div', attrs={'class':'presence'}).text
    cont_split = cont.split(' ')
    if cont_split[0] != 'Last' and cont_split[0] != 'Offline':
        online = True
    else:
        online = False
    output = [gamertag, cont, online]
    return output

class Frame(wx.Frame):
    
    def __init__(self):
        wx.Frame.__init__(self, parent=None, title="Xbox Alert")
        self.fSizer = wx.BoxSizer(wx.VERTICAL)
        panel = MyPanel(self)
        self.fSizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(self.fSizer)
        self.Fit()
        self.Show()

class MyPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.frame = parent
#--------------------SIZERS---------------------------------------#
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        controlSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.timeSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.widgetSizer = wx.BoxSizer(wx.VERTICAL)
        self.output_sizer = wx.BoxSizer(wx.VERTICAL)
        
#----------------------Add and remove section----------------------#
        self.text = wx.TextCtrl(self, -1, size=(250,30))
        controlSizer.Add(self.text, 0, wx.CENTER|wx.ALL, 5)      
        self.addButton = wx.Button(self, label='Add')
        self.addButton.Bind(wx.EVT_BUTTON, self.on_button)
        self.removeButton = wx.Button(self, label='Remove')
        self.removeButton.Bind(wx.EVT_BUTTON, self.on_remove_button)
        controlSizer.Add(self.addButton, 0 , wx.CENTER|wx.ALL, 5)
        controlSizer.Add(self.removeButton, 0, wx.CENTER|wx.ALL, 5)

#----------------------Refresh time section--------------------------#
        self.timeBar = wx.TextCtrl(self, -1)
        self.timeButton = wx.Button(self, label='Set refresh rate (seconds)')
        self.timeButton.Bind(wx.EVT_BUTTON, self.on_time_button)
        self.timeSizer.Add(self.timeBar, 0, wx.CENTER|wx.ALL, 5)
        self.timeSizer.Add(self.timeButton, 0, wx.CENTER|wx.ALL, 5)
        
#----------------------Display section--------------------------------#
        self.controller = wx.TextCtrl(self, -1,size = (500,300), style = wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_RICH2|wx.HSCROLL)

#----------------------Display build section--------------------------#
        self.widgetSizer.Add(self.controller, 0)
        self.widgetSizer.Add(self.output_sizer,0)
        self.mainSizer.Add(controlSizer, 0, wx.CENTER)
        self.mainSizer.Add(self.timeSizer, 0, wx.CENTER|wx.ALL, 5)
        self.mainSizer.Add(self.widgetSizer, 0, wx.CENTER|wx.ALL, 10)        
        self.SetSizer(self.mainSizer)

#---------------------Gamertag file check section----------------------#
        try:
            f = open('gamertags.txt','r')
        except:
            f = open('gamertags.txt', 'w')
        f.close()

#---------------------Run section--------------------------------------#
        self.timer = 10
        self.on_timer()
    
    def on_button(self, event):
        tag = self.text.GetValue()
        add_user(tag)
        self.text.Clear()

    def on_remove_button(self, event):
        remove_user(self.text.GetValue())
        self.text.Clear()

    def on_time_button(self, event):
        print self.timer
        newTime = self.timeBar.GetValue()
        try:
            if newTime != '':
                self.timer = newTime
                print self.timer
        except:
            print self.time
            pass
            
    def on_timer(self):
        self.controller.Clear()
        f = open('gamertags.txt','r')
        self.readit = f.read().splitlines()
        for each in self.readit:
            try:
                self.apps = is_online(each)
                if self.apps[-1] == False:
                    self.controller.SetDefaultStyle(wx.TextAttr(wx.RED))
                elif self.apps[-1] == True:
                    self.controller.SetDefaultStyle(wx.TextAttr(wx.GREEN))
                self.controller.AppendText('{0} {1}\n\n'.format(self.apps[0],self.apps[1]))
            except Exception as e:
                print e
                continue
        self.frame.fSizer.Layout()
        self.frame.Fit()
        if self.timer < 10:
            self.timer = 10
        wx.CallLater(self.sec(self.timer), self.on_timer)  

    def sec(self, secs):
        seconds = int(secs) * 1000
        return seconds

if __name__=='__main__':
    app = wx.App(False)
    frame = Frame()

app.MainLoop()
