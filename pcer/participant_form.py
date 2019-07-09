import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication)
from PyQt5 import QtCore
from pcer_window import PcerWindow

class ParticipantForm(PcerWindow):

    continue_with_the_experiment = QtCore.pyqtSignal()

    def __init__(self):
        super(QWidget, self).__init__()
        self.initBaseUI()
        self.initUI()

    def initUI(self):
        continueButton = QPushButton("Continue")
        exitButton = QPushButton("Exit experiment")

        continueButton.clicked.connect(self.onContinueButtonClick)
        exitButton.clicked.connect(self.onExitButtonClick)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        
        hbox.addWidget(exitButton)
        hbox.addWidget(continueButton)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        
        self.setLayout(vbox)
        
        self.setWindowTitle('Participant information')

    def onContinueButtonClick(self):
        print("ParticipantForm.onContinueButtonClick")
        self.continue_with_the_experiment.emit()

    def onExitButtonClick(self):
        print("ParticipantForm.onExitButtonClick")
        QApplication.instance().quit()
