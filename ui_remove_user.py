# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_RemoveUser.ui'
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
        Dialog.resize(289, 90)
        Dialog.setMaximumSize(QtCore.QSize(16777215, 90))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        Dialog.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/resources/Icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.formLayout = QtGui.QFormLayout(Dialog)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.formLayout.setLayout(0, QtGui.QFormLayout.LabelRole, self.horizontalLayout)
        self.removeUsersCombo = QtGui.QComboBox(Dialog)
        self.removeUsersCombo.setObjectName(_fromUtf8("removeUsersCombo"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.removeUsersCombo)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.removeButton = QtGui.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.removeButton.setFont(font)
        self.removeButton.setObjectName(_fromUtf8("removeButton"))
        self.horizontalLayout_2.addWidget(self.removeButton)
        self.cancelButton = QtGui.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.cancelButton.setFont(font)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.horizontalLayout_2.addWidget(self.cancelButton)
        self.formLayout.setLayout(1, QtGui.QFormLayout.SpanningRole, self.horizontalLayout_2)
        self.userRemoveStatus = QtGui.QLabel(Dialog)
        self.userRemoveStatus.setText(_fromUtf8(""))
        self.userRemoveStatus.setObjectName(_fromUtf8("userRemoveStatus"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.userRemoveStatus)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Remove User", None))
        self.label.setText(_translate("Dialog", "User", None))
        self.removeUsersCombo.setToolTip(_translate("Dialog", "Added Users", None))
        self.removeButton.setToolTip(_translate("Dialog", "Click To Remove User", None))
        self.removeButton.setText(_translate("Dialog", "Remove", None))
        self.cancelButton.setToolTip(_translate("Dialog", "Click To Close Window", None))
        self.cancelButton.setText(_translate("Dialog", "Cancel", None))

import all_resources_rc
