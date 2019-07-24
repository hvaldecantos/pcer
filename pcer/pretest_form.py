import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication, QLabel, QComboBox)
from PyQt5 import QtCore
from pcer_window import PcerWindow

class PretestForm(PcerWindow):

    submit_answer = QtCore.pyqtSignal()

    def __init__(self, experiment):
        super(PretestForm, self).__init__(experiment)

    def initUI(self):
        submitButton = QPushButton("Submit answer")

        submitButton.clicked.connect(self.onSubmitButtonClick)

        # < temporary code: this code should build from the
        # questions in the pretest.yml file, and more ...
        q1 = QLabel()
        q1.setText('q1:')
        a1 = QComboBox()
        a1.addItem("DCI")
        a1.addItem("OO")

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        
        hbox.addWidget(submitButton)

        self.vbox.addWidget(q1)
        self.vbox.addWidget(a1)
        self.vbox.addStretch(1)
        self.vbox.addLayout(hbox)
        # temporary code >
        
        self.setWindowTitle('Pretest')

    def onSubmitButtonClick(self):
        print("PretestForm.onSubmitButtonClick")
        self.submit_answer.emit()
