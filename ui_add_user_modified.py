# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_AddUser_modified.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.setWindowModality(QtCore.Qt.NonModal)
        Dialog.resize(373, 140)
        Dialog.setMaximumSize(QtCore.QSize(16777215, 140))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        Dialog.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/resources/Icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_4.addWidget(self.label_3)
        self.addedUsersCombo = QtGui.QComboBox(Dialog)
        self.addedUsersCombo.setObjectName(_fromUtf8("addedUsersCombo"))
        self.horizontalLayout_4.addWidget(self.addedUsersCombo)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.userID = QtGui.QLineEdit(Dialog)
        self.userID.setObjectName(_fromUtf8("userID"))
        self.horizontalLayout.addWidget(self.userID)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.userPassword = QtGui.QLineEdit(Dialog)
        self.userPassword.setEchoMode(QtGui.QLineEdit.Password)
        self.userPassword.setObjectName(_fromUtf8("userPassword"))
        self.horizontalLayout_2.addWidget(self.userPassword)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.addUserButton = QtGui.QPushButton(Dialog)
        self.addUserButton.setObjectName(_fromUtf8("addUserButton"))
        self.horizontalLayout_3.addWidget(self.addUserButton)
        self.cancelButton = QtGui.QPushButton(Dialog)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.horizontalLayout_3.addWidget(self.cancelButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.ackMsg = QtGui.QLabel(Dialog)
        self.ackMsg.setText(_fromUtf8(""))
        self.ackMsg.setObjectName(_fromUtf8("ackMsg"))
        self.verticalLayout.addWidget(self.ackMsg)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Add User", None))
        self.label_3.setText(_translate("Dialog", "Added Users", None))
        self.addedUsersCombo.setToolTip(_translate("Dialog", "Users", None))
        self.label.setText(_translate("Dialog", "Gmail ID       ", None))
        self.userID.setToolTip(_translate("Dialog", "Enter Your Gmail ID Here", None))
        self.label_2.setText(_translate("Dialog", "Password     ", None))
        self.userPassword.setToolTip(_translate("Dialog", "Enter Your Gmail Password Here", None))
        self.addUserButton.setToolTip(_translate("Dialog", "Click To Add User", None))
        self.addUserButton.setText(_translate("Dialog", "Add User", None))
        self.cancelButton.setToolTip(_translate("Dialog", "Close This Window", None))
        self.cancelButton.setText(_translate("Dialog", "Cancel", None))

import all_resources_rc
