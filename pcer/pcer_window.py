import sys
from PyQt5.QtWidgets import QWidget, QDesktopWidget
from PyQt5 import QtCore

class PcerWindow(QWidget):

    def __init__(self):
        super(PcerWindow, self).__init__()

    def initBaseUI(self):
    	self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
    	self.width = 800
    	self.height = 300
    	self.setFixedSize(self.width, self.height)
    	self.centerOnScreen()

    def centerOnScreen (self):
        resolution = QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2)) 
        print(resolution.height())
