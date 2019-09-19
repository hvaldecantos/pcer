import sys
from PyQt5.QtWidgets import (QPushButton, QHBoxLayout)
from PyQt5 import QtCore
from pcer_window import PcerWindow

class EndForm(PcerWindow):

    back = QtCore.pyqtSignal()
    show_task = QtCore.pyqtSignal()
    group_box = None

    def __init__(self, experiment):
        super(EndForm, self).__init__(experiment)

    def initUI(self):
        backButton = QPushButton("Back")
        backButton.clicked.connect(self.onBackButtonClick)

        hbox = QHBoxLayout()
        hbox.addStretch(1)

        hbox.addWidget(backButton)

        self.group_box = self.experiment.form_builder.build_end_message()
        self.vbox.addWidget(self.group_box)

        self.vbox.addStretch(1)
        self.vbox.addLayout(hbox)
        
        self.setWindowTitle('System presentation')

    def onBackButtonClick(self):
        print("EndForm.onBackButtonClick")
        self.back.emit()
