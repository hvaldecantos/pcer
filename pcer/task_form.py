import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication)
from PyQt5 import QtCore
from pcer_window import PcerWindow

class TaskForm(PcerWindow):

    submit_answer = QtCore.pyqtSignal()
    read_code = QtCore.pyqtSignal()

    def __init__(self, experiment = None):
        super(TaskForm, self).__init__(experiment)
        self.initBaseUI()
        self.initUI()

    def initUI(self):
        submitButton = QPushButton("Submit answer")
        readButton = QPushButton("Read code")

        submitButton.clicked.connect(self.onSubmitButtonClick)
        readButton.clicked.connect(self.onReadButtonClick)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        
        hbox.addWidget(submitButton)
        hbox.addWidget(readButton)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        
        self.setLayout(vbox)
        
        self.setWindowTitle('Task presentation')

    def onSubmitButtonClick(self):
        print("TaskForm.onSubmitButtonClick")
        self.submit_answer.emit()

    def onReadButtonClick(self):
        print("TaskForm.onReadButtonClick")
        self.read_code.emit()
        
