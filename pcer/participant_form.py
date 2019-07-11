import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication, QLineEdit, QLabel, QComboBox, QPlainTextEdit)
from PyQt5 import QtCore
from pcer_window import PcerWindow

class ParticipantForm(PcerWindow):

    continue_with_the_experiment = QtCore.pyqtSignal()

    def __init__(self, experiment):
        super(ParticipantForm, self).__init__(experiment)
        self.initBaseUI()
        self.initUI()

    def initUI(self):
        continueButton = QPushButton("Continue")
        loadButton = QPushButton("Load")
        exitButton = QPushButton("Exit experiment")

        continueButton.clicked.connect(self.onContinueButtonClick)
        loadButton.clicked.connect(self.onLoadButtonClick)
        exitButton.clicked.connect(self.onExitButtonClick)

        idLabel = QLabel()
        idLabel.setText('ID:')
        idField = QLineEdit()
        groupLabel = QLabel()
        groupLabel.setText('Group:')
        groupCombo = QComboBox()
        groupCombo.addItem("DCI")
        groupCombo.addItem("OO")
        statusLabel = QLabel()
        statusLabel.setText('Status:')
        statusText = QPlainTextEdit()

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        
        hbox.addWidget(exitButton)
        hbox.addWidget(loadButton)        
        hbox.addWidget(continueButton)

        vbox = QVBoxLayout()
        vbox.addWidget(idLabel)
        vbox.addWidget(idField)
        vbox.addWidget(groupLabel)
        vbox.addWidget(groupCombo)
        vbox.addWidget(statusLabel)
        vbox.addWidget(statusText)
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        
        self.setLayout(vbox)
        
        self.setWindowTitle('Participant information')

    def onContinueButtonClick(self):
        print("ParticipantForm.onContinueButtonClick")
        self.continue_with_the_experiment.emit()

    def onLoadButtonClick(self):
        print("ParticipantForm.onLoadButtonClick")
        self.experiment.openParticipanSession(1234)

    def onExitButtonClick(self):
        print("ParticipantForm.onExitButtonClick")
        QApplication.instance().quit()
