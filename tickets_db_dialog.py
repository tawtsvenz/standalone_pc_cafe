# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tickets_db_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 30, 401, 21))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ticketNumLabel = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.ticketNumLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.ticketNumLabel.setObjectName("ticketNumLabel")
        self.horizontalLayout.addWidget(self.ticketNumLabel)
        self.timeLeftLabel = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.timeLeftLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.timeLeftLabel.setObjectName("timeLeftLabel")
        self.horizontalLayout.addWidget(self.timeLeftLabel)
        self.initialTimeLabel = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.initialTimeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.initialTimeLabel.setObjectName("initialTimeLabel")
        self.horizontalLayout.addWidget(self.initialTimeLabel)
        self.dateCreatedLabel = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.dateCreatedLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.dateCreatedLabel.setObjectName("dateCreatedLabel")
        self.horizontalLayout.addWidget(self.dateCreatedLabel)
        self.dateBoughtLabel = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.dateBoughtLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.dateBoughtLabel.setObjectName("dateBoughtLabel")
        self.horizontalLayout.addWidget(self.dateBoughtLabel)
        self.scrollArea = QtWidgets.QScrollArea(Dialog)
        self.scrollArea.setGeometry(QtCore.QRect(0, 50, 401, 191))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 399, 189))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Tickets Database"))
        self.ticketNumLabel.setText(_translate("Dialog", "Ticket No."))
        self.timeLeftLabel.setText(_translate("Dialog", "Time Left"))
        self.initialTimeLabel.setText(_translate("Dialog", "Initial Time"))
        self.dateCreatedLabel.setText(_translate("Dialog", "Date Created"))
        self.dateBoughtLabel.setText(_translate("Dialog", "Date Bought"))
