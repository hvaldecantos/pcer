import sys
import os
import yaml
from PyQt5.QtWidgets import (QWidget, QPushButton,
     QApplication, QDesktopWidget, QListWidget, QTextEdit)
from PyQt5.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat, QFontMetrics, QFontInfo
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
        config = yaml.load(open("config.yml"), Loader = yaml.SafeLoader)
        self.height_in_characters = config['code_viewer']['document']['height_in_characters']
        self.font_pixel_size = config['code_viewer']['document']['font_pixel_size']
        self.margin_pixel_size = config['code_viewer']['document']['margin_pixel_size']
        self.status_bar_height = config['code_viewer']['status_bar_height']
        super(CodeViewer, self).__init__(experiment)

    def initUI(self):
        self.vbox.addStretch(1) # => necessary to send the status bar at the bottom
        self.listWidth = (self.width / 4) * 1       # 1/4 for the side bar
        self.editorWidth = (self.width / 4) * 3     # 3/4 for the document
        self.backButtonWidth = self.listWidth / 2   # back button in the middle of the side bar

        self.setupEditor()

        self.setWindowTitle('Code Viewer')
        self.setupFileList()
        self.setupBackButton()
        self.setFixedSize(self.width, self.editorHeight + self.status_bar_height)
        self.centerOnScreen()

        self.code_path = self.experiment.getSourceCodePath()

    def setupFileList(self):
        listWidget = QListWidget(self)
        listWidget.move(0, 0)
        listWidget.resize(self.listWidth, self.editorHeight)
        listWidget.addItems(self.experiment.getExperimentalSystemFilenames())
        listWidget.itemClicked.connect(self.onListItemClick)

    def setupBackButton(self):
        backButton = QPushButton("Back", self)
        backButton.clicked.connect(self.onBackButtonClick)
        backButton.move(50, self.editorHeight - 50)
        backButton.resize(self.listWidth - 100, 25)

    def setupEditor(self):
        font = QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)

        font.setPixelSize(self.font_pixel_size)

        


        self.editorHeight = self.height_in_characters * QFontMetrics(font).lineSpacing()

        self.editor = MyQTextEdit(self)
        self.editor.setFont(font)
        self.editor.move(self.listWidth, 0)
        self.editor.resize(self.editorWidth, self.editorHeight)
        # self.editor.setStyleSheet("QTextEdit { padding-left:0; padding-top:0; padding-bottom:0; padding-right: 0}");
        self.editor.document().setDocumentMargin(self.margin_pixel_size)
        print("documentMargin(): %f pixels?" % self.editor.document().documentMargin())
        self.editor.setReadOnly(True)

        self.highlighter = Highlighter(self.editor.document())

        self.reportCodeViewerProperties(font)

    def reportCodeViewerProperties(self, font):
        wposition = self.pos()
        font_info = QFontInfo(font)
        print("---------- Code Viewer Report ----------")
        print("Size: width: %d, height: %d)" % (self.width, self.height))
        print("Top-Left position in screen: (%d, %d)" % (wposition.x(), wposition.y()))
        print("Top-Right position in screen: (%d, %d)" % (wposition.x() + self.width, wposition.y()))
        print("Bottom-Left position in screen: (%d, %d)" % (wposition.x(), wposition.y() + self.height))
        print("Bottom-Right position in screen: (%d, %d)" % (wposition.x() + self.width, wposition.y() + self.height))
        print("---------- Side Bar    Report ----------")
        print("Size: width: %d, height: %d)" % (self.listWidth, self.editorHeight))
        print("Top-Left position in screen: (%d, %d)" % (wposition.x(), wposition.y()))
        print("Top-Right position in screen: (%d, %d)" % (wposition.x() + self.listWidth, wposition.y()))
        print("Bottom-Left position in screen: (%d, %d)" % (wposition.x(), wposition.y() + self.editorHeight))
        print("Bottom-Right position in screen: (%d, %d)" % (wposition.x() + self.listWidth, wposition.y() + self.editorHeight))
        print("---------- Code Editor Report ----------")
        print("Size: width: %d, height: %d)" % (self.editorWidth, self.editorHeight))
        print("Top-Left position in screen: (%d, %d)" % (wposition.x() + self.listWidth, wposition.y()))
        print("Top-Right position in screen: (%d, %d)" % (wposition.x() + self.listWidth + self.editorWidth, wposition.y()))
        print("Bottom-Left position in screen: (%d, %d)" % (wposition.x() + self.listWidth, wposition.y() + self.editorHeight))
        print("Bottom-Right position in screen: (%d, %d)" % (wposition.x() + self.listWidth + self.editorWidth, wposition.y() + self.editorHeight))
        print("---------- Status Bar  Report ----------")
        print("Size: width: %d, height: %d)" % (self.width, self.status_bar_height))
        print("Top-Left position in screen: (%d, %d)" % (wposition.x(), wposition.y() + self.editorHeight))
        print("Top-Right position in screen: (%d, %d)" % (wposition.x() + self.width, wposition.y() + self.editorHeight))
        print("Bottom-Left position in screen: (%d, %d)" % (wposition.x(), wposition.y() + self.editorHeight + self.status_bar_height))
        print("Bottom-Right position in screen: (%d, %d)" % (wposition.x() + self.width, wposition.y() + self.editorHeight + self.status_bar_height))
        print("----------                    ----------")
        print("Codeviewer left pixel: (%d, %d)" % (self.width, self.height))
        print("Document top left pixel: (%d, %d)" % (self.listWidth, 0))
        # print("font family: %s" % font.family())
        print("overline(): %d" % font.overline())
        print("font pixelSize: %d" % font.pixelSize())
        print("font pointSize: %d" % font.pointSize())
        print("font pointSizeF: %d" % font.pointSizeF())
        print("-------- QFontInfo --------")
        print("family(): %s" % font_info.family())
        print("pixelSize(): %d" % font_info.pixelSize())
        print("pointSize(): %d" % font_info.pointSize())
        print("pointSizeF(): %d" % font_info.pointSizeF())

        print("QFontMetrics.lineSpacing(): %d" % QFontMetrics(font).lineSpacing())
        print("QFontMetrics.leading(): %d" % QFontMetrics(font).leading())
        print("QFontMetrics.height(): %d" % QFontMetrics(font).height())
        print("QFont.pixelSize(): %d" % font.pixelSize())
        print("QFontInfo.pixelSize(): %d" % QFontInfo(font).pixelSize())

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
