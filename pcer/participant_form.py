import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication, QLineEdit, QLabel, QComboBox, QPlainTextEdit, QMessageBox)
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
        if len(status) is not 0:
            self.statusText.insertPlainText(str(status))
        self.idField.setText(self.experiment.participant_id)
        index = self.groupCombo.findText(self.experiment.participant_group)
        self.groupCombo.setCurrentIndex(index)

    def onContinueButtonClick(self):
        print("ParticipantForm.onContinueButtonClick")
        print(self.idField.text(), self.groupCombo.currentText())
        #new_participant is a flag which will indicate whether added participant is new or already exists
        new_participant = self.experiment.addParticipant(self.idField.text(), self.groupCombo.currentText())
        if new_participant or self.experiment.participant_id == self.idField.text():
            self.continue_with_the_experiment.emit()
        else:
            self.popUpWarning()

    def onLoadButtonClick(self):
        print("ParticipantForm.onLoadButtonClick")
        self.experiment.openParticipanSession(1234)
        self.experiment.setCurrentParticipant(self.idField.text(), self.groupCombo.currentText())
        status = str(self.experiment.getParticipantStatus(self.experiment.participant_id))
        print(status)
        self.statusText.setPlainText(status)

    def onExitButtonClick(self):
        print("ParticipantForm.onExitButtonClick")
        QApplication.instance().quit()

    #Function Contains code for displaying Warning
    def popUpWarning(self):
        warning = QMessageBox()
        warning.setIcon(QMessageBox.Warning)
        warning.setText('ID Exist. Please use Load Button')
        warning.setWindowTitle('Warning')
        warning.setStandardButtons(QMessageBox.Ok)
        warning.exec_()
