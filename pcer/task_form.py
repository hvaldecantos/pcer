import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication)
from PyQt5 import QtCore

class TaskForm(QWidget):

    submit_answer = QtCore.pyqtSignal()
    read_code = QtCore.pyqtSignal()

    def __init__(self):
        super(QWidget, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
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
        
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Task presentation')

    def onSubmitButtonClick(self):
        print("TaskForm.onSubmitButtonClick")
        self.submit_answer.emit()

    def onReadButtonClick(self):
        print("TaskForm.onReadButtonClick")
        self.read_code.emit()
        
