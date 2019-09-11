import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication, QLineEdit, QLabel, QComboBox, QPlainTextEdit)
from PyQt5 import QtCore
from pcer_window import PcerWindow
from participant_already_exist_error import ParticipantAlreadyExistError
from participant_does_not_exist_error import ParticipantDoesNotExistError
import json
import yaml

class ParticipantForm(PcerWindow):

    continue_with_the_experiment = QtCore.pyqtSignal()
    calibrate_eye_tracker = QtCore.pyqtSignal()

    def __init__(self, experiment):
        config = yaml.load(open("config.yml"), Loader = yaml.SafeLoader)
        self.tracking_device = config['tracker']['device']
        super(ParticipantForm, self).__init__(experiment)

    def initUI(self):
        continueButton = QPushButton("Continue")
        loadButton = QPushButton("Load")
        exitButton = QPushButton("Exit experiment")
        self.calibrateButton = QPushButton("Calibrate ET")

        if not self.experiment.participant_id or self.tracking_device != "eye tracker":
            self.calibrateButton.setEnabled(False)

        continueButton.clicked.connect(self.onContinueButtonClick)
        loadButton.clicked.connect(self.onLoadButtonClick)
        exitButton.clicked.connect(self.onExitButtonClick)
        self.calibrateButton.clicked.connect(self.onCalibrateButtonClick)

        idLabel = QLabel()
        idLabel.setText('ID:')
        self.idField = QLineEdit()
        self.idField.textEdited.connect(self.clean_status)

        groupLabel = QLabel()
        groupLabel.setText('Group:')
        self.groupCombo = QComboBox()

        for group in self.experiment.getGroups():
            self.groupCombo.addItem(group)

        statusLabel = QLabel()
        statusLabel.setText('Status:')
        self.statusText = QPlainTextEdit()
        self.statusText.setReadOnly(True)

        self.loadCurrentParticipantStatus()

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        
        hbox.addWidget(exitButton)
        hbox.addWidget(self.calibrateButton)
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
        self.setParticipantIdGroupInStatusBar(id, group)

    def loadCurrentParticipantStatus(self):
        print("ParticipantForm.loadCurrentParticipantStatus")
        print(self.experiment.participant_id)
        try:
            status = self.experiment.getParticipantStatus(self.experiment.participant_id)
        except ParticipantDoesNotExistError as e:
            status = {}
        
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
        try:
            status = self.experiment.getParticipantStatus(participant_id)
            self.setIdGroupFieldInTheForm(status['id'], status['group'])
            self.statusText.setPlainText(json.dumps(status, indent=4, sort_keys=False))
            self.experiment.setCurrentParticipant(self.idField.text(), self.groupCombo.currentText())
            if self.tracking_device == "eye tracker":
                self.calibrateButton.setEnabled(True)
        except ParticipantDoesNotExistError as e:
            self.popUpWarning(e.msg)
            self.idField.setFocus()

    def onExitButtonClick(self):
        print("ParticipantForm.onExitButtonClick")
        QApplication.instance().quit()

    def onCalibrateButtonClick(self):
        print("onCalibrateButtonClick")
        self.calibrate_eye_tracker.emit()
