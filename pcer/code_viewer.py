import sys
import os
import yaml
from PyQt5.QtWidgets import (QPushButton, QMessageBox, QApplication, QListWidget, QTextEdit)
from PyQt5.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat, QFontMetrics, QFontInfo, QPainter, QPen, QPixmap, QMouseEvent #, QCursor
from PyQt5 import QtCore
from PyQt5.QtCore import QFile, QRegExp, Qt, QRectF,  QPoint, QEvent
from pcer_window import PcerWindow
from datetime import datetime
from eye_tracker import ET


class TrackerTextEdit(QTextEdit):
    scrollbar_displacement = 0
    filename = None
    csv_file = None
    header = None
    x = 0
    y = 0

    def __init__(self, csv_filename, parent=None):
        config = yaml.load(open("config.yml"), Loader = yaml.SafeLoader)
        tracking_data_path = config['tracker']['tracking_data_path']

        self.csv_file = open(os.path.join(tracking_data_path, csv_filename + '.csv'),'a+')
        self.csv_file.seek(0)
        if self.csv_file.read() == "":
            self.csv_file.write(self.header)
        else:
            self.csv_file.seek(0, os.SEEK_END)
        super(TrackerTextEdit, self).__init__(parent)

    def setFilename(self, filename):
        self.filename = filename

    def paintEvent(self, event):
        painter = QPainter(self.viewport())
        pen = QPen(Qt.SolidLine)
        pen.setColor(Qt.black)
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawEllipse(self.x - 15, self.y - 15, 30, 30)
        super(TrackerTextEdit, self).paintEvent(event)


class EyeTrackerTextEdit(TrackerTextEdit):
    x_offset = 0
    y_offset = 0
    x2 = 0
    y2 = 0

    def __init__(self, csv_filename, parent=None):
        self.header = "timestamp1,timestamp2,microseconds,x,y,pupildiam,filename\n"
        super(EyeTrackerTextEdit, self).__init__(csv_filename, parent)

    def scrollContentsBy(self, dx, dy):
        super(EyeTrackerTextEdit, self).scrollContentsBy(dx, dy)
        self.scrollbar_displacement += dy
        print(self.scrollbar_displacement)

    def gazeMoveEvent(self, x, y, diam, timestamp):
        # print("x: %d, y: %d, diam: %f" % (x,y, diam))

        secs = (timestamp / 1000000)
        mins = secs / 60

        micro = (timestamp % 1000000)
        seco = secs % 60
        minu = mins % 60
        hora = mins / 60

        # t = datetime.time(microseconds = timestamp)

        self.x = x - self.x_offset
        self.y = y - self.y_offset

        if((self.x_offset <= x and x <= self.x2) and (self.y_offset <= y and y <= self.y2)):
            # str_dat = "'%s',%ld,%d,%d,%f,'%s'\n" % (datetime.now(),timestamp, self.x, self.y - self.scrollbar_displacement, diam, self.filename)
            str_dat = "'%s','%02d:%02d:%02d.%06d',%ld,%d,%d,%f,'%s'\n" % (datetime.now(), hora, minu, seco, micro, timestamp, self.x, self.y - self.scrollbar_displacement, diam, self.filename)
            self.csv_file.write(str_dat)
            self.update()


class MouseTrackerTextEdit(TrackerTextEdit):

    def __init__(self, csv_filename, parent=None):
        self.header = "timestamp,x,y,filename\n"
        super(MouseTrackerTextEdit, self).__init__(csv_filename, parent)
        self.setMouseTracking(True)

    def scrollContentsBy(self, dx, dy):
        super(MouseTrackerTextEdit, self).scrollContentsBy(dx, dy)
        self.scrollbar_displacement += dy
        event = QMouseEvent(QEvent.MouseMove, QPoint(self.x, self.y), Qt.NoButton, QApplication.mouseButtons(), Qt.NoModifier)
        self.mouseMoveEvent(event)
        print(self.scrollbar_displacement)

    def keyPressEvent(self, event):
        if (event.modifiers() & QtCore.Qt.ShiftModifier):
            print 'Saving document as png picture...'
            self.save()

    def mouseMoveEvent(self, event):
        self.x = event.x()
        self.y = event.y()
        str_dat = "'%s',%d,%d,'%s'\n" % (datetime.now(), self.x, self.y - self.scrollbar_displacement, self.filename)
        self.csv_file.write(str_dat)
        self.update()

    def save(self):
        doc = self.document()
        pixmap = QPixmap(doc.size().width(), doc.size().height())
        pixmap.fill(Qt.white)
        painter = QPainter(pixmap)
        doc.drawContents(painter, QRectF(0, 0, doc.size().width(),  doc.size().height()))
        painter.end()
        pixmap.save("%s.png" % self.filename, "PNG")


class CodeViewer(PcerWindow):

    back = QtCore.pyqtSignal()

    def __init__(self, experiment, et, timer):
        config = yaml.load(open("config.yml"), Loader = yaml.SafeLoader)
        self.height_in_characters = config['code_viewer']['document']['height_in_characters']
        self.font_pixel_size = config['code_viewer']['document']['font_pixel_size']
        self.margin_pixel_size = config['code_viewer']['document']['margin_pixel_size']
        self.hide_scroll_bar = config['code_viewer']['document']['hide_scroll_bar']
        self.status_bar_height = config['code_viewer']['status_bar_height']
        self.padding_left = config['code_viewer']['document']['padding_left']
        self.padding_top = config['code_viewer']['document']['padding_top']
        self.padding_bottom = config['code_viewer']['document']['padding_bottom']
        self.padding_right = config['code_viewer']['document']['padding_right']
        self.use_leading_space = config['code_viewer']['document']['use_leading_space']
        self.tracking_device = config['tracker']['device']
        self.sidebar_percentage_width = config['code_viewer']['sidebar']['percentage_width']
        self.sidebar_font_type = config['code_viewer']['sidebar']['font_type']
        self.sidebar_font_pixel_size = config['code_viewer']['sidebar']['font_pixel_size']

        self.keywords = config['keywords']['common']
        self.keywords_paradigm_bold = config['keywords'][experiment.participant_group + "_bold"]
        self.keywords_paradigm_italic = config['keywords'][experiment.participant_group + "_italic"]

        self.et = et
        self.timer = timer
        self.timer.timeout_signal.connect(self.popupTimeoutMessage)
        super(CodeViewer, self).__init__(experiment)

    def initUI(self):
        self.vbox.addStretch(1) # => necessary to send the status bar at the bottom

        self.listWidth = self.width * self.sidebar_percentage_width
        self.editorWidth = self.width * (1 - self.sidebar_percentage_width)
        self.backButtonWidth = self.listWidth / 2

        self.setupEditor()
        self.setWindowTitle('Code Viewer')
        self.setupFileList()
        self.setupBackButton()
        self.setFixedSize(self.width, self.editorHeight + self.status_bar_height)
        self.centerOnScreen()

        self.current_file = self.experiment.getCurrentOpenedFilename()
        self.code_path = self.experiment.getSourceCodePath()

        if(self.current_file):
            found = self.listWidget.findItems(self.current_file, QtCore.Qt.MatchExactly)
            found[0].setSelected(True)
            self.show()
            self.openFile(os.path.join(self.code_path, self.current_file))
            self.timer.start()

    def popupTimeoutMessage(self):
        self.editor.document().clear()
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Reading time is over")
        msg.setText("For the current system and the remaining question, you should answer them without reading the code again.")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.buttonClicked.connect(self.onBackButtonClick)
        msg.exec_()

    def setupFileList(self):
        self.listWidget = QListWidget(self)

        font = QFont (self.sidebar_font_type)
        font.setPixelSize(self.sidebar_font_pixel_size)
        font.setFixedPitch(True)
        self.listWidget.setFont(font)
        self.listWidget.move(0, 0)
        self.listWidget.resize(self.listWidth, self.editorHeight)
        self.listWidget.addItems(self.experiment.getCurrentExperimentalSystemFilenames())
        self.listWidget.currentItemChanged.connect(self.onCurrentItemChanged)

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

        if self.use_leading_space:
            line_height = QFontMetrics(font).lineSpacing()
        else:
            line_height = QFontMetrics(font).height()
        self.editorHeight = (self.height_in_characters * line_height) + \
                             self.margin_pixel_size + \
                             self.padding_top + \
                             self.padding_bottom

        # Selecting the tracker device
        self.editor = None
        csv_filename = self.experiment.participant_id + "_" + self.experiment.current_system_id
        if self.tracking_device == "eye tracker":
            self.editor = EyeTrackerTextEdit(csv_filename, self)
            self.et.plugg(self.editor)
        elif self.tracking_device == "mouse":
            self.editor = MouseTrackerTextEdit(csv_filename, self)
        else:
            raise Exception("You should especify your tracker device: 'eye tracker' or 'mouse'.")

        self.editor.setFont(font)
        self.editor.move(self.listWidth, 0)
        self.editor.resize(self.editorWidth, self.editorHeight)
        self.editor.setStyleSheet("QTextEdit {padding-left: %s; padding-top: %s; padding-bottom: %s; padding-right: %s}" %
                                        (self.padding_left, self.padding_top, self.padding_bottom, self.padding_right));
        self.editor.document().setDocumentMargin(self.margin_pixel_size)
        self.editor.setReadOnly(True)
        if self.hide_scroll_bar:
            self.editor.verticalScrollBar().setStyleSheet("QScrollBar:vertical {width: 0px;}")

        self.highlighter = Highlighter(self.keywords, self.keywords_paradigm_bold, self.keywords_paradigm_italic, self.editor.document())

        self.reportCodeViewerProperties(font)

    def reportCodeViewerProperties(self, font):
        wposition = self.pos()
        font_info = QFontInfo(font)
        print("---------- Code Viewer Report ----------")
        print("Size: width: %d, height: %d" % (self.width, self.height))
        print("Top-Left position in screen: (%d, %d)" % (wposition.x(), wposition.y()))
        print("Top-Right position in screen: (%d, %d)" % (wposition.x() + self.width, wposition.y()))
        print("Bottom-Left position in screen: (%d, %d)" % (wposition.x(), wposition.y() + self.height))
        print("Bottom-Right position in screen: (%d, %d)" % (wposition.x() + self.width, wposition.y() + self.height))
        print("---------- Side Bar    Report ----------")
        print("Size: width: %d, height: %d" % (self.listWidth, self.editorHeight))
        print("Top-Left position in screen: (%d, %d)" % (wposition.x(), wposition.y()))
        print("Top-Right position in screen: (%d, %d)" % (wposition.x() + self.listWidth, wposition.y()))
        print("Bottom-Left position in screen: (%d, %d)" % (wposition.x(), wposition.y() + self.editorHeight))
        print("Bottom-Right position in screen: (%d, %d)" % (wposition.x() + self.listWidth, wposition.y() + self.editorHeight))
        print("---------- Code Editor Report ----------")
        print("Size: width: %d, height: %d" % (self.editorWidth, self.editorHeight))
        print("Margins: %f pixels" % self.editor.document().documentMargin())
        print("Top-Left position in screen: (%d, %d)" % (wposition.x() + self.listWidth, wposition.y()))
        print("Top-Right position in screen: (%d, %d)" % (wposition.x() + self.listWidth + self.editorWidth, wposition.y()))
        print("Bottom-Left position in screen: (%d, %d)" % (wposition.x() + self.listWidth, wposition.y() + self.editorHeight))
        print("Bottom-Right position in screen: (%d, %d)" % (wposition.x() + self.listWidth + self.editorWidth, wposition.y() + self.editorHeight))
        print("Padding: left: %d, top: %d, bottom: %d, right: %d" % (self.padding_left, self.padding_top, self.padding_bottom, self.padding_right))
        print("---------- Font report (font) ----------")
        print("font family: %s" % font.family())
        print("font pixelSize: %d" % font.pixelSize())
        print("font pointSize: %d" % font.pointSize())
        print("font pointSizeF: %d" % font.pointSizeF())
        print("QFont.pixelSize(): %d" % font.pixelSize())
        print("---------- QFontInfo   (font) ----------")
        print("family(): %s" % font_info.family())
        print("pixelSize(): %d" % font_info.pixelSize())
        print("pointSize(): %d" % font_info.pointSize())
        print("pointSizeF(): %d" % font_info.pointSizeF())
        print("QFontInfo.pixelSize(): %d" % font_info.pixelSize())
        print("---------- QFontMetrics (font) ---------")
        print("QFontMetrics.lineSpacing(): %d" % QFontMetrics(font).lineSpacing())
        print("QFontMetrics.leading(): %d" % QFontMetrics(font).leading())
        print("QFontMetrics.height(): %d" % QFontMetrics(font).height())
        print("---------- Eye tracking area  ----------")
        x1 = wposition.x() + self.listWidth + self.padding_left
        y1 = wposition.y() + self.padding_top
        x2 = wposition.x() + self.listWidth + self.editorWidth - self.padding_right
        y2 = wposition.y() + self.editorHeight - self.padding_bottom
        self.editor.x_offset = x1 # For the eye tracker, as it uses the entire screen
        self.editor.y_offset = y1 # For the eye tracker, as it uses the entire screen
        self.editor.x2 = x2
        self.editor.y2 = y2
        print("Size: width: %d, height: %d" % (x2 - x1, y2 - y1))
        print("Top-Left position in screen: (%d, %d)" % (x1, y1))
        print("Top-Right position in screen: (%d, %d)" % (x2, y1))
        print("Bottom-Left position in screen: (%d, %d)" % (x1, y2))
        print("Bottom-Right position in screen: (%d, %d)" % (x2, y2))
        print("x_offset = %d" % x1)
        print("y_offset = %d" % y1)
        print("---------- Status Bar  Report ----------")
        print("Size: width: %d, height: %d" % (self.width, self.status_bar_height))
        print("Top-Left position in screen: (%d, %d)" % (wposition.x(), wposition.y() + self.editorHeight))
        print("Top-Right position in screen: (%d, %d)" % (wposition.x() + self.width, wposition.y() + self.editorHeight))
        print("Bottom-Left position in screen: (%d, %d)" % (wposition.x(), wposition.y() + self.editorHeight + self.status_bar_height))
        print("Bottom-Right position in screen: (%d, %d)" % (wposition.x() + self.width, wposition.y() + self.editorHeight + self.status_bar_height))
        print("----------------------------------------")

    def onCurrentItemChanged(self, current_item, previous_item):
        if(not self.current_file):
            self.timer.start()

        # current_file is the past clicked file
        if self.current_file:
            self.experiment.setScrollDisplacement(self.current_file, self.editor.scrollbar_displacement)
        else:
            self.experiment.setScrollDisplacement(current_item.text(), self.editor.scrollbar_displacement)

        # uptades current_file to the current clicked file
        self.current_file = current_item.text()
        self.experiment.setCurrentOpenedFilename(self.current_file)
        self.openFile(os.path.join(self.code_path, current_item.text()))

    def onBackButtonClick(self):
        if self.current_file:
            self.experiment.setScrollDisplacement(self.current_file, self.editor.scrollbar_displacement)
        if self.tracking_device == "eye tracker": self.et.unplugg()
        self.editor.csv_file.close()
        self.back.emit()

    def openFile(self, path=None):
        if not path:
            path, _ = QFileDialog.getOpenFileName(self, "Open File", '',
                    "C++ Files (*.cpp *.h)")
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

                self.editor.setFilename(self.current_file)
                self.editor.setPlainText(text)

                try:
                    amount = self.experiment.getScrollDisplacement(self.current_file)
                    self.editor.verticalScrollBar().setValue(amount * (-1))
                except KeyError as e:
                    pass


class Highlighter(QSyntaxHighlighter):
    def __init__(self, keywords, keywords_paradigm_bold, keywords_paradigm_italic, parent=None):
        super(Highlighter, self).__init__(parent)

        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(Qt.darkBlue)
        keywordFormat.setFontWeight(QFont.Bold)
        a = [(QRegExp(pattern), keywordFormat) for pattern in keywords]

        keywordParadigmFormatBold = QTextCharFormat()
        keywordParadigmFormatBold.setForeground(Qt.darkRed)
        keywordParadigmFormatBold.setFontWeight(QFont.Bold)
        b = [(QRegExp(pattern), keywordParadigmFormatBold) for pattern in keywords_paradigm_bold]

        keywordParadigmFormatItalic = QTextCharFormat()
        keywordParadigmFormatItalic.setForeground(Qt.darkRed)
        keywordParadigmFormatItalic.setFontItalic(True)
        keywordParadigmFormatItalic.setFontWeight(QFont.Normal)
        c = [(QRegExp(pattern), keywordParadigmFormatItalic) for pattern in keywords_paradigm_italic]

        self.highlightingRules = a + b + c

        classFormat = QTextCharFormat()
        classFormat.setFontWeight(QFont.Bold)
        classFormat.setForeground(Qt.darkMagenta)
        self.highlightingRules.append((QRegExp("\\bQ[A-Za-z]+\\b"), classFormat))

        singleLineCommentFormat = QTextCharFormat()
        singleLineCommentFormat.setForeground(Qt.red)
        self.highlightingRules.append((QRegExp("//[^\n]*"),
                singleLineCommentFormat))

        self.multiLineCommentFormat = QTextCharFormat()
        self.multiLineCommentFormat.setForeground(Qt.red)

        quotationFormat = QTextCharFormat()
        quotationFormat.setForeground(Qt.darkGreen)
        self.highlightingRules.append((QRegExp("\"([^\"]*)\""), quotationFormat))

        functionFormat = QTextCharFormat()
        functionFormat.setFontItalic(True)
        functionFormat.setForeground(Qt.blue)
        self.highlightingRules.append((QRegExp("\\b[A-Za-z0-9_]+(?=\\()"), functionFormat))

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
