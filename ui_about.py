# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_About.ui'
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
        Dialog.resize(782, 496)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        Dialog.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/resources/Icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setText(_fromUtf8(""))
        self.label.setPixmap(QtGui.QPixmap(_fromUtf8("SplashScreen_medium.png")))
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setMaximumSize(QtCore.QSize(120, 16777215))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_3.addWidget(self.label_4)
        self.labelProductName = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.labelProductName.setFont(font)
        self.labelProductName.setAutoFillBackground(True)
        self.labelProductName.setStyleSheet(_fromUtf8("color: rgb(0, 0, 63);"))
        self.labelProductName.setTextFormat(QtCore.Qt.RichText)
        self.labelProductName.setOpenExternalLinks(True)
        self.labelProductName.setObjectName(_fromUtf8("labelProductName"))
        self.horizontalLayout_3.addWidget(self.labelProductName)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setMaximumSize(QtCore.QSize(120, 16777215))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_4.addWidget(self.label_5)
        self.labelVersion = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setUnderline(False)
        self.labelVersion.setFont(font)
        self.labelVersion.setAutoFillBackground(True)
        self.labelVersion.setStyleSheet(_fromUtf8("color: rgb(0, 0, 63);"))
        self.labelVersion.setTextFormat(QtCore.Qt.RichText)
        self.labelVersion.setOpenExternalLinks(True)
        self.labelVersion.setObjectName(_fromUtf8("labelVersion"))
        self.horizontalLayout_4.addWidget(self.labelVersion)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setMaximumSize(QtCore.QSize(120, 16777215))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_5.addWidget(self.label_6)
        self.labelOrganisation = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setUnderline(False)
        self.labelOrganisation.setFont(font)
        self.labelOrganisation.setAutoFillBackground(True)
        self.labelOrganisation.setStyleSheet(_fromUtf8("color: rgb(0, 0, 63);"))
        self.labelOrganisation.setTextFormat(QtCore.Qt.RichText)
        self.labelOrganisation.setOpenExternalLinks(True)
        self.labelOrganisation.setObjectName(_fromUtf8("labelOrganisation"))
        self.horizontalLayout_5.addWidget(self.labelOrganisation)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.weblabel = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setUnderline(True)
        self.weblabel.setFont(font)
        self.weblabel.setAutoFillBackground(True)
        self.weblabel.setStyleSheet(_fromUtf8("color: rgb(0, 0, 255);"))
        self.weblabel.setTextFormat(QtCore.Qt.RichText)
        self.weblabel.setOpenExternalLinks(True)
        self.weblabel.setObjectName(_fromUtf8("weblabel"))
        self.horizontalLayout_2.addWidget(self.weblabel)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.licenseButton = QtGui.QPushButton(Dialog)
        self.licenseButton.setObjectName(_fromUtf8("licenseButton"))
        self.horizontalLayout.addWidget(self.licenseButton)
        spacerItem = QtGui.QSpacerItem(558, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.closeButton = QtGui.QPushButton(Dialog)
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.horizontalLayout.addWidget(self.closeButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "About", None))
        self.label_4.setText(_translate("Dialog", "Product Name:", None))
        self.labelProductName.setText(_translate("Dialog", "ProductName", None))
        self.label_5.setText(_translate("Dialog", "Version:", None))
        self.labelVersion.setText(_translate("Dialog", "Version", None))
        self.label_6.setText(_translate("Dialog", "Developed By:", None))
        self.labelOrganisation.setText(_translate("Dialog", "Organisation", None))
        self.weblabel.setText(_translate("Dialog", "<a href=\"http://webspot.co.in/\">Click here to check out our website!</a>", None))
        self.licenseButton.setToolTip(_translate("Dialog", "Click To View License", None))
        self.licenseButton.setText(_translate("Dialog", "License", None))
        self.closeButton.setToolTip(_translate("Dialog", "Click To Close", None))
        self.closeButton.setText(_translate("Dialog", "Close", None))

import all_resources_rc
