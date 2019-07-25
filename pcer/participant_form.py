import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication, QLineEdit, QLabel, QComboBox, QPlainTextEdit, QMessageBox)
from PyQt5 import QtCore
from pcer_window import PcerWindow
from participant_already_exist_error import ParticipantAlreadyExistError
import json

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
        self.idField.textEdited.connect(self.clean_status)

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

    def isValidInput(self):
        return (self.idField.text() != '' and self.groupCombo.currentIndex() >= 0)

    def clean_status(self):
        self.statusText.clear()
        self.groupCombo.setCurrentIndex(-1)

    def setIdGroupFieldInTheForm(self, id, group):
        self.idField.setText(id)
        index = self.groupCombo.findText(group)
        self.groupCombo.setCurrentIndex(index)

    def loadCurrentParticipantStatus(self):
        print("ParticipantForm.loadCurrentParticipantStatus")
        print(self.experiment.participant_id)
        status = self.experiment.getParticipantStatus(self.experiment.participant_id)
        self.statusText.setPlainText(json.dumps(status, indent=4, sort_keys=False))
        self.setIdGroupFieldInTheForm(self.experiment.participant_id, self.experiment.participant_group)

    def onContinueButtonClick(self):
        print("ParticipantForm.onContinueButtonClick")
        print(self.idField.text(), self.groupCombo.currentText())
        if self.isValidInput():
            try:
                self.experiment.addParticipant(self.idField.text(), self.groupCombo.currentText())
                self.continue_with_the_experiment.emit()
            except ParticipantAlreadyExistError as e:
                if self.experiment.participant_id == self.idField.text():
                    self.continue_with_the_experiment.emit()
                else:
                    self.popUpWarning(e.msg + "\nPlease use Load Button.")
        else:
            self.popUpWarning("ID and Group inputs cannot be empty.")

    def onLoadButtonClick(self):
        print("ParticipantForm.onLoadButtonClick")
        participant_id = self.idField.text()
        status = self.experiment.getParticipantStatus(participant_id)
        
        if len(status) > 0: # the participant exists in the DB
            self.setIdGroupFieldInTheForm(status[0]['id'], status[0]['group'])
            self.statusText.setPlainText(json.dumps(status, indent=4, sort_keys=False))
            self.experiment.setCurrentParticipant(self.idField.text(), self.groupCombo.currentText())
        else:
            self.popUpWarning("Participant ID = %s does not exist." % (participant_id))
            self.idField.setFocus()
            # self.loadCurrentParticipantStatus()

    def onExitButtonClick(self):
        print("ParticipantForm.onExitButtonClick")
        QApplication.instance().quit()

    def popUpWarning(self, msg):
        warning = QMessageBox()
        warning.setIcon(QMessageBox.Warning)
        warning.setText(msg)
        warning.setWindowTitle('Warning')
        warning.setStandardButtons(QMessageBox.Ok)
        warning.exec_()
