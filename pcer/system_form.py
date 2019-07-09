import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication)
from PyQt5 import QtCore
from pcer_window import PcerWindow

class SystemForm(PcerWindow):

    back = QtCore.pyqtSignal()
    show_task = QtCore.pyqtSignal()

    def __init__(self):
        super(QWidget, self).__init__()
        self.initBaseUI()
        self.initUI()

    def initUI(self):
        showTaskButton = QPushButton("Show task")
        backButton = QPushButton("Back")

        showTaskButton.clicked.connect(self.onShowTaskButtonClick)
        backButton.clicked.connect(self.onBackButtonClick)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        
        hbox.addWidget(backButton)
        hbox.addWidget(showTaskButton)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        
        self.setLayout(vbox)
        
        self.setWindowTitle('System presentation')

    def onShowTaskButtonClick(self):
        print("SystemForm.onShowTaskButtonClick")
        self.show_task.emit()

    def onBackButtonClick(self):
        print("SystemForm.onBackButtonClick")
        self.back.emit()
