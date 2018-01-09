__author__ = 'Raman Pandey'
#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import win32con # pywin32 extension
import win32gui

import cefpython3.cefpython_py27 as cefpython
from cefpython3 import cefwindow

from memory_profiler import profile

class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.button = QPushButton("ShowCEF")
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)
        self.button.clicked.connect(self.CefSimple)

    @profile
    def CefSimple(self):


        appSettings = {} # See: http://code.google.com/p/cefpython/wiki/AppSettings
        appSettings["multi_threaded_message_loop"] = False
        cefpython.Initialize(appSettings)

        wndproc = {
            win32con.WM_CLOSE: self.QuitApplication,
            win32con.WM_SIZE: cefpython.WindowUtils.OnSize,
            win32con.WM_SETFOCUS: cefpython.WindowUtils.OnSetFocus,
            win32con.WM_ERASEBKGND: cefpython.WindowUtils.OnEraseBackground
        }

        windowID = cefwindow.CreateWindow("CefAdvanced", "cefadvanced", 800, 600, None, None, "icon.ico", wndproc)
        windowInfo = cefpython.WindowInfo()
        windowInfo.SetAsChild(windowID)

        browserSettings = {} # See: http://code.google.com/p/cefpython/wiki/BrowserSettings
        browserSettings["history_disabled"] = True
        browserSettings["application_cache_disabled"] = True
        browser = cefpython.CreateBrowserSync(windowInfo, browserSettings, "http://www.google.de")
        cefpython.MessageLoop()
        #cefpython.Shutdown()
        #self.close()


    def QuitApplication(parent, windowID, msg, wparam, lparam):
        cefpython.QuitMessageLoop()
        win32gui.DestroyWindow(windowID)
        #browser = cefpython.GetBrowserByWindowHandle(windowID)
        #browser.CloseBrowser()

        className = cefwindow.GetWindowClassName(windowID)
        win32gui.UnregisterClass(className, None)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())