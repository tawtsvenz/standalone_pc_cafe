# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'db_manager.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DBManager(object):
    def setupUi(self, DBManager):
        DBManager.setObjectName("DBManager")
        DBManager.resize(800, 600)
        self.horizontalLayoutWidget = QtWidgets.QWidget(DBManager)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 801, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.tableView = QtWidgets.QTableView(DBManager)
        self.tableView.setGeometry(QtCore.QRect(0, 40, 800, 500))
        self.tableView.setObjectName("tableView")

        self.retranslateUi(DBManager)
        QtCore.QMetaObject.connectSlotsByName(DBManager)

    def retranslateUi(self, DBManager):
        _translate = QtCore.QCoreApplication.translate
        DBManager.setWindowTitle(_translate("DBManager", "Form"))
        self.label.setText(_translate("DBManager", "TextLabel"))