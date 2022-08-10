import sys
import re
from PyQt5.QtWidgets import QMainWindow,QApplication
from PyQt5 import uic
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtGui import *
def do_find_highlight(self, pattern):
    cursor = self.editor.textCursor()
    # Setup the desired format for matches
    format = QTextCharFormat()
    format.setBackground(QBrush(QColor("blue")))

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