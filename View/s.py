import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from PyQt5.QtWidgets import QMainWindow,QApplication
from PyQt5 import uic
from PyQt5.uic import loadUi

from PyQt5 import QtGui
from PyQt5.QtGui import *
from hashlib import *
import hashlib


class MainWindow(QMainWindow):
     def __init__(self):
         super(MainWindow, self).__init__()
         self.resize(400, 300)

         # Button
         self.button = QPushButton(self)
         self.button.setGeometry(0, 0, 400, 300)
         self.button.setText('Main Window')
         self.button.setStyleSheet('font-size:40px')

         # Sub Window
         self.sub_window = SubWindow()

         # Button Event
         self.button.clicked.connect(self.sub_window.show)


class SubWindow(QDialog):
     def __init__(self):
         super(SubWindow, self).__init__()
         self.resize(400, 300)
         loadUi('find.ui', self)



if __name__ == '__main__':
     app = QApplication([])
     window = MainWindow()
     window.show()
     sys.exit(app.exec_())