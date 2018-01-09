__author__ = 'Raman Pandey'

from PyQt4.Qt import *
from PyQt4 import Qt,uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import all_resources_rc,ui_about

# aboutbase,aboutform = uic.loadUiType('ui_About.ui')
class About(QDialog,ui_about.Ui_Dialog):
    def __init__(self,scanMan,parent=None):
        super(About,self).__init__(parent)
        self._parent = parent
        self._scanMan = scanMan
        self.setupUi(self)
        
        productName = self._scanMan._app.productName
        productVersion = self._scanMan._app.version
        organisation = self._scanMan._app.organisation

        self.label.setPixmap(QPixmap(":/resources/SplashScreen_medium_pro.png"))
        self.labelProductName.setText(productName)
        self.labelVersion.setText(productVersion)
        self.labelOrganisation.setText(organisation)
        
        self.weblabel.linkActivated.connect(self.openLink)
        self.connect(self.closeButton, SIGNAL('clicked()'), self.closeDialog)
        self.connect(self.licenseButton, SIGNAL('clicked()'), self.showLicense)
        
    def showLicense(self):
        '''
        show the pdf license
        '''
        pass

    def openLink(self):
        '''nothing extra to do as link opening has now been taken care in rich text hyperlink qlabel!!'''
        return
        
    def closeDialog(self):
        self.close()
