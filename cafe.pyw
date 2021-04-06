
import sys
from datetime import datetime

from PyQt5 import QtCore, QtGui, QtWidgets

from cafe_time_main_ui import Ui_MainWindow
import utils

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__() #Call inherited superclass init method
        
        #self.setWindowFlags(self.windowFlags() | QtCore.Qt.CustomizeWindowHint)
        #self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)
        self.setWindowFlags(QtCore.Qt.Window |
            QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.FramelessWindowHint)
        
        self.gui = Ui_MainWindow()
        self.gui.setupUi(self)
        self.setupSlots()
        self.showFullScreen()
        self.gui.timeCodeEdit.setFocus()
        
        self.current_time_code = '-1' #time code in use
        self.time_left = 0
        
        self.correct_geometry = QtCore.QRect(552, 210, 816, 600)
        self.fullscreen_geometry = QtCore.QRect(0, 0, 1920, 1080)
        
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.countdown)
        self.timer.start(1000) #update every second
        print('Initialised')
        
    def setupSlots(self):
        self.gui.okButton.clicked.connect(self.updateTimeLeft)
        self.gui.timeCodeEdit.returnPressed.connect(self.updateTimeLeft)
        self.gui.logoffButton.clicked.connect(self.logOff)
        print('Slots setup')
        
    def updateTimeLeft(self):
        time_code = self.gui.timeCodeEdit.text()
        self.gui.timeCodeEdit.setText('')
        time_left = utils.check_time_code(time_code)
        if len(time_code) <= 0:
            self.showToastMessage("Code is empty! Enter code!")
        elif time_left > 0 and self.current_time_code != time_code:
            #if new time_code add new time to current time
            utils.update_time_code(self.current_time_code, 0) #invalidate old time code
            if self.time_left > 0:
                #its a subsequent ticket being added to current ticket so remove bonus time
                time_left -= utils.bonus_time
            self.time_left += time_left
            #update new time code to current
            #also check if time code is sold and update that status with date sold if not
            sold = utils.is_ticket_sold(time_code)
            dt = None
            if not sold:
                dt = datetime.now()
                print('updating code date_sold')
            self.current_time_code = time_code
            utils.update_time_code(self.current_time_code, self.time_left, date_sold=dt)
            
            self.showNormal()
            self.showToastMessage('Time added')
        elif self.current_time_code == time_code:
            self.showToastMessage('Code in use!')
        elif time_left == 0:
            self.showToastMessage('Code already used!')
        elif time_left < 0:
            self.showToastMessage('Wrong code!!')
        else:
            self.showToastMessage('Wrong code!!')
        self.gui.timeLeftLabel.setText(self.getTimeLeftString())
        self.gui.timeCodeEdit.setFocus()
    
    def getTimeLeftString(self):
        '''Return formatted string containing time left'''
        s = ''
        hours = self.time_left // 3600
        minutes = (self.time_left % 3600) // 60
        seconds = (self.time_left % 3600) % 60
        if hours > 0:
            if hours > 1:
                s = 'TIME LEFT: {:} hrs {:} mins {:0>2d}'.format(hours, minutes, seconds)
            else:
                s = 'TIME LEFT: {:} hr {:} mins {:0>2d}'.format(hours, minutes, seconds)
        else:
            if minutes > 1:
                s = 'TIME LEFT:  {:} mins {:0>2d}'.format(minutes, seconds)
            else:
                s = 'TIME LEFT:  {:} min {:0>2d}'.format(minutes, seconds)
        return s
        
    def logOff(self):
        utils.update_time_code(self.current_time_code, self.time_left)
        self.current_time_code = '-1'
        self.time_left = 0
        self.showToastMessage('Logged off')
        print('logged off')
        self.gui.timeCodeEdit.setFocus()
    
    
    def showToastMessage(self, msg):
        self.gui.messagesLabel.setText(msg)
        self.timer.singleShot(3000, lambda: self.gui.messagesLabel.setText(''))
    
    def closeEvent(self, event):
        utils.update_time_code(self.current_time_code, self.time_left)
        #ignore close event
        event.ignore()
    
    _count = 60
    def countdown(self):
        #countdown as long as self.time is greater than 0
        print(self.geometry())
        if self.time_left > 0:
            self.time_left -= 1
            if self.windowState() == QtCore.Qt.WindowFullScreen:
                self.showNormal()
                print('Normal window shown')
            else:
                #fix geometry if not centered and sized properly
                if self.geometry() != self.correct_geometry:
                    self.setGeometry(self.correct_geometry)
                    print('normal window Geometry corrected')
        else:
            if not self.isActiveWindow():
                utils.close_foreground_app()
                print('Closing foreground app')
            if self.windowState() != QtCore.Qt.WindowFullScreen:
                def func():
                    self.showFullScreen()
                    self.logOff()
                self.timer.singleShot(450, func)
                print('Changing to fullscreen')
            else:
                #fix geometry if fullscreen and sized properly
                if self.geometry() != self.fullscreen_geometry:
                    self.setGeometry(self.fullscreen_geometry)
                    print('fullscreen window Geometry corrected')
                
        MyWindow._count -= 1
        self.gui.timeLeftLabel.setText(self.getTimeLeftString())
        if (MyWindow._count <= 0):
            MyWindow._count = 60
            #update database
            utils.update_time_code(self.current_time_code, self.time_left)
            print('Database updated')
            
        

app = QtWidgets.QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()
