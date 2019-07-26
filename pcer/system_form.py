import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication, QLabel)
from PyQt5 import QtCore
from pcer_window import PcerWindow

class SystemForm(PcerWindow):

    back = QtCore.pyqtSignal()
    show_task = QtCore.pyqtSignal()

    def __init__(self, experiment):
        super(SystemForm, self).__init__(experiment)

    def initUI(self):
        showTaskButton = QPushButton("Show task")
        backButton = QPushButton("Back")

        showTaskButton.clicked.connect(self.onShowTaskButtonClick)
        backButton.clicked.connect(self.onBackButtonClick)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        
        hbox.addWidget(backButton)
        hbox.addWidget(showTaskButton)

        # Get the system info to fill the system form
        system = self.experiment.getExperimentalSystem()
        system_name = QLabel()
        system_name.setText(system['name'])
        self.vbox.addWidget(system_name)

        system_description = QLabel()
        system_description.setText(system['description'])
        self.vbox.addWidget(system_description)
        # --------------------------------------

        self.vbox.addStretch(1)
        self.vbox.addLayout(hbox)
        
        self.setWindowTitle('System presentation')

    def onShowTaskButtonClick(self):
        print("SystemForm.onShowTaskButtonClick")
        self.show_task.emit()

    def onBackButtonClick(self):
        print("SystemForm.onBackButtonClick")
        self.back.emit()
