__author__ = 'Raman Pandey'
from cefpython3 import cefpython
from PyQt4 import Qt,QtCore,QtGui
import win32gui,win32con

class ClientHandler:
    mainBrowser = None # May be None for global client callbacks.

    def __init__(self):
        pass


    # -------------------------------------------------------------------------
    # RequestHandler
    # -------------------------------------------------------------------------

    def OnBeforeBrowse(self, browser, frame, request, isRedirect):
        # print("[wxpython.py] RequestHandler::OnBeforeBrowse()")
        # print("    url = %s" % request.GetUrl()[:100])
        # Handle "magnet:" links.
        if request.GetUrl().startswith("magnet:"):
            # print("[wxpython.p] RequestHandler::OnBeforeBrowse(): "
            #         "magnet link clicked, cancelling browse request")
            return True
        return False

    def OnBeforeResourceLoad(self, browser, frame, request):
        # print("[wxpython.py] RequestHandler::OnBeforeResourceLoad()")
        # print("    url = %s" % request.GetUrl()[:100])
        return False

    def OnResourceRedirect(self, browser, frame, oldUrl, newUrlOut):
        # print("[wxpython.py] RequestHandler::OnResourceRedirect()")
        # print("    old url = %s" % oldUrl[:100])
        # print("    new url = %s" % newUrlOut[0][:100])
        pass

    def GetAuthCredentials(self, browser, frame, isProxy, host, port, realm,
            scheme, callback):
        # This callback is called on the IO thread, thus print messages
        # may not be visible.
        # print("[wxpython.py] RequestHandler::GetAuthCredentials()")
        # print("    host = %s" % host)
        # print("    realm = %s" % realm)
        # callback.Continue(username="aanuj", password="ram21gas")
        callback.Continue(username="", password="")
        return True

    def OnQuotaRequest(self, browser, originUrl, newSize, callback):
        # print("[wxpython.py] RequestHandler::OnQuotaRequest()")
        # print("    origin url = %s" % originUrl)
        # print("    new size = %s" % newSize)
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
            # print("[wxpython.py] RequestHandler::GetCookieManager():"\
            #         " created cookie manager")
            cookieManager = cefpython.CookieManager.CreateManager("")
            browser.SetUserData("cookieManager", cookieManager)
            return cookieManager

    def OnProtocolExecution(self, browser, url, allowExecutionOut):
        # There's no default implementation for OnProtocolExecution on Linux,
        # you have to make OS system call on your own. You probably also need
        # to use LoadHandler::OnLoadError() when implementing this on Linux.
        # print("[wxpython.py] RequestHandler::OnProtocolExecution()")
        # print("    url = %s" % url)
        if url.startswith("magnet:"):
            # print("[wxpython.py] Magnet link allowed!")
            allowExecutionOut[0] = True

    def _OnBeforePluginLoad(self, browser, url, policyUrl, info):
        # This is a global callback set using SetGlobalClientCallback().
        # Plugins are loaded on demand, only when website requires it,
        # the same plugin may be called multiple times.
        # This callback is called on the IO thread, thus print messages
        # may not be visible.
        # print("[wxpython.py] RequestHandler::_OnBeforePluginLoad()")
        # print("    url = %s" % url)
        # print("    policy url = %s" % policyUrl)
        # print("    info.GetName() = %s" % info.GetName())
        # print("    info.GetPath() = %s" % info.GetPath())
        # print("    info.GetVersion() = %s" % info.GetVersion())
        # print("    info.GetDescription() = %s" % info.GetDescription())
        # False to allow, True to block plugin.
        return False

    def _OnCertificateError(self, certError, requestUrl, callback):
        # This is a global callback set using SetGlobalClientCallback().
        # print("[wxpython.py] RequestHandler::_OnCertificateError()")
        # print("    certError = %s" % certError)
        # print("    requestUrl = %s" % requestUrl)
        if requestUrl == "https://testssl-expire.disig.sk/index.en.html":
            # print("    Not allowed!")
            return False
        if requestUrl \
                == "https://testssl-expire.disig.sk/index.en.html?allow=1":
            print("    Allowed!")
            callback.Continue(True)
            return True
        return False

    def OnRendererProcessTerminated(self, browser, status):
        # print("[wxpython.py] RequestHandler::OnRendererProcessTerminated()")
        statuses = {
            cefpython.TS_ABNORMAL_TERMINATION: "TS_ABNORMAL_TERMINATION",
            cefpython.TS_PROCESS_WAS_KILLED: "TS_PROCESS_WAS_KILLED",
            cefpython.TS_PROCESS_CRASHED: "TS_PROCESS_CRASHED"
        }
        statusName = "Unknown"
        if status in statuses:
            statusName = statuses[status]
        with open('CrashStatus.txt',w) as crashStatus:
            crashStatus.write(statusName)
        crashStatus.close()
        # print("    status = %s" % statusName)

    def OnPluginCrashed(self, browser, pluginPath):
        # print("[wxpython.py] RequestHandler::OnPluginCrashed()")
        # print("    plugin path = %s" % pluginPath)
        pass
    # -------------------------------------------------------------------------
    # LifespanHandler
    # -------------------------------------------------------------------------

    # ** This callback is executed on the IO thread **
    # Empty place-holders: popupFeatures, client.
    def OnBeforePopup(self, browser, frame, targetUrl, targetFrameName,
            popupFeatures, windowInfo, client, browserSettings,
            noJavascriptAccess):
        # print("[wxpython.py] LifespanHandler::OnBeforePopup()")
        # print("    targetUrl = %s" % targetUrl)

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
        # print("[wxpython.py] LifespanHandler::_OnAfterCreated()")
        # print("    browserId=%s" % browser.GetIdentifier())
        pass

    def RunModal(self, browser):
        # print("[wxpython.py] LifespanHandler::RunModal()")
        # print("    browserId=%s" % browser.GetIdentifier())
        pass

    def DoClose(self, browser):
        # print("[wxpython.py] LifespanHandler::DoClose()")
        # print("    browserId=%s" % browser.GetIdentifier())
        pass

    def OnBeforeClose(self, browser):
        # print("[wxpython.py] LifespanHandler::OnBeforeClose")
        # print("    browserId=%s" % browser.GetIdentifier())
        pass

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
        windowInfo.SetAsChild(int(self.winId()))
        self.browser = cefpython.CreateBrowserSync(windowInfo,browserSettings={},navigateUrl="about:None")
        self.browser.GetMainFrame().LoadUrl(url)
        self.clientHandler.mainBrowser = self.browser
        self.browser.SetClientHandler(self.clientHandler)
        self.show()

    def exitAppWnd(self):
        print "Browser window may Be CLosed!!!"
        # cefpython.QuitMessageLoop()
        win32gui.DestroyWindow(self.winId())
        # frame = self.browser.GetMainFrame()
		# browser = frame.GetBrowser()
		# browser.CloseBrowser(True)
    def getUrlToBeLoaded(self):
        frame = self.browser.GetMainFrame()
        browser = frame.GetBrowser()
        url = browser.GetUrl()
        return url

    def moveEvent(self, event):
        cefpython.WindowUtils.OnSize(int(self.winId()), 0, 0, 0)

    def resizeEvent(self, event):
        cefpython.WindowUtils.OnSize(int(self.winId()), 0, 0, 0)