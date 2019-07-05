import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication)
from PyQt5 import QtCore

class SystemForm(QWidget):

    back = QtCore.pyqtSignal()

    def __init__(self):
        super(QWidget, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        submitButton = QPushButton("Continue")
        backButton = QPushButton("Back")

        submitButton.clicked.connect(self.onContinueButtonClick)
        backButton.clicked.connect(self.onBackButtonClick)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        
        hbox.addWidget(backButton)
        hbox.addWidget(submitButton)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        
        self.setLayout(vbox)
        
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('System presentation')

    def onContinueButtonClick(self):
        print("SystemForm.onContinueButtonClick")

    def onBackButtonClick(self):
        print("SystemForm.onBackButtonClick")
        self.back.emit()
