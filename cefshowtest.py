# An example of embedding CEF browser in a PyQt4 application.
# Tested with PyQt 4.10.3 (Qt 4.8.5).

#Implementing CEF with Proxy Settings
import platform,psutil,win32gui,win32con
if platform.architecture()[0] != "32bit":
    raise Exception("Architecture not supported: %s" % platform.architecture()[0])

import platform
if platform.architecture()[0] != "32bit":
    raise Exception("Architecture not supported: %s" \
            % platform.architecture()[0])

import os, sys
libcef_dll = os.path.join(os.path.dirname(os.path.abspath(__file__)),
        'libcef.dll')
if os.path.exists(libcef_dll):
    # Import a local module
    if 0x02070000 <= sys.hexversion < 0x03000000:
        import cefpython_py27 as cefpython
    elif 0x03000000 <= sys.hexversion < 0x04000000:
        import cefpython_py32 as cefpython
    else:
        raise Exception("Unsupported python version: %s" % sys.version)
else:
    # Import an installed package
    from cefpython3 import cefpython

from PyQt4 import QtGui
from PyQt4 import QtCore

def GetApplicationPath(file=None):
    import re, os, platform
    # On Windows after downloading file and calling Browser.GoForward(),
    # current working directory is set to %UserProfile%.
    # Calling os.path.dirname(os.path.realpath(__file__))
    # returns for eg. "C:\Users\user\Downloads". A solution
    # is to cache path on first call.
    if not hasattr(GetApplicationPath, "dir"):
        if hasattr(sys, "frozen"):
            dir = os.path.dirname(sys.executable)
        elif "__file__" in globals():
            dir = os.path.dirname(os.path.realpath(__file__))
        else:
            dir = os.getcwd()
        GetApplicationPath.dir = dir
    # If file is None return current directory without trailing slash.
    if file is None:
        file = ""
    # Only when relative path.
    if not file.startswith("/") and not file.startswith("\\") and (
            not re.search(r"^[\w-]+:", file)):
        path = GetApplicationPath.dir + os.sep + file
        if platform.system() == "Windows":
            path = re.sub(r"[/\\]+", re.escape(os.sep), path)
        path = re.sub(r"[/\\]+$", "", path)
        return path
    return str(file)

def ExceptHook(excType, excValue, traceObject):
    import traceback, os, time, codecs
    # This hook does the following: in case of exception write it to
    # the "error.log" file, display it to the console, shutdown CEF
    # and exit application immediately by ignoring "finally" (os._exit()).
    errorMsg = "\n".join(traceback.format_exception(excType, excValue,
            traceObject))
    errorFile = GetApplicationPath("error.log")
    try:
        appEncoding = cefpython.g_applicationSettings["string_encoding"]
    except:
        appEncoding = "utf-8"
    if type(errorMsg) == bytes:
        errorMsg = errorMsg.decode(encoding=appEncoding, errors="replace")
    try:
        with codecs.open(errorFile, mode="a", encoding=appEncoding) as fp:
            fp.write("\n[%s] %s\n" % (
                    time.strftime("%Y-%m-%d %H:%M:%S"), errorMsg))
    except:
        print("[pyqt.py] WARNING: failed writing to error file: %s" % (
                errorFile))
    # Convert error message to ascii before printing, otherwise
    # you may get error like this:
    # | UnicodeEncodeError: 'charmap' codec can't encode characters
    errorMsg = errorMsg.encode("ascii", errors="replace")
    errorMsg = errorMsg.decode("ascii", errors="replace")
    print("\n"+errorMsg+"\n")
    cefpython.QuitMessageLoop()
    cefpython.Shutdown()
    os._exit(1)

class ClientHandler:
    mainBrowser = None # May be None for global client callbacks.

    def __init__(self):
        pass

    # -------------------------------------------------------------------------
    # DisplayHandler
    # -------------------------------------------------------------------------

    def OnAddressChange(self, browser, frame, url):
        print("[wxpython.py] DisplayHandler::OnAddressChange()")
        print("    url = %s" % url)

    def OnTitleChange(self, browser, title):
        print("[wxpython.py] DisplayHandler::OnTitleChange()")
        print("    title = %s" % title)

    def OnTooltip(self, browser, textOut):
        # OnTooltip not yet implemented (both Linux and Windows),
        # will be fixed in next CEF release, see Issue 783:
        # https://code.google.com/p/chromiumembedded/issues/detail?id=783
        print("[wxpython.py] DisplayHandler::OnTooltip()")
        print("    text = %s" % textOut[0])

    statusMessageCount = 0
    def OnStatusMessage(self, browser, value):
        if not value:
            # Do not notify in the console about empty statuses.
            return
        self.statusMessageCount += 1
        if self.statusMessageCount > 3:
            # Do not spam too much.
            return
        print("[wxpython.py] DisplayHandler::OnStatusMessage()")
        print("    value = %s" % value)

    def OnConsoleMessage(self, browser, message, source, line):
        print("[wxpython.py] DisplayHandler::OnConsoleMessage()")
        print("    message = %s" % message)
        print("    source = %s" % source)
        print("    line = %s" % line)

    # -------------------------------------------------------------------------
    # KeyboardHandler
    # -------------------------------------------------------------------------

    def OnPreKeyEvent(self, browser, event, eventHandle,
            isKeyboardShortcutOut):
        print("[wxpython.py] KeyboardHandler::OnPreKeyEvent()")

    def OnKeyEvent(self, browser, event, eventHandle):
        if event["type"] == cefpython.KEYEVENT_KEYUP:
            # OnKeyEvent is called twice for F5/Esc keys, with event
            # type KEYEVENT_RAWKEYDOWN and KEYEVENT_KEYUP.
            # Normal characters a-z should have KEYEVENT_CHAR.
            return False
        print("[wxpython.py] KeyboardHandler::OnKeyEvent()")
        print("    type=%s" % event["type"])
        print("    modifiers=%s" % event["modifiers"])
        print("    windows_key_code=%s" % event["windows_key_code"])
        print("    native_key_code=%s" % event["native_key_code"])
        print("    is_system_key=%s" % event["is_system_key"])
        print("    character=%s" % event["character"])
        print("    unmodified_character=%s" % event["unmodified_character"])
        print("    focus_on_editable_field=%s" \
                % event["focus_on_editable_field"])
        linux = (platform.system() == "Linux")
        windows = (platform.system() == "Windows")
        # F5
        if (linux and event["native_key_code"] == 71) \
                or (windows and event["windows_key_code"] == 116):
            print("[wxpython.py] F5 pressed, calling"
                    " browser.ReloadIgnoreCache()")
            browser.ReloadIgnoreCache()
            return True
        # Escape
        if (linux and event["native_key_code"] == 9) \
                or (windows and event["windows_key_code"] == 27):
            print("[wxpython.py] Esc pressed, calling browser.StopLoad()")
            browser.StopLoad()
            return True
        # F12
        if (linux and event["native_key_code"] == 96) \
                or (windows and event["windows_key_code"] == 123):
            print("[wxpython.py] F12 pressed, calling"
                    " browser.ShowDevTools()")
            browser.ShowDevTools()
            return True
        return False

    # -------------------------------------------------------------------------
    # RequestHandler
    # -------------------------------------------------------------------------

    def OnBeforeBrowse(self, browser, frame, request, isRedirect):
        print("[wxpython.py] RequestHandler::OnBeforeBrowse()")
        print("    url = %s" % request.GetUrl()[:100])
        # Handle "magnet:" links.
        if request.GetUrl().startswith("magnet:"):
            print("[wxpython.p] RequestHandler::OnBeforeBrowse(): "
                    "magnet link clicked, cancelling browse request")
            return True
        return False

    def OnBeforeResourceLoad(self, browser, frame, request):
        print("[wxpython.py] RequestHandler::OnBeforeResourceLoad()")
        print("    url = %s" % request.GetUrl()[:100])
        return False

    def OnResourceRedirect(self, browser, frame, oldUrl, newUrlOut):
        print("[wxpython.py] RequestHandler::OnResourceRedirect()")
        print("    old url = %s" % oldUrl[:100])
        print("    new url = %s" % newUrlOut[0][:100])

    def GetAuthCredentials(self, browser, frame, isProxy, host, port, realm,
            scheme, callback):
        # This callback is called on the IO thread, thus print messages
        # may not be visible.
        print("[wxpython.py] RequestHandler::GetAuthCredentials()")
        print("    host = %s" % host)
        print("    realm = %s" % realm)
        callback.Continue(username="aanuj", password="ram21gas")
        return True

    def OnQuotaRequest(self, browser, originUrl, newSize, callback):
        print("[wxpython.py] RequestHandler::OnQuotaRequest()")
        print("    origin url = %s" % originUrl)
        print("    new size = %s" % newSize)
        callback.Continue(True)
        return True

    def GetCookieManager(self, browser, mainUrl):
        # Create unique cookie manager for each browser.
        # You must set the "unique_request_context_per_browser"
        # application setting to True for the cookie manager
        # to work.
        # Return None to have one global cookie manager for
        # all CEF browsers.
        if not browser:
            # The browser param may be empty in some exceptional
            # case, see docs.
            return None
        cookieManager = browser.GetUserData("cookieManager")
        if cookieManager:
            return cookieManager
        else:
            print("[wxpython.py] RequestHandler::GetCookieManager():"\
                    " created cookie manager")
            cookieManager = cefpython.CookieManager.CreateManager("")
            browser.SetUserData("cookieManager", cookieManager)
            return cookieManager

    def OnProtocolExecution(self, browser, url, allowExecutionOut):
        # There's no default implementation for OnProtocolExecution on Linux,
        # you have to make OS system call on your own. You probably also need
        # to use LoadHandler::OnLoadError() when implementing this on Linux.
        print("[wxpython.py] RequestHandler::OnProtocolExecution()")
        print("    url = %s" % url)
        if url.startswith("magnet:"):
            print("[wxpython.py] Magnet link allowed!")
            allowExecutionOut[0] = True

    def _OnBeforePluginLoad(self, browser, url, policyUrl, info):
        # This is a global callback set using SetGlobalClientCallback().
        # Plugins are loaded on demand, only when website requires it,
        # the same plugin may be called multiple times.
        # This callback is called on the IO thread, thus print messages
        # may not be visible.
        print("[wxpython.py] RequestHandler::_OnBeforePluginLoad()")
        print("    url = %s" % url)
        print("    policy url = %s" % policyUrl)
        print("    info.GetName() = %s" % info.GetName())
        print("    info.GetPath() = %s" % info.GetPath())
        print("    info.GetVersion() = %s" % info.GetVersion())
        print("    info.GetDescription() = %s" % info.GetDescription())
        # False to allow, True to block plugin.
        return False

    def _OnCertificateError(self, certError, requestUrl, callback):
        # This is a global callback set using SetGlobalClientCallback().
        print("[wxpython.py] RequestHandler::_OnCertificateError()")
        print("    certError = %s" % certError)
        print("    requestUrl = %s" % requestUrl)
        if requestUrl == "https://testssl-expire.disig.sk/index.en.html":
            print("    Not allowed!")
            return False
        if requestUrl \
                == "https://testssl-expire.disig.sk/index.en.html?allow=1":
            print("    Allowed!")
            callback.Continue(True)
            return True
        return False

    def OnRendererProcessTerminated(self, browser, status):
        print("[wxpython.py] RequestHandler::OnRendererProcessTerminated()")
        statuses = {
            cefpython.TS_ABNORMAL_TERMINATION: "TS_ABNORMAL_TERMINATION",
            cefpython.TS_PROCESS_WAS_KILLED: "TS_PROCESS_WAS_KILLED",
            cefpython.TS_PROCESS_CRASHED: "TS_PROCESS_CRASHED"
        }
        statusName = "Unknown"
        if status in statuses:
            statusName = statuses[status]
        print("    status = %s" % statusName)

    def OnPluginCrashed(self, browser, pluginPath):
        print("[wxpython.py] RequestHandler::OnPluginCrashed()")
        print("    plugin path = %s" % pluginPath)

    # -------------------------------------------------------------------------
    # LoadHandler
    # -------------------------------------------------------------------------

    def OnLoadingStateChange(self, browser, isLoading, canGoBack,
            canGoForward):
        print("[wxpython.py] LoadHandler::OnLoadingStateChange()")
        print("    isLoading = %s, canGoBack = %s, canGoForward = %s" \
                % (isLoading, canGoBack, canGoForward))

    def OnLoadStart(self, browser, frame):
        print("[wxpython.py] LoadHandler::OnLoadStart()")
        print("    frame url = %s" % frame.GetUrl()[:100])

    def OnLoadEnd(self, browser, frame, httpStatusCode):
        print("[wxpython.py] LoadHandler::OnLoadEnd()")
        print("    frame url = %s" % frame.GetUrl()[:100])
        # For file:// urls the status code = 0
        print("    http status code = %s" % httpStatusCode)
        # Tests for the Browser object methods
        self._Browser_LoadUrl(browser)

    def _Browser_LoadUrl(self, browser):
        if browser.GetUrl() == "data:text/html,Test#Browser.LoadUrl":
             browser.LoadUrl("file://"+GetApplicationPath("wxpython.html"))

    def OnLoadError(self, browser, frame, errorCode, errorTextList, failedUrl):
        print("[wxpython.py] LoadHandler::OnLoadError()")
        print("    frame url = %s" % frame.GetUrl()[:100])
        print("    error code = %s" % errorCode)
        print("    error text = %s" % errorTextList[0])
        print("    failed url = %s" % failedUrl)
        # Handle ERR_ABORTED error code, to handle the following cases:
        # 1. Esc key was pressed which calls browser.StopLoad() in OnKeyEvent
        # 2. Download of a file was aborted
        # 3. Certificate error
        if errorCode == cefpython.ERR_ABORTED:
            print("[wxpython.py] LoadHandler::OnLoadError(): Ignoring load "
                    "error: Esc was pressed or file download was aborted, "
                    "or there was certificate error")
            return;
        customErrorMessage = "My custom error message!"
        frame.LoadUrl("data:text/html,%s" % customErrorMessage)

    # -------------------------------------------------------------------------
    # LifespanHandler
    # -------------------------------------------------------------------------

    # ** This callback is executed on the IO thread **
    # Empty place-holders: popupFeatures, client.
    def OnBeforePopup(self, browser, frame, targetUrl, targetFrameName,
            popupFeatures, windowInfo, client, browserSettings,
            noJavascriptAccess):
        print("[wxpython.py] LifespanHandler::OnBeforePopup()")
        print("    targetUrl = %s" % targetUrl)

        # Custom browser settings for popups:
        # > browserSettings[0] = {"plugins_disabled": True}

        # Set WindowInfo object:
        # > windowInfo[0] = cefpython.WindowInfo()

        # On Windows there are keyboard problems in popups, when popup
        # is created using "window.open" or "target=blank". This issue
        # occurs only in wxPython. PyGTK or PyQt do not require this fix.
        # The solution is to create window explicitilly, and not depend
        # on CEF to create window internally.
        # If you set allowPopups=True then CEF will create popup window.
        # The wx.Frame cannot be created here, as this callback is
        # executed on the IO thread. Window should be created on the UI
        # thread. One solution is to call cefpython.CreateBrowser()
        # which runs asynchronously and can be called on any thread.
        # The other solution is to post a task on the UI thread, so
        # that cefpython.CreateBrowserSync() can be used.
        cefpython.PostTask(cefpython.TID_UI, self._CreatePopup, targetUrl)

        allowPopups = False
        return not allowPopups

    def _CreatePopup(self, url):
        frame = MainFrame(url=url, popup=True)
        frame.Show()

    def _OnAfterCreated(self, browser):
        # This is a global callback set using SetGlobalClientCallback().
        print("[wxpython.py] LifespanHandler::_OnAfterCreated()")
        print("    browserId=%s" % browser.GetIdentifier())

    def RunModal(self, browser):
        print("[wxpython.py] LifespanHandler::RunModal()")
        print("    browserId=%s" % browser.GetIdentifier())

    def DoClose(self, browser):
        print("[wxpython.py] LifespanHandler::DoClose()")
        print("    browserId=%s" % browser.GetIdentifier())

    def OnBeforeClose(self, browser):
        print("[wxpython.py] LifespanHandler::OnBeforeClose")
        print("    browserId=%s" % browser.GetIdentifier())

    # -------------------------------------------------------------------------
    # JavascriptDialogHandler
    # -------------------------------------------------------------------------

    def OnJavascriptDialog(self, browser, originUrl, acceptLang, dialogType,
                   messageText, defaultPromptText, callback,
                   suppressMessage):
        print("[wxpython.py] JavascriptDialogHandler::OnJavascriptDialog()")
        print("    originUrl="+originUrl)
        print("    acceptLang="+acceptLang)
        print("    dialogType="+str(dialogType))
        print("    messageText="+messageText)
        print("    defaultPromptText="+defaultPromptText)
        # If you want to suppress the javascript dialog:
        # suppressMessage[0] = True
        return False

    def OnBeforeUnloadJavascriptDialog(self, browser, messageText, isReload,
            callback):
        print("[wxpython.py] OnBeforeUnloadJavascriptDialog()")
        print("    messageText="+messageText)
        print("    isReload="+str(isReload))
        # Return True if the application will use a custom dialog:
        #   callback.Continue(allow=True, userInput="")
        #   return True
        return False

    def OnResetJavascriptDialogState(self, browser):
        print("[wxpython.py] OnResetDialogState()")

    def OnJavascriptDialogClosed(self, browser):
        print("[wxpython.py] OnDialogClosed()")

class MainWindow(QtGui.QMainWindow):
    mainFrame = None

    def __init__(self):
        super(MainWindow, self).__init__(None)
        self.createMenu()
        self.btn = QtGui.QPushButton("Terminate")
        self.btn.show()
        self.mainFrame = MainFrame(self)
        self.mainFrame.loadCustumUrl("http://www.google.com")
        self.btn.clicked.connect(self.mainFrame.exitApp)
        self.setCentralWidget(self.mainFrame)
        self.resize(1024, 768)
        self.setWindowTitle('PyQT CEF 3 example')
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    def createMenu(self):
        menubar = self.menuBar()
        filemenu = menubar.addMenu("&File")
        filemenu.addAction(QtGui.QAction("Open", self))
        filemenu.addAction(QtGui.QAction("Exit", self))
        aboutmenu = menubar.addMenu("&About")

    def focusInEvent(self, event):
        cefpython.WindowUtils.OnSetFocus(int(self.centralWidget().winId()), 0, 0, 0)

    def closeEvent(self, event):
        self.mainFrame.browser.CloseBrowser()

class MainFrame(QtGui.QWidget):
    browser = None

    def __init__(self, parent=None,url=None):
        super(MainFrame, self).__init__(parent)
        pass
	
    def loadCustumUrl(self,url):
        self.clientHandler = ClientHandler()
        cefpython.SetGlobalClientCallback("OnCertificateError",self.clientHandler._OnCertificateError)
        cefpython.SetGlobalClientCallback("OnBeforePluginLoad",self.clientHandler._OnBeforePluginLoad)
        cefpython.SetGlobalClientCallback("OnAfterCreated",self.clientHandler._OnAfterCreated)
        windowInfo = cefpython.WindowInfo()
        print "WIndow Infor",windowInfo
        windowInfo.SetAsChild(self.winId())
        print "WIn Id",int(self.winId())
        self.browser = cefpython.CreateBrowserSync(windowInfo,browserSettings={},navigateUrl="about:None")
        self.browser.GetMainFrame().LoadUrl("http://www.google.com")
        self.clientHandler.mainBrowser = self.browser
        self.browser.SetClientHandler(self.clientHandler)
        # cefpython.MessageLoop()
        self.show()

    def exitApp(self):
        print "Browser window may Be CLosed!!!"
        # cefpython.QuitMessageLoop()
        win32gui.DestroyWindow(self.winId())
        # browser = cefpyton.GetBrowserByWindowHandle(self.winId())
        # browser.CloseBrowser()
		
    def moveEvent(self, event):
        cefpython.WindowUtils.OnSize(int(self.winId()), 0, 0, 0)

    def resizeEvent(self, event):
        cefpython.WindowUtils.OnSize(int(self.winId()), 0, 0, 0)

class CefApplication(QtGui.QApplication):
    timer = None

    def __init__(self, args):
        super(CefApplication, self).__init__(args)
        self.createTimer()

    def createTimer(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.onTimer)
        self.timer.start(10)

    def onTimer(self):
        # The proper way of doing message loop should be:
        # 1. In createTimer() call self.timer.start(0)
        # 2. In onTimer() call MessageLoopWork() only when
        #    QtGui.QApplication.instance()->hasPendingEvents() returns False.
        # But... there is a bug in Qt, hasPendingEvents() returns always true.
        cefpython.MessageLoopWork()

    def stopTimer(self):
        # Stop the timer after Qt message loop ended, calls to MessageLoopWork()
        # should not happen anymore.
        self.timer.stop()

if __name__ == '__main__':
    print("[pyqt.py] PyQt version: %s" % QtCore.PYQT_VERSION_STR)
    print("[pyqt.py] QtCore version: %s" % QtCore.qVersion())

    # Intercept python exceptions. Exit app immediately when exception
    # happens on any of the threads.
    sys.excepthook = ExceptHook

    # Application settings
    settings = {
        "debug": True, # cefpython debug messages in console and in log_file
        "log_severity": cefpython.LOGSEVERITY_INFO, # LOGSEVERITY_VERBOSE
        "log_file": GetApplicationPath("debug.log"), # Set to "" to disable.
        "release_dcheck_enabled": True, # Enable only when debugging.
        # This directories must be set on Linux
        "locales_dir_path": cefpython.GetModuleDirectory()+"/locales",
        "resources_dir_path": cefpython.GetModuleDirectory(),
        "browser_subprocess_path": "%s/%s" % (
            cefpython.GetModuleDirectory(), "subprocess"),
    }
    settings["multi_threaded_message_loop"] = False
    # Command line switches set programmatically
    switches = {
        "proxy-server": "http://nknproxy.iitk.ac.in:3128",
        # "proxy-auto-detect":True,
        # "enable-media-stream": "",
        # "--invalid-switch": "" -> Invalid switch name
    }

    cefpython.Initialize(settings, switches)

    app = CefApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec_()
    app.stopTimer()

    # Need to destroy QApplication(), otherwise Shutdown() fails.
    # Unset main window also just to be safe.
    del mainWindow
    del app

    cefpython.Shutdown()
