'''
Created on Dec 21, 2014

@author: Raman Pandey
'''
# from ui_loggerLeftPanel import *
from PyQt4.QtCore import QUrl
from PyQt4 import Qt,uic,QtCore,QtGui,QtWebKit
from PyQt4.QtSql import *
from PyQt4.Qt import QWebView
import sqlite3,os,sys,imaplib,ui_user_info_modified,operator

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
# userbase,userform=uic.loadUiType('uiUserInfo_modified_2.ui')
class ui_userinfoLeftPanel(QtGui.QDialog,ui_user_info_modified.Ui_Dialog):
    #def __init__(self,parent=None):
    def __init__(self,scanMan, parent=None):
        super(ui_userinfoLeftPanel,self).__init__(parent)
        self.setupUi(self)
        self._scanMan = scanMan
        self.parent = parent
        self.emailVal = 0
        self._initViews()
        self.connected = False
        self.username=""
        self.password=""
        self.scanButton.setEnabled(False)
        self.stopScanButton.setEnabled(False)
        QtCore.QObject.connect(self.usersCombo,QtCore.SIGNAL("currentIndexChanged(const QString&)"),self.getUserLoginData)
        QtCore.QObject.connect(self,QtCore.SIGNAL("updateEmailCount"),self.updateEmailCount)
        self.deleteMailOn.toggled.connect(self.deleteMailSignal)
        self.deleteMailOff.toggled.connect(self.stopDeletingMails)
        self._connectSlots()
        self.fillUsersCombo()#Shows Users Combo Box
        QtCore.QObject.connect(self,QtCore.SIGNAL("changeConnected"),self.connectedStatus)
        QtCore.QObject.connect(self,QtCore.SIGNAL("connectionFailed"),self.connectionFail)
        QtCore.QObject.connect(self,QtCore.SIGNAL("loginChallenge"),self.loginChallenge)


    def updateEmailCount(self):
        self.emailVal += 1
        self.emailsValue.setText(QtCore.QString(str(self.emailVal)))
        print "Email Count Updated",self.emailVal
        # if (self.emailVal > 300):
        #     self.parent.clearCacheDirectory()

    def connectionFail(self,ex):
        msgbox = QtGui.QMessageBox()
        msgbox.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(':/resources/Icon.png')))
        msgbox.setWindowTitle("Information")
        msgbox.setText('Connection Failed!!!\n' + ex)
        msgbox.setStandardButtons(QtGui.QMessageBox.Ok)
        msgbox.exec_()
        self.loggerTextArea.append("Connection Failed!!!")
        self.connectButton.setIcon(QtGui.QIcon(QtGui.QPixmap(':/resources/Connect.png')))
        self.connectButton.setIconSize(QtCore.QSize(140,50))
        self.connectButton.setEnabled(True)

    def deleteMailSignal(self):
        # self._scanMan._app.wnd.mail_delete = True
        self._scanMan.mailToBeDeleted = True
        print "Mail Should Be Deleted"

    def connectedStatus(self):
        self.connectButton.setIcon(QtGui.QIcon(QtGui.QPixmap(':/resources/Connected.png')))
        self.connectButton.setIconSize(QtCore.QSize(140,50))

    def loginChallenge(self,ex):
        msgbox = QtGui.QMessageBox()
        msgbox.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(':/resources/Icon.png')))
        msgbox.setWindowTitle("Information")
        msgbox.setText('Connection Failed!!!\n' + ex)
        msgbox.setStandardButtons(QtGui.QMessageBox.Ok)
        msgbox.exec_()
        self.loggerTextArea.append("Connection Failed!!!")
        self.connectButton.setIcon(QtGui.QIcon(QtGui.QPixmap(':/resources/Connect.png')))
        self.connectButton.setIconSize(QtCore.QSize(140,50))
        self.connectButton.setEnabled(True)

    def stopDeletingMails(self):
        # self._scanMan._app.wnd.mail_delete = False
        self._scanMan.mailToBeDeleted = False
        print "Mail WOuld Not Be Deleted"

    def getUserLoginData(self):
        # self.getUserData()
        # self.connectButton.setText("Connect")
        self.emailsValue.setText("0")
        self.parent.currentStatus = 0
        self.connectButton.setIcon(QtGui.QIcon(QtGui.QPixmap(':/resources/Connect.png')))
        # self.connectButton.setStyleSheet("background-image: url(':/resources/Connect.png');")
        self.connectButton.setEnabled(True)
        print "login data to be captured here"
        # self.configureDB()
        self.username= str(self.usersCombo.currentText())
        self.conn = sqlite3.connect('smartusers.db')
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT password FROM users WHERE username = '"+self.username+"'")
        self.optChangeDataPwd =  self.cur.fetchall()
        if(self.optChangeDataPwd == []):
            print "There is no such user!"
        else:
            self.password = self.optChangeDataPwd[0][0]
            print "Username after change : " + self.username
            print "Password after change : " + self.password
            return self.username,self.password

    def fillUsersCombo(self):
        if (os.path.exists('smartusers.db')):
            # self.getUserData()
            self.configureDB()
            self.model = QSqlTableModel()
            self.model.setTable("users")
            self.model.select()
            self.usersCombo.setModel(self.model)
            self.usersCombo.setModelColumn(self.model.fieldIndex("username"))

    def configureDB(self):
        # self.cur.execute("SELECT password FROM users WHERE username = '"+self.username+"'")
        # CONFIG_DATABASE_PATH = "L:/src/"
        # CONFIG_DATABASE_NAME = "smartusers.db"
        DATABASE_NAME = "smartusers.db"
        # filename = os.path.join(CONFIG_DATABASE_PATH,CONFIG_DATABASE_NAME)
        # print filename
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName(DATABASE_NAME)
        db.open()

        # comboView = QSqlQueryModel()
        # comboView.setQuery("SELECT username FROM users",db)
        # self.usersCombo.setModel(comboView)
        # print "Username : "+self.username
        self.conn = sqlite3.connect('smartusers.db')
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS users(username varchar,password varchar,totalEmails varchar,unreadEmails varchar)")
        self.cur.execute("SELECT username,password FROM users")
        self.dbData=self.cur.fetchall()
        if(self.dbData and len(self.dbData)>0):
            # print "Password :- " + self.password
            print "Username is: " + self.dbData[0][0]
            if(self.dbData[0] and len(self.dbData[0])):
                print "password is: " + self.dbData[0][1]
        # self.username = self.dbData[0][0]
        # self.password = self.dbData[0][1]
        db.close()
        '''
        if(len(self.password)<0):
            print "No entry"
        else:
            print "Password : "+self.password
        # if( self.dbData[0][0] == self.username):
        #     self.password = self.dbData[0][1]
        #     print self.password
        '''
    def updateTableData(self):
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
        print "username",statsData
        conn.close()

        header = ['Username', 'Total Emails', 'Unread Emails']
        tm = MyTableModel(statsData, header)
        self.userInfoTableView.setModel(tm)
    def _initViews(self):
        # self.textBoxEmailID.setText(self._scanMan.getUsername())
        #this has to be the convention for naming textBoxes in user interfaces:
        #similarly buttons other than ok, cancel should begin with 'button'
        #similarly combo boxes would be named like 'comboOptions'
        # self.splitter_2.setSizes([312,100])
        # self.userInfoTableView.setMinimumSize(50,20)
        # self.updateTableData()
        self.checkBoxEnableSound.setVisible(False)
        self.loggerTextArea.setStyleSheet("color : #000000;")#Forcing Logger text color to black
        self.connectButton.setText("")
        self.scanButton.setText("")
        self.stopScanButton.setText("")
        self.connectButton.setIcon(QtGui.QIcon(QtGui.QPixmap(':/resources/Connect.png')))
        self.connectButton.setIconSize(QtCore.QSize(140,50))
        # self.scanButton.setIcon(QtGui.QIcon(QtGui.QPixmap(':/resources/Sq.Start.png')))
        # self.scanButton.setStyleSheet("background-image: url(':/resources/New-Start.png'); width:45%;height:55%;	background-repeat: no-repeat;")
        # self.stopScanButton.setIcon(QtGui.QIcon(QtGui.QPixmap(':/resources/Sq.-Pause-n-Switch.png')))
        # self.stopScanButton.setStyleSheet("background-image: url(':/resources/Pause-or-Switch.png'); width:1%;height:1%; background-repeat: no-repeat;")
        # self.scanButton.setIconSize(QtCore.QSize(450,33))
        # self.stopScanButton.setIconSize(QtCore.QSize(160,60))
        # self.scanButton.setEnabled(False)
        # self.stopScanButton.setEnabled(False)
        self.scanButton.setEnabled(True)
        self.stopScanButton.setEnabled(True)
        self.checkBoxEnableSound.setChecked(not self._scanMan._app.enableSoundFlag)
        self.splitter_2.setSizes([320,420])
        # self.textBoxPassword.setText(self._scanMan.getPassword())
        # self.radioPanel = ui_RadioLeftPanel(self._scanMan)
        # QtGui.QWidget.set
        # self.radioPanel
        # self.loggerPanel =ui_LoggerLeftPanel(self._scanMan)
        # self.layout().addWidget(self.radioPanel)
        # self.layout().addWidget(self.loggerPanel)
        self.prepareRadioWidget()

    def prepareRadioWidget(self):
        # self.radioWebView.settings().setAttribute(Qt.QWebSettings.PluginsEnabled, True)
        # self.radioWebView.settings().setAttribute(Qt.QWebSettings.AcceleratedCompositingEnabled, True)
        # self.radioWebView.settings().setAttribute(Qt.QWebSettings.JavascriptEnabled, True)
        Radiostr = '''
        <center>
        <iframe src="http://www.partyviberadio.com/player/embed-auto/reggae.html" style="border:0px #FFFFFF solid; width:95%; height:80%; position:absolute;" name="embed-light" scrolling="no" frameborder="1" marginheight="0px" marginwidth="0px" >
        </iframe>
        </center>
        '''
        # self.radioWebView.load(QUrl.fromLocalFile('embedRadio.html'))
        # self.radioWebView.setHtml(Radiostr)
        # self.radioWebView.loadFinished.connect(self.RadioLoaded)

    def RadioLoaded(self):
        self.loggerTextArea.append('Radio Loaded!')
    #refractoring to conventional, more visible code:
    def _connectSlots(self):
        QtCore.QObject.connect(self.connectButton, QtCore.SIGNAL('clicked()'), self.tryConnect)
        QtCore.QObject.connect(self.scanButton, QtCore.SIGNAL('clicked()'), self.tryStartScan)
        QtCore.QObject.connect(self.stopScanButton, QtCore.SIGNAL('clicked()'), self.tryStopScan)
        QtCore.QObject.connect(self.checkBoxEnableSound, QtCore.SIGNAL('stateChanged(int)'), self.soundEnableToggled)
        # QtCore.QObject.connect(self.checkBoxEnableSound, QtCore.SIGNAL('clicked()'), self.tryStopScan)

    '''
    set sound enable on or off
    '''
    def soundEnableToggled(self, newState):
        self.enableSound(not (newState>0))

    def enableSound(self, enable=True):
        self._scanMan._app.enableSoundFlag = enable
        print "mute audio val",enable
        for popup in self.parent.additionalWidgets:
            popup.webwnd.settings().setAttribute(QtWebKit.QWebSettings.PluginsEnabled, enable)
            popup.webwnd.settings().clearMemoryCaches()
            popup.webwnd.reload()
        # self.webwnd.settings().setAttribute(QtWebKit.QWebSettings.PluginsEnabled, enable)
        # self.webwnd.settings().setAttribute(QtWebKit.QWebSettings.AcceleratedCompositingEnabled, False)
        # self.webwnd.settings().setAttribute(QtWebKit.QWebSettings.JavascriptEnabled, False)
        # self.webwnd.settings().setAttribute(QtWebKit.QWebSettings.WebGLEnabled,False)
        # QtWebKit.QWebSettings.globalSettings().setAttribute(QtWebKit.QWebSettings.PluginsEnabled,enable)

    """
    returns whatever is written in email id text box
    """
    def getUserName(self):
        # return str(self.textBoxEmailID.text())
        return str(self.username)
    """
    returns whatever is written in password text box
    """
    def getPassword(self):
        return str(self.password)


    def tryConnect(self):
        # self._scanMan._app.wnd.cefmodule.Shutdown()

        if(self.usersCombo.currentText() == ""):
            msgbox = QtGui.QMessageBox()
            msgbox.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(':/resources/Icon.png')))
            msgbox.setWindowTitle("Information")
            msgbox.setText('You Have To Add User Before Continue!!!')
            msgbox.setStandardButtons(QtGui.QMessageBox.Ok)
            msgbox.exec_()
            return
        else:
            self.loggerTextArea.append("Connecting...")
            try:
                if self.getUserName()!='' and self.getPassword()!='':
                    self._scanMan.setUsername(self.getUserName())
                    self._scanMan.setPassword(self.getPassword())
                    self._scanMan.connectUser()
            except Exception as ex:
                raise

    def tryStopScan(self):
        self._scanMan._app.wnd.currentStatus = 2
        self.usersCombo.setEnabled(True)
        # self.connectButton.setEnabled(True)
        self.stopScanButton.setEnabled(False)
        self.scanButton.setEnabled(True)
        self.loggerTextArea.append('Stopped')

    def tryStartScan(self):
        try:
            self.emailVal = 0
            self.emailsValue.setText("0")
            self._scanMan.tryStartScan()
            self.userValue.setText(self.getUserName())
            self.usersCombo.setEnabled(False)
            self.stopScanButton.setEnabled(True)
            self.scanButton.setEnabled(False)
            self.loggerTextArea.append('Viewing...')

        except Exception as ex:
            raise ex
