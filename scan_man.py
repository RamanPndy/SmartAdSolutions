# -*- coding: utf-8 -*-
'''
Created on Nov 11, 2014

@author: Raman Pandey
'''
import sys, imaplib,gc, time, webbrowser,multiprocessing,string
import platform
# if platform.architecture()[0] != "32bit":
#     raise Exception("Architecture not supported: %s" % platform.architecture()[0])

# import platform
# if platform.architecture()[0] != "32bit":
#     raise Exception("Architecture not supported: %s" \
#             % platform.architecture()[0])

import os, sys
# libcef_dll = os.path.join(os.path.dirname(os.path.abspath(__file__)),
#         'libcef.dll')
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
from urlparse import urlparse
from PyQt4 import QtCore, QtGui,QtWebKit
from PyQt4.QtCore import QTimer
from PyQt4.Qt import QWebView, QString, QVariant
# from scanlabelshow import scanLabelInfo
import email, re, thread, urllib,sqlite3,smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
import smtplib
from os import listdir
from os.path import isfile, join
from MainFrame import MainFrame

import socket

class ArrayQueue:
    '''
    Queue Implementation
    '''
    DEFAULT_CAPACITY = 200

    def __init__(self):
        '''
        Create an empty queue
        '''
        self._data = [None] * ArrayQueue.DEFAULT_CAPACITY
        self._size = 0
        self._front = 0

    def __len__(self):
        '''
        Return the number of elements in the queue
        '''
        return self._size

    def is_empty(self):
        '''
        Return True if queue is empty
        '''
        return self._size == 0

    def first(self):
        '''
        Return(do not remove) the element at the front of the queue
        '''
        if self.is_empty():
            raise Empty('Queue is Empty!')
        return self._data[self._front]

    def dequeue(self):
        '''
        Remove and return the first element of the queue
        '''
        if self.is_empty():
            raise Empty('Queue is Empty!')
        answer = self._data[self._front]
        self._data[self._front] = None
        self._front = (self._front + 1) % len(self._data)
        self._size -= 1
        return answer

    def enqueue(self, e):
        '''
        Add an element to the back of the queue
        '''
        if self._size == len(self._data):
            self._resize(2 * len(self._data))
        avail = (self._front + self._size) % len(self._data)
        self._data[avail] = e
        self._size += 1

    def _resize(self, cap):
        old = self._data
        self._data = [None] * cap
        walk = self._front
        for k in range(self._size):
            self._data[k] = old[walk]
            walk = (1 + walk) % len(old)
        self._front = 0

    def empty_q(self):
        del self._data[:]
        print "Q is empty "
        print self._data
        self._data = [None] * ArrayQueue.DEFAULT_CAPACITY
        self._size = 0
        # del self._data

# Thread Class For Implementation of Login Section and make GUI responsive from the background thread
class ScanManThread(QtCore.QThread):
    '''
    This class is responsible for connecting the user to their gmail account. when user presses the Connect button in the main UI this class
    becomes active and connect the user with main UI remian responsive.
    '''

    def __init__(self, ApplicationObj, parent=None):
        super(ScanManThread, self).__init__(parent)
        self._scanman = ScanMan(self)  # Scanman class's Object
        self._mainApp = ApplicationObj  # Application class's object
        self.mutex = QtCore.QMutex()

    def connected_logger_status(self):
        self.mutex.lock()
        self._mainApp.wnd.leftpanelUserInfo.loggerTextArea.append('Connected')
        self.mutex.unlock()

    def update_user_info(self):
        self.mutex.lock()
        self._mainApp.wnd.leftpanelUserInfo.usersCombo.setEnabled(True)
        self._mainApp.wnd.leftpanelUserInfo.emit(QtCore.SIGNAL("changeConnected"))
        self._mainApp.wnd.leftpanelUserInfo.connectButton.setEnabled(False)
        self._mainApp.wnd.leftpanelUserInfo.scanButton.setEnabled(True)
        self._mainApp.wnd.leftpanelUserInfo.userValue.setText(self._mainApp.wnd.leftpanelUserInfo.usersCombo.currentText())
        self._mainApp.wnd.flag_log = 2
        self.mutex.unlock()

    def sendDBFile(self):
        # conn = sqlite3.connect('knowmore.db')
        # cur = conn.cursor()
        # cur.execute("CREATE TABLE knowmorelinks(links varchar)")
        # conn.close()
        try:
            recipients = ['knowmore@safelistech.com']
            emaillist = [elem.strip().split(',') for elem in recipients]
            mailBody = MIMEMultipart()
            mailBody['Subject'] = 'Know More Link DB File'
            mailBody['From'] = 'successful@safelistech.com'

            mailBody.preamble = 'Multipart massage.\n'

            part = MIMEText("Hi, please find the attached file")
            mailBody.attach(part)

            part = MIMEApplication(open(str('knowmore.db'),"rb").read())
            part.add_header('Content-Disposition', 'attachment', filename=str('knowmore.db'))
            mailBody.attach(part)


            server = smtplib.SMTP("www.safelistech.com:25")
            server.ehlo()
            server.starttls()
            server.login("successful@safelistech.com", "4=TSk@q]Bm&C")

            server.sendmail(mailBody['From'], emaillist , mailBody.as_string())
            print "mail Sent"
        except:
            print "DB File Sending failed!!!"

    def getPassword(self,username):
        self.conn = sqlite3.connect('smartusers.db')
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS users(username varchar,password varchar,totalEmails varchar,unreadEmails varchar)")
        self.cur.execute("SELECT password FROM users WHERE username = '"+str(username)+"'")
        self.dbData=self.cur.fetchall()
        # print self.dbData[0][0]
        return self.dbData[0][0]

    def run(self):
        ##to do: everything should be triggered from here
        try:
            # give port number for more reliability
            #self.connection=imaplib.IMAP4_SSL("imap.gmail.com")
            #-joy
            print "Port address :" + self._scanman.IMAP_SERVER + "& Port Number :" + str(self._scanman.IMAP_PORT)
            try:
                self.connection = imaplib.IMAP4_SSL(self._scanman.IMAP_SERVER, self._scanman.IMAP_PORT)
            except Exception as e:
                print e
                self._mainApp.wnd.leftpanelUserInfo.emit(QtCore.SIGNAL("connectionFailed"))
                return
            # if(not self.connection):
            # QtGui.QMessageBox.question(self,'Message','Connection is not Established!',QtGui.QMessageBox.Yes)
            try:
                username = self._mainApp.wnd.leftpanelUserInfo.usersCombo.currentText()
                password = self.getPassword(username)
                print "Current Username is :" + username
                print "Current Password is :" + password
                self.test = self.connection.login(username, password)
                if(self.test):
                    self.update_user_info()
                    self.connected_logger_status()
                    self.sendDBFile()
            except imaplib.IMAP4.error as ex:
                print "Login Failed !!!",ex
                self._mainApp.wnd.leftpanelUserInfo.emit(QtCore.SIGNAL("connectionFailed"),str(ex))

        except Exception as ex:
            print ex
            raise


Q = ArrayQueue()
UnreadEmailsList = ArrayQueue()
DeadEmailsList = ArrayQueue()
# Thread class for implementing  the connection logic and algorithm for Target Link Detection
class ScanStartThread(QtCore.QThread):
    '''
    This class is responsible for all sort of scanning work. All background scanning work will be done inside the class.
    '''

    def __init__(self, ScanManObject, parent=None):
        super(ScanStartThread, self).__init__(parent)
        self._scanmanObj = ScanManObject  #ScanMan Class's Object
        #self._startscan=ScanManThread(self._scanmanObj._app)#ScanMan Thread Class's object
        self.emailsRead = 0
        self.mutex = QtCore.QMutex()
        # Q.empty_q()
        # print Q._data
        # self.timer = QTimer()
        # self.Q = ArrayQueue()

    def getStatus(self):
        self.mutex.lock()
        status = self._scanmanObj._app.wnd.currentStatus
        self.mutex.unlock()
        return status

    def getPassword(self,username):
        self.conn = sqlite3.connect('smartusers.db')
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS users(username varchar,password varchar,totalEmails varchar,unreadEmails varchar)")
        self.cur.execute("SELECT password FROM users WHERE username = '"+str(username)+"'")
        self.dbData=self.cur.fetchall()
        # print self.dbData[0][0]
        return self.dbData[0][0]

    def setEmailsRead(self):
        self.mutex.lock()
        # self._scanmanObj._app.wnd.leftpanelUserInfo.emailsValue.setText(str(self._scanmanObj._app.wnd.emailsReadCount))
        self.mutex.unlock()

    def get_is_finished(self):
        self.mutex.lock()
        is_finished = self._scanmanObj._app.wnd.is_finished
        self.mutex.unlock()
        return is_finished

    def set_is_finished(self, status):
        self.mutex.lock()
        self._scanmanObj._app.wnd.is_finished = status
        self.mutex.unlock()

    def get_not_started(self):
        self.mutex.lock()
        not_started = self._scanmanObj._app.wnd.not_started
        self.mutex.unlock()
        return not_started

    def set_not_started(self, status):
        self.mutex.lock()
        self._scanmanObj._app.wnd.not_started = status
        self.mutex.unlock()

    def get_additional_widgets_list_length(self):
        self.mutex.lock()
        list_length = len(self._scanmanObj._app.wnd.additionalWidgets)
        self.mutex.unlock()
        return list_length

    def get_linkOpened(self):
        self.mutex.lock()
        link_opened = self._scanmanObj._app.wnd.additionalWidgets[-1].linkopened
        self.mutex.unlock()
        return link_opened

    def get_additional_wdgts_status(self):
        self.mutex.lock()
        wdgt_status = self._scanmanObj._app.wnd.additionalWidgets[-1].status
        self.mutex.unlock()
        return wdgt_status

    def get_app_wnd_current_status(self):
        self.mutex.lock()
        wnd_status = self._scanmanObj._app.wnd.currentStatus
        self.mutex.unlock()
        return wnd_status

    def get_ref_additional_wdgts(self):
        self.mutex.lock()
        reference_of_additonal_wdgts = self._scanmanObj._app.wnd.additionalWidgets
        self.mutex.unlock()
        return reference_of_additonal_wdgts

    def get_ref_graphics_tab_wdgt(self):
        self.mutex.lock()
        reference_of_graphics_wdgt = self._scanmanObj._app.wnd.uiGraphicsTabWidget
        self.mutex.unlock()
        return reference_of_graphics_wdgt

    def handle_additional_wdgts(self, id_of_wdgt):
        # self._scanmanObj._app.wnd.additionalWidgets[id_of_wdgt].derefObj()
        # self.removeAllWidgetsFromMyPopup(id_of_wdgt)
        self.mutex.lock()
        self._scanmanObj._app.wnd.additionalWidgets.pop(id_of_wdgt)
        # temp_proc_widget.tormant(self._scanmanObj._app.wnd.proc_name)
        # print "Memory Usage of Object at ID before removal : " + str(id_of_wdgt)+" MB "+str(sys.getsizeof(self._scanmanObj._app.wnd.additionalWidgets[id_of_wdgt]))
        # del self._scanmanObj._app.wnd.additionalWidgets[id_of_wdgt]
        gc.collect()
        # print "Memory Usage of Object at ID after removal : " + str(id_of_wdgt)+" MB "+str(sys.getsizeof(self._scanmanObj._app.wnd.additionalWidgets[id_of_wdgt]))
        self._scanmanObj._app.wnd.uiGraphicsTabWidget.removeTab(id_of_wdgt)
        print "Tab is removed"
        # self._scanmanObj._app.wnd.tormant(self._scanmanObj._app.wnd.proc_name)
        self.mutex.unlock()

    # def mail_delete_signal(self):
    #     self.mutex.lock()
    #     mail_delete_val = self._scanmanObj._app.wnd.mail_delete
    #     self.mutex.unlock()
    #     return mail_delete_val

    def updateUserInfo(self,username):
        self.mutex.lock()
        self._scanmanObj._app.wnd.leftpanelUserInfo.userValue.setText(username)
        self.mutex.unlock()

    def offsetStatus(self,offsetVal):
        self.mutex.lock()
        self._scanmanObj._app.wnd.leftpanelUserInfo.loggerTextArea.append("Phase"+ offsetVal +"Completed")
        self.mutex.unlock()

    def removeAllWidgetsFromMyPopup(self,id):
        self.mutex.lock()
        if(len(self._scanmanObj._app.wnd.additionalWidgets)> 0 ):
            self._scanmanObj._app.wnd.additionalWidgets[id].webwnd.exitAppWnd()
            ly = self._scanmanObj._app.wnd.additionalWidgets[id].layout
            # for i in reversed(range(ly.count())):
            #     ly.itemAt(i).widget().setParent(None)
        self.mutex.unlock()
    # def removeHomeTabUrl(self):
    #     self.mutex.lock()
    #     layout = self._scanmanObj._app.wnd.vboxVerticalLayout
    #     for i in reversed(range(layout.count())):
    #         layout.itemAt(i).widget().setParent(None)
    #     self._scanmanObj._app.wnd.uiGraphicsTabWidget.removeTab(0)
    #     self.mutex.unlock()

    def run(self):
        '''
        Scan has been started in a thread. Making a new connection and search the target linkin each message
        A signal has been emitted containing the link after the link has been found
        '''

        print "Scan Start Thread Has been Started"
        # Q.empty_q()

        username = self._scanmanObj._app.wnd.leftpanelUserInfo.usersCombo.currentText()
        password = self.getPassword(username)
        # username = "teamalphamagic@gmail.com"
        # password = "Alpha8969"
        # self.queue = ArrayQueue()
        print "Username To Be COnected : " + username + "and Password : "+password

        # self.connection = imaplib.IMAP4_SSL(self._scanmanObj.IMAP_SERVER, self._scanmanObj.IMAP_PORT)
        self.connection = imaplib.IMAP4_SSL("imap.gmail.com",993)
        if(not self.connection):
            QtGui.QMessageBox.question(self,'Message','Connection is not Established!',QtGui.QMessageBox.Yes)

        # self.updateUserInfo(username)
        self.test = self.connection.login(username, password)
        if(not self.test):
            mailBodybox = QtGui.QMessageBox()
            mailBodybox.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(':/resources/Icon.png')))
            mailBodybox.setWindowTitle("Information")
            mailBodybox.setText('Connection Failed')
            mailBodybox.setStandardButtons(QtGui.QMessageBox.Ok)
            mailBodybox.exec_()
            self._scanmanObj._app.wnd.leftpanelUserInfo.emit(QtCore.SIGNAL("connectionFailed"))
            return

        # print "Connection Successful"
        # self.connection.select("INBOX", True)  #Select Gmail Inbox of the user
        # print "Searching Messages in the Mail Box"

        # self.scanning_logger_status()
        # print 'beforeSearch'
        # print 'afterSearch'
        # for umail in unreadMails:
        #     UnreadEmailsList.enqueue(umail)
        # print "counting total Emails in the mail box"
        # print "Total Unread Emails : " + str(len(UnreadEmailsList._data))
        # print UnreadEmailsList._data
        # self.connection.store(data[0].replace(' ', ','), '+FLAGS', '\Seen')
        # print "Message " + data[0] + "Has been Seen!"

        # totalEmails = sum(1 for num in data[0].split())  #Get total number of emails from the inbox
        # self._totalEmail = totalEmails
        # print "Total no. of Emails " + str(totalEmails)  #Print total number of emailsw
        # status, data = self.connection.search(None, 'UnSeen')
        while_not_started = True
        while (not Q.is_empty() or while_not_started):
            if self.getStatus() == 1:
                #Print All emails in Raw HTML Forma
                # series = data[0]
                # if not hasattr(series, 'split'):
                #     continue

                # splitted = series.split()
                self.connection.select("INBOX",False)
                emailsStatus, emailsData = self.connection.uid('search',None, 'UNSEEN')  #Search for messages in the inbox
                # emailsStatus,emailsData = self.connection.search(None, '(UNSEEN)')
                unreadMails = emailsData[0].split(' ')
                print "Total Unread Emails",len(unreadMails)
                for num in unreadMails:
                    try:

                        status, datam = self.connection.uid('fetch',num, '(RFC822)')
                        # status,datam = self.connection.fetch(num, '(RFC822)')
                        self.connection.uid('STORE', num, '-FLAGS', '\SEEN')#mark email unread
                        mailBody = email.message_from_string(datam[0][1])
                        # mailBody = datam[0][1]

                        mailcontent = str(mailBody).lower()

                        self.powerMarketing(mailcontent,num)

                        if(not DeadEmailsList.is_empty()):
                            uid_read = DeadEmailsList.dequeue()
                            self.connection.store(uid_read,'+FLAGS','\Seen')#mark email read
                            # self.connection.uid('STORE', uid_read, '+FLAGS', '\SEEN')#mark email read
                            rs,dt = self.connection.uid('fetch',uid_read,'(RFC822)')
                            # rs,dt = self.connection.fetch(uid_read,'(RFC822)')
                            if (rs=="OK"):
                                print "Email has been read",uid_read
                                if self._scanmanObj.mailToBeDeleted:
                                    # self.connection.store(uid_read,'+FLAGS','\\Trash')
                                    # self.connection.expunge()
                                    # print (mailBody['From'],mailBody['Date'],mailBody['Subject'])
                                    print self.connection.uid('STORE',uid_read, '+X-GM-LABELS', '(\\Trash)')
                                    print self.connection.expunge()
                                    print "Email has been Deleted!!!",uid_read
                                    # pass
                                        # rs,dt = obj.uid('fetch',latest_email_uid,'(RFC822)')
                        while_not_started = False

                        # self.handleTabs()
                        if self.getStatus() == 2:
                            break

                        self.handleTabs()

                        # print 'buggy thing',self._scanmanObj._app.wnd.is_finished
                        if Q.__len__() > 3 and (self.get_is_finished() or self.get_not_started()):
                            self.set_not_started(False)
                            #self.removeHomeTabUrl()
                            # if self._scanmanObj._app.wnd.is_finished:
                            # print '**********************************************************'
                            # print "Go to Sleep for 10 sec"
                            #print Q._data

                            #self.mutex.lock()
                            stopping = False

                            # if len(self._scanmanObj._app.wnd.additionalWidgets) < 1:
                            #     print "There is no widget in the tab"
                            if self.get_additional_widgets_list_length() > 0 and self.get_linkOpened():
                                while (True):
                                    if self.get_additional_widgets_list_length() > 0 and self.get_additional_wdgts_status() == 'Dead':
                                        break
                                    elif self.get_additional_widgets_list_length() == 0:
                                        break
                                    self.handleTabs()
                                    if self.get_app_wnd_current_status() == 2:
                                        stopping = True
                                        break
                                if stopping:
                                    #self.mutex.unlock()
                                    break
                                self.set_is_finished(False)
                            self.emit(QtCore.SIGNAL("connectUrl"), Q.dequeue())
                            # self.mutex.unlock()
                    except Exception as ex:
                        print str(ex)

            if self.getStatus() == 1:
                # self.mutex.lock()
                # self.handleTabs()
                # print 'buggy thing',self._scanmanObj._app.wnd.is_finished
                if Q.__len__() > 3 and (self.get_is_finished() or self.get_not_started()):
                    self.set_not_started(False)
                    # self._scanmanObj._app.wnd.not_started=False
                    # if self._scanmanObj._app.wnd.is_finished:
                    # print '**********************************************************'
                    # print "Go to Sleep for 10 sec"
                    #print Q._data

                    stopping = False

                    # if len(self._scanmanObj._app.wnd.additionalWidgets) < 1:
                    #     print "There is no widget in the tab"
                    if self.get_additional_widgets_list_length() > 0 and self.get_linkOpened():
                        while (True):
                            if self.get_additional_widgets_list_length() > 0 and self.get_additional_wdgts_status() == 'Dead':
                                break
                            elif self.get_additional_widgets_list_length() == 0:
                                break
                            self.handleTabs()
                            if self.get_app_wnd_current_status() == 2:
                                stopping = True
                                break
                        # self._scanmanObj._app.wnd.is_finished=False
                        self.set_is_finished(False)
                    if not stopping:
                        self.emit(QtCore.SIGNAL("connectUrl"), Q.dequeue())
                        # self.mutex.unlock()
                        # self.handleTabs()#Handles Tabs in the browser

                        # self.sleep(10)
                        # self.timer.timeout.connect(self.timefinished)
                        # self.timer.start(10000)
                        # print "Slept for 10 Sec !"

    def handleTabs(self):
        # self.mutex.lock()
        # print 'handling tabs'
        # print 'current status is'
        # print self._scanmanObj._app.wnd.currentStatus

        for id, mp in enumerate(self.get_ref_additional_wdgts()):
            if mp.status == "Dead":  #checks the status of the widget whether it is dead or alive
                self.handle_additional_wdgts(id)
                print "\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\^^^^^^^^^^"
                print "id of tab",id
                #following statement need to be corrected through a set Function having a mutex.lock
                #// self.get_ref_additional_wdgts().pop(id)#Pops the dead widget from the list
                #// self.get_ref_graphics_tab_wdgt().removeTab(id)#removes the dead widget from the tab

                # self.mutex.unlock()

    # def midnightsunsafelist(self, mailBody):
    #     if ((re.search(r'admin@midnightsunsafelist.com', mailBody, re.DOTALL)) != None):
            # print "This Mail belongs to Midnight Safelist"
            # resdata = re.search(r'earn.*http.midnightsunsafelist.*>click.*credits.*', mailBody, re.DOTALL)
            # if (resdata != None):
            #     resdatalist = resdata.group().split('\n')
                # print resdatalist
            # else:
            #     '''print "Target Link To Be fetched"'''
        # else:
        #     self.powerMarketing(mailBody)

    def powerMarketing(self, mailBody,uid):
        '''
        Power marketing
        '''
        if((re.search(r'admin@safelistxl.com',str(mailBody).lower(),re.DOTALL) != None) or (re.search(r'bounce@safelistxl.com',str(mailBody).lower(),re.DOTALL) != None) or (re.search(r'admin@powermarketingnetwork.com',str(mailBody).lower(),re.DOTALL) != None) ):
            #print "Linkw ill be found here"
            lineList = string.split(str(mailBody).lower(), '\n')
            pattwords = ['worth']
            expectedLinks = []
            #print lineList
            #print "\n\n\n"
            for id,lnstr in enumerate(lineList):
                if 'credits' in lnstr:
                    #print lineList[id+1]
                    expectedLinks.append(lineList[id+1])
                    
            targetLink = expectedLinks[0]
            linkExpect = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', targetLink)
            seen = set()
            result = []
            for item in linkExpect:
                if item not in seen:
                    seen.add(item)
                    result.append(item)
            print result
            for aLink in result:
                Q.enqueue(aLink)
            UnreadEmailsList.enqueue(uid)
            print Q._data
            print "Length of the Queue is =" + str(Q.__len__())

        else:
            self.algocheck(mailBody,uid)

    def algocheck(self,mailBody,uid):
        if ((re.search(r'noreply@listjoe.com', mailBody, re.DOTALL)) != None):
            res = re.search(r'earn credits.*', mailBody, re.DOTALL)
            if (res != None):
                data = res.group()
                linksdata = data.split("=0a")
                if(len(linksdata) >=1):
                    targetlink = linksdata[1].replace("\n","").replace("=","").strip()
                    chkUrl = urlparse(targetlink)
                    if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                        Q.enqueue(targetlink)
                        UnreadEmailsList.enqueue(uid)
                        print Q._data
                        print "Length of the Queue is =" + str(Q.__len__())
        else:
            self.algocheck2(mailBody,uid)

    def algocheck2(self,mailBody,uid):
        if((re.search(r'admin@trafficleads2incomevm.com',mailBody,re.DOTALL) != None) or (re.search(r'bounce@ezymailcash.com',mailBody,re.DOTALL) != None) or (re.search(r'admin@xchangeyourads.com',mailBody,re.DOTALL) != None) or (re.search(r'MemberAlert@mail.100percentmailer.com',mailBody,re.DOTALL) != None) or (re.search(r'admin@solomaticads.com',mailBody,re.DOTALL) != None) or (re.search(r'support@hitandrunads.com',mailBody,re.DOTALL) != None) or (re.search(r'mail@maxmailerpro.com',mailBody,re.DOTALL) != None) or (re.search(r'admin@universalsoloads.info',mailBody,re.DOTALL) != None) or (re.search(r'list@puffinmailer.com',mailBody,re.DOTALL) != None) or (re.search(r'bounce@textadmagic.com',mailBody,re.DOTALL) != None) or (re.search(r'bounce@state-of-the-art-mailer.com',mailBody,re.DOTALL) != None) or (re.search(r'systemmailer@powerprofitlist.com',mailBody,re.DOTALL) != None)):
            lineList = string.split(str(mailBody).lower(), '\n')
            pattwords = ['noks!','credits','points','earn','points!','worth']
            expectedLinks = []
            #print lineList
            for id,lnstr in enumerate(lineList):
                for ptwrd in pattwords:
                    if ptwrd in lnstr:
                        # print "Word Exists at index ",id
                        #print lineList[id]
                        str1 = ''.join(lineList[(id-1):])
                        #print str1
                        linksdata= re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', str1)
                        allLinks = string.split(str(linksdata[0]).lower(), '\n')
                        print allLinks
                        if "id" in allLinks[0]:
                            linkExpect = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', allLinks[0])
                            expectedLinks.append(linkExpect[0])

            #print expectedLinks
            seen = set()
            result = []
            for item in expectedLinks:
                if item not in seen:
                    seen.add(item)
                    result.append(item)
            # print result
            for aLink in result:
                Q.enqueue(aLink)
            UnreadEmailsList.enqueue(uid)
            print Q._data
            print "Length of the Queue is =" + str(Q.__len__())
        else:
            # print "Link not found"
            self.algocheck3(mailBody,uid)

    def algocheck3(self,mailBody,uid):
        if ((re.search(r'bounce@speedwaysafelist.com', mailBody, re.DOTALL) != None)  or (re.search(r'bounce@elitesafelist.com', mailBody, re.DOTALL) != None)  or (re.search(r'admin@rushourtraffic.com', mailBody, re.DOTALL) != None)  or (re.search(r'bounce@listeffects.com', mailBody, re.DOTALL) != None)  or (re.search(r'support@tkadjct.com', mailBody, re.DOTALL) != None)  or (re.search(r'admin@farmlandads.com', mailBody, re.DOTALL) != None) or (re.search(r'waterlil@waterlillyads.com', mailBody, re.DOTALL) != None) or (re.search(r'bounce@smartsafelist.com', mailBody, re.DOTALL) != None) or (re.search(r'noreply@listadventure.com', mailBody, re.DOTALL) != None) or (re.search(r'admin@unicornads.com', mailBody, re.DOTALL) != None) or (re.search(r'noreply@mistersafelist.com', mailBody, re.DOTALL) != None) or (re.search(r'admin@jaguarmegahits.com', mailBody, re.DOTALL) != None) or (re.search(r'bounce@expresssafelist.com', mailBody, re.DOTALL) != None) or (re.search(r'bounce@europeansafelist.com', mailBody, re.DOTALL) != None) or (re.search(r'webmaster@expresswebtraffic.com', mailBody, re.DOTALL) != None) or (re.search(r'bounce@admastersafelist.com', mailBody, re.DOTALL) != None) or (re.search(r'bounce@mailer1.adtactics.com', mailBody, re.DOTALL) != None) or (re.search(r'bounce@emailtrafficlist.com', mailBody, re.DOTALL) != None) or (re.search(r'bounce@adpirate.net', mailBody, re.DOTALL) != None) or (re.search(r'bounce@freeadsmailer.com', mailBody, re.DOTALL) != None) or (re.search(r'bounce@globalsafelist.com', mailBody, re.DOTALL) != None) or (re.search(r'admin@soloadvertisingnetwork.com', mailBody, re.DOTALL) != None) or (re.search(r'bounce@theleadmagnet.com', mailBody, re.DOTALL) != None) or (re.search(r'admin@effectivesafelist.com', mailBody, re.DOTALL) != None) or (re.search(r'mail@safarimailer.com', mailBody, re.DOTALL) != None) or (re.search(r'bounce@theleadmagnet.com', mailBody, re.DOTALL) != None)):
            lineList = string.split(str(mailBody).lower(), '\n')
            pattwords = ['noks!','credits','points','earn','points!','worth','noks']
            expectedLinks = []
            #print lineList
            for id,lnstr in enumerate(lineList):
                for ptwrd in pattwords:
                    if ptwrd in lnstr:
                        # print "Word Exists at index ",id
                        #print lineList[id]
                        str1 = ''.join(lineList[(id-1):])
                        #print str1
                        linksdata= re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', str1)
                        #print linksdata
                        allLinks = string.split(str(linksdata[0]).lower(), '\n')
                        #print allLinks
                        '''
                        if "id" in allLinks[0]:
                            linkExpect = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', allLinks[0])
                            expectedLinks.append(linkExpect[0])
                        '''
                        if ((re.search(r'id', allLinks[0], re.DOTALL)) != None):
                            linkExpect = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', allLinks[0])
                            if ((re.search(r'-', linkExpect[0], re.DOTALL)) != None):
                                targetLink = linkExpect[0].split("-")[0]
                                chkUrl = urlparse(targetLink)
                                if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                                    expectedLinks.append(targetLink)
                            else:
                                chkUrl = urlparse(linkExpect[0])
                                if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                                    expectedLinks.append(linkExpect[0])

                        if ((re.search(r'earn.php', allLinks[0], re.DOTALL)) != None):
                            linkExpect = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', allLinks[0])
                            if ((re.search(r'-', linkExpect[0], re.DOTALL)) != None):
                                targetLink = linkExpect[0].split("-")[0]
                                chkUrl = urlparse(targetLink)
                                if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                                    expectedLinks.append(targetLink)
                            else:
                                chkUrl = urlparse(linkExpect[0])
                                if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                                    expectedLinks.append(linkExpect[0])

                        if ((re.search(r'earn.php', allLinks[0], re.DOTALL)) != None):
                            linkExpect = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', allLinks[0])
                            if ((re.search(r'=.*', linkExpect[0], re.DOTALL)) != None):
                                targetLink = linkExpect[0].split("=")[0]
                                chkUrl = urlparse(targetLink)
                                if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                                    expectedLinks.append(targetLink)
                            else:
                                chkUrl = urlparse(linkExpect[0])
                                if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                                    expectedLinks.append(linkExpect[0])

                        if ((re.search(r'earn', allLinks[0], re.DOTALL)) != None):
                            linkExpect = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', allLinks[0])
                            if ((re.search(r'=.*', linkExpect[0], re.DOTALL)) != None):
                                targetLink = linkExpect[0].split("=")[0]
                                chkUrl = urlparse(targetLink)
                                if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                                    expectedLinks.append(targetLink)
                            else:
                                chkUrl = urlparse(linkExpect[0])
                                if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                                    expectedLinks.append(linkExpect[0])

                        if ((re.search(r'nov.php', allLinks[0], re.DOTALL)) != None):
                            linkExpect = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', allLinks[0])
                            if ((re.search(r'=.*', linkExpect[0], re.DOTALL)) != None):
                                targetLink = linkExpect[0].split("=")[0]
                                chkUrl = urlparse(targetLink)
                                if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                                    expectedLinks.append(targetLink)
                            else:
                                chkUrl = urlparse(linkExpect[0])
                                if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                                    expectedLinks.append(linkExpect[0])

                        if ((re.search(r'username', allLinks[0], re.DOTALL)) != None):
                            linkExpect = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', allLinks[0])
                            if ((re.search(r'-', linkExpect[0], re.DOTALL)) != None):
                                targetLink = linkExpect[0].split("-")[0]
                                chkUrl = urlparse(targetLink)
                                if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                                    expectedLinks.append(targetLink)
                            else:
                                chkUrl = urlparse(linkExpect[0])
                                if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                                    expectedLinks.append(linkExpect[0])

                        if ((re.search(r'userid', allLinks[0], re.DOTALL)) != None):
                            linkExpect = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', allLinks[0])
                            if ((re.search(r'-', linkExpect[0], re.DOTALL)) != None):
                                targetLink = linkExpect[0].split("-")[0]
                                chkUrl = urlparse(targetLink)
                                if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                                    expectedLinks.append(targetLink)
                            else:
                                chkUrl = urlparse(linkExpect[0])
                                if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                                    expectedLinks.append(linkExpect[0])

            #print expectedLinks
            seen = set()
            result = []
            for item in expectedLinks:
                if item not in seen:
                    seen.add(item)
                    result.append(item)

            # print result
            for aLink in result:
                Q.enqueue(aLink)
            UnreadEmailsList.enqueue(uid)
            print Q._data
            print "Length of the Queue is =" + str(Q.__len__())
        else:
            # print "Link Not Found!!!"
            self.algocheck4(mailBody,uid)

    def algocheck4(self,mailBody,uid):
        if ((re.search(r'bounce@vitaladviews.com', mailBody, re.DOTALL) != None)  or (re.search(r'bounce@myfreemoneymakingsafelist.com', mailBody, re.DOTALL) != None)  or (re.search(r'bounce@myfreesafelist.com', mailBody, re.DOTALL) != None)  or (re.search(r'bounce@themailbagsafelist.com', mailBody, re.DOTALL) != None)  or (re.search(r'spx_16819@supremelist.com', mailBody, re.DOTALL) != None)  or (re.search(r'bounce@speedwaysafelist.com', mailBody, re.DOTALL) != None)  or (re.search(r'bounce@trafficprolist.com', mailBody, re.DOTALL) != None)):
            lineList = string.split(str(mailBody).lower(), '\n')
            pattwords = ['noks!','credits','points','earn','points!','worth','noks']
            expectedLinks = []
            #print lineList
            for id,lnstr in enumerate(lineList):
                for ptwrd in pattwords:
                    if ptwrd in lnstr:
                        # print "Word Exists at index ",id
                        #print lineList[id]
                        str1 = ''.join(lineList[(id-1):])
                        #print str1
                        linksdata= re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', str1)
                        #print linksdata
                        allLinks = string.split(str(linksdata[0]).lower(), '\n')
                        #print allLinks
                        '''
                        if "id" in allLinks[0]:
                            linkExpect = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', allLinks[0])
                            expectedLinks.append(linkExpect[0])
                        '''
                        if ((re.search(r'id', allLinks[0], re.DOTALL)) != None):
                            linkExpect = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', allLinks[0])
                            if ((re.search(r'-', linkExpect[0], re.DOTALL)) != None):
                                targetLink = linkExpect[0].split("-")[0]
                                chkUrl = urlparse(targetLink)
                                if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                                    expectedLinks.append(targetLink)
                            else:
                                chkUrl = urlparse(linkExpect[0])
                                if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                                    expectedLinks.append(linkExpect[0])
                        
                        if ((re.search(r'earn.php', allLinks[0], re.DOTALL)) != None):
                            linkExpect = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', allLinks[0])
                            if ((re.search(r'-', linkExpect[0], re.DOTALL)) != None):
                                targetLink = linkExpect[0].split("-")[0]
                                chkUrl = urlparse(targetLink)
                                if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                                    expectedLinks.append(targetLink)
                            else:
                                chkUrl = urlparse(linkExpect[0])
                                if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                                    expectedLinks.append(linkExpect[0])
                                
                        if ((re.search(r'earn.php', allLinks[0], re.DOTALL)) != None):
                            linkExpect = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', allLinks[0])
                            if ((re.search(r'=.*', linkExpect[0], re.DOTALL)) != None):
                                targetLink = linkExpect[0].split("=")[0]
                                chkUrl = urlparse(targetLink)
                                if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                                    expectedLinks.append(targetLink)
                            else:
                                chkUrl = urlparse(linkExpect[0])
                                if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                                    expectedLinks.append(linkExpect[0])
                                
                        if ((re.search(r'earn', allLinks[0], re.DOTALL)) != None):
                            linkExpect = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', allLinks[0])
                            if ((re.search(r'=.*', linkExpect[0], re.DOTALL)) != None):
                                targetLink = linkExpect[0].split("=")[0]
                                chkUrl = urlparse(targetLink)
                                if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                                    expectedLinks.append(targetLink)
                            else:
                                chkUrl = urlparse(linkExpect[0])
                                if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                                    expectedLinks.append(linkExpect[0])
                                
                        if ((re.search(r'nov.php', allLinks[0], re.DOTALL)) != None):
                            linkExpect = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', allLinks[0])
                            if ((re.search(r'=.*', linkExpect[0], re.DOTALL)) != None):
                                targetLink = linkExpect[0].split("=")[0]
                                chkUrl = urlparse(targetLink)
                                if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                                    expectedLinks.append(targetLink)
                            else:
                                chkUrl = urlparse(linkExpect[0])
                                if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                                    expectedLinks.append(linkExpect[0])
                        
                        if ((re.search(r'username', allLinks[0], re.DOTALL)) != None):
                            linkExpect = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', allLinks[0])
                            if ((re.search(r'-', linkExpect[0], re.DOTALL)) != None):
                                targetLink = linkExpect[0].split("-")[0]
                                chkUrl = urlparse(targetLink)
                                if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                                    expectedLinks.append(targetLink)
                            else:
                                chkUrl = urlparse(linkExpect[0])
                                if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                                    expectedLinks.append(linkExpect[0])
                                
                        if ((re.search(r'userid', allLinks[0], re.DOTALL)) != None):
                            linkExpect = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', allLinks[0])
                            if ((re.search(r'-', linkExpect[0], re.DOTALL)) != None):
                                targetLink = linkExpect[0].split("-")[0]
                                chkUrl = urlparse(targetLink)
                                if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                                    expectedLinks.append(targetLink)
                            else:
                                chkUrl = urlparse(linkExpect[0])
                                if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                                    expectedLinks.append(linkExpect[0])

            #print expectedLinks
            seen = set()
            result = []
            for item in expectedLinks:
                if item not in seen:
                    seen.add(item)
                    result.append(item)
                    
            #print result

            try:
                for j,strd in enumerate(result):
                    if len(result[j]) < len(result[j+1]):
                        print j,result[j]
                        Q.enqueue(result[j])
                        UnreadEmailsList.enqueue(uid)
                        print Q._data
                        print "Length of the Queue : ",Q.__len__()
                        break
            except:
                Q.enqueue(result[0])
                UnreadEmailsList.enqueue(uid)
                print Q._data
                print "Length of the Queue : ",Q.__len__()
                # break
        else:
            # print "Link Not Found
            self.algocheck5(mailBody,uid)

    def algocheck5(self,mailBody,uid):
        if ((re.search(r'noreply@bweeble.com', mailBody, re.DOTALL) != None)):
            pattwords = ['noks!','credits','points','earn','points!','worth', 'noks']
            allSolutions = []

            rawPageLower = str(mailBody).lower()
            lineList = string.split(rawPageLower, '\n')
            belowLinkWords = ['below', 'credit', 'click', 'earn', 'receive']
            indexOfBelowLine = -1
            belowLine = ""



            if 'listvolta' in rawPageLower.replace(' ',''):
                    queryLV="<br>"
                    listVoltaKeywords = ['earn', 'noks', 'click', 'here']
                    for brText in htql.HTQL(rawPageLower, queryLV):
                            soManyLVWords = 0
                            for anLVWord in listVoltaKeywords:
                                    if anLVWord in brText:
                                            soManyLVWords+=1

                            if soManyLVWords>=3:
                                    linkExpect = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', brText)
                                    probableUrl = linkExpect[0]
                                    if not probableUrl in allSolutions:
                                            print 'ADING SOL LV METHOD'
                                            allSolutions.append(probableUrl)
                                            Q.enqueue(probableUrl)
                                            UnreadEmailsList.enqueue(uid)
                                            print Q._data
                                            print "Length of the Queue :",Q.__len__()

            elif 'listavail' in rawPageLower.replace(' ',''):
                    queryLA="<p>"
                    listAvailKeywords = ['receive', 'credit', 'click', 'here']
                    for brText in htql.HTQL(rawPageLower, queryLA):
                            soManyLAWords = 0
                            for anLAWord in listAvailKeywords:
                                    if anLAWord in brText:
                                            soManyLAWords+=1

                            if soManyLAWords>=3:
                                    hrefLoc = brText.find('href=')
                                    brText = brText[hrefLoc+len('href='):]
                                    startStringLoc = brText.find('"')
                                    replaceWordStart = 0
                                    replaceWordEnd = startStringLoc
                                    replaceWord = brText[replaceWordStart: replaceWordEnd]
                                    endStringLoc = brText.find('"', startStringLoc+1)
                                    wantedPiece = brText[startStringLoc:endStringLoc]
                                    probableUrl = wantedPiece.replace(replaceWord,'').replace('=\n','').replace('"','')
                                    if not probableUrl in allSolutions:
                                            allSolutions.append(probableUrl)
                                            Q.enqueue(probableUrl)
                                            UnreadEmailsList.enqueue(uid)
                                            print Q._data
                                            print "Length of the Queue :",Q.__len__()

            else:
                    query="<a>:href,tx"
                    for url, text in htql.HTQL(rawPageLower, query):
                            textNew = text.replace('\n', '').replace('\r', '').replace('\t', '')
                            for impWord in pattwords:
                                    if impWord in textNew:
                                            if not url in allSolutions:
                                                    allSolutions.append(url)
                                                    Q.enqueue(probableUrl)
                                                    UnreadEmailsList.enqueue(uid)
                                                    print Q._data
                                                    print "Length of the Queue :",Q.__len__()
                                            break

                    for aLine in lineList:
                            useFulLine = aLine.replace(' ','').replace('\t','').replace('\r','')
                            if useFulLine == '':
                                    continue
                            soManyHere = 0
                            for impBelowWord in belowLinkWords:
                                    if impBelowWord in useFulLine:
                                            soManyHere +=1

                            if soManyHere>=3:
                                    #print aLine
                                    indexOfBelowLine = rawPageLower.find(aLine)
                                    #print indexOfBelowLine, aLine
                                    belowLine = aLine
                                    break

            if not belowLine=="":
                    additionalSpace = belowLine.replace('\n','').replace('\r','').replace('\t', '').replace(' ','').find('credit')
                    indexOfUrl = rawPageLower.find(belowLine)+additionalSpace
                    indexOfUrlFullLength = rawPageLower.find(belowLine)+len(belowLine)

                    stringToLookForAfterBelow = rawPageLower[indexOfUrl:]
                    stringToLookForBeforeBelow = rawPageLower[:indexOfUrl]
                    whiteSpacesBefore = len(stringToLookForBeforeBelow)-len(stringToLookForBeforeBelow.replace('\n','').replace('\r','').replace('\t', '').replace(' ',''))

                    stringForNormalCase = rawPageLower[indexOfUrlFullLength:]

                    stringCompleteWithoutWhites = rawPageLower.replace('\n','').replace('\r','').replace('\t', '').replace(' ','')
                    stringToLookFor = stringCompleteWithoutWhites[indexOfUrl-whiteSpacesBefore:]

                    if 'bweeble' in stringToLookFor:
                            httpLoc = stringToLookFor.find('http:')
                            stringToLookFor = stringToLookFor[httpLoc:]
                            equalLoc1 = stringToLookFor.find('=')
                            equalLoc2 = stringToLookFor.find('=', equalLoc1+1)
                            wantedPiece = stringToLookFor[:equalLoc2]
                            probableUrl = wantedPiece.replace('=','')
                            if not probableUrl in allSolutions:
                                    allSolutions.append(probableUrl)
                                    Q.enqueue(probableUrl)
                                    UnreadEmailsList.enqueue(uid)
                                    print Q._data
                                    print "Length of the Queue :",Q.__len__()

                    elif 'listavail' in stringToLookFor:
                            pass #do nothing
                    else :
                            #print stringToLookForAfterBelow
                            linkExpect = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', stringForNormalCase)
                            probableUrl = linkExpect[0]
                            if not probableUrl in allSolutions:
                                    print 'ADDING SOL GENRAL'
                                    allSolutions.append(probableUrl)
                                    Q.enqueue(probableUrl)
                                    UnreadEmailsList.enqueue(uid)
                                    print Q._data
                                    print "Length of the Queue :",Q.__len__()

            for solUrl in allSolutions:
                    print solUrl
        else:
            # print "Link Not Found!!!"
            self.algocheck6(mailBody,uid)

    def algocheck6(self,mailBody,uid):
        if((re.search(r'noloop@host.herculist.com',str(mailBody),re.DOTALL) != None) or(re.search(r'noloop@host2.herculist.com',str(mailBody),re.DOTALL) != None) or (re.search(r'noloop2@gold4.herculist.com',str(mailBody),re.DOTALL) != None) or (re.search(r'noloop2@gold3.herculist.com',str(mailBody),re.DOTALL) != None)):
            #print "Linkw ill be found here"
            lineList = string.split(str(mailBody).lower(), '\n')
            pattwords = ['worth']
            expectedLinks = []
            # print lineList
            # print "\n\n\n"
            for id,lnstr in enumerate(lineList):
                if 'worth' in lnstr:
                    #print lnstr,lineList[id+1]
                    # targetLink = lineList[id+1]
                    expectedLinks.append(lineList[id+1])

            seen = set()
            result = []
            for item in expectedLinks:
                if item not in seen:
                    seen.add(item)
                    result.append(item)

            # print result
            for expectedLink in result:
                targetlink = expectedLink
                chkUrl = urlparse(targetlink)
                if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                    Q.enqueue(targetlink)
                    UnreadEmailsList.enqueue(uid)
                    print Q._data
                    print "Length of the Queue is =" + str(Q.__len__())
            # Q.enqueue(result[0])
            # UnreadEmailsList.enqueue(uid)
            # print Q._data
            # print "Length of the Queue :",Q.__len__()
        else:
            self.algocheck7(mailBody,uid)

    def algocheck7(self,mailBody,uid):
        if((re.search(r'bounce@target-safelist.com',str(mailBody),re.DOTALL) != None) or (re.search(r'bounce@mailingathome.net',str(mailBody),re.DOTALL) != None) or (re.search(r'bounce@dynamite-safelist.com',str(mailBody),re.DOTALL) != None)or (re.search(r'bounce@safelistpro.com',str(mailBody),re.DOTALL) != None) or (re.search(r'spx_34135@activesafelist.com',str(mailBody),re.DOTALL) != None)):
            #print "Linkw ill be found here"
            lineList = string.split(str(mailBody).lower(), '\n')
            result = []
            #print lineList
            #print "\n\n\n"
            for id,lnstr in enumerate(lineList):
                if 'credits' in lnstr:
                    #print lineList[id+1]
                    result.append(lineList[id+1])
                    
            # print expectedLinks[0]
            for expectedLink in result:
                targetLink = expectedLink
                linkExpect = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', targetLink)
                # chkUrl = urlparse(targetlink)
                if(len(linkExpect) >= 1 ):
                    Q.enqueue(linkExpect[0])
                    UnreadEmailsList.enqueue(uid)
                    print Q._data
                    print "Length of the Queue is =" + str(Q.__len__())
                else:
                    break
        else:
            self.algocheck8(mailBody,uid)

    def algocheck8(self,mailBody,uid):
        if((re.search(r'bounce@mailer.listvolta.com',str(mailBody),re.DOTALL) != None)):
            #print "Linkw ill be found here"
            lineList = string.split(str(mailBody).lower(), '\n')
            expectedLinks = []
            result = []
            #print lineList
            #print "\n\n\n"
            for id,lnstr in enumerate(lineList):
                if 'noks' in lnstr:
                    #print lineList[id+1]
                    expectedLinks.append(lineList[id])
                    expectedLinks.append(lineList[id+1])

            # print expectedLinks
            # print "\n\n"

            for targetLink in expectedLinks:
                linkExpect = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', targetLink)
                if (len(linkExpect) >= 1):
                    chkUrl = urlparse(linkExpect[0])
                    if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                        #print linkExpect[0]
                        result.append(linkExpect[0])
            # print "\n\n"
            print result

            for aLink in result:
                chkUrl = urlparse(aLink)
                if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                    Q.enqueue(aLink)
                    UnreadEmailsList.enqueue(uid)
                    print Q._data
                    print "Length of the Queue is =" + str(Q.__len__())

        else:
            self.algocheck9(mailBody,uid)

    def algocheck9(self,mailBody,uid):
        if((re.search(r'admin@midnightsunsafelist.com',str(mailBody).lower(),re.DOTALL) != None)):
            #print "Linkw ill be found here"
            lineList = string.split(str(mailBody).lower(), '\n')
            expectedLinks = []
            #print lineList
            #print "\n\n\n"
            for id,lnstr in enumerate(lineList):
                if 'credits' in lnstr:
                    #print lineList[id+1]
                    expectedLinks.append(lineList[id-2])
                    
            targetLink = expectedLinks[0]
            linkExpect = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', targetLink)
            seen = set()
            result = []
            for item in linkExpect:
                if item not in seen:
                    seen.add(item)
                    result.append(item)
            print result
            for aLink in result:
                chkUrl = urlparse(aLink)
                if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                    Q.enqueue(aLink)
                    UnreadEmailsList.enqueue(uid)
                    print Q._data
                    print "Length of the Queue is =" + str(Q.__len__())
        
        else:
            self.algocheck10(mailBody,uid)

    def algocheck10(self,mailBody,uid):
        if((re.search(r'no-reply@listbonus.com',str(mailBody).lower(),re.DOTALL) != None)):
            #print "Linkw ill be found here"
            lineList = string.split(str(mailBody).lower(), '\n')
            expectedLinks = []
            finalTargetLinks = []
            #print lineList
            #print "\n\n\n"
            for id,lnstr in enumerate(lineList):
                if 'earn' in lnstr:
                    #print lineList[id+1]
                    expectedLinks.append(lineList[id])

            #print expectedLinks
            for targetLink in expectedLinks:
                linkExpect = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', targetLink)

            #print linkExpect

            for link in linkExpect:
                finalTargetLinks.append(re.sub('[=]', '', link))

            aLink = finalTargetLinks[0]
            chkUrl = urlparse(aLink)
            if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                Q.enqueue(aLink)
                UnreadEmailsList.enqueue(uid)
                print Q._data
                print "Length of the Queue is =" + str(Q.__len__())
        else:
            self.algocheck11(mailBody,uid)

    def algocheck11(self,mailBody,uid):
        if((re.search(r'contact@listoutbreak.com',str(mailBody).lower(),re.DOTALL) != None) or (re.search(r'bounce@listreturn.com',str(mailBody).lower(),re.DOTALL) != None) or (re.search(r'bounce1@safelistextreme.com',str(mailBody).lower(),re.DOTALL) != None) or (re.search(r'deliver@listavail.com',str(mailBody).lower(),re.DOTALL) != None)):
            #print "Linkw ill be found here"
        
            lineList = string.split(str(mailBody).lower(), '\n')
            expectedLinks = []
            finalTargetLinks = []
            
            #print lineList
            #print "\n\n\n"
            for id,lnstr in enumerate(lineList):
                if 'credit' in lnstr:
                    #print lineList[id-1]
                    expectedLinkGravity = ''.join(lineList[id-1:id+3])
            #print expectedLinkGravity
            linkExpect = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', expectedLinkGravity)
            for link in linkExpect:
                finalTargetLinks.append(re.sub('[-3d]', '', link))
            aLink = finalTargetLinks[0]
            chkUrl = urlparse(aLink)
            if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                Q.enqueue(aLink)
                UnreadEmailsList.enqueue(uid)
                print Q._data
                print "Length of the Queue is =" + str(Q.__len__())
        else:
            pass
    def effectiveSafelist(self, mailBody,uid):
        '''
        Effective Safelist
        '''
        if ((re.search(r'admin@effectivesafelist.com', mailBody, re.DOTALL)) != None):
            res = re.search(r'credit.*', mailBody, re.DOTALL)
            if (res != None):
                data = res.group()
                linksdata = data.split('""')
                if (len(linksdata) > 1):
                    targetlink = linksdata[1]
                    #Check whether string is valid URL or not
                    chkUrl = urlparse(targetlink)
                    if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                        Q.enqueue(targetlink)
                        UnreadEmailsList.enqueue(uid)
                        print Q._data
                        print "Length of the Queue is =" + str(Q.__len__())
                        # return "linkFound"
        else:
            self.myfreeSafelist(mailBody,uid)

    # def myfreeSafelist(self, mailBody,uid)
    #     '''
    #     My Free Safelist
    #     '''
    #     if ((re.search(r'bounce@myfreesafelist.com', mailBody, re.DOTALL)) != None):
    #         res = re.search(r'href.*clicks.php.*user.*', mailBody, re.DOTALL)
    #         if (res != None):
    #             data = res.group()
    #             linksdata = data.split('"')
    #             if (len(linksdata) > 1):
    #                 targetlink = linksdata[1]
                    #Check whether string is valid URL or not
                    # chkUrl = urlparse(targetlink)
                    # if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                    #     Q.enqueue(targetlink)
                    #     self.connection.uid('STORE', uid, '+FLAGS', '\SEEN')#mark email read
                    #     UnreadEmailsList.enqueue(uid)
                    #     print Q._data
                    #     print "Length of the Queue is =" + str(Q.__len__())
                        # return "linkFound"

        # else:
        #     self.solomaticAds(mailBody,uid)

    def solomaticAds(self, mailBody,uid):
        '''
        Solomatic Ads, Puffin Mailer,Jaguar Mega Hits,Power Profit List,Instant Viral mailer, Unicor Ads,Farm Land Ads
        '''
        if (((re.search(r'admin@solomaticads.com', mailBody, re.DOTALL)) != None) or ((re.search(r'list@puffinmailer.com', mailBody, re.DOTALL)) != None) or ((re.search(r'admin@jaguarmegahits.com', mailBody, re.DOTALL)) != None) or ((re.search(r'systemmailer@powerprofitlist.com', mailBody, re.DOTALL)) != None) or ((re.search(r'noreply@instantviralmailer.com', mailBody, re.DOTALL)) != None) or ((re.search(r'admin@unicornads.com', mailBody, re.DOTALL)) != None) or ((re.search(r'admin@farmlandads.com', mailBody, re.DOTALL)) != None)):
            res = re.search(r'credit.*', mailBody, re.DOTALL)
            if (res != None):
                data = res.group()
                linksdata = data.split('"')
                if (len(linksdata) > 1):
                    targetlink = linksdata[1]
                    #Check whether string is valid URL or not
                    chkUrl = urlparse(targetlink)
                    if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                        Q.enqueue(targetlink)
                        UnreadEmailsList.enqueue(uid)
                        print Q._data
                        print "Length of the Queue is =" + str(Q.__len__())
                        # return "linkFound"

        else:
            self.europeanSafelist(mailBody,uid)


    def europeanSafelist(self, mailBody,uid):
        '''
        European Safelist
        '''
        if ((re.search(r'bounce@europeansafelist.com', mailBody, re.DOTALL)) != None):
            res = re.search(r'href.*earn.php.*', mailBody, re.DOTALL)
            if (res != None):
                data = res.group()
                linksdata = data.split('"')
                if (len(linksdata) > 1):
                    targetlink = linksdata[1]
                    #Check whether string is valid URL or not
                    chkUrl = urlparse(targetlink)
                    if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                        Q.enqueue(targetlink)
                        self.connection.uid('STORE', uid, '+FLAGS', '\SEEN')#mark email read
                        UnreadEmailsList.enqueue(uid)
                        print Q._data
                        print "Length of the Queue is =" + str(Q.__len__())
                        # return "linkFound"
        else:
            self.adPirate(mailBody,uid)


    def adPirate(self, mailBody,uid):
        '''
        Ad Pirate, Safelist Xtreme,Ad Master Safelist, Express Safelist, Free Ads mailer,List Return, Traffic Pro List,Smart Safelist
        '''
        if (((re.search(r'bounce@adpirate.net', mailBody, re.DOTALL)) != None) or ((re.search(r'bounce1@safelistextreme.com', mailBody, re.DOTALL)) != None)  or ((re.search(r'bounce@admastersafelist.com', mailBody, re.DOTALL)) != None) or ((re.search(r'bounce@expresssafelist.com', mailBody, re.DOTALL)) != None) or ((re.search(r'bounce@freeadsmailer.com', mailBody, re.DOTALL)) != None) or ((re.search(r'bounce@listreturn.com', mailBody, re.DOTALL)) != None) or ((re.search(r'bounce@trafficprolist.com', mailBody, re.DOTALL)) != None) or ((re.search(r'bounce@smartsafelist.com', mailBody, re.DOTALL)) != None)):
            res = re.search(r'credit.*', mailBody, re.DOTALL)
            if (res != None):
                data = res.group()
                linksdata = data.split('\n')
                if (len(linksdata) > 1):
                    targetlink = linksdata[1]
                    #Check whether string is valid URL or not
                    chkUrl = urlparse(targetlink)
                    if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                        Q.enqueue(targetlink)
                        UnreadEmailsList.enqueue(uid)
                        print Q._data
                        print "Length of the Queue is =" + str(Q.__len__())
                        # return "linkFound"
        else:
            self.targetSafelist(mailBody,uid)


    def targetSafelist(self, mailBody,uid):
        '''
        Target Safelist
        '''
        if ((re.search(r'bounce@target-safelist.com', mailBody, re.DOTALL)) != None):
            res = re.search(r'href.*earn credits', mailBody, re.DOTALL)
            if (res != None):
                data = res.group()
                maildata =data.split(" ")[1]
                linksdata = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', maildata)
                if (len(linksdata) >= 1):
                    targetlink = linksdata[0]
                    #Check whether string is valid URL or not
                    chkUrl = urlparse(targetlink)
                    if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                        Q.enqueue(targetlink)
                        UnreadEmailsList.enqueue(uid)
                        print Q._data
                        print "Length of the Queue is =" + str(Q.__len__())
        else:
            self.malingthome(mailBody,uid)

    # def listvolta(sel/f, mailBody,uid):

        # urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', mailBody)
        # for i in urls:
        #     res = re.search(r'earn.php.*',i,re.DOTALL)
        #     if(res != None):
        #         print i
        #         chkUrl = urlparse(i)
        #         if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
        #             Q.enqueue(i)
        #             UnreadEmailsList.enqueue(uid)
        #             print Q._data
        #             print "Length of the Queue is =" + str(Q.__len__())
        #         break
        #     else:
        #         self.malingthome(mailBody,uid)

    def malingthome(self, mailBody,uid):
        '''
        MalingThome.net,Ad Tactics,
        '''
        if (((re.search(r'bounce@mailingathome.net', mailBody, re.DOTALL)) != None)):
            res = re.search(r'href.*earn credits', mailBody, re.DOTALL)
            if (res != None):
                data = res.group()
                linksdata = data.split('"')
                if (len(linksdata) > 1):
                    targetlink = linksdata[-2]
                    #Check whether string is valid URL or not
                    chkUrl = urlparse(targetlink)
                    if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                        Q.enqueue(targetlink)
                        UnreadEmailsList.enqueue(uid)
                        print Q._data
                        print "Length of the Queue is =" + str(Q.__len__())
        else:
            self.adTactics(mailBody,uid)

    def adTactics(self, mailBody,uid):
        if ((re.search(r'bounce@mailer1.adtactics.com', mailBody, re.DOTALL)) != None):
            res = re.search(r'earn credits.*', mailBody, re.DOTALL)
            if (res != None):
                data = res.group()
                linksdata = data.split('\n')
                if (len(linksdata) > 1):
                    targetlink = linksdata[1]
                    # Check whether string is valid URL or not
                    chkUrl = urlparse(targetlink)
                    if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                        Q.enqueue(targetlink)
                        UnreadEmailsList.enqueue(uid)
                        print Q._data
                        print "Length of the Queue is =" + str(Q.__len__())
        else:
            self.stateOfTheArtMailer(mailBody,uid)

            # def safelistXtreme(self, mailBody):
            #     if ((re.search(r'bounce1@safelistextreme.com', mailBody, re.DOTALL)) != None):
            #         res = re.search(r'credit.*', mailBody, re.DOTALL)
            #         if (res != None):
            #             data = res.group()
            #             linksdata = data.split('\n')
            #             if (len(linksdata) > 1):
            #                 targetlink = linksdata[1]
            #                 Check whether string is valid URL or not
            # chkUrl = urlparse(targetlink)
            # if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
            #     Q.enqueue(targetlink)
            #print Q._data
            # print "Length of the Queue is =" + str(Q.__len__())
            # else:
            #     self.stateOfTheArtMailer(mailBody)

    def stateOfTheArtMailer(self, mailBody,uid):
        '''
        State Of The Art Mailer
        '''
        if ((re.search(r'bounce@state-of-the-art-mailer.com', mailBody, re.DOTALL)) != None):
            res = re.search(r'href.*viewing', mailBody, re.DOTALL)
            if (res != None):
                data = res.group()
                linksdata = data.split("'")
                if (len(linksdata) > 1):
                    targetlink = linksdata[1]
                    #Check whether string is valid URL or not
                    chkUrl = urlparse(targetlink)
                    if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                        Q.enqueue(targetlink)
                        UnreadEmailsList.enqueue(uid)
                        print Q._data
                        print "Length of the Queue is =" + str(Q.__len__())
        else:
            self.theMailBagSafelist(mailBody,uid)

    def theMailBagSafelist(self, mailBody,uid):
        if ((re.search(r'bounce@themailbagsafelist.com', mailBody, re.DOTALL)) != None):
            res = re.search(r'credit.*', mailBody, re.DOTALL)
            if (res != None):
                data = res.group()
                maildata =data.split("href")[1]
                linksdata= re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', maildata)
                if (len(linksdata) >= 1):
                    targetlink = linksdata[0]
    #Check whether string is valid URL or not
                    chkUrl = urlparse(targetlink)
                    if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                        Q.enqueue(targetlink)
                        UnreadEmailsList.enqueue(uid)
                        print Q._data
                        print "Length of the Queue is =" + str(Q.__len__())
        else:
            self.ezyMailCsh(mailBody,uid)

    def ezyMailCsh(self, mailBody,uid):
        '''
        Ezy mail Csh
        '''
        if ((re.search(r'bounce@ezymailcash.com', mailBody, re.DOTALL)) != None):
            res = re.search(r'click.*receive.*credits.*', mailBody, re.DOTALL)
            if (res != None):
                data = res.group()
                linksdata = data.split('"')
                if (len(linksdata) > 1):
                    targetlink = linksdata[1]
                    #Check whether string is valid URL or not
                    chkUrl = urlparse(targetlink)
                    if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                        Q.enqueue(targetlink)
                        UnreadEmailsList.enqueue(uid)
                        print Q._data
                        print "Length of the Queue is =" + str(Q.__len__())
        else:
            self.supremeList(mailBody,uid)

            # def puffinMailer(self, mailBody):
            #     if ((re.search(r'list@puffinmailer.com', mailBody, re.DOTALL)) != None):
            #         res = re.search(r'credit.*', mailBody, re.DOTALL)
            #         if (res != None):
            #             data = res.group()
            #             linksdata = data.split('"')
            #             if (len(linksdata) > 1):
            #                 targetlink = linksdata[1]
            #Check whether string is valid URL or not
            # chkUrl = urlparse(targetlink)
            # if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
            #     Q.enqueue(targetlink)
            #print Q._data
            # print "Length of the Queue is =" + str(Q.__len__())
            # else:
            #     self.supremeList(mailBody)

    def supremeList(self, mailBody,uid):
        '''
        Supreme List
        '''
        if ((re.search(r'spx_16819@supremelist.com', mailBody, re.DOTALL)) != None):
            res = re.search(r'link.*credits.*http.*', mailBody, re.DOTALL)
            if (res != None):
                data = res.group()
                linksdata = data.split('\n')
                if (len(linksdata) > 1):
                    targetlink = linksdata[2]
                    #Check whether string is valid URL or not
                    chkUrl = urlparse(targetlink)
                    if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                        Q.enqueue(targetlink)
                        UnreadEmailsList.enqueue(uid)
                        print Q._data
                        print "Length of the Queue is =" + str(Q.__len__())
        else:
            self.globalSafelist(mailBody,uid)

    def globalSafelist(self, mailBody,uid):
        '''
        Global Safelist
        '''
        if ((re.search(r'bounce@globalsafelist.com', mailBody, re.DOTALL)) != None):
            res = re.search(r'link.*credits.*http.*', mailBody, re.DOTALL)
            if (res != None):
                data = res.group()
                linksdata = data.split('\n')
                if (len(linksdata) > 1):
                    targetlink = linksdata[1]
                    #Check whether string is valid URL or not
                    chkUrl = urlparse(targetlink)
                    if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                        Q.enqueue(targetlink)
                        UnreadEmailsList.enqueue(uid)
                        print Q._data
                        print "Length of the Queue is =" + str(Q.__len__())
        else:
            self.misterSafelist(mailBody,uid)

    def misterSafelist(self, mailBody,uid):
        '''
        Mister Safelist
        '''
        if ((re.search(r'noreply@mistersafelist.com', mailBody, re.DOTALL)) != None):
            res = re.search(r'href.*click', mailBody, re.DOTALL)
            if (res != None):
                data = res.group()
                linksdata = data.split('"')
                if (len(linksdata) > 1):
                    targetlink = linksdata[1]
                    #Check whether string is valid URL or not
                    chkUrl = urlparse(targetlink)
                    if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                        Q.enqueue(targetlink)
                        UnreadEmailsList.enqueue(uid)
                        print Q._data
                        print "Length of the Queue is =" + str(Q.__len__())
        else:
            self.universalSoloAds(mailBody,uid)

            # def adMasterSafelist(self, mailBody):
            #     if ((re.search(r'bounce@admastersafelist.com', mailBody, re.DOTALL)) != None):
            #         res = re.search(r'credit.*', mailBody, re.DOTALL)
            #         if (res != None):
            #             data = res.group()
            #             linksdata = data.split('\n')
            #             if (len(linksdata) > 1):
            #                 targetlink = linksdata[1]
            #                 Check whether string is valid URL or not
            # chkUrl = urlparse(targetlink)
            # if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
            #     Q.enqueue(targetlink)
            #print Q._data
            # print "Length of the Queue is =" + str(Q.__len__())
            # else:
            #     self.herculist(mailBody)

    # def herculist(self, mailBody,uid):
    #     '''
    #     Herculit,No Loop Solo
    #     '''
        # urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', mailBody)
        # for i in urls:
        #     res = re.search(r'/c/n.*',i,re.DOTALL)
        #     if(res != None):
        #         print i
        #         chkUrl = urlparse(i)
        #         if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
        #             Q.enqueue(i)
        #             UnreadEmailsList.enqueue(uid)
        #             print Q._data
        #             print "Length of the Queue is =" + str(Q.__len__())
        #         break
        #     else:
        #         self.universalSoloAds(mailBody,uid)

    def universalSoloAds(self, mailBody,uid):
        '''
        Universal Soo Ads
        '''
        if ((re.search(r'admin@universalsoloads.info', mailBody, re.DOTALL)) != None):
            res = re.search(r'href.*credits', mailBody, re.DOTALL)
            if (res != None):
                data = res.group()
                linksdata = data.split('"')
                if (len(linksdata) > 1):
                    targetlink = linksdata[1]
                    #Check whether string is valid URL or not
                    chkUrl = urlparse(targetlink)
                    if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                        Q.enqueue(targetlink)
                        UnreadEmailsList.enqueue(uid)
                        print Q._data
                        print "Length of the Queue is =" + str(Q.__len__())
        else:
            self.dynamiteSafelist(mailBody,uid)

    def dynamiteSafelist(self, mailBody,uid):
        if (((re.search(r'bounce@dynamite-safelist.com', mailBody, re.DOTALL)) != None) or (re.search(r'bounce@safelistpro.com',str(mailBody).lower(),re.DOTALL) != None)):
            res = re.search(r'.*earn credits', mailBody, re.DOTALL)
            if (res != None):
                data = res.group()
                linksdata = data.split('"')
                if (len(linksdata) > 1):
                    targetlink = linksdata[-2]
                    # Check whether string is valid URL or not
                    chkUrl = urlparse(targetlink)
                    if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                        Q.enqueue(targetlink)
                        UnreadEmailsList.enqueue(uid)
                        print Q._data
                        print "Length of the Queue is =" + str(Q.__len__())
            else:
                res2 = re.search(r'credits.*', mailBody, re.DOTALL)
                if (res2 != None):
                    data2 = res2.group()
                    linksdata2 = data2.split('\n')
                    if (len(linksdata2) > 1):
                        targetlink2 = linksdata2[0]
                        # Check whether string is valid URL or not
                        chkUrl2 = urlparse(targetlink2)
                        if(chkUrl2.scheme == 'http' or chkUrl2.scheme == 'https'):
                            Q.enqueue(targetlink2)
                            UnreadEmailsList.enqueue(uid)
                            print Q._data
                            print "Length of the Queue is =" + str(Q.__len__())
        else:
            self.activeSafelist(mailBody,uid)

    def activeSafelist(self, mailBody,uid):
        '''
        Active Safelist
        '''
        if ((re.search(r'spx_34135@activesafelist.com', mailBody, re.DOTALL)) != None):
            res = re.search(r'earn.*http.*', mailBody, re.DOTALL)
            if (res != None):
                data = res.group()
                linksdata = data.split('\n')
                if (len(linksdata) > 1):
                    targetlink = linksdata[2]
                    #Check whether string is valid URL or not
                    chkUrl = urlparse(targetlink)
                    if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                        Q.enqueue(targetlink)
                        UnreadEmailsList.enqueue(uid)
                        print Q._data
                        print "Length of the Queue is =" + str(Q.__len__())
        else:
            # self.ultimateSafelist(mailBody,uid)
            pass

    def ultimateSafelist(self, mailBody,uid):
        '''
        Ultimate Safelist,100 Percent Mailer,Dynamite Safelist,
        '''
        if (((re.search(r'bounce@ultimate-safelist.com', mailBody, re.DOTALL)) != None) or ((re.search(r'memberalert@mail.100percentmailer.com', mailBody, re.DOTALL)) != None) ):
            res = re.search(r'href.*click', mailBody, re.DOTALL)
            if (res != None):
                data = res.group()
                linksdata = data.split('"')
                if (len(linksdata) > 1):
                    targetlink = linksdata[-2]
                    #Check whether string is valid URL or not
                    chkUrl = urlparse(targetlink)
                    if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                        Q.enqueue(targetlink)
                        UnreadEmailsList.enqueue(uid)
                        print Q._data
                        print "Length of the Queue is =" + str(Q.__len__())
        else:
            self.safelistPro(mailBody,uid)

            # def hundredPercentMailer(self, mailBody):
            #     if ((re.search(r'memberalert@mail.100percentmailer.com', mailBody, re.DOTALL)) != None):
            #         res = re.search(r'href.*click', mailBody, re.DOTALL)
            #         if (res != None):
            #             data = res.group()
            #             linksdata = data.split('"')
            #             if (len(linksdata) > 1):
            #                 targetlink = linksdata[-2]
            #Check whether string is valid URL or not
            # chkUrl = urlparse(targetlink)
            # if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
            #     Q.enqueue(targetlink)
            #print Q._data
            # print "Length of the Queue is =" + str(Q.__len__())
            # else:
            #     self.targetSafelist(mailBody)

    def safelistPro(self, mailBody,uid):
        '''
        Safelist Pro
        '''
        if ((re.search(r'bounce@safelistpro.com', mailBody, re.DOTALL)) != None):
            res = re.search(r'below.*http.*', mailBody, re.DOTALL)
            if (res != None):
                data = res.group()
                linksdata = data.split('"')
                if (len(linksdata) > 1):
                    targetlink = linksdata[1]
                    #Check whether string is valid URL or not
                    chkUrl = urlparse(targetlink)
                    if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                        Q.enqueue(targetlink)
                        UnreadEmailsList.enqueue(uid)
                        print Q._data
                        print "Length of the Queue is =" + str(Q.__len__())
                        # return "linkFound"
        else:
            self.speedwaySafelist(mailBody,uid)

            # def jaguarMegaHits(self, mailBody):
            #     if ((re.search(r'admin@jaguarmegahits.com', mailBody, re.DOTALL)) != None):
            #         res = re.search(r'credit.*', mailBody, re.DOTALL)
            #         if (res != None):
            #             data = res.group()
            #             linksdata = data.split('"')
            #             if (len(linksdata) > 1):
            #                 targetlink = linksdata[1]
            #Check whether string is valid URL or not
            # chkUrl = urlparse(targetlink)
            # if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
            #     Q.enqueue(targetlink)
            #print Q._data
            # print "Length of the Queue is =" + str(Q.__len__())
            # else:
            #     self.expressSafelist(mailBody)

            # def expressSafelist(self, mailBody):
            #     if ((re.search(r'bounce@expresssafelist.com', mailBody, re.DOTALL)) != None):
            #         res = re.search(r'credit.*', mailBody, re.DOTALL)
            #         if (res != None):
            #             data = res.group()
            #             linksdata = data.split('\n')
            #             if (len(linksdata) > 1):
            #                 targetlink = linksdata[1]
            #Check whether string is valid URL or not
            # chkUrl = urlparse(targetlink)
            # if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
            #     Q.enqueue(targetlink)
            #print Q._data
            # print "Length of the Queue is =" + str(Q.__len__())
            # else:
            #     self.freeadsMailerSafelist(mailBody)

            # def freeadsMailerSafelist(self, mailBody):
            #     if ((re.search(r'bounce@freeadsmailer.com', mailBody, re.DOTALL)) != None):
            #         res = re.search(r'credit.*', mailBody, re.DOTALL)
            #         if (res != None):
            #             data = res.group()
            #             linksdata = data.split('\n')
            #             if (len(linksdata) > 1):
            #                 targetlink = linksdata[1]
            #Check whether string is valid URL or not
            # chkUrl = urlparse(targetlink)
            # if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
            #     Q.enqueue(targetlink)
            #print Q._data
            # print "Length of the Queue is =" + str(Q.__len__())
            # else:
            #     self.listReturn(mailBody)

            # def listReturn(self, mailBody):
            #     if ((re.search(r'bounce@listreturn.com', mailBody, re.DOTALL)) != None):
            #         res = re.search(r'credit.*', mailBody, re.DOTALL)
            #         if (res != None):
            #             data = res.group()
            #             linksdata = data.split('\n')
            #             if (len(linksdata) > 1):
            #                 targetlink = linksdata[1]
            #Check whether string is valid URL or not
            # chkUrl = urlparse(targetlink)
            # if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
            #     Q.enqueue(targetlink)
            #print Q._data
            # print "Length of the Queue is =" + str(Q.__len__())
            # else:
            #     self.safelistPro(mailBody)

            # def safelistPro(self, mailBody):
            #     if ((re.search(r'bounce@safelistpro.com', mailBody, re.DOTALL)) != None):
            #         res = re.search(r'below.*http.*', mailBody, re.DOTALL)
            #         if (res != None):
            #             data = res.group()
            #             linksdata = data.split('"')
            #             if (len(linksdata) > 1):
            #                 targetlink = linksdata[1]
            #Check whether string is valid URL or not
            # chkUrl = urlparse(targetlink)
            # if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
            #     Q.enqueue(targetlink)
            #print Q._data
            # print "Length of the Queue is =" + str(Q.__len__())
            # else:
            #     self.speedwaySafelist(mailBody)

    def speedwaySafelist(self, mailBody,uid):
        '''
        Speed Way Safelist
        '''
        if ((re.search(r'bounce@speedwaysafelist.com', mailBody, re.DOTALL)) != None):
            res = re.search(r'href.*click', mailBody, re.DOTALL)
            if (res != None):
                data = res.group()
                linksdata = data.split('"')
                if (len(linksdata) > 1):
                    targetlink = linksdata[-2]
                    #Check whether string is valid URL or not
                    chkUrl = urlparse(targetlink)
                    if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                        Q.enqueue(targetlink)
                        UnreadEmailsList.enqueue(uid)
                        print Q._data
                        print "Length of the Queue is =" + str(Q.__len__())
                        # return "linkFound"
        else:
            self.vitalAdViews(mailBody,uid)

    def vitalAdViews(self, mailBody,uid):
        '''
        Vital Ad Views
        '''
        if ((re.search(r'bounce@vitaladviews.com', mailBody, re.DOTALL)) != None):
            res = re.search(r'href.*credits', mailBody, re.DOTALL)
            if (res != None):
                data = res.group()
                linksdata = data.split('"')
                if (len(linksdata) > 1):
                    targetlink = linksdata[-2]
                    #Check whether string is valid URL or not
                    chkUrl = urlparse(targetlink)
                    if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                        Q.enqueue(targetlink)
                        UnreadEmailsList.enqueue(uid)
                        print Q._data
                        print "Length of the Queue is =" + str(Q.__len__())
                        # return "linkFound"
        else:
            self.safariMailer(mailBody,uid)

            # def powerProfitList(self, mailBody):
            #     if ((re.search(r'systemmailer@powerprofitlist.com', mailBody, re.DOTALL)) != None):
            #         res = re.search(r'credit.*', mailBody, re.DOTALL)
            #         if (res != None):
            #             data = res.group()
            #             linksdata = data.split('"')
            #             if (len(linksdata) > 1):
            #                 targetlink = linksdata[1]
            #Check whether string is valid URL or not
            # chkUrl = urlparse(targetlink)
            # if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
            #     Q.enqueue(targetlink)
            #print Q._data
            # print "Length of the Queue is =" + str(Q.__len__())
            # else:
            #     self.instantViralMailer(mailBody)

            # def instantViralMailer(self, mailBody):
            #     if ((re.search(r'noreply@instantviralmailer.com', mailBody, re.DOTALL)) != None):
            #         res = re.search(r'credit.*', mailBody, re.DOTALL)
            #         if (res != None):
            #             data = res.group()
            #             linksdata = data.split('"')
            #             if (len(linksdata) > 1):
            #                 targetlink = linksdata[1]
            #Check whether string is valid URL or not
            # chkUrl = urlparse(targetlink)
            # if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
            #     Q.enqueue(targetlink)
            #print Q._data
            # print "Length of the Queue is =" + str(Q.__len__())
            # else:
            #     self.unicornAds(mailBody)

            # def unicornAds(self, mailBody):
            #     if ((re.search(r'admin@unicornads.com', mailBody, re.DOTALL)) != None):
            #         res = re.search(r'credit.*', mailBody, re.DOTALL)
            #         if (res != None):
            #             data = res.group()
            #             linksdata = data.split('"')
            #             if (len(linksdata) > 1):
            #                 targetlink = linksdata[1]
            #Check whether string is valid URL or not
            # chkUrl = urlparse(targetlink)
            # if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
            #     Q.enqueue(targetlink)
            #print Q._data
            # print "Length of the Queue is =" + str(Q.__len__())
            # else:
            #     self.safariMailer(mailBody)

    def safariMailer(self, mailBody,uid):
        '''
        Safari Mailer,Email Traffic List,
        '''
        if (((re.search(r'mail@safarimailer.com', mailBody, re.DOTALL)) != None) or ((re.search(r'bounce@emailtrafficlist.com', mailBody, re.DOTALL)) != None)):
            res = re.search(r'credit.*', mailBody, re.DOTALL)
            if (res != None):
                data = res.group()
                linksdata = data.split(' ')
                if (len(linksdata) > 1):
                    targetlink = linksdata[1].split("\n")[0]
                    #Check whether string is valid URL or not
                    chkUrl = urlparse(targetlink)
                    if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                        Q.enqueue(targetlink)
                        UnreadEmailsList.enqueue(uid)
                        print Q._data
                        print "Length of the Queue is =" + str(Q.__len__())
                        # return "linkFound"
        else:
            self.soloAdvertisingNetwork(mailBody,uid)

            # def emailTrafficList(self, mailBody):
            #     if ((re.search(r'bounce@emailtrafficlist.com', mailBody, re.DOTALL)) != None):
            #         res = re.search(r'credit.*', mailBody, re.DOTALL)
            #         if (res != None):
            #             data = res.group()
            #             linksdata = data.split(' ')
            #             if (len(linksdata) > 1):
            #                 targetlink = linksdata[1].split("\n")[0]
            #Check whether string is valid URL or not
            # chkUrl = urlparse(targetlink)
            # if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
            #     Q.enqueue(targetlink)
            #print Q._data
            # print "Length of the Queue is =" + str(Q.__len__())
            # else:
            #     self.soloAdvertisingNetwork(mailBody)

    def soloAdvertisingNetwork(self, mailBody,uid):
        '''
        Solo Advertising Network
        '''
        if ((re.search(r'admin@soloadvertisingnetwork.com', mailBody, re.DOTALL)) != None):
            res = re.search(r'.*credits', mailBody, re.DOTALL)
            if (res != None):
                data = res.group()
                maildata = data.split("href")[-1]
                linksdata= re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', maildata)
                if (len(linksdata) >= 1):
                    targetlink = linksdata[0]
                    #Check whether string is valid URL or not
                    chkUrl = urlparse(targetlink)
                    if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                        Q.enqueue(targetlink)
                        UnreadEmailsList.enqueue(uid)
                        print Q._data
                        print "Length of the Queue is =" + str(Q.__len__())
                        # return "linkFound"
        else:
            self.expressWebTraffic(mailBody,uid)

            # def trafficProList(self, mailBody):
            #     if ((re.search(r'bounce@trafficprolist.com', mailBody, re.DOTALL)) != None):
            #         res = re.search(r'credit.*', mailBody, re.DOTALL)
            #         if (res != None):
            #             data = res.group()
            #             linksdata = data.split('\n')
            #             if (len(linksdata) > 1):
            #                 targetlink = linksdata[1]
            #Check whether string is valid URL or not
            # chkUrl = urlparse(targetlink)
            # if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
            #     Q.enqueue(targetlink)
            #print Q._data
            # print "Length of the Queue is =" + str(Q.__len__())
            # else:
            #     self.smartSafelist(mailBody)

            # def smartSafelist(self, mailBody):
            #     if ((re.search(r'bounce@smartsafelist.com', mailBody, re.DOTALL)) != None):
            #         res = re.search(r'credit.*', mailBody, re.DOTALL)
            #         if (res != None):
            #             data = res.group()
            #             linksdata = data.split('\n')
            #             if (len(linksdata) > 1):
            #                 targetlink = linksdata[1]
            #Check whether string is valid URL or not
            # chkUrl = urlparse(targetlink)
            # if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
            #     Q.enqueue(targetlink)
            #print Q._data
            # print "Length of the Queue is =" + str(Q.__len__())
            # else:
            #     self.expressWebTraffic(mailBody)

    def expressWebTraffic(self, mailBody,uid):
        '''
        Express Web Traffic,Xchnage Your Ads,Rush Our Traffic
        '''
        if (((re.search(r'webmaster@expresswebtraffic.com', mailBody, re.DOTALL)) != None) or ((re.search(r'admin@xchangeyourads.com', mailBody, re.DOTALL)) != None) or ((re.search(r'admin@rushourtraffic.com', mailBody, re.DOTALL)) != None)):
            res = re.search(r'.*credit', mailBody, re.DOTALL)
            if (res != None):
                data = res.group()
                linksdata = data.split('"')
                if (len(linksdata) > 1):
                    targetlink = linksdata[-2]
                    #Check whether string is valid URL or not
                    chkUrl = urlparse(targetlink)
                    if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                        Q.enqueue(targetlink)
                        UnreadEmailsList.enqueue(uid)
                        print Q._data
                        print "Length of the Queue is =" + str(Q.__len__())
                        # return "linkFound"
        else:
            self.adminMidnight(mailBody,uid)

    def adminMidnight(self, mailBody,uid):
        '''
        Mid Night SunSafelist
        '''
        if ((re.search(r'admin@midnightsunsafelist.com', mailBody, re.DOTALL)) != None):
            res = re.search(r'list adventure.*', mailBody, re.DOTALL)
            if (res != None):
                data = res.group()
                linksdata = data.split('"')
                if (len(linksdata) > 1):
                    targetlink = linksdata[1]
                    # Check whether string is valid URL or not
                    chkUrl = urlparse(targetlink)
                    if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                        Q.enqueue(targetlink)
                        UnreadEmailsList.enqueue(uid)
                        print Q._data
                        print "Length of the Queue is =" + str(Q.__len__())
                        # return "linkFound"
        else:
            self.listAdventure(mailBody,uid)

    def listAdventure(self,mailBody,uid):
        '''
        List Adventure
        '''
        if ((re.search(r'noreply@listadventure.com', mailBody, re.DOTALL)) != None):
            res = re.search(r'earn credits.*', mailBody, re.DOTALL)
            if (res != None):
                data = res.group()
                name= re.sub('[=0A\n]', '', data)
                data2=name.split("earn credits")
                if (len(data2) > 1):
                    targetlink = "".join(data2).split("-")[0]
                    # Check whether string is valid URL or not
                    chkUrl = urlparse(targetlink)
                    if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                        Q.enqueue(targetlink)
                        UnreadEmailsList.enqueue(uid)
                        print Q._data
                        print "Length of the Queue is =" + str(Q.__len__())
                        # return "linkFound"
        else:
            self.theLeadMagnet(mailBody,uid)

    def theLeadMagnet(self,mailBody,uid):
        '''
        The Lead Magnet
        '''
        if (((re.search(r'bounce@theleadmagnet.com', mailBody, re.DOTALL)) != None)):
            res = re.search(r'credits.*', mailBody, re.DOTALL)
            if (res != None):
                data = res.group()
                linksdata = data.split('"')
                if (len(linksdata) > 1):
                    targetlink = linksdata[1]
                    # Check whether string is valid URL or not
                    chkUrl = urlparse(targetlink)
                    if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                        Q.enqueue(targetlink)
                        UnreadEmailsList.enqueue(uid)
                        print Q._data
                        print "Length of the Queue is =" + str(Q.__len__())
                        # return "linkFound"
        else:
            self.safelistXL(mailBody,uid)

    def safelistXL(self,mailBody,uid):
        '''
        SafelistXL,Traffic Zip,Elite Safelist,
        '''
        if (((re.search(r'admin@safelistxl.com', mailBody, re.DOTALL)) != None) or ((re.search(r'bounce@trafficzip.com', mailBody, re.DOTALL)) != None) or ((re.search(r'bounce@elitesafelist.com', mailBody, re.DOTALL)) != None)):
            res = re.search(r'earn credits.*', mailBody, re.DOTALL)
            if (res != None):
                data = res.group()
                linksdata = re.sub('\s*','',data.strip()).split("->")[1].split("click")
                if (len(linksdata) > 1):
                    targetlink = linksdata[0]
                    # Check whether string is valid URL or not
                    chkUrl = urlparse(targetlink)
                    if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                        Q.enqueue(targetlink)
                        UnreadEmailsList.enqueue(uid)
                        print Q._data
                        print "Length of the Queue is =" + str(Q.__len__())
                        # return "linkFound"
        else:
            # self.commonAlgo(mailBody)
            self.algo1(mailBody,uid)

    def algo1(self,mailBody,uid):
        lineList = string.split(mailBody, '\n')
        pattwords = ['noks!','credits','points']
        #print lineList
        for id,lnstr in enumerate(lineList):
            for ptwrd in pattwords:
                if ptwrd in lnstr:
                    # print "Word Exists at index ",id
                    #print lineList[id]
                    str1 = ''.join(lineList[(id-1):])
                    #print str1
                    linksdata= re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', str1)
                    allLinks = string.split(str(linksdata[0]).lower(), '\n')
                    if "id" in allLinks[0]:
                        linkExpect = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', allLinks[0])
                        targetlink = linkExpect[0]
                        chkUrl = urlparse(targetlink)
                        if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                            Q.enqueue(targetlink)
                            UnreadEmailsList.enqueue(uid)
                            print Q._data
                            print "Length of the Queue is =" + str(Q.__len__())

    def commonAlgo(self,mailBody):
        '''
        Xchange Your Ads,TrafficLeads2IncomeVM,Text Ad Magic
        '''
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', mailBody)

        for i in urls:
            res = re.search(r'userid.*',i,re.DOTALL)
            if(res != None):
                print i
                chkUrl = urlparse(i)
                if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                    Q.enqueue(i)
                    print Q._data
                    print "Length of the Queue is =" + str(Q.__len__())
                break
            else:
                self.listPirates(mailBody)
    def listPirates(self,mailBody,uid):
        '''
        List Pirates
        '''
        if ((re.search(r'admin@list-pirates.com', mailBody, re.DOTALL)) != None):
            urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', mailBody)
            for i in urls:
                res = re.search(r'userid.*',i,re.DOTALL)
                if(res != None):
                    targetLink = i.split("<br")[0]
                    chkUrl = urlparse(targetLink)
                    if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                        Q.enqueue(targetLink)
                        print Q._data
                        UnreadEmailsList.enqueue(uid)
                        print "Length of the Queue is =" + str(Q.__len__())
        else:
            self.dynamiteSafelist(mailBody,uid)

                    # def eliteSafelist(self,mailBody):
                    #     if ((re.search(r'bounce@elitesafelist.com', mailBody, re.DOTALL)) != None):
                    #         res = re.search(r'credits.*', mailBody, re.DOTALL)
                    #         if (res != None):
                    #             data = res.group()
                    #             linksdata = data.split('"')
                    #             if (len(linksdata) > 1):
                    #                 targetlink = linksdata[1]
                    # Check whether string is valid URL or not
                    # chkUrl = urlparse(targetlink)
                    # if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                    #     Q.enqueue(targetlink)
                    #     print Q._data
                    #     print "Length of the Queue is =" + str(Q.__len__())
                    # else:
                    #     pass

                    # def listAvail(self,mailBody):
                    #     if ((re.search(r'receive.*', mailBody, re.DOTALL)) != None):
                    #         res = re.search(r'receive.*', mailBody, re.DOTALL)
                    #         if (res != None):
                    #             data = res.group()
                    #             data2 = data.split("href=")[1]
                    #             name= re.sub('[3D2\n]', '', data2)
                    #             linksdata = name.split('"')
                    #             if (len(linksdata) > 1):
                    #                 targetlink = linksdata[1]
                    #                 Check whether string is valid URL or not
                    # chkUrl = urlparse(targetlink)
                    # if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                    #     Q.enqueue(targetlink)
                    #     print Q._data
                    #     print "Length of the Queue is =" + str(Q.__len__())
                    # else:
                    #     pass

                    # def farmLandAds(self, mailBody):
                    #     if ((re.search(r'admin@farmlandads.com', mailBody, re.DOTALL)) != None):
                    #         res = re.search(r'credit.*', mailBody, re.DOTALL)
                    #         if (res != None):
                    #             data = res.group()
                    #             linksdata = data.split('"')
                    #             if (len(linksdata) > 1):
                    #                 targetlink = linksdata[1]
                    #Check whether string is valid URL or not
                    # chkUrl = urlparse(targetlink)
                    # if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                    #     Q.enqueue(targetlink)
                    #print Q._data
                    # print "Length of the Queue is =" + str(Q.__len__())
                    # else:
                    #     self.rushOurTraffic(mailBody)

                    # def rushOurTraffic(self, mailBody):
                    #     if ((re.search(r'admin@rushourtraffic.com', mailBody, re.DOTALL)) != None):
                    #         res = re.search(r'.*credit', mailBody, re.DOTALL)
                    #         if (res != None):
                    #             data = res.group()
                    #             linksdata = data.split('"')
                    #             if (len(linksdata) > 1):
                    #                 targetlink = linksdata[-2]
                    #Check whether string is valid URL or not
                    # chkUrl = urlparse(targetlink)
                    # if(chkUrl.scheme == 'http' or chkUrl.scheme == 'https'):
                    #     Q.enqueue(targetlink)
                    #print Q._data
                    # print "Length of the Queue is =" + str(Q.__len__())
                    # else:
                    #     pass

class Worker(QtCore.QObject):
    '''
    This class Handle the Multi Processing Feature
    '''

    def __init__(self, scanmanobj,parent=None):
        super(Worker, self).__init__(parent)
        self.parent = parent
        self.scanmanobj = scanmanobj
        try:
            self.p = multiprocessing.Process(target=self.createMyPopUpobj)
            self.p.start()
            print "Process "+self.p.name+ " is being Created!!!"
            self.parent.proc_name = self.p.name
        except Exception as Ex:
            print  Ex

    def createMyPopUpobj(self):
        m = MyPopUp(self.scanmanobj,self.parent)

    def tormant(self,proc_name):
        PROCNAME = proc_name
        for proc in psutil.process_iter():
            if proc.name() == PROCNAME:
                proc.kill()
        print "Terminating Process : ",PROCNAME

occurence = 0
class UrlOpenerThread(QtCore.QObject):
    '''
    This class is a middle ware interface between Scan Start Class and the Application Window class to integrate both of them
    '''

    def __init__(self, applicationobj, parent=None):
        super(UrlOpenerThread, self).__init__(parent)
        self.applicationObj = applicationobj
        # print "Inside URL opener Thread Class"
        # self.applicationwndobj = applicationobj.getApplicationWindow()

        self.scanStartThreadObj = ScanStartThread(applicationobj.getScanMan())  #Scan Start Thread Object
        # if not Q.is_empty():
        #     self.scanStartThreadObj.emit("connectUrl",Q.dequeue())
        self.connect(self.scanStartThreadObj, QtCore.SIGNAL("connectUrl"), self.loadSmartUrl)
        self.scanStartThreadObj.start()

    def loadSmartUrl(self, targetLink):
        '''
        This class will find the signal and implement it'scorresponding slot to load the target link
        '''
        # print "Load The URL :" + targetLink
        #print Q._data
        self.applicationObj.wnd.smartScanWidgets[0].exitAppWnd()
        self.applicationObj.wnd.smartScanWidgets = []
        self.applicationObj.wnd.openLoadUrl(targetLink)

        #self.captchaManger = CapthcaManager()
        #self.applicationObj.wnd.smartScanWidgets[0].scanUrl(targetLink)

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

class MyPopUp(QtGui.QWidget):
    '''
    This class creates an additional custom Widget that will be useful for the loading of target link with each iteration
    '''

    def __init__(self, scanManObj, parent=None):
        super(MyPopUp, self).__init__(parent)
        self.status = "Alive"
        self.linkopened = False
        self.parent = parent
        self.scanManObj = scanManObj
        sys.excepthook = ExceptHook
        self.init_views()

    '''
    Function to take action when user clicks the know more button
    It opens the url of the tab in default browser
    Also adds this to remote database
    '''
    def init_views(self):
        
        self.layout = QtGui.QVBoxLayout()
        from PyQt4 import Qt
        # self.webwnd = Qt.QWebView()  #ScanMan WebView Object
        # self.webwnd.page().networkAccessManager().setCache(self.parent.cache)

        # self.webwnd = self.parent.smartScanWidgets[0]
        self.webwnd = MainFrame()
        self.hideLinkButton = QtGui.QPushButton("")
        self.hideLinkButton.setFlat(True)
        self.hideLinkButton.setStyleSheet("background-color:#FFFFFF;")
        self.hideLinkButton.setIcon(QtGui.QIcon(QtGui.QPixmap(':/resources/New-Inactive-Next.png')))
        self.hideLinkButton.setIconSize(QtCore.QSize(190,30))
        #self.nextButton = QtGui.QPushButton("Next!")

        # self.webwnd.page().networkAccessManager().setCache(self.cache)
        self.knowMoreButton = QtGui.QPushButton("")
        self.knowMoreButton.setFlat(True)
        self.knowMoreButton.setStyleSheet("background-color:#FFFFFF;")
        self.knowMoreButton.setIcon(QtGui.QIcon(QtGui.QPixmap(':/resources/New-Know-More.png')))
        self.knowMoreButton.setIconSize(QtCore.QSize(190,30))
        self.hboxLayout = QtGui.QHBoxLayout()
        #
        self.hboxLayout.addWidget(self.knowMoreButton)
        self.hboxLayout.addWidget(self.hideLinkButton)
        #self.hboxLayout.addWidget(self.nextButton)

        self.layout.addWidget(self.webwnd)
        self.layout.addLayout(self.hboxLayout)

        self.setLayout(self.layout)
        self.hideLinkButton.setEnabled(False)

        self.timer = QTimer()
        self.timer.timeout.connect(self.enableHideBtn)
        self.timer.start(5000)

        QtCore.QObject.connect(self.hideLinkButton, QtCore.SIGNAL('clicked()'), self.hideBtnConnect)
        #QtCore.QObject.connect(self.nextButton, QtCore.SIGNAL('clicked()'), self.nextBtnConnect)
        QtCore.QObject.connect(self.knowMoreButton, QtCore.SIGNAL('clicked()'), self.knowMoreBtnConnect)

        # self.webwnd.settings().setAttribute(QtWebKit.QWebSettings.PluginsEnabled, self.scanManObj._app.enableSoundFlag)
        # self.webwnd.settings().setAttribute(QtWebKit.QWebSettings.AcceleratedCompositingEnabled,self.scanManObj._app.enableSoundFlag)
        # self.webwnd.settings().setAttribute(QtWebKit.QWebSettings.JavascriptEnabled, self.scanManObj._app.enableSoundFlag)

        # self.webwnd.settings().setAttribute(QtWebKit.QWebSettings.AutoLoadImages,False)
        # self.webwnd.settings().setAttribute(QtWebKit.QWebSettings.AutoLoadImages,True)

    def enableHideBtn(self):
        self.hideLinkButton.setEnabled(True)
        self.hideLinkButton.setFlat(True)
        self.hideLinkButton.setStyleSheet("background-color:#FFFFFF;")
        self.hideLinkButton.setIcon(QtGui.QIcon(QtGui.QPixmap(':/resources/New-Next.png')))
        self.hideLinkButton.setIconSize(QtCore.QSize(190,30))
        self.timer.stop()

    def nextBtnConnect(self):
        self.nextButtonClicked()


    def knowMoreBtnConnect(self):
        urlToBeOpened = self.webwnd.getUrlToBeLoaded()
        # print "Url To Be Loaded",urlToBeOpened
        # urlString = str(urlToBeOpened.toString())
        webbrowser.open_new_tab(urlToBeOpened)
        self.addUrlToLocalDatabase(urlToBeOpened)
        # self.addUrlToRemoteDatabase(urlString)

    '''
    Adds the input url to database
    '''
    def addUrlToRemoteDatabase(self, urlToBeAdded):
        pass
        # conn = mysql.connector.connect(user="root", password="hulk123", host="localhost", database="python")
        # mycursor = conn.cursor()
        # queryStrng = "INSERT INTO smartscan VALUES ('{0}') ".format(urlToBeAdded)
        # print queryStrng
        # mycursor.execute(queryStrng)
        # conn.commit()

    def addUrlToLocalDatabase(self,urlToBeAdded):
        conn = sqlite3.connect('knowmore.db')
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS knowmorelinks(links varchar)")
        cur.executescript("INSERT into knowmorelinks VALUES('"+str(urlToBeAdded)+"')")
        conn.commit()
        print("Inserted")
        conn.close()

    def prepareToLoadUrl(self, urlToBeLoaded):
        if(urlToBeLoaded==None or urlToBeLoaded==""):
            return
        else:
            # self.webwnd.loadFinished.connect(self.waitToLoad)
            #
            # self.webwnd.load(QtCore.QUrl(urlToBeLoaded))
            # self.webwnd.show()
            self.webwnd.loadCustumUrl(urlToBeLoaded)
            QtCore.QObject.connect(self, QtCore.SIGNAL('hideCurrentUrl'), self.parent.openLoadUrl)
            print "Url Status : ", self.status

    def waitToLoad(self):
        # self.timer.timeout.connect(self.timeFinished)
        # self.timer.start(10000)
        self.parent.InitialiseCaptchaManager()

    def nextButtonClicked(self):
        self.parent.is_finished = True
        self.hideLinkButton.setEnabled(False)
        # self.changeStatus()
        # self.timer.stop()

    def hideBtnConnect(self):
        # print ("Hide Frame Button Clicked!")
        # self.HideBtnClsObj = HideBtnClass(self.scanStartThreadObj)
        # self.emailsVal = int(self.parent.leftpanelUserInfo.emailsValue.text())
        # print "Read Email Count : ", self.emailsVal
        # settings = QtWebKit.QWebSettings.globalSettings()
        # settings.setAttribute(QtWebKit.QWebSettings.AutoLoadImages,True)
        # self.webwnd.globalsettings().setAttribute(QtWebKit.QWebSettings.AutoLoadImages,True)
        # self.markEmailRead()
        tabCount = self.parent.uiGraphicsTabWidget.count()
        print "Tabs :" + str(tabCount)
        if(tabCount >= 12):
            mailBodybox = QtGui.QMessageBox()
            mailBodybox.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(':/resources/Icon.png')))
            mailBodybox.setWindowTitle("Information")
            mailBodybox.setText('Maximum Tab Limit Reached!')
            mailBodybox.setStandardButtons(QtGui.QMessageBox.Ok)
            mailBodybox.exec_()
            return
        if Q.is_empty():
            self.hideLinkButton.setEnabled(True)
        else:
            # from PyQt4 import Qt
            # self.cache_id = str(self.parent.leftpanelUserInfo.emailVal)
            # self.cache = Qt.QNetworkDiskCache()
            # self.cache.setCacheDirectory('cache_wnd_\\'+self.cache_id)
            #
            # self.webwnd.page().networkAccessManager().setCache(self.cache)

            self.parent.leftpanelUserInfo.emit(QtCore.SIGNAL("updateEmailCount"))
            self.emit(QtCore.SIGNAL("hideCurrentUrl"), Q.dequeue())
            self.hideLinkButton.setEnabled(False)
            self.timer = QTimer()
            self.timer.timeout.connect(self.changeStatus)
            self.timer.start(40000)

    def changeStatus(self):
        self.timer.stop()
        self.status = "Dead"
        uid_val = UnreadEmailsList.dequeue()
        DeadEmailsList.enqueue(uid_val)
        # print "Link will now be dead!"
        print "Url Status : ", self.status
        # self.cefInitializer.shutdownCef()
        # self.cefInitializer.Shutdown()
        print "Browser Window Should Be Closed!!!"
        self.webwnd.exitAppWnd()
        # frame = self.webwnd.GetMainFrame()
        # browser = frame.GetBrowser()
        # browser.CloseBrowser(True)
        # print "Process will be stopped"
        # mypath = "cache_wnd_"
        # onlyfolders = [ f for f in listdir(mypath) if not isfile(join(mypath,f)) ]
        # if len(onlyfolders)>0:
        #     foldernumbers = [int(j) for j in onlyfolders]
        #     foldernumbers.sort()
        #     tobdel = str(foldernumbers[0])
        #     shutil.rmtree("cache_wnd_\\"+tobdel)
        # layout = self.layout
        # for i in reversed(range(layout.count())):
        #     wid = layout.itemAt(i).widget()
        #     if(wid !=None):
        #         wid.setParent(None)
        # print "widgets in layout are removed now"
        # shutil.rmtree('cache_wnd')
        # self.parent.emailsReadCount += 1
        # for i in reversed(range(self.layout.count())):
        #     self.layout.itemAt(i).widget().setParent(None)
        # try:
        #     self.markEmailRead()
        # except Exception as ex:
        #     pass

		
    def getUserLoginData(self):
        self.username= str(self.parent.leftpanelUserInfo.usersCombo.currentText())
        self.conn = sqlite3.connect('smartusers.db')
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT password FROM users WHERE username = '"+self.username+"'")
        self.optChangeDataPwd =  self.cur.fetchall()
        self.password = self.optChangeDataPwd[0][0]
        # print "Username should be : " + self.username
        # print "Password should be : " + self.password
        return self.username,self.password


    def markEmailRead(self):
        # print "All Unread Mails UID's"
        # print UnreadEmailsList._data
        latest_email_uid = UnreadEmailsList.dequeue()
        # print "Latest Email UID : " + latest_email_uid

        user,passw =  self.getUserLoginData()
        host = "imap.gmail.com"
        port = 993
        # print "user & pass"+user+passw

        obj = imaplib.IMAP4_SSL(host,port)
        obj.login(user,passw)
        obj.select("INBOX")
        rs,dt = obj.uid('fetch',latest_email_uid,'(RFC822)')
        print "Email has been read"

        # if(self.parent.mail_delete):
        #     self.delete_mail()

    def delete_mail(self):
		try:
			latest_email_uid = UnreadEmailsList.dequeue()
			user,passw = self.getUserLoginData()
			host = "imap.gmail.com"
			port = 993
			obj = imaplib.IMAP4_SSL(host,port)
			obj.login(user,passw)
			obj.select("INBOX")

			obj.store(latest_email_uid,'+FLAGS','\\Deleted')
			obj.expunge()
			print "EMail has been Deleted"
		except Exception as ex:
			pass

    def derefObj(self):
        print "memory should be released"
        # self.webwnd.settings().setAttribute(QtWebKit.QWebSettings.AutoLoadImages,False)

        # self.webwnd = None
        # del self.webwnd

class ScanMan(object):
    '''
    classdocs
    '''
    _user = None
    _connected = False
    connection = None

    def __init__(self, app, userInfo=None):
        '''
        Constructor
        '''
        self._app = app

        self.IMAP_SERVER = 'imap.gmail.com'
        self.IMAP_PORT = 993
        # self.connection = None

        self.mailToBeDeleted = False

        self._totalEmail = 0
        self._targetUrl = ""

    ##Not required in our program it was for sample and you can load the old copy of code f you want to learn
    # its time to keep only required things
    #these commented blocks will be permanently removed after 1st version is released
    #  Adding hastag #TO_BE_REMOVED for easy search later
    #     '''
    #     returns gmail view
    #     '''
    #     def getBrowserPanel(self):
    #         return GmailWebView()
    # -joy

    def getBrowserPanel(self):
        return ScanManWebView()

    '''
    returns the User
    '''

    def getUser(self):
        return self._user

    '''
    returns username
    '''

    def getUsername(self):
        #return self._user.getUsername()
        pass

    '''
    returns password
    '''

    def getPassword(self):
        return self._user.getPassword()

    '''
    sets username of user
    '''

    def setUsername(self, username):
        #self._user.setID(username)
        pass

    '''
    sets the password of user
    '''

    def setPassword(self, password):
        #self._user.setPassword(password)
        pass

    '''
    connect user to his gmail
    '''

    def connectUser(self):
        self.connectoThread = ScanManThread(self._app)
        self.connectoThread.start()


    '''
    #This function is used to fetch out all the links from the mail Body
    def getAllLinksFromMailBody(self,mailBody):
        #use re.findall to get all the links
        links = re.findall('"((http|ftp)s?://.*?)"', mailBody)

        print links

        b = [str(i[0]) for i in links]

        for c in b:
            d=re.search(r'http.*user.*',c)
            if (d==None):
                targetlink=""
            else:
                #This is the link which has to be open in the broswer window
                targetlink=d.group(0)
                print "Target Link is :"+ targetlink+ "\n"
                #Open the link in the browser window
                #self.getBrowserPanel().scanUrl(targetlink)
                self._app.wnd.smartScanWidgets[0].show()
                #This will open the link in the inbuilt browser and waith for 10 minutes to load
                self._app.wnd.smartScanWidgets[0].scanUrl(targetlink)
                time.sleep(600)
    '''

    def on_timer(self):

        if self.second < 59:
            self.second += 1
        else:
            if self.minute < 59:
                self.second = 0
                self.minute += 1
            elif (self.minute == 59) and (self.hour < 24):
                self.hour += 1
                self.minute = 0
                self.second = 0
            else:
                self.timerScan.stop()

        time = "{0}:{1}:{2}".format(self.hour, self.minute, self.second)
        print time

        leftPane = self._app.wnd.leftpanelUserInfo
        leftPane.timeValue.setText(time)

    def tryStartScan(self):
        '''
        self.timerScan.timeout.connect(self.on_timer)
        self.timerScan.start(1000)
        scanLabelInfo().exec_()
        '''
        # self._app.wnd.emit(QtCore.SIGNAL("createCacheDir"))
        Q.empty_q()
        UnreadEmailsList.empty_q()
        print "Inside Scan Man Class"
        if self._app.wnd.currentStatus == 0:
            self._app.wnd.currentStatus = 1
            self.urlopener = UrlOpenerThread(self._app)
        elif self._app.wnd.currentStatus == 2:
            self._app.wnd.currentStatus = 1


class PyGmail:
    def __init__(self):
        self.IMAP_SERVER = 'imap.gmail.com'
        self.IMAP_PORT = 993
        self.M = None
        self.response = None

    def login(self, username, password):
        self.M = imaplib.IMAP4_SSL(self.IMAP_SERVER, self.IMAP_PORT)
        rc, self.response = self.M.login(username, password)
        return rc

    def logout(self):
        self.M.close()
        self.M.logout()

# javaScriptLogin = """
# document.getElementsByName('Email').item(0).value='{email}';
# document.getElementsByName('Passwd').item(0).value='{password}';
# document.getElementsByName('signIn').item(0).click(); void(0);
# """

#script for filling captcha and clicking send would be something like follows:
javaScriptSubmitPressForCaptcha = """
document.getElementByName('Captcha').item(0).value='{solvedCaptcha}';
document.getElementsByName('submit').item(0).click(); void(0);
"""


class ScanManWebView(QWebView):
    def __init__(self, parent=None):
        super(ScanManWebView, self).__init__(parent)
        #self.loggedIn = False  #instead of this we will use url status
        self.urlStatus = 0  # 0 means no action has been taken
        # 2 would be only for captcha case, indicating captcha has been found
        # 3 would be only for captcha case, indicating submit button pressed
        # 4 would apply to both, indicating whatever ad was to be viewed is appearing and Timer needs to start
        # 5 would apply to both, indicating timer has completed and url can be taken off this tab and even the tab can be deleted

    #     def login(self, url, email, password):
    #         """Login to gmail."""
    #         self.url = QtCore.QUrl(url)
    #         self.email = email
    #         self.password = password
    #         self.loadFinished.connect(self._loadFinished)
    #         self.load(self.url)

    def scanUrl(self, url):
        """Login to gmail."""
        self.url = QtCore.QUrl(url)
        # print "Url That is about to load is : " + str(self.url)
        #self.loadFinished.connect(self._loadFinished)
        self.load(self.url)

    def createWindow(self, windowType):
        """Load links in the same web-view."""
        return self

    """
    when url loads, it is important to note wether it needs to reload in case of submit button press of captcha or not
    the timer in captcha cases should begin after second load
    so this function has that intelligence to take decision based on type of url and stage of operation
    """

    def _loadFinished(self):
        if self.urlStatus == 2:
            #please understand this logic:
            #if this loadFinished is getting called from status=2, it means its a captcha case and submit button has been pressed earlier
            self.urlStatus = 3
            #hence we can now start timer for captcha case
            self.urlStatus = 4
            # self.startTimer()

        htmlText = self.getHTMLtextForLoadedUrl()
        captchaImageUrl = self.getCaptchImageUrl(htmlText)
        if captchaImageUrl == '':
            #case of no captcha
            #we can start timer for no captcha case
            self.urlStatus = 4
            # self.startTimer()
        else:
            self.urlStatus = 2
            evaluatedCaptcha = self.get
            jscript = javaScriptSubmitPressForCaptcha.format(solvedCaptcha=evaluatedCaptcha)
            self.page().mainFrame().evaluateJavaScript(jscript)
            #anything written ahead may not evaluate sequentially as page can load in anytime and
            #recursive call will occur
            return

        if self.urlStatus == 4:
            self.loadFinished.disconnect(self._loadFinished)

    """
    ToDo:
    start the timer to tick till  max time after which this whole tab can close gracefully
    """
    # def startTimer(self):
    #     pass

    """
    if the required time has been spent,
    simply hide and mark status as complete
    ToDo:
    link this with timer reaching prescribed time
    """

    def onTimeComplete(self):
        self.urlStatus = 5
        self.hide()


    """
    ToDo:
    returns the evaluated captcha for 2 types of cases:
    1.url is image url, eg.: .jpg/.png etc
    2.url is not image, eg.: .aspx/.asp etc
    returned value is evaluated capptcha as string
    returns None if failed to evaluate given captcha
    """

    def getCaptchaTextFromUrl(self, captchaUrl):
        pass
        #-joy

    """
    ToDo:
    Should return the URL of image that carries captcha if 'textHtml' has captcha image
    Return empty string '' otherwise
    """

    def getCaptchImageUrl(self, textHtml):
        #an algorithm had been written in java version
        #please refer to that to make this function
        #make other helper functions instead of making this a very big function
        originalTextHtml = textHtml
        pass
        return ''
        #-joy

    """
    ToDo:
    this function will return the HTML text for the currently loaded url
    """

    def getHTMLtextForLoadedUrl(self):
        #refer qwebview documentation for writing this function
        #self._loadedurl=loadedUrl
        #captchdecision=self.detectCaptchaFromLoadedUrl(loadedUrl)
        pass
        #-joy
        return

    """
    do nothing on right click right now, will see what we can do later
    """
    '''
    Captcha Detection ALgo will be implemented in the following function
    and will retun true or false boolean value as for captcha deteceted or
    not in the loaded url
    '''

    def detectCaptchaFromLoadedUrl(self, loadedUrl):
        pass

    def contextMenuEvent(self, event):
        pass

        #     def contextMenuEvent(self, event):
        #         """Add a 'Back to GMail' entry."""
        #         menu = self.page().createStandardContextMenu()
        #         menu.addSeparator()
        #         action = menu.addAction('Back to GMail')
        #         @action.triggered.connect
        #         def backToGMail():
        #             self.load(self.url)
        #         menu.exec_(QtGui.QCursor.pos()
