import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication)
from PyQt5 import QtCore
from pcer_window import PcerWindow

class ParticipantForm(PcerWindow):

    submit_info = QtCore.pyqtSignal()

    def __init__(self):
        super(PcerWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.initBaseUI()
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
        self.setWindowTitle('Participant information')

    def onSubmitButtonClick(self):
        print("ParticipantForm.onSubmitButtonClick")
        self.submit_info.emit()

    def onExitButtonClick(self):
        print("ParticipantForm.onExitButtonClick")
        QApplication.instance().quit()
