import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication, QLineEdit, QLabel, QComboBox, QPlainTextEdit)
from PyQt5 import QtCore
from pcer_window import PcerWindow

class ParticipantForm(PcerWindow):

    continue_with_the_experiment = QtCore.pyqtSignal()

    def __init__(self, experiment):
        super(ParticipantForm, self).__init__(experiment)

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
        self.loadCurrentParticipantStatus()

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        
        hbox.addWidget(exitButton)
        hbox.addWidget(loadButton)        
        hbox.addWidget(continueButton)

        self.vbox.addWidget(idLabel)
        self.vbox.addWidget(self.idField)
        self.vbox.addWidget(groupLabel)
        self.vbox.addWidget(self.groupCombo)
        self.vbox.addWidget(statusLabel)
        self.vbox.addWidget(self.statusText)
        self.vbox.addStretch(1)
        self.vbox.addLayout(hbox)
        
        self.setWindowTitle('Participant information')

    def loadCurrentParticipantStatus(self):
        print("ParticipantForm.loadCurrentParticipantStatus")
        print(self.experiment.participant_id)
        status = self.experiment.getParticipantStatus(self.experiment.participant_id)
        self.statusText.insertPlainText(str(status))
        self.idField.setText(self.experiment.participant_id)
        index = self.groupCombo.findText(self.experiment.participant_group)
        self.groupCombo.setCurrentIndex(index)

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
