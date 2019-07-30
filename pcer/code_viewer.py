import sys
import os
import yaml
from PyQt5.QtWidgets import (QWidget, QPushButton,
     QApplication, QDesktopWidget, QListWidget, QTextEdit)
from PyQt5.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat, QFontMetrics
from PyQt5 import QtCore
from PyQt5.QtCore import QFile, QRegExp, Qt
from pcer_window import PcerWindow


class MyQTextEdit(QTextEdit):
    scrollbar_displacement = 0

    def __init__(self, parent=None):
        super(MyQTextEdit, self).__init__(parent)

    def scrollContentsBy(self, dx, dy):
        super(MyQTextEdit, self).scrollContentsBy(dx, dy)
        self.scrollbar_displacement += dy
        print(self.scrollbar_displacement)

class CodeViewer(PcerWindow):

    back = QtCore.pyqtSignal()

    def __init__(self, experiment):
        super(CodeViewer, self).__init__(experiment)

    def initUI(self):
        self.vbox.addStretch(1) # => necessary to send the status bar at the bottom
        self.heightWithStatusBar = self.height - 40
        self.listWidth = (self.width / 4) * 1
        self.editorWidth = (self.width / 4) * 3
        self.backButtonWidth = self.listWidth / 2
        self.setWindowTitle('Code Viewer')
        self.setupFileList()
        self.setupBackButton()
        self.setupEditor()
        self.code_path = self.experiment.getSourceCodePath()

    def setupFileList(self):
        listWidget = QListWidget(self)
        listWidget.move(0, 0)
        listWidget.resize(self.listWidth, self.heightWithStatusBar)
        listWidget.addItems(self.experiment.getExperimentalSystemFilenames())
        listWidget.itemClicked.connect(self.onListItemClick)

    def setupBackButton(self):
        backButton = QPushButton("Back", self)
        backButton.clicked.connect(self.onBackButtonClick)
        backButton.move(50, self.heightWithStatusBar - 50)
        backButton.resize(self.listWidth - 100, 25)

    def setupEditor(self):
        font = QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(10)

        self.editor = MyQTextEdit(self)
        self.editor.setFont(font)
        self.editor.move(self.listWidth, 0)
        self.editor.resize(self.editorWidth, self.heightWithStatusBar)
        self.highlighter = Highlighter(self.editor.document()) 

    def onListItemClick(self, l):
        self.openFile(os.path.join(self.code_path, l.text()))

    def onBackButtonClick(self):
        print("TaskForm.onBackButtonClick")
        self.back.emit()

    def openFile(self, path=None):
        if not path:
            path, _ = QFileDialog.getOpenFileName(self, "Open File", '',
                    "C++ Files (*.cpp *.h)")
        print(path)
        if path:
            inFile = QFile(path)
            if inFile.open(QFile.ReadOnly | QFile.Text):
                text = inFile.readAll()

                try:
                    # Python v3.
                    text = str(text, encoding='ascii')
                except TypeError:
                    # Python v2.
                    text = str(text)

                self.editor.setPlainText(text)
                self.editor.verticalScrollBar().setValue(120) # to jump the scroll to a saved position
    

class Highlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(Highlighter, self).__init__(parent)

        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(Qt.darkBlue)
        keywordFormat.setFontWeight(QFont.Bold)

        keywordPatterns = ["\\babstract\\b", "\\bcontinue\\b", "\\bfor\\b",
                "\\bnew\\b", "\\bswitch\\b", "\\bassert\\b", "\\bdefault\\b",
                "\\bgoto\\b", "\\bpackage\\b", "\\bsynchronized\\b", "\\bboolean\\b",
                "\\bdo\\b", "\\bif\\b", "\\bprivate\\b", "\\bthis\\b",
                "\\bbreak\\b", "\\bdouble\\b", "\\bimplements\\b", "\\bprotected\\b",
                "\\bthrow\\b", "\\bbyte\\b", "\\belse\\b", "\\bimport\\b",
                "\\bpublic\\b", "\\bthrows\\b", "\\bcase\\b", "\\benum\\b",
                "\\bintanceof\\b", "\\breturn\\b", "\\btransient\\b", "\\bcatch\\b",
                "\\bextends\\b", "\\bint\\b", "\\bshort\\b", "\\btry\\b",
                "\\bchar\\b", "\\bfinal\\b", "\\binterface\\b", "\\bstatic\\b",
                "\\bvoid\\b", "\\bclass\\b", "\\bfinally\\b", "\\blong\\b",
                "\\bstrictfp\\b", "\\bvolatile\\b", "\\bconst\\b", "\\bfloat\\b",
                "\\bnative\\b", "\\bsuper\\b", "\\bwhile\\b", "\\btrue\\b"
                "\\bfalse\\b", "\\bnull\\b"]

        self.highlightingRules = [(QRegExp(pattern), keywordFormat)
                for pattern in keywordPatterns]

        classFormat = QTextCharFormat()
        classFormat.setFontWeight(QFont.Bold)
        classFormat.setForeground(Qt.darkMagenta)
        self.highlightingRules.append((QRegExp("\\bQ[A-Za-z]+\\b"),
                classFormat))

        singleLineCommentFormat = QTextCharFormat()
        singleLineCommentFormat.setForeground(Qt.red)
        self.highlightingRules.append((QRegExp("//[^\n]*"),
                singleLineCommentFormat))

        self.multiLineCommentFormat = QTextCharFormat()
        self.multiLineCommentFormat.setForeground(Qt.red)

        quotationFormat = QTextCharFormat()
        quotationFormat.setForeground(Qt.darkGreen)
        self.highlightingRules.append((QRegExp("\".*\""), quotationFormat))

        functionFormat = QTextCharFormat()
        functionFormat.setFontItalic(True)
        functionFormat.setForeground(Qt.blue)
        self.highlightingRules.append((QRegExp("\\b[A-Za-z0-9_]+(?=\\()"),
                functionFormat))

        self.commentStartExpression = QRegExp("/\\*")
        self.commentEndExpression = QRegExp("\\*/")

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        startIndex = 0
        if self.previousBlockState() != 1:
            startIndex = self.commentStartExpression.indexIn(text)

        while startIndex >= 0:
            endIndex = self.commentEndExpression.indexIn(text, startIndex)

            if endIndex == -1:
                self.setCurrentBlockState(1)
                commentLength = len(text) - startIndex
            else:
                commentLength = endIndex - startIndex + self.commentEndExpression.matchedLength()

            self.setFormat(startIndex, commentLength,
                    self.multiLineCommentFormat)
            startIndex = self.commentStartExpression.indexIn(text,
                    startIndex + commentLength);
