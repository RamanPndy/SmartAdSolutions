__author__ = 'Raman Pandey'

import ui_remove_user
from PyQt4.Qt import *
from PyQt4 import Qt,uic,QtCore,QtGui
from PyQt4.QtSql import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sqlite3,os,sys

# removeuserbase,removeuserform = uic.loadUiType('ui_RemoveUser.ui')
class RemoveUser(QDialog,ui_remove_user.Ui_Dialog):
    def __init__(self,scanMan,parent=None):
        super(RemoveUser,self).__init__(parent)
        # self.ui = Ui_Dialog()
        self.setupUi(self)
        self._parent = parent
        self._scanMan = scanMan
        # self.setupUi(self)
        if(os.path.exists("smartusers.db")):
            self.initView()
        QtCore.QObject.connect(self.removeButton,QtCore.SIGNAL("clicked()"),self.getUserRemoveData)
        QtCore.QObject.connect(self.cancelButton,QtCore.SIGNAL("clicked()"),self.cancelDlg)
        QtCore.QObject.connect(self.removeUsersCombo,QtCore.SIGNAL("currentIndexChanged(const QString&)"),self.clearRemoveLabel)

    def cancelDlg(self):
        self.close()

    def clearRemoveLabel(self):
        self.userRemoveStatus.setText("")

    def getUserRemoveData(self):
        self.username= str(self.removeUsersCombo.currentText())
        # print "user tO bE REMOVED : " + self.username
        if(self.username == ""):
            msgbox = QtGui.QMessageBox()
            msgbox.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(':/resources/Icon.png')))
            msgbox.setWindowTitle("Information")
            msgbox.setText('There Is No User To Be Removed!!!')
            msgbox.setStandardButtons(QtGui.QMessageBox.Ok)
            msgbox.exec_()
            return
        else:
            conn = sqlite3.connect('smartusers.db')
            cur = conn.cursor()
            # query = "INSERT into users VALUES('"+str(self.userID.text())+"','"+str(self.userPassword.text())+"')"
            # cur.execute("INSERT into users VALUES('"+str(self.userID.text())+"','"+str(self.userPassword.text())+"')")
            cur.executescript("DELETE FROM users WHERE username = '"+self.username+"' ")
            conn.commit()
            print("Deleted")
            self.initView()
            self.userRemoveStatus.setText("User Removed!")
            # self._parent.displayTableData()
            # self._parent.addUserPanel.dbFetchOp()

    def initView(self):
        DATABASE_NAME = "smartusers.db"
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName(DATABASE_NAME)
        db.open()
        self.model = QSqlTableModel()
        self.model.setTable("users")
        self.model.select()
        self.removeUsersCombo.setModel(self.model)
        self._parent.leftpanelUserInfo.usersCombo.setModel(self.model)
        db.close()











