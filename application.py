'''
Created on Nov 11, 2014

@authors: Raman Pandey

Last Edit: 15-05-2015
'''
import os, sys, shutil, platform, getpass, datetime, time, re,imaplib,subprocess,urllib2,sqlite3,webbrowser
from PyQt4 import uic, QtCore, Qt, QtGui
import all_resources_rc,ui_application_window,endecyption,encrypt2
from os import listdir
from os.path import isfile, join
import socket
import platform

#
# import platform
# if platform.architecture()[0] != "64bit":
#     raise Exception("Architecture not supported: %s" \
#             % platform.architecture()[0])

print platform.architecture()
import os, sys
libcef_dll = os.path.join(os.path.dirname(os.path.abspath(__file__)),
        'libcef.dll')
# if os.path.exists(libcef_dll):
#     # Import a local module
#     if 0x02070000 <= sys.hexversion < 0x03000000:
#         import cefpython_py27 as cefpython
#     elif 0x03000000 <= sys.hexversion < 0x04000000:
#         import cefpython_py32 as cefpython
#     else:
#         raise Exception("Unsupported python version: %s" % sys.version)
# else:
    # Import an installed package
from cefpython3 import cefpython

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
# guiapp = Qt.QApplication([])
guiapp = CefApplication(sys.argv)
if platform.architecture()[0] != "32bit":
    # raise Exception("Architecture not supported: %s" % platform.architecture()[0])
    raise Exception(
        QtGui.QMessageBox.information(None, 'Error', "Architecture not supported: "+ platform.architecture()[0]))
splashPixMap=QtGui.QPixmap(":/resources/New-Splash-Screen.png")
splashWidget = QtGui.QWidget()
splashscreen = QtGui.QSplashScreen(splashWidget, splashPixMap)
progressBar = QtGui.QProgressBar(splashscreen)
progressBar.setGeometry(splashscreen.width()/12, 11*splashscreen.height()/12,10*splashscreen.width()/12, splashscreen.height()/40)
font = splashscreen.font()
font.setBold(True)
splashscreen.setFont(font)
col = QtGui.QColor(20, 20, 240)

def updateSplashProgress(percent):
    splashscreen.showMessage("Loading...")  #%s"%str(percent)+'%',QtCore.Qt.AlignBottom, col)
    progressBar.setValue(percent)

updateSplashProgress(0)
# splashscreen.showMessage("Loading...0%",QtCore.Qt.AlignBottom, col)

splashscreen.show()

from scan_man import ScanMan, ScanManThread, MyPopUp
from ui_userinfoLeftPanel import *


time.sleep(0.2)
updateSplashProgress(10)
# splashscreen.showMessage("Loading...10%",QtCore.Qt.AlignBottom, col)

# from ui_Radio import *
# from ui_loggerLeftPanel import *
# from status import statusInfo
from all_resources_rc import *
# os.environ["http_proxy"]="aanuj:ram21gas@nknproxy.iitk.ac.in:3128"
# os.environ["https_proxy"]="aanuj:ram21gas@nknproxy.iitk.ac.in:3128"
time.sleep(0.2)
updateSplashProgress(20)
# splashscreen.showMessage("Loading...20%",QtCore.Qt.AlignBottom, col)

# from pytesser import *
# from PyQt4.Qt import QNetworkProxyFactory
# from PyQt4.QtWebKit import QWebPage, QWebSettings
# from PIL import Image
import add_user,remove_user,about_dialog,welcome_dialog,operator,uuid,shutil,datetime,socket,smtplib,multiprocessing
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from PyQt4 import QtSql
from uuid import getnode as get_mac

_scanMan = None

def __dependencies_for_freezing():
    import sip


#QNetworkProxyFactory.setUseSystemConfiguration(True)
# QWebSettings.globalSettings().setAttribute(QWebSettings.AcceleratedCompositingEnabled, True)
# QWebSettings.globalSettings().setAttribute(QWebSettings.PluginsEnabled, True)
# QWebSettings.globalSettings().setAttribute(QWebSettings.AutoLoadImages, True)

time.sleep(0.2)
updateSplashProgress(30)
# splashscreen.showMessage("Loading...30%",QtCore.Qt.AlignBottom, col)

testJsString1 = '''
function getPosition(element) {
    var xPosition = 0;
    var yPosition = 0;
  
    while(element) {
        xPosition += (element.offsetLeft - element.scrollLeft + element.clientLeft);
        yPosition += (element.offsetTop - element.scrollTop + element.clientTop);
        element = element.offsetParent;
    }
    return { x: xPosition, y: yPosition };
}
function foo(){
	'''
testJsString2 = '''
	var n;
	var x = document.getElementsByTagName("IMG");
	for(var i=0;i<x.length;i++){
		imgElement = x[i].src;
		n = imgElement.search("image.php")
		if(n != -1){
		//alert("Element is found at index :" + i+"will be:" + imgElement)
		//alert("Size of the image is :" + x[i].width + "X" + x[i].height)
		var position = getPosition(x[i])
		//alert("The image is located at: " + position.x + ", " + position.y)
		dimension.getXposition(position.x + "," + position.y + "," + x[i].width + "," + x[i].height)
		//dimension.getXposition("Ycoord:"+position.y)
		//dimension.getXposition("Width:"+x[i].width)
		//dimension.getXposition("Height:"+x[i].height)
		/*
		var textToSave = 'The image is located at: ' + position.x + ', ' + position.y + 'with Dimensions : ' + x[i].width + 'X' + x[i].height
		alert(textToSave)
		var hiddenElement = document.createElement('a');
		hiddenElement.href = 'data:attachment/text,' + encodeURI(textToSave);
		hiddenElement.target = '_blank';
		hiddenElement.download = 'myFile.txt';
		hiddenElement.click();
		alert("File Has Been Saved!")
		*/
		//cropImage(x[i],position.x,position.y,x[i].width,x[i].height)
		}
	}
}
foo()
'''

modelProjectSet = None


class Application(QtCore.QObject):
    def __init__(self):
        """ Application Constructor"""
        self.version = "1.0"
        self.pro = True
        self.productName = "Smart Ad Viewer [Lifetime]"
        if self.pro:
			self.productName=self.productName
        self.proTabLimit = 12
        self.classicTabLimit = 3
		
        self.organisation = "Kanopy Techno Solutions"
        self.wnd = None
        self.enableSoundFlag = True
        self.tabLimit = self.proTabLimit if self.pro else self.classicTabLimit
        
#         time.sleep(0.2)
#         splashscreen.showMessage("Loading...60%",QtCore.Qt.AlignBottom, col)
        
        # Set app directory for saving data
        self._appDir = os.getcwd()

        ## Init Managers
        self._scanMan = ScanMan(self)  # this will have all information of user
#         time.sleep(0.2)
#         splashscreen.showMessage("Loading...70%",QtCore.Qt.AlignBottom, col)
        
        ##Initialise Views for User Interface
        time.sleep(0.2)
        updateSplashProgress(90)
        # splashscreen.showMessage("Loading...90%",QtCore.Qt.AlignBottom, col)
        self.initViews()
        #Important Show Intial License Dialog Box
        # self.wnd.showWelcomeMsg()
        self.wnd.setEnabled(True)

    def initViews(self):
        """Initializes the different views (aka tabs) in our application."""
        try:
            self.wnd = ApplicationWindow(self)
            updateSplashProgress(100)
            # splashscreen.showMessage("Loading...100%",QtCore.Qt.AlignBottom, col)

            self.wnd.showMaximized()
            self.wnd.setEnabled(True)
            # self.wnd.setEnabled(False)
        except Exception as ex:
            msgbox = QtGui.QMessageBox()
            msgbox.setWindowTitle("Information")
            msgbox.setText("Error initiating window: "+str(ex))
            msgbox.setStandardButtons(QtGui.QMessageBox.Ok)
            msgbox.exec_()
        # self.wnd.welcomePanel.setEnabled(True)
        # self.wnd.userInfoTableView.setModel(modelProjectSet)

    def getScanMan(self):
        '''
        returns scanning manager
        '''
        return self._scanMan

    def getUser(self):
        '''
        returns the user of scanning manager scanman
        '''
        scanMan = self.getScanMan()
        user = scanMan.getUser()
        return user

    def getApplicationWindow(self):
        return ApplicationWindow(self)

    def projectModelSet(self):
        return modelProjectSet


class TabHandlingThread(QtCore.QThread):
    '''
    This class is responsible for all sort of scanning work. All background scanning work will be done inside the class.
    '''
    def __init__(self,parent = None):
        super(TabHandlingThread,self).__init__(parent)
        # self._scanmanObj=ScanManObject#ScanMan Class's Object
        #self._startscan=ScanManThread(self._scanmanObj._app)#ScanMan Thread Class's object
        # self.emailsRead=0

    def run(self):
        self.sleep(10)
        print "Slept for 10 sec more!"


from MainFrame import MainFrame

class MyTableModel(QtCore.QAbstractTableModel):
    def __init__(self, datain, headerdata, parent=None, *args):
        """ datain: a list of lists
            headerdata: a list of strings
        """
        QtCore.QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata = datain
        self.headerdata = headerdata

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        return len(self.arraydata[0])

    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()
        elif role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
        return QtCore.QVariant(self.arraydata[index.row()][index.column()])

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(self.headerdata[col])
        return QtCore.QVariant()

    def sort(self, Ncol, order):
        """Sort table by given column number.
        """
        self.emit(QtCore.SIGNAL("layoutAboutToBeChanged()"))
        self.arraydata = sorted(self.arraydata, key=operator.itemgetter(Ncol))
        if order == QtCore.Qt.DescendingOrder:
            self.arraydata.reverse()
        self.emit(QtCore.SIGNAL("layoutChanged()"))

# appBase, appForm = uic.loadUiType('uiApplicationWindow.ui')
class ApplicationWindow(QtGui.QMainWindow,ui_application_window.Ui_MainWindow):
    def __init__(self, app, parent=None):
        # print appBase
        # self.createTimer()
        appFrozen = False
        self.defaultRemoved = False
        self.remainDays = 31

        # self.cacheTimer = Qt.QTimer()
        # self.cacheTimer.timeout.connect(self.clearCacheDirectory)
        # self.cacheTimer.start(20000)
        self.additionalWidgets = []
        if appFrozen:
            super(ApplicationWindow, self).__init__(parent, QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowMaximizeButtonHint)
        else:
            super(ApplicationWindow, self).__init__(parent)
        self.setupUi(self)
        self.cefModule = cefpython

        # self.proxyPanel = proxy_connection.ProxyConn(app.getScanMan(),self)
        self.leftpanelUserInfo = ui_userinfoLeftPanel(app.getScanMan(), self)


        self.aboutPanel = about_dialog.About(app.getScanMan(), self)
        # self.welcomePanel = welcome_dialog.Welcome(app.getScanMan(),self)

        self.is_finished = False
        self.not_started = True
        self.mark_as_read = False
        # self.mail_delete = False

        self.currentStatus = 0 # 0 implies Not Started 1 implies Running and 2 implies Stopped
        # self.linkopened= False
        # self.setWindowFlags(QtCore.Qt.WindowMaximizeButtonHint)
        self._app = app
        self._validLicense = False
        self.flag_log = 1
        self.flag_logger_display = 0
        self.inbox_stats_display = 0
        self.emailsReadCount = 0
        self.leftpanelUserInfo.refreshBtn.clicked.connect(self.refreshTableData)
        self.displayTableData(initialising=True)
        QtCore.QObject.connect(self,QtCore.SIGNAL("createCacheDir"),self.createCacheDir)
        # self.splitter_2.setSizes([715,472])
        # self.splitter_2.setMinimumSize(10,472)
        self.controlTabWidget.setMinimumSize(320,0)
        try:
            self.createKnowMoreDB()
        except Exception as ex:
            msgbox = QtGui.QMessageBox(self)
            msgbox.setWindowTitle("Information")
            msgbox.setText("Error creating database: "+str(ex))
            msgbox.setStandardButtons(QtGui.QMessageBox.Ok)
            msgbox.exec_()
        # splashscreen.showMessage("Loading...95%",QtCore.Qt.AlignBottom, col)
        updateSplashProgress(95)
        # self.userInfoTableView.setSortingEnabled(True)
        # self.userInfoTableView.setHorizontalHeader("Users")
        # self.userInfoTableView.setModel(app.projectModelSet())
        # self.refreshButton = QtGui.QPushButton()
        # self.refreshButton.setText("Refresh")
        # splitter_1 = QtGui.QSplitter(QtCore.Qt.Horizontal)
        # splitter_1.addWidget(self.refreshButton)
        # self.splitter.addWidget(splitter_1)
        # self.refreshButton.show()
        # splitter_1.sh*ow()
        self.log_msg = "Welcome To %s!" %self._app.productName

        #No need to add scan action like this, always keep seperate window actions whenever possible
        #self.toolBar.addAction(self.actionScan)
        #-joy

        #this is not info, this is dialog ...use proper names for variables otherwise it will become very confusing that you wont
        #understand your own code later on
        #self.leftpanelUserInfo=ui_userinfoLeftPanel()
        # -joy
        # self.welcomePanel.exec_()
        # self.radioPanel = ui_RadioLeftPanel(app.getScanMan())

        # self.loggerPanel =ui_LoggerLeftPanel(app.getScanMan())

        self.controlTabWidget.addTab(self.leftpanelUserInfo, "Controls")

        # splashscreen.showMessage("Loading...97%",QtCore.Qt.AlignBottom, col)
        updateSplashProgress(97)
        #this will remove the button you added!!! so if you use this, make sure to programatically add button
        #at top right!!
        #         self.uiGraphicsTabWidget.clear()
        #-joy
        #         self.uiGraphicsTabWidget.clear()
        # cache = Qt.QNetworkDiskCache()
        # cache.setCacheDirectory('cache')

        # self.timer = QtCore.QTimer()
        # self.timer.timeout.connect(self.clearCacheDirectory)
        # self.timer.start(1800000)

        # gmailWebView = self._app.getScanMan().getBrowserPanel()
        gmailWebView = MainFrame()
        # gmailWebView.page().networkAccessManager().setCache(cache)

        # self.editTableDlg = EditItemDialog()
        #now we should make a widget with a button at top, browser in middle and spring spacer at bottom
        #this special widget should have an addUrlTab function to add new qwebbrowsers above the spacer...
        #lot of careful work is required in making this nicely
        #a simple way is to maintain a list of tabs (qwebviewers)

        self.smartScanWidgets = [
            gmailWebView]  #this is temporary, this widget is what should have the above described structure
        #         self.uiGraphicsTabWidget.addTab(self.smartScanWidget, "Web Browser")
        self.vboxVerticalLayout = self.uiGraphicsTab.layout()

        # splashscreen.showMessage("Loading...98%",QtCore.Qt.AlignBottom, col)
        updateSplashProgress(98)
        if len(self.smartScanWidgets) > 0:
            # a more generalised way to insert in order needs to be developed
            self.vboxVerticalLayout.insertWidget(self.vboxVerticalLayout.count() - 1, self.smartScanWidgets[0])
            self.smartScanWidgets[0].loadCustumUrl('https://www.safelistech.com')
            # self.smartScanWidgets[0].show()
            # self.smartScanWidgets[0].scanUrl('http://www.safelistech.com')

        # self.addUsersCombo()
        # self.vboxVerticalLayout.addWidget(self.editTableDlg)
        # splashscreen.showMessage("Loading...99%",QtCore.Qt.AlignBottom, col)
        updateSplashProgress(99)
        self.setAppwindowTitle(self._app.productName)

        self._connectSlots()

        """set the relative sizes of the widgets in the vertical splitter"""
        self.splitter.setSizes([400, 100])
        """populate menu_recent_projects"""

        self._progressDialog = None
        # self.displayTableData()
        if (self.flag_log == 1):
            '''self.logWindow.setPlainText(self.log_msg)'''
    def setProxyData(self,type,host,port,username,password):
        conn = sqlite3.connect('proxydata.db')
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS proxydata(host varchar,port varchar,username varchar,password varchar)")
        cur.executescript("INSERT into proxydata VALUES('"+str(host)+"','"+str(port)+"','"+str(username)+"','"+str(password)+"')")
        conn.commit()
        print "Proxy Data Inserted"
        conn.close()
        # os.environ["http_proxy"] = ("'{0}':'{1}'@'{2}':'{3}'".format(username,password,host,port))
        # os.environ["https_proxy"] = ("'{0}':'{1}'@'{2}':'{3}'".format(username,password,host,port))
        self.leftpanelUserInfo.loggerTextArea.append("Proxy Data Has Been Set!!!")

    def createCacheDir(self):
        self.cache = Qt.QNetworkDiskCache()
        self.cache.setCacheDirectory('cache')
        # self.timerwndLoad = QTimer()

    def clearCacheDirectory(self):
        try:
            mypath = "cacheSAV"
            onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
            print "All Required FIles",onlyfiles
            for cachefile in onlyfiles:
                try:

                    os.remove(os.path.join(".",mypath,cachefile))
                    print cachefile,"Cache FIle is deleted"
                except:
                    print cachefile,"File is not delted"
        except Exception as ex:
            print "Cache Could not be cleared!!!"
            # if(os.path.exists("cacheSAV")):
            #     shutil.rmtree("cacheSAV")

        # print "Old Cache Deleted"
        # self.cache = Qt.QNetworkDiskCache()
        # self.cache.setCacheDirectory('cache')
        # print "New Cache Created"
    
    def convertToTwo(self,num):
        if (len(str(num)) == 1):
            newnum = "0"+str(num)
            return newnum
        else:
            return str(num)

    def getCurrentTimeVal(self):
        try:

            # proxy = urllib2.ProxyHandler({'http': 'http://aanuj:ram21gas@nknproxy.iitk.ac.in:3128','https': 'http://aanuj:ram21gas@nknproxy.iitk.ac.in:3128'})
            # auth = urllib2.HTTPBasicAuthHandler()
            # opener = urllib2.build_opener(proxy, auth, urllib2.HTTPHandler)
            # urllib2.install_opener(opener)

            conn = urllib2.urlopen('https://www.safelistech.com/time.php')
            return_str = conn.read()
            print return_str

            data = return_str.split("T")
            datepart = data[0].split("-")
            timepart = data[1].split("+")
            year = datepart[0]
            month = datepart[1]
            date = datepart[2]
            timesec = timepart[0].split(":")
            hour = timesec[0]
            minute = timesec[1]
            seconds = timesec[2]
            print "retrieve date and time value"
            print year,month,date,hour,minute,seconds
            dobj = datetime.datetime(int(year),int(month),int(date),int(hour),int(minute),int(seconds))
            return dobj
        except Exception as ex:
            print "Could not created date time object",ex


    def sendTrackingDetails(self):
        try:
            ipAddr = socket.gethostbyname(socket.gethostname())
            startDobj = self.getCurrentTimeVal()
            startYear = startDobj.year
            startMonth = startDobj.month
            startDate = startDobj.date()
            startDay = startDobj.day
            startHour = startDobj.hour
            startMinute = startDobj.minute
            startSeconds = startDobj.second
        except:
            print "data could not be retieved due to no internet connection"
            msgbox = QtGui.QMessageBox(self)
            msgbox.setWindowTitle("Information")
            msgbox.setText("Your System should have Internet Connection to Continue!!!\nSoftware is now Closing !!! ")
            msgbox.setStandardButtons(QtGui.QMessageBox.Ok)
            msgbox.exec_()
            self.close()

        try:
            recipients = ["tracker@safelistech.com"]
            emaillist = [elem.strip().split(',') for elem in recipients]
            msg = MIMEMultipart()
            msg['Subject'] = 'Tracking Detailsw'
            msg['From'] = 'successful@safelistech.com'

            msg.preamble = 'Multipart massage.\n'

            part = MIMEText("IP Address:"+str(ipAddr)+"\n"+"Date:"+str(startDate)+str(startMonth)+str(startYear)+ "\n" + "Time:"+ str(startHour)+":"+str(startMinute)+":"+str(startSeconds))
            msg.attach(part)

            # username = os.getenv('proxy_username')
            # password = os.getenv('proxy_password')

            server = smtplib.SMTP_SSL(host="www.safelistech.com:",port=465,timeout=10)
            server.ehlo()
            server.starttls()
            server.set_debuglevel(2)
            server.login("successful@safelistech.com","4=TSk@q]Bm&C")

            server.sendmail(msg['From'], emaillist , msg.as_string())
            print "Tracking Details Sent!!!"
        except:
            print "Tracking Details Sending Failed"

    def showWelcomeMsg(self):
        ed = endecyption.CryptAlgo()
        e = encrypt2.EndecryAlgo()
        fname = "license.lic"
        licenseValidated = False
        if(not os.path.isfile(fname)):
            # self.welcomePanel.exec_()
            pass
        else:
            licfile = "license.lic"
            with open(licfile,'r+') as outfile:
                # licContent = ed.decrypt_text(ed.decrypt_text(outfile.read()))
                licContent = e.decryp(outfile.read())
                # print len(licContent)
                bigkey = licContent[0:39]
                datepart = licContent[39:]
                print "datepart",datepart
                regyear = datepart[0:4]
                regmonth = datepart[4:6]
                regdate = datepart[6:8]
                reghr = datepart[8:10]
                regminute = datepart[10:12]
                regsec = datepart[12:14]
                print regyear,regmonth,regdate,reghr,regminute,regsec
                dreg = datetime.datetime(int(regyear),int(regmonth),int(regdate),int(reghr),int(regminute),int(regsec))
                dnow = self.getCurrentTimeVal()
                try:
                    delta = dnow-dreg
                    self.remainDays = 31 - delta.days
                    # secondsElapsed = delta.seconds
                    # timeelapsed = delta.seconds/(3600*720.0)
                    # print "Total Time Elapsed",int(timeelapsed)
                    self.sendTrackingDetails()
                    if self.remainDays:
                        datVal = self.remainDays
                        self.leftpanelUserInfo.loggerTextArea.setHtml("<html><head></head><body><p><span style='color:#00aaff;font-size:18px'>Welcome To Smart Ad Viewer!!!</span><br /><span style='color:red'>THIS IS A TRIAL VERSION AND IT WILL EXPIRE IN %s DAYS !!!</span></p></body></html>"%datVal)
                    if(delta.days >= 31):
                        msgbox = QtGui.QMessageBox(self)
                        msgbox.setWindowTitle("Information")
                        msgbox.setText("Your Trial Period is Over! Please Upgrade To Lifetime License!!!\nApplication will now close !!! ")
                        msgbox.setStandardButtons(QtGui.QMessageBox.Ok)
                        msgbox.exec_()

                        self.close()
                        exit(0)
                        # return
                except Exception as ex:
                    print "There is no data exists, error is ",str(ex)
                # print licContent
                lc2 = ed.decrypt_text(ed.decrypt_text(bigkey))
                varMacidsoft = lc2[27:]
                varOtpsoft = lc2[13:27]
                varorderid = lc2[0:13]
                # print "mac id decrypted:",varMacidsoft
                # print "OTP decrypted",varOtpsoft
                # print "Order Id decrypted",varorderid
                macStr = str(uuid.uuid1())[-12:]
                # print "mac id original:",macStr
                # self.sendTrackingDetails()
                if(varMacidsoft.strip() == macStr.strip()):
                    print "Valid License File"
                    self._validLicense = True
                    # self.close()
                else:
                    msgbox = QtGui.QMessageBox(self)
                    # msgbox.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(':/resources/Icon.png')))
                    msgbox.setWindowTitle("Information")
                    msgbox.setText("This is not a valid License File.Please ask for valid License File!!!")
                    msgbox.setStandardButtons(QtGui.QMessageBox.Ok)
                    msgbox.exec_()
                    self.close()
                    exit(0)
        if self._validLicense:
            self.setEnabled(True)
            return
        else:
            msgbox = QtGui.QMessageBox(self)
            msgbox.setWindowTitle("Information")
            msgbox.setText("License File is not Found!!!\nCould not authenticate license, Closing...!!!")
            msgbox.setStandardButtons(QtGui.QMessageBox.Ok)
            msgbox.exec_()
            self.close()
            exit(0)

    def createKnowMoreDB(self):
        if os.path.exists('knowmore.db'):
            os.remove('knowmore.db')
            conn = sqlite3.connect('knowmore.db')
            cur = conn.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS knowmorelinks(links varchar)")
            conn.close()

    def refreshTableData(self):
        self.leftpanelUserInfo.loggerTextArea.append("Refreshing...")
        self.leftpanelUserInfo.loggerTextArea.append("Viewing...")
        # self.displayTableData()
        self.getStatsData()

    def getStatsData(self):
        DATABASE_NAME = "smartusers.db"
        conn = sqlite3.connect(DATABASE_NAME)
        cur = conn.cursor()
        cur.execute("SELECT username,password FROM users")
        dbData =  cur.fetchall()
        for data in dbData:
            username = data[0]
            password = data[1]
            print "Username : " + username
            print "Password : " + password
            totalM,unreadM =self.getEmailCount(username,password)
            cur.execute("UPDATE users SET totalEmails ='"+totalM+"'WHERE username = '"+username+"' ")
            cur.execute("UPDATE users SET unreadEmails ='"+unreadM+"'WHERE username = '"+username+"' ")
            conn.commit()
        cur.execute("SELECT username,totalEmails,unreadEmails FROM users")
        statsData = cur.fetchall()
        # print "username",statsData
        conn.close()

        header = ['Username', 'Total Emails', 'Unread Emails']
        tm = MyTableModel(statsData, header)
        self.leftpanelUserInfo.userInfoTableView.setModel(tm)

        print "data updated"

    def displayTableData(self, initialising=False):
        DATABASE_NAME = "smartusers.db"

        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName(DATABASE_NAME)
        db.open()

        projectModel = QSqlQueryModel()
        # projectModel.setQuery("select username,totalEmails,unreadEmails from users",db)
        # projectModel.setHeaderData(0,QtCore.Qt.Horizontal,"Username")
        # projectModel.setHeaderData(1,QtCore.Qt.Horizontal,"Total Emails")

        header = ['Username', 'Total Emails', 'Unread Emails']
        # tm = MyTableModel(statsheader)
        # self.leftpanelUserInfo.userInfoTableView.setModel(tm)
        # self.leftpanelUserInfo.userInfoTableView.setModel(projectModel)
        # self.leftpanelUserInfo.userInfoTableView.setSortingEnabled(True)


        # self.updateTableData()
        db.close()
        if initialising:
            return

        conn = sqlite3.connect(DATABASE_NAME)
        cur = conn.cursor()
        cur.execute("SELECT username,password FROM users")
        dbData =  cur.fetchall()
        for data in dbData:
            username = data[0]
            password = data[1]
            print "Username : " + username
            print "Password : " + password
            totalM,unreadM =self.getEmailCount(username,password)
            cur.execute("UPDATE users SET totalEmails ='"+totalM+"'WHERE username = '"+username+"' ")
            cur.execute("UPDATE users SET unreadEmails ='"+unreadM+"'WHERE username = '"+username+"' ")
            conn.commit()

            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName(DATABASE_NAME)
            db.open()

            projectModel = QSqlQueryModel()
            projectModel.setQuery("select username,totalEmails,unreadEmails from users",db)

            self.leftpanelUserInfo.userInfoTableView.setModel(projectModel)
            self.leftpanelUserInfo.userInfoTableView.setSortingEnabled(True)

            # self.updateTableData()
            db.close()

        # projectView = QTableView()
        # projectView.setModel(projectModel)
        # projectView.show()
    # def updateTableData(self):
    #     DATABASE_NAME = "smartusers.db"
    #     conn = sqlite3.connect(DATABASE_NAME)
    #     cur = conn.cursor()
    #     cur.execute("SELECT username,password FROM users")
    #     dbData =  cur.fetchall()
    #     for data in dbData:
    #         username = data[0]
    #         password = data[1]
    #         print "Username : " + username
    #         print "Password : " + password
    #         totalM,unreadM =self.getEmailCount(username,password)
    #         cur.execute("UPDATE users SET totalEmails ='"+totalM+"'WHERE username = '"+username+"' ")
    #         cur.execute("UPDATE users SET unreadEmails ='"+unreadM+"'WHERE username = '"+username+"' ")
    #         conn.commit()

    def getEmailCount(self,username,password):
        M = imaplib.IMAP4_SSL('imap.gmail.com',993)
        M.login(username, password)
        print "Total Mails : " + str(M.select('INBOX')[1][0])
        unreadMails = M.search(None,'UnSeen')
        print "Total Unread Mails : "+ str(len(unreadMails[1][0].split(" ")))
        return str(M.select('INBOX')[1][0]),str(len(unreadMails[1][0].split(" ")))


    def closeEvent(self, e):
        print 'enterCloseEvent'
        try:
            for mypop in self.additionalWidgets:
                mypop.webwnd.exitAppWnd()

            self.additionalWidgets=[]

            for defView in self.smartScanWidgets:
                defView.exitAppWnd()
            self.smartScanWidgets = []

            cefpython.Shutdown()
        except:
            pass
        finally:
            e.accept()

    def changeEvent(self, e):
        # print 'enter change event'
        e.ignore()
        super(ApplicationWindow, self).changeEvent(e)
        return
        if e.type() == QtCore.QEvent.WindowStateChange:
            if self.windowState() & QtCore.Qt.WindowMinimized:
                print 'eneterMinimizeEvent'
                e.ignore()
                return

    def updateLogWindow(self, logMsg):
        '''
        Trying to Log Status
        '''
        if (self.flag_log == 2):
            self.logWindow.setPlainText("Connection Successfull!")

    def openLoadUrl(self, targetLink):
        '''
        This function is responsible to load the link that was sent into the custom browser.

        Primarily this function removes the current tab at index 0 and then add the new custom tab at the same index with the custom widget.
        '''
        if not self.defaultRemoved:

            self.uiGraphicsTabWidget.removeTab(0)  # Remove the current Tabe at index 0
            self.defaultRemoved = True
        # self.uiGraphicsTabWidget.removeTab(0)
        # print "Target Link To Be Loaded on Custom Browser :" + targetLink
        self.additionalWidgets.append(MyPopUp(self._app.getScanMan(), self))  # Append objects of Worker Process in additional widget list
        # self.additionalWidgets.append(Worker(self._app.getScanMan(),self))
        # self.timer = QTimer()
        # self.timer.timeout.connect(self.timeFinished)
        # self.timer.start(10000)#start timer for 10 sec
        # self.additionalWidget.setVisible(False)
        # self.proc_name = self.proc.name
        self.addTabWithProcess(self.additionalWidgets,targetLink)

        # self.additionalWidget.webwnd.loadFinished.connect(self.waitToLoad)
        # self.additionalWidget.webwnd.load(QtCore.QUrl(targetLink))
        # self.additionalWidget.webwnd.show()
        # print "Target link Shown!"
#         QtCore.QObject.connect(self.additionalWidgets, QtCore.SIGNAL('tryLoadNewTab'), self.hideUrl)
        # QtCore.QObject.connect(self.additionalWidgets, QtCore.SIGNAL('hideCurrentUrl'), self.hideUrl)
    # def timeFinished(self):
    #     print '_----------------____________--------------_'
    #     self.is_finished = True
    #     self.additionalWidgets[-1].clickBtn.setEnabled(False)
    #     self.additionalWidgets[-1].changeStatus()
    def addTabWithProcess(self,additionalWidgets,targetLink):
        self.uiGraphicsTabWidget.addTab(additionalWidgets[-1], "Ad Tab")
        self.uiGraphicsTabWidget.setCurrentIndex(len(additionalWidgets)-1)

        additionalWidgets[-1].prepareToLoadUrl(targetLink)
        additionalWidgets[-1].linkopened=True

    def tormant(self,proc_name):
        PROCNAME = proc_name
        for proc in psutil.process_iter():
            if proc.name() == PROCNAME:
               proc.kill()
        print "Terminating",PROCNAME


    def InitialiseCaptchaManager(self):
        # print "Wait to Load!"
        # self.timer = QTimer()
        # self.timer.timeout.connect(self.timeFinished)
        # self.timer.start(10000)#start timer for 10 sec
        # self.timerwndLoad.timeout.connect(self.loadwndfinished)
        # self.timerwndLoad.start(10000)
        self.captchaManager = CaptchaManager(self)
        self.captchaManager._loadFinished()

    def loadwndfinished(self):
        print "Url Has Been Loaded after 10 sec!"

    def hideUrl(self, newTargetLink):
        # self.additionalWidgets[-1].clickBtn.setEnabled(False)
        # print "Hide Current Url"
        # print "Load new Url : " + str(newTargetLink)
        # print "Current Tab Index : " + str(self.uiGraphicsTabWidget.currentIndex())

        newIndex = self.uiGraphicsTabWidget.currentIndex() + 1
        # print "New Index Position : " + str(newIndex)
        self.additionalWidgets.append(MyPopUp(self._app.getScanMan(),self))  # Creates object of additional widget class
        # self.uiGraphicsTabWidget.addTab(self.additionalWidget,"Web Bowser 2")
        #self.uiGraphicsTabWidget.setCurrentIndex(newIndex)
        # self.uiGraphicsTabWidget.addTab(self.additionalWidgets[-1], "New Tab Browser")
        self.additionalWidgets[-1].prepareToLoadUrl(newTargetLink)
        # self.additionalWidget2.webwnd.loadFinished.connect(self.waitToLoad)
        # self.additionalWidget2.webwnd.load(QtCore.QUrl(newTargetLink))
        # self.additionalWidget2.webwnd.show()
        # print " New Target link has b*33een Shown!"
        # self.waitToFinish = TabHandlingThread()
        # self.waitToFinish.start()
        # self.additionalWidgets[-1].webwnd.stop()
        # print "Page Loading has been stopped!"
        # QtCore.QObject.connect(self.additionalWidget2.clickBtn, QtCore.SIGNAL('clicked()'), self.indexManager)

    # def indexManager(self):
    #     self.totalTabs = self.uiGraphicsTabWidget.count()
    #     print "Total Tabs : " + str(self.totalTabs)
    #
    #     self.additionalWidgetList = [None] * self.totalTabs
    #     self.additionalWidgetList[self.totalTabs-1]= MyPopUp(self._app.getScanMan())
    #     self.uiGraphicsTabWidget.addTab(self.additionalWidgetList[self.totalTabs-1],"New Browser")
    #     QtCore.QObject.connect(self.additionalWidgetList[self.totalTabs-1], QtCore.SIGNAL('hideCurrentUrl'), self.loadNewHideUrl)
    #     QtCore.QObject.connect(self.additionalWidgetList[self.totalTabs-1].clickBtn, QtCore.SIGNAL('clicked()'), self.indexManager)
    #     #self.additionalWidgetList[totalTabs-1].clickBtn.setVisible(False)
    #     #QtCore.QObject.connect(self.additionalWidgetList[self.totalTabs-1], QtCore.SIGNAL('hideCurrentUrl'), self.loadNewHideUrl)
    #
    # def loadNewHideUrl(self,newTargetLink):
    #     print "LOad the URL which to be loaded after hide : " + newTargetLink
    #     self.additionalWidgetList[self.totalTabs-1].webwnd.loadFinished.connect(self.waitToLoad)
    #     self.additionalWidgetList[self.totalTabs-1].webwnd.load(QtCore.QUrl(newTargetLink))
    #     self.additionalWidgetList[self.totalTabs-1].webwnd.show()
    #     print " New Target link has been Shown!"

    def _connectSlots(self):
        QtCore.QObject.connect(self.actionExit, QtCore.SIGNAL('triggered()'), self.exitApp)
        # QtCore.QObject.connect(self.actionUser, QtCore.SIGNAL('triggered()'), self.openUserInfoDialog)
        # QtCore.QObject.connect(self.actionTimeSet, QtCore.SIGNAL('triggered()'), self.openTimeSetDialog)
        QtCore.QObject.connect(self.actionAdd_User,QtCore.SIGNAL('triggered()'),self.openAddUserWindow)
        QtCore.QObject.connect(self.actionRemove_User,QtCore.SIGNAL('triggered()'),self.openRemoveUserWindow)
        QtCore.QObject.connect(self.actionTutorial,QtCore.SIGNAL('triggered()'),self.openTutorial)
        QtCore.QObject.connect(self.actionAbout,QtCore.SIGNAL('triggered()'),self.openAboutDlg)
        QtCore.QObject.connect(self.actionLogger,QtCore.SIGNAL('triggered()'),self.displayLogger)
        QtCore.QObject.connect(self.actionInbox_Stats,QtCore.SIGNAL('triggered()'),self.displayInboxStats)
        # QtCore.QObject.connect(self.actionConnection_Settings_2,QtCore.SIGNAL('triggered()'),self.displayProxyDialog)

    def displayProxyDialog(self):
        self.proxyPanel.show()

    def displayLogger(self):
        self.flag_logger_display = 1-self.flag_logger_display
        if(self.flag_logger_display % 2 == 0):
            self.leftpanelUserInfo.loggerTextArea.setVisible(True)
        else:
            self.leftpanelUserInfo.loggerTextArea.setVisible(False)

    def displayInboxStats(self):
        self.inbox_stats_display = 1-self.inbox_stats_display
        if(self.inbox_stats_display % 2 == 0):
            self.leftpanelUserInfo.userInfoTableView.setVisible(True)
            self.leftpanelUserInfo.refreshBtn.setVisible(True)
        else:
            self.leftpanelUserInfo.userInfoTableView.setVisible(False)
            self.leftpanelUserInfo.refreshBtn.setVisible(False)

    def openTutorial(self):
        # subprocess.Popen(["SmartAdViewerGuide.pdf"],shell=True)
        urlToBeOpened = 'Smart Ad Viewer Help Guide.html'
        webbrowser.open_new_tab(urlToBeOpened)
	
    def openAddUserWindow(self):
        self.addUserPanel = add_user.AddUser(app.getScanMan(),self)
        self.addUserPanel.setWindowTitle("Add User To Our Database")
        # self.addUserPanel.ackMsg.setVisible(False)
        self.addUserPanel.exec_()

    def openRemoveUserWindow(self):
        self.removeUserPanel = remove_user.RemoveUser(app.getScanMan(), self)
        self.removeUserPanel.setWindowTitle("Remove User From Our Database")
        # self.removeUserPanel.userRemoveStatus.setVisible(False)
        self.removeUserPanel.exec_()

    def openAboutDlg(self):
		#self.aboutPanel.setAppwindowTitle("About")
        self.aboutPanel.exec_()
    
    def exitApp(self):
        self.close()

    
    '''
    sets the main window title
    '''
    def setAppwindowTitle(self, applicationWindowTitle):
        self.setWindowTitle(str(applicationWindowTitle))


    # def openUserInfoDialog(self):
        # infoSetDialog(self._app.getUser()).exec_()


    # def openScanStatusDialog(self):
        # statusInfo().exec_()


    # def openTimeSetDialog(self):
    #     self.timesetDialog = timeset()
    #     self.timesetDialog.setWindowTitle("Time Settings")
    #     self.timesetDialog.show()
    #     self.timesetDialog.exec_()


    def getUser(self):
        scanman = self._app.getScanMan()
        return scanman.getUser()


class CaptchaManager(QtCore.QThread):
    def __init__(self, appWndObj, parent=None):
        super(CaptchaManager, self).__init__(parent)
        self.appWndObj = appWndObj
        print "Captcha Manager's Object Has Been Created!"

        def run(self):
            print "Captcha Manager's Thread has Been Started!"
            self._loadFinished()

    def _loadFinished(self):
        print "Load Has Been Finished!"

        # self.timer = QTimer()
        # self.timer.timeout.connect(self.timeFinished)
        # self.timer.start(10000)#start timer for 10 sec
        if len(self.appWndObj.additionalWidgets)>0:
            self.frame = self.appWndObj.additionalWidgets[-1].webwnd.page().mainFrame()
            self.htmlContent = unicode(self.frame.toHtml()).encode('utf-8')
            # print self.htmlContent
            searchObj = re.search(r' .* code below and hit continue.*', self.htmlContent, re.DOTALL)

            if searchObj:
                print "This Page has Captcha Detected!"
                self.frame.addToJavaScriptWindowObject('dimension', Dimension(self.appWndObj.additionalWidgets[-1].webwnd))
                self.appWndObj.additionalWidgets[-1].webwnd.page().setViewportSize(self.frame.contentsSize())
                image = Qt.QImage(self.appWndObj.additionalWidgets[-1].webwnd.page().viewportSize(), Qt.QImage.Format_ARGB32)
                painter = QtGui.QPainter(image)
                self.frame.render(painter)
                painter.end()
                image.save('test.png')
                print("Image Has Been Saved!")

                # imgSrc =imgsrc.format(captchalink =captchlink)
                testJsString = testJsString1 + testJsString2
                #print testJsString
                #testjsstring=testJsString2.format(captchalink =captchlink)
                #testJsString=testJsString1 + testjsstring + testJsString3
                #print testJsString

                self.frame.evaluateJavaScript(testJsString)
                print "Script Evaluated"

                capDimension = Dimension()
                capval = capDimension.getCapthcaText()
                capVal = int(capval)
                captchaFillScript = '''
                var x = document.getElementsByName("num");
                //alert (x.length)
                x[0].value={CaptchaValue}
                //alert("Captcha Text is :" + x[0].value)
                document.getElementsByName('continue').item(0).click()
                '''.format(CaptchaValue=capVal)
                self.frame.evaluateJavaScript(captchaFillScript)
                print "Captcha Has Been Filled!"

            else:
                print "This Page Doesn't has Captcha! "

    def timeFinished(self):
        print "Page Loading time has been finished!"

class Dimension(QtCore.QObject):
    @QtCore.pyqtSlot(str)
    def getXposition(self, data1):
        print data1
        dimensionVariables = data1.split(',')
        print "X Coordinate :" + dimensionVariables[0]
        print "Y Coordinate :" + dimensionVariables[1]
        print "Width :" + dimensionVariables[2]
        print "Height :" + dimensionVariables[3]
        Xpos = int(dimensionVariables[0])
        Ypos = int(dimensionVariables[1])
        width = int(dimensionVariables[2])
        height = int(dimensionVariables[3])
        left = Xpos
        right = left + width
        top = Ypos
        bottom = top + height
        im = Image.open('test.png')
        crop_im = im.crop((left, top, right, bottom))
        crop_im.save("crop_image.gif")
        print "Image Has been Cropped!"

    def getCapthcaText(self):
        print "Inside getCapthcaText!"
        img = Image.open("crop_image.gif")
        captchatxt = image_to_string(img).replace(" ", "")
        print captchatxt
        captchaValue = self.convertToInt(captchatxt)
        print captchaValue
        return captchaValue

    def convertToInt(self, captchatxt):
        print "Inside convertTo Int!"
        numstr = captchatxt
        newStr = ""
        allowedChars = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        for aChar in numstr:
            if aChar in allowedChars:
                newStr = newStr + aChar
            else:
                pass

        print str(int(newStr))
        return newStr

time.sleep(0.2)
# splashscreen.showMessage("Loading...50%",QtCore.Qt.AlignBottom, col)
updateSplashProgress(50)

if __name__ == '__main__':
    # Intercept python exceptions. Exit app immediately when exception
    # happens on any of the threads.
    sys.excepthook = ExceptHook

    # Application settings
    settings = {
        "debug": True, # cefpython debug messages in console and in log_file
        # "application_cache_disabled":True,
        # "page_cache_disabled":True,
        "log_severity": cefpython.LOGSEVERITY_INFO, # LOGSEVERITY_VERBOSE
        "log_file": GetApplicationPath("debug.log"), # Set to "" to disable.
        "release_dcheck_enabled": True, # Enable only when debugging.
        # This directories must be set on Linux
        "locales_dir_path": cefpython.GetModuleDirectory()+"/locales",
        "resources_dir_path": cefpython.GetModuleDirectory(),
        "browser_subprocess_path": "%s/%s" % (
            cefpython.GetModuleDirectory(), "subprocess"),
    }
    settings["cache_path"] = "cacheSAV"
    settings["persist_session_cookies"] = True
    settings["ignore_certificate_errors"] = True
    # settings["disable-plugins"] = True
    # Command line switches set programmatically
    switches = {
         # "proxy-server": "http://nknproxy.iitk.ac.in:3128",
        #"proxy-auto-detect":True,
        # "enable-media-stream": "",
        # "--invalid-switch": "" -> Invalid switch name
    }
    switches["disable-javascript-open-windows"] = False
    # switches["no-proxy-server"] = True

    # Application settings2
    settings2 = {
        "debug": True, # cefpython debug messages in console and in log_file
        # "application_cache_disabled":True,
        # "page_cache_disabled":True,
        "log_severity": cefpython.LOGSEVERITY_INFO, # LOGSEVERITY_VERBOSE
        "log_file": GetApplicationPath("debug.log"), # Set to "" to disable.
        "release_dcheck_enabled": True, # Enable only when debugging.
        # This directories must be set on Linux
        "locales_dir_path": cefpython.GetModuleDirectory()+"/locales",
        "resources_dir_path": cefpython.GetModuleDirectory(),
        "browser_subprocess_path": "%s/%s" % (
            cefpython.GetModuleDirectory(), "subprocess"),
    }
    settings2["cache_path"] = "cacheSAV"
    settings2["persist_session_cookies"] = True
    # Command line switches set programmatically
    switches2 = {
         # "proxy-server": "http://nkgjjnproxy.iitk.ac.in:3128",
        # "proxy-auto-detect":True,
        # "enable-media-stream": "",
        # "--invalid-switch": "" -> Invalid switch name
    }


    cefpython.Initialize(settings, switches)
    time.sleep(2)
    #cefpython.Shutdown()
    # print dir(cefpython)


    app = Application()

    splashscreen.finish(splashWidget)

    # cefpython.Initialize(settings, switches)

    # app.getApplicationWindow().userInfoTableView.setModel(projectModel)
    sys.exit(guiapp.exec_())
    guiapp.stopTimer()

