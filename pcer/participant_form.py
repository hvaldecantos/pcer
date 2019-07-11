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
        self.idField = QLineEdit()
        groupLabel = QLabel()
        groupLabel.setText('Group:')
        self.groupCombo = QComboBox()
        self.groupCombo.addItem("DCI")
        self.groupCombo.addItem("OO")
        statusLabel = QLabel()
        statusLabel.setText('Status:')
        self.statusText = QPlainTextEdit()
        self.statusText.setReadOnly(True)
        self.statusText.insertPlainText('Here goes the status of patricipat\n')

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        
        hbox.addWidget(exitButton)
        hbox.addWidget(loadButton)        
        hbox.addWidget(continueButton)

        vbox = QVBoxLayout()
        vbox.addWidget(idLabel)
        vbox.addWidget(self.idField)
        vbox.addWidget(groupLabel)
        vbox.addWidget(self.groupCombo)
        vbox.addWidget(statusLabel)
        vbox.addWidget(self.statusText)
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        
        self.setLayout(vbox)
        
        self.setWindowTitle('Participant information')

    def onContinueButtonClick(self):
        print("ParticipantForm.onContinueButtonClick")
        print(self.idField.text(), self.groupCombo.currentText())
        self.experiment.addParticipant(self.idField.text(), self.groupCombo.currentText())
        self.continue_with_the_experiment.emit()

    def onLoadButtonClick(self):
        print("ParticipantForm.onLoadButtonClick")
        self.experiment.openParticipanSession(1234)

    def onExitButtonClick(self):
        print("ParticipantForm.onExitButtonClick")
        QApplication.instance().quit()
