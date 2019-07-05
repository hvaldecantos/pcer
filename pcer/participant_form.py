import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication)
from PyQt5 import QtCore

class ParticipantForm(QWidget):

    def __init__(self):
        super(QWidget, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        submitButton = QPushButton("Submit info")
        exitButton = QPushButton("Exit experiment")

        submitButton.clicked.connect(self.onSubmitButtonClick)
        exitButton.clicked.connect(self.onExitButtonClick)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        
        hbox.addWidget(exitButton)
        hbox.addWidget(submitButton)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        
        self.setLayout(vbox)
        
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Buttons')

    def onSubmitButtonClick(self):
        print("onSubmitButtonClick")

    def onExitButtonClick(self):
        print("onExitButtonClick")
        self.close()
