# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_WelcomeDialog.ui'
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
        Dialog.resize(483, 173)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        Dialog.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/resources/Icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.welcomeMsg = QtGui.QLabel(Dialog)
        self.welcomeMsg.setObjectName(_fromUtf8("welcomeMsg"))
        self.verticalLayout.addWidget(self.welcomeMsg)
        self.plsWaitmsg = QtGui.QLabel(Dialog)
        self.plsWaitmsg.setObjectName(_fromUtf8("plsWaitmsg"))
        self.verticalLayout.addWidget(self.plsWaitmsg)
        self.emailidBox = QtGui.QLineEdit(Dialog)
        self.emailidBox.setObjectName(_fromUtf8("emailidBox"))
        self.verticalLayout.addWidget(self.emailidBox)
        self.orderidBox = QtGui.QLineEdit(Dialog)
        self.orderidBox.setObjectName(_fromUtf8("orderidBox"))
        self.verticalLayout.addWidget(self.orderidBox)
        self.otpBox = QtGui.QLineEdit(Dialog)
        self.otpBox.setReadOnly(False)
        self.otpBox.setObjectName(_fromUtf8("otpBox"))
        self.verticalLayout.addWidget(self.otpBox)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.NextBtn = QtGui.QPushButton(Dialog)
        self.NextBtn.setObjectName(_fromUtf8("NextBtn"))
        self.horizontalLayout.addWidget(self.NextBtn)
        self.cloaseBtn = QtGui.QPushButton(Dialog)
        self.cloaseBtn.setObjectName(_fromUtf8("cloaseBtn"))
        self.horizontalLayout.addWidget(self.cloaseBtn)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.cloaseBtn, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.close)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.otpBox, self.NextBtn)
        Dialog.setTabOrder(self.NextBtn, self.cloaseBtn)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Welcome", None))
        self.welcomeMsg.setText(_translate("Dialog", "License File Doesn\'t Exists!\n"
"Please Enter the OTP provided at your Email Address and Click Next To continue.\n"
"Make sure you have an internet connection before proceeding.", None))
        self.plsWaitmsg.setText(_translate("Dialog", "Please wait while we authenticate password and generate license file...", None))
        self.emailidBox.setPlaceholderText(_translate("Dialog", "Enter Email ID Here", None))
        self.orderidBox.setPlaceholderText(_translate("Dialog", "Enter Order ID Here", None))
        self.otpBox.setPlaceholderText(_translate("Dialog", "Enter OTP here", None))
        self.NextBtn.setText(_translate("Dialog", "Next", None))
        self.cloaseBtn.setText(_translate("Dialog", "Close", None))

import all_resources_rc
