#this application will contain the pop up windows for configuring the editor

import sys
import re
from PyQt5.QtWidgets import QMainWindow,QApplication
from PyQt5 import uic
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
class mainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow,self).__init__()
        loadUi("Editor.ui",self)
        self.setWindowTitle('Notepad')
        #this will basically control the zoom of the screen
        self.editor.setFont(QFont('Aerial',10))
        # instantiating all the classed we will be needing for the popUp windows
        self.findWin = Find(self)
        self.findWin.pushButton.clicked.connect(self.get_Findval)
        self.find_allWin = FindAll(self)
        self.find_allWin.pushButton.clicked.connect(self.get_FindAllval)
        #this widget is giving an error so fix this as well in the final version
        self.replace_win = Replace(self)
        self.replace_win.replaceButton.clicked.connect(self.get_replaceValue1)
        self.replace_win.replaceAllButton.clicked.connect(self.get_replaceValue2)
        self.replace_win.cancelButton.clicked.connect(self.get_replaceValue3)
        self.page_setupWin = PageSetup(self)
        self.help_win = getHelp()

        #these are the hash values that will be used to find whether there are any changes or not
        self.newHash = 0
        self.oldHash = 0
        self.text=""
        test_text=""
        #these are the words that will be used to find values:
        self.findWord=""
        self.replaceWord=""

        #these will basically control the coloring of the canvas
        self.text_Color=""
        self.background_Color=""


        #handling the custom actions in here
        #font action
        self.fileName=" "#this will be set when the user saves the file in local storage
        self.fontMenu.triggered.connect(self.fontAction)#since this is an action therefore listening to the triggered event

        #background color action
        self.bgColorAction.triggered.connect(self.bgColor)

        #text color action
        self.textColorAction.triggered.connect(self.textColor)

        #rest of the actions needs to be handled differently since custom widgets are used in this

        #find action
        self.FindAction.triggered.connect(self.findHandler)

        #find all action

        self.findAllAction.triggered.connect(self.findAllHandler)
        #find prev action
        self.findPrecAction.triggered.connect(self.findPrevAction)
        #find next action
        self.FindNextAction.triggered.connect(self.findNextAction)

        #replace action
        self.ReplaceAction.triggered.connect(self.replaceAction)

        #these are all the file Actions

         #new file action
        self.NewAction.triggered.connect(self.newHandler)
         #new window action
        self.NewWindowAction.triggered.connect(self.newWindowHandler)
        # open file action
        self.OpenAction.triggered.connect(self.openHandler)
        #save file action
        self.SaveAction.triggered.connect(self.saveHandler)
        #save as file action
        self.SaveAsAction.triggered.connect(self.saveAsHandler)
        #print text action
        self.PrintAction.triggered.connect(self.printHandler)
        # page setup action
        self.SetupAction.triggered.connect(self.setupHandler)
        #Toggle Action
        self.ToggleAction.triggered.connect(self.toggleHandler)
        #exit action
        self.ExitAction.triggered.connect(self.exitAction)


        #these are all the view action

        #zoom in action
        self.ZoomInAction.triggered.connect(self.zoomInHandler)
        #zoom out action
        self.ZoomOutAction.triggered.connect(self.zoomOutHandler)

        #these are all the theme actions


        #this is the help action
        self.helpAction.triggered.connect(self.giveHelp)

        #these will control the theme of the text editor
        self.darkTheme1.triggered.connect(self.darkTheme1_controller)
        self.darkTheme2.triggered.connect(self.darkTheme2_controller)
        self.darkTheme3.triggered.connect(self.darkTheme3_controller)
        self.darkTheme4.triggered.connect(self.darkTheme4_controller)
        self.lightTheme1.triggered.connect(self.lightTheme1_controller)
        self.lightTheme2.triggered.connect(self.lightTheme2_controller)
        self.lightTheme3.triggered.connect(self.lightTheme3_controller)
        self.lightTheme4.triggered.connect(self.lightTheme4_controller)
        #these are all the file action handlers
          #this functionality is addded to bring back the screen to normal configuration if the user Affirm witht the changes
        #these variables will be used to set the margin for QText edit
        self.topPadding=0
        self.leftPadding=0
        self.bottomPadding=0
        self.rightPadding=0
        self.editor.setStyleSheet(f'padding-top:{self.topPadding}px;padding-left:{self.leftPadding}px;padding-bottom:{self.bottomPadding}px;padding-right:{self.rightPadding}px')
        self.page_setupWin.pushButton.clicked.connect(self.geometryChanges)
        self.page_setupWin.pushButton_2.clicked.connect(lambda x:self.page_setupWin.close())
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_F5:
            self.affirm()

    def wheelEvent(self, event):
        try:
            delta=event.angleDelta () / 120
            if delta.y() == 1:
                self.zoomInHandler()
            elif delta.y() == -1:
                self.zoomOutHandler()
        except Exception as e:
            print(e)


    def affirm(self):
        text=self.editor.toPlainText()
        self.editor.setText(text)

    #this function will open a new text file in the same menu and therefore erasing the previous tect ask the user to save the file before
    #erasing the text


    # this function will detect whether there are any changes made to the text or not
    # by comparing the hashes of old and new text



    def changes(self):
        self.newHash=self.getHash(self.editor.toPlainText())
        if self.newHash == self.oldHash:
            return True
        else:
            self.oldHash=self.newHash
            return False

    def getHash(self,text:str):
        hash = sha512(text.encode())
        return hash.hexdigest()
    #this function will display a warning in case there are any unchaned changes in the text file
    def displayWarning(self):
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Warning)
        self.msg.setText("Unsaved Changes")
        self.msg.setInformativeText("You have some unsaved changes in your file please save them before closing the file or else the info will be lost")
        self.msg.setWindowTitle("Unsaved Changes")
        self.msg.setDetailedText("Save the file before closing")
        self.msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        self.msg.buttonClicked.connect(self.msgbtnHandler)
        self.msg.show()

    def msgbtnHandler(self,val):
        print(f'This is the response value {val.text()}')

    # this function will open the new window and the original window will be unchanged
    def newHandler(self):
        try:

            # if there are some unsaved changes display warning
            if self.changes() == False:
                self.displayWarning()

            # else clear the text from the editor
            elif self.changes() == True:
                self.editor.clear()
        except Exception as e:
            print(e)


    def newWindowHandler(self):
        try:
            print('Will open a new window')
        except Exception as e:
            print(e)

    #this function will open a text file from the local storage
    def openHandler(self):
        try:
            filename = QFileDialog.getOpenFileName(self, 'Open File', 'All Files (*.txt*)')
            if filename[0]:
                f = open(filename[0], 'r')
                with f:
                    data = f.read()
                    self.editor.setText(data)
        except Exception as e:
            print(e)

    #using window modified for saving purpose
    #this will save the changes made to the file
    def saveHandler(self):
        try:
            with open(r'{}'.format(fileName),mode="w")as f:
                text = self.editor.toPlainText()
                f.write(text)
                f.close()
                self.fileName=fileName
        except Exception as e:
            print(e)

    #this will save the text file in the local storage
    def saveAsHandler(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "All Files (*);;Text Files (*.txt)")
        try:
            with open(r'{}'.format(fileName),mode="w")as f:
                text = self.editor.toPlainText()
                f.write(text)
                f.close()
                self.fileName=fileName
        except Exception as e:
            print(e)
    #this will open the print GUI integrate this in case bahut jyada free
    def printHandler(self):
        pass
    #this will handle the page setup handler
    def setupHandler(self):
        try:
            self.clearFocus()
            self.page_setupWin.show()


        except Exception as e:
            print(e)
    def geometryChanges(self):
        try:
            self.leftPadding = self.page_setupWin.lineEdit.text()
            self.rightPadding = self.page_setupWin.lineEdit_2.text()
            self.topPadding = self.page_setupWin.lineEdit_3.text()
            self.bottomPadding = self.page_setupWin.lineEdit_4.text()
            self.editor.setStyleSheet(
                f'padding-top:{self.topPadding}px;padding-left:{self.leftPadding}px;padding-bottom:{self.bottomPadding}px;padding-right:{self.rightPadding}px')
            self.page_setupWin.close()
        except Exception as e:
            print(e)
    def toggleHandler(self):
        pass

    #this will close the application if there are any unsaved changes ask the user to save them before closing the window
    def exitAction(self):
        try:
            exitApp()
        except Exception as e:
            print('unable to close the application!')
            print(e)


    #these are the theme handlers

    def darkHandler(self):
        pass
    def lightHandler(self):
        pass

    #these are the view handler

    def zoomInHandler(self):
        try:
            self.editor.zoomIn(1)
        except Exception as e:
            print(e)
    def zoomOutHandler(self):
        try:
            self.editor.zoomOut(1)
        except Exception as e:
            print(e)



    def fontAction(self):
        try:
            font, bOk = QFontDialog.getFont()
            if bOk:
                try:
                    self.editor.setFont(font)
                except Exception as e:
                    print(e)

        except Exception as e:
            print(e)

#this will change the backgriound color
    def bgColor(self):
        try:
            color = QColorDialog.getColor()
            name= color.name()
            self.background_Color=name
            self.setStyleSheet('background-color: ' + self.background_Color + ';color: ' + self.text_Color)
            self.editor.setStyleSheet('background-color: ' + self.background_Color + ';color: ' + self.text_Color)
            color = QColor(name)#this will basically create a QColor object
            #print(f'the background color is {name} ')

        except Exception as e:
            print(e)

#this will change the text color
    def textColor(self):
        try:
            color = QColorDialog.getColor()
            name = color.name()
            print(name)
            self.text_Color=name
            self.setStyleSheet('background-color: ' + self.background_Color + ';color: ' + self.text_Color)
            self.editor.setStyleSheet('background-color: ' + self.background_Color + ';color: ' + self.text_Color)
            color = QColor(name)#this will basically create a QColor object
           # print(f'the background color is {name} ')

        except Exception as e:
            print(e)

   #need to modify the code here since using self freezes both the screen and not using does not show the second screen
    def findHandler(self,checked):
        try:
            self.clearFocus()
            self.findWin.show()


        except Exception as e:
            print(e)

    def findAllHandler(self):
        try:
            self.clearFocus()
            self.find_allWin.show()

        except Exception as e:
            print(e)


    def findPrevAction(self):
        try:
            self.clearFocus()
            self.find_prevWin.show()

        except Exception as e:
            print(e)

    def findNextAction(self):
        try:
            self.clearFocus()
            self.find_nextWin.show()
        except Exception as e:
            print(e)

    def replaceAction(self):
        try:
            self.clearFocus()
            self.replace_win.show()
        except Exception as e:
            print(e)


    def giveHelp(self):
        try:
            self.clearFocus()
            self.help_win.show()
        except Exception as e:
            print(e)

    #these functions will control the theme of the canvas



    def darkTheme1_controller(self):
        try:
            self.setStyleSheet('background-color: #00007f;color:#ffffff')
            self.editor.setStyleSheet('background-color: #00007f;color:#ffffff')
        except Exception as e:
            print(e)

    def darkTheme2_controller(self):
        try:
            self.setStyleSheet('background-color:#c8096f;color:#00007f')
            self.editor.setStyleSheet('background-color:#c8096f;color:#00007f')
        except Exception as e:
            print(e)
    def darkTheme3_controller(self):
        try:
            self.setStyleSheet('background-color:#00007f;color:#ff007f')
            self.editor.setStyleSheet('background-color:#00007f;color:#ff007f')
        except Exception as e:
            print(e)
    def darkTheme4_controller(self):
        try:
            self.setStyleSheet('background-color:#000000;color:#1505c8')
            self.editor.setStyleSheet('background-color:#000000;color:#1505c8')
        except Exception as e:
            print(e)
    def lightTheme1_controller(self):
        try:
            self.setStyleSheet('background-color:#ffaa7f;color:#00007f')
            self.editor.setStyleSheet('background-color:#ffaa7f;color:#00007f')
        except Exception as e:
            print(e)
    def lightTheme2_controller(self):
        try:
            self.setStyleSheet('background-color:#ff557f;color:#00ffff')
            self.editor.setStyleSheet('background-color:#ff557f;color:#00ffff')
        except Exception as e:
            print(e)
    def lightTheme3_controller(self):
        try:
            self.setStyleSheet('background-color:#55ff7f;color:#ff0000')
            self.editor.setStyleSheet('background-color:#55ff7f;color:#ff0000')
        except Exception as e:
            print(e)
    def lightTheme4_controller(self):
        try:
            self.setStyleSheet('background-color:#ffff7f;color:#ff007f')
            self.editor.setStyleSheet('background-color:#ffff7f;color:#ff007f')
        except Exception as e:
            print(e)


    #need to learn Q text cursor for this functionality and then add this functionality for
    #all the functions
    def get_Findval(self):
        try:
            self.findWord=self.findWin.lineEdit.text()
            cursor = self.editor.textCursor()
            # Setup the desired format for matches
            format = QTextCharFormat()
            format.setBackground(QBrush(QColor("blue")))
            format.setForeground(QBrush(QColor("white")))

            # Setup the regex engine
            re = QRegularExpression(self.findWord)
            i = re.globalMatch(self.editor.toPlainText())  # QRegularExpressionMatchIterator

            # iterate through all the matches and highlight
            while i.hasNext():
                match = i.next()  # QRegularExpressionMatch

                # Select the matched text and apply the desired format
                cursor.setPosition(match.capturedStart(), QTextCursor.MoveAnchor)
                cursor.setPosition(match.capturedEnd(), QTextCursor.KeepAnchor)
                cursor.mergeCharFormat(format)
                break
        except Exception as e:
            print(e)

    #these are bacically the util functions that willr return theh modified text or simply the indexes of the words that need to be modified
    #this is the approach that will be followed we will be working with the the index of words will be returned and then usning the cursor we
    #will be implementing the changes

    #this function will simply return a tupple (start,end)
    def find_valUtil(self,text:str,sentence:str):
        pass

    def get_FinNextdval(self):
        try:
            self.findWord=self.find_prevWin.lineEdit.text()
            cursor = self.editor.textCursor()
            # Setup the desired format for matches
            format = QTextCharFormat()
            format.setBackground(QBrush(QColor("blue")))
            format.setForeground(QBrush(QColor("white")))

            # Setup the regex engine
            re = QRegularExpression(self.findWord)
            i = re.globalMatch(self.editor.toPlainText())  # QRegularExpressionMatchIterator
            match = i[1]  # QRegularExpressionMatch
            cursor.setPosition(match.capturedStart(), QTextCursor.MoveAnchor)
            cursor.setPosition(match.capturedEnd(), QTextCursor.KeepAnchor)
            cursor.mergeCharFormat(format)

        except Exception as e:
            print(e)


    def get_FindAllval(self):
        try:
            self.findWord=self.find_allWin.lineEdit.text()
            self.do_find_highlight(self.findWord)

        except Exception as e:
            print(e)

    def get_replaceValue1(self):
        try:
            cursor=self.editor.textCursor()
            self.findWord = self.replace_win.findEdit.text()
            self.replaceWord = self.replace_win.replaceEdit.text()
            self.text = self.editor.toPlainText()
            new_string = str(self.text)
            try:
                new_string = new_string.replace(self.findWord, self.replaceWord, 1)
                self.editor.setText(new_string)
                self.do_find_highlight(self.replaceWord)
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)
# this will replace all the instance of the word,sane logic just get the count of word first and then replace them all
    def get_replaceValue2(self):
        try:
            self.findWord = self.replace_win.findEdit.text()
            self.replaceWord = self.replace_win.replaceEdit.text()
            self.text = self.editor.toPlainText()
            new_string = str(self.text)
            count=self.find_frequency(self.findWord,self.text)
            try:
                new_string = new_string.replace(self.findWord, self.replaceWord, count)
                self.editor.setText(new_string)
                self.do_find_highlight(self.replaceWord)
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)

    def find_frequency(self,find:str,text:str):
        #this function will have a bacic assumption that all the words are space serprated
        count=0
        words = text.split(' ')
        for word in words:
            if word == find:
                count=count+1
        return count

    def do_find_highlight(self, pattern):
        cursor = self.editor.textCursor()
        # Setup the desired format for matches
        format = QTextCharFormat()
        format.setBackground(QBrush(QColor("blue")))
        format.setForeground(QBrush(QColor("white")))

        # Setup the regex engine
        re = QRegularExpression(pattern)
        i = re.globalMatch(self.editor.toPlainText())  # QRegularExpressionMatchIterator

        # iterate through all the matches and highlight
        while i.hasNext():
            match = i.next()  # QRegularExpressionMatch

            # Select the matched text and apply the desired format
            cursor.setPosition(match.capturedStart(), QTextCursor.MoveAnchor)
            cursor.setPosition(match.capturedEnd(), QTextCursor.KeepAnchor)
            cursor.mergeCharFormat(format)
    def get_replaceValue3(self):
        self.replace_win.close()




class getHelp(QWidget):
    def __init__(self):
        super().__init__()

        self.im = QPixmap("./gorilla.png")
        self.label = QLabel()
        self.label.setPixmap(self.im)
        self.grid = QGridLayout()
        self.grid.addWidget(self.label, 1, 1)
        self.setLayout(self.grid)

        self.setGeometry(50, 50, 320, 200)
        self.setWindowTitle("PyQT show image")


class Find(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)
        loadUi('find.ui',self)

class FindAll(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)
        loadUi('findAll.ui',self)


class PageSetup(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)
        loadUi('pageSetup.ui',self)

class Replace(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)
        loadUi('replace.ui',self)


app=QApplication(sys.argv)
global dlgMain
dlgMain= mainWindow()
dlgMain.show()
def exitApp():
    sys.exit(app.exec_())
try:
    sys.exit(app.exec_())
except:
    print("Exiting the app")