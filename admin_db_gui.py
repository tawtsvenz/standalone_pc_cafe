
import sys, os
from PyQt5 import QtCore, QtGui, QtWidgets, QtSql
from PyQt5.QtCore import Qt

import tawsql
from db_manager import Ui_DBManager

script_loc = os.path.abspath(os.path.dirname(__file__))
print(script_loc)
os.chdir(script_loc)


class DBModel(QtSql.QSqlTableModel):
    
    def __init__(self):
        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('data.db')
    
        super().__init__()
       
        self.setTable('codes_table')
        self.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.select()
        
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.gui = Ui_DBManager()
        self.gui.setupUi(self)
        
        self.table = self.gui.tableView
        
        self.model = DBModel()
        self.table.setModel(self.model)
        
        
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()