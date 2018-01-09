__author__ = 'Raman Pandey'

import ui_add_user_modified
from PyQt4.Qt import *
from PyQt4 import Qt,uic,QtCore,QtGui
from PyQt4.QtSql import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sqlite3,os,sys,re

# adduserbase,adduserform = uic.loadUiType('ui_AddUser_modified.ui')
class AddUser(QDialog,ui_add_user_modified.Ui_Dialog):
    def __init__(self,scanMan,parent=None):
        super(AddUser,self).__init__(parent)
        self._parent = parent
        self._scanMan = scanMan
        self.setupUi(self)
        self._initViews()
        self._connectSlots()
        # self.checkDbFileAlreadyExsits()
        # self.dbFetchOp()
        self.entryFilled = False

    def checkDbFileAlreadyExsits(self):
        if (os.path.isfile("smartusers.db")):
            msgbox = QtGui.QMessageBox()
            msgbox.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(':/resources/Icon.png')))
            msgbox.setWindowTitle("Information")
            msgbox.setText('smartusers.db already exists!!! at the location :'+ os.path.abspath('smartusers.db'))
            msgbox.setStandardButtons(QtGui.QMessageBox.Ok)
            msgbox.exec_()
            return

    def _initViews(self):
        pass

    def _connectSlots(self):
        QtCore.QObject.connect(self.addUserButton,QtCore.SIGNAL("clicked()"),self.addUserInDB)
        QtCore.QObject.connect(self.cancelButton,QtCore.SIGNAL("clicked()"),self.cancelEntry)

    def cancelEntry(self):
        self.close()

    def addUserInDB(self):
        if(self.addedUsersCombo.count() > 9):
            msgbox = QtGui.QMessageBox()
            msgbox.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(':/resources/Icon.png')))
            msgbox.setWindowTitle("Information")
            msgbox.setText('Maximum Users Add Limit Reached!!!')
            msgbox.setStandardButtons(QtGui.QMessageBox.Ok)
            msgbox.exec_()
            return
        else:
            if(self.userID.text() == "" or self.userPassword.text() == ""):
                self.reply = QMessageBox.question(self,'Message','You have to fill entries before continue',QMessageBox.Yes)
                if(self.reply):
                    AddUser(self._scanMan)
            else:
                user_email_id= self.userID.text()
                res = re.match("^[a-z0-9](\.?[a-z0-9]){0,}@g(oogle)?mail\.com$",user_email_id,re.I)
                if(res != None):

                    conn = sqlite3.connect('smartusers.db')
                    cur = conn.cursor()
                    # cur.execute("CREATE TABLE IF NOT EXISTS users(username varchar,password varchar,totalEmails varchar,unreadEmails varchar)")
                    # query = "INSERT into users VALUES('"+str(self.userID.text())+"','"+str(self.userPassword.text())+"')"
                    try:
                        cur.execute("SELECT username from users")
                        allUsers = cur.fetchall()
                        for user in allUsers:
                            if user_email_id == user[0]:
                                msgbox = QtGui.QMessageBox()
                                msgbox.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(':/resources/Icon.png')))
                                msgbox.setWindowTitle("Information")
                                msgbox.setText('This Email ID already exists!!!')
                                msgbox.setStandardButtons(QtGui.QMessageBox.Ok)
                                msgbox.exec_()
                                return
                    except Exception as ex:
                        print "There are no users at this time!!!"

                    cur.execute("CREATE TABLE IF NOT EXISTS users(username varchar,password varchar,totalEmails varchar,unreadEmails varchar)")
                    cur.executescript("INSERT into users VALUES('"+str(user_email_id)+"','"+str(self.userPassword.text())+"','n/a','n/a')")
                    print("Inserted")
                    conn.commit()
                    print "Inserted"
                    self.showAddedUsers()
                    # self._scanMan._app.wnd.addUsersCombo()
                    self.updateUsersCombo()
                    # self._parent.displayTableData()
                else:
                    msgbox = QtGui.QMessageBox()
                    msgbox.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(':/resources/Icon.png')))
                    msgbox.setWindowTitle("Information")
                    msgbox.setText('Please Enter Valid Gmail ID!!!')
                    msgbox.setStandardButtons(QtGui.QMessageBox.Ok)
                    msgbox.exec_()
                    return

    def showAddedUsers(self):
        self.dbFetchOp()
        self.ackMsg.setText("User Added!")
        self.userID.setText("")
        self.userPassword.setText("")

    def updateUsersCombo(self):
        DATABASE_NAME = "smartusers.db"
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName(DATABASE_NAME)
        db.open()
        self.model = QSqlTableModel()
        self.model.setTable("users")
        self.model.select()
        self._scanMan._app.wnd.leftpanelUserInfo.usersCombo.setModel(self.model)
        # self._scanMan._app.wnd.removeUserPanel.removeUsersCombo.setModel(self.model)
        db.close()

    def dbFetchOp(self):
        DATABASE_NAME = "smartusers.db"
        # filename = os.path.join(CONFIG_DATABASE_PATH,CONFIG_DATABASE_NAME)
        # print filename
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName(DATABASE_NAME)
        db.open()
        self.model = QSqlTableModel()
        self.model.setTable("users")
        self.model.select()
        self.addedUsersCombo.setModel(self.model)
        self.addedUsersCombo.setModelColumn(self.model.fieldIndex("username"))
        db.close()








