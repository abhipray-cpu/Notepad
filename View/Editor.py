import sys
from PyQt5.QtWidgets import QMainWindow,QApplication
from PyQt5 import uic
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtGui import *
from hashlib import *


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("Editor.ui", self)
        self.editor.setFont(QFont('Aerial', 10))
        # these are the hash values that will be used to find whether there are any changes or not
        self.newHash = 0
        self.oldHash = 0

        # these will basically control the coloring of the canvas
        self.text_Color = ""
        self.background_Color = ""

        # handling the custom actions in here
        # font action
        self.fileName = " "  # this will be set when the user saves the file in local storage
        self.fontMenu.triggered.connect(
            self.fontAction)  # since this is an action therefore listening to the triggered event

        # background color action
        self.bgColorAction.triggered.connect(self.bgColor)

        # text color action
        self.textColorAction.triggered.connect(self.textColor)

        # rest of the actions needs to be handled differently since custom widgets are used in this

        # find action
        self.FindAction.triggered.connect(self.findHandler)

        # find all action

        self.findAllAction.triggered.connect(self.findAllHandler)
        # find prev action
        self.findPrecAction.triggered.connect(self.findPrevAction)
        # find next action
        self.FindNextAction.triggered.connect(self.findNextAction)

        # replace action
        self.ReplaceAction.triggered.connect(self.replaceAction)

        # these are all the file Actions

        # new file action
        self.NewAction.triggered.connect(self.newHandler)
        # new window action
        self.NewWindowAction.triggered.connect(self.newWindowHandler)
        # open file action
        self.OpenAction.triggered.connect(self.openHandler)
        # save file action
        self.SaveAction.triggered.connect(self.saveHandler)
        # save as file action
        self.SaveAsAction.triggered.connect(self.saveAsHandler)
        # print text action
        self.PrintAction.triggered.connect(self.printHandler)
        # page setup action
        self.SetupAction.triggered.connect(self.setupHandler)
        # Toggle Action
        self.ToggleAction.triggered.connect(self.toggleHandler)
        # exit action
        self.ExitAction.triggered.connect(self.exitAction)

        # these are all the view action

        # zoom in action
        self.ZoomInAction.triggered.connect(self.zoomInHandler)
        # zoom out action
        self.ZoomOutAction.triggered.connect(self.zoomOutHandler)

        # these are all the theme actions

        # this is the help action
        self.helpAction.triggered.connect(self.giveHelp)

        # these will control the theme of the text editor
        self.darkTheme1.triggered.connect(self.darkTheme1_controller)
        self.darkTheme2.triggered.connect(self.darkTheme2_controller)
        self.darkTheme3.triggered.connect(self.darkTheme3_controller)
        self.darkTheme4.triggered.connect(self.darkTheme4_controller)
        self.lightTheme1.triggered.connect(self.lightTheme1_controller)
        self.lightTheme2.triggered.connect(self.lightTheme2_controller)
        self.lightTheme3.triggered.connect(self.lightTheme3_controller)
        self.lightTheme4.triggered.connect(self.lightTheme4_controller)
        # these are all the file action handlers

    # this function will open a new text file in the same menu and therefore erasing the previous tect ask the user to save the file before
    # erasing the text

    # this function will detect whether there are any changes made to the text or not
    # by comparing the hashes of old and new text



if __name__ == '__main__':
     app = QApplication([])
     window = MainWindow()
     window.show()
     sys.exit(app.exec_())