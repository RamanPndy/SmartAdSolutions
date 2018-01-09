__author__ = 'Raman Pandey'

from PyQt4.Qt import *
from PyQt4 import Qt,uic,QtCore
from PyQt4.QtGui import *
import ui_welcome_dialog
import os.path
from uuid import getnode as get_mac
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
import smtplib,imaplib
from getMacAddr import *
from datetime import datetime, timedelta
import email,time,re


# aboutbase,aboutform = uic.loadUiType('ui_About.ui')
class Welcome(QDialog,ui_welcome_dialog.Ui_Dialog):
    def __init__(self,scanMan,parent=None):
        super(Welcome,self).__init__(parent)
        self._parent = parent
        self._scanMan = scanMan
        self.setupUi(self)
        self.prepareUi()
        self._connectSlots()

    def prepareUi(self):
        '''
        '''
        self.plsWaitmsg.setVisible(False)
        self.welcomeMsg.setVisible(True)
        self.orderidBox.setEnabled(True)
        self.otpBox.setEnabled(True)
        self.NextBtn.setEnabled(True)
        self.NextBtn.setFocusPolicy(QtCore.Qt.TabFocus)
        self.NextBtn.setFocus()

    def _connectSlots(self):
        QtCore.QObject.connect(self.NextBtn,QtCore.SIGNAL("clicked()"),self.checkLicenseFile)

    def checkLicenseFile(self):
        self.orderidval = self.orderidBox.text()
        self.otpVal = self.otpBox.text()
        self.plsWaitmsg.setVisible(True)
        self.welcomeMsg.setVisible(False)
        self.orderidBox.setEnabled(False)
        self.otpBox.setEnabled(False)
        self.NextBtn.setEnabled(False)
        if(self.otpVal == str("12345abcde6789") and self.orderidval == str("hello123")):
            self.mac_addr = getMac().mac_val()
            print self.mac_addr
            recipients = ['raman.pndy@gmail.com']
            emaillist = [elem.strip().split(',') for elem in recipients]
            msg = MIMEMultipart()
            msg['Subject'] = 'Request To generate License File'
            msg['From'] = 'raman.pndy@gmail.com'

            msg.preamble = 'Multipart massage.\n'

            part = MIMEText("OTP : "+str(self.otpVal)+ "\n" + "Mac Address : "+ str(self.mac_addr)+ "\n" + "Order ID : "+ str(self.orderidval))
            msg.attach(part)
            #
            # part = MIMEApplication(open(str('knowmore.db'),"rb").read())
            # part.add_header('Content-Disposition', 'attachment', filename=str('knowmore.db'))
            # msg.attach(part)

            server = smtplib.SMTP("smtp.gmail.com:587")
            server.ehlo()
            server.starttls()
            server.login("raman.pndy@gmail.com", "smart brother")

            server.sendmail(msg['From'], emaillist , msg.as_string())
            print "OTP and Order ID and Mac Address Sent!!!"
            time.sleep(5)
            self.checkVerificationStatus()

        else:
            msgbox = QMessageBox(self)
            msgbox.setWindowTitle("Information")
            msgbox.setText("This is not a valid OTP.Please Enter valid OTP and Order ID provided!!!")
            msgbox.setStandardButtons(QMessageBox.Ok)
            msgbox.exec_()
            self.prepareUi()

    def checkVerificationStatus(self):
        HOST = 'imap.gmail.com'
        USERNAME = 'raman.pndy@gmail.com'
        PASSWORD = 'smart brother'
        ssl = True

        today = datetime.today()
        cutoff = today - timedelta(days=1)

        ## Connect, login and select the INBOX
        server = IMAPClient(HOST, use_uid=True, ssl=ssl)
        server.login(USERNAME, PASSWORD)
        select_info = server.select_folder('INBOX')

        messages = server.search(
            ['FROM "shivam7est@gmail.com"', 'SINCE %s' % cutoff.strftime('%d-%b-%Y')])
        response = server.fetch(messages, ['RFC822'])

        for msgid, data in response.iteritems():
            msg_string = data['RFC822']
            msg = email.message_from_string(msg_string)
            if(msg['Subject'] == "Verified"):
                # server.logout()
                self.generateLicenseFile()
                msgbox = QMessageBox(self)
                msgbox.setWindowTitle("Information")
                msgbox.setText("User Verified!!!")
                msgbox.setStandardButtons(QMessageBox.Ok)
                msgbox.exec_()
                self.close()
                self._parent._validLicense = True

    def generateLicenseFile(self):
        HOST = 'imap.gmail.com'
        PORT = 993
        USERNAME = 'raman.pndy@gmail.com'
        PASSWORD = 'smart brother'

        conn = imaplib.IMAP4_SSL(HOST,PORT)
        test = conn.login(USERNAME,PASSWORD)
        if(test):
            conn.select('Inbox')
            typ, data = conn.search(None, 'SUBJECT', "Verified",'UnSeen')
            for num in data[0].split():
                typm, datam = conn.fetch(num, '(RFC822)')
                #print('Message %s\n%s\n' % (num, datam[0][1]))
                mailBody = datam[0][1]
                mailVal = re.search(r'Email.*', mailBody, re.DOTALL)
                if(mailVal != None):
                    mailValArr = mailVal.group().split("\n")
                    EmailVal = mailValArr[0].replace("\r","").split(":")
                    OrderidVal = mailValArr[1].replace("\r","").split(":")
                    MacidVal = mailValArr[2].replace("\r","").split(":")
                    OtpVal = mailValArr[3].replace("\r","").split(":")
                    varEmail = EmailVal[1]
                    varOrderid = OrderidVal[1]
                    varMacid = MacidVal[1]
                    varOtp = OtpVal[1]
                    bigkey = mailValArr[4].replace("\r","")
                    print varEmail,varOrderid,varMacid,varOtp
                    print "Big Key :" + str(bigkey)
                    with open("license.lic",'w') as licenseFile:
                        licenseFile.write(bigkey)
                        licenseFile.close()
                    msgbox = QMessageBox(self)
                    msgbox.setWindowTitle("Information")
                    msgbox.setText("License File Generated!!!")
                    msgbox.setStandardButtons(QMessageBox.Ok)
                    msgbox.exec_()
                    conn.logout()
                    print "License File is generated!!!"