import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication, QLabel, QComboBox, QGroupBox)
from PyQt5 import QtCore
from pcer_window import PcerWindow

class PretestForm(PcerWindow):

    submit_answer = QtCore.pyqtSignal()

    def __init__(self, experiment):
        super(PretestForm, self).__init__(experiment)

    def initUI(self):
        submitButton = QPushButton("Submit answer")
        submitButton.clicked.connect(self.onSubmitButtonClick)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(submitButton)

        
        group_box = self.experiment.form_builder.build_pretest_form()
        self.vbox.addWidget(group_box)
        self.vbox.addStretch(1)
        self.vbox.addLayout(hbox)
        self.setWindowTitle('Pretest')

    def onSubmitButtonClick(self):
        print("PretestForm.onSubmitButtonClick")
        self.submit_answer.emit()
