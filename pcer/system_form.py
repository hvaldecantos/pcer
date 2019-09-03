import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication, QLabel, QMessageBox)
from PyQt5 import QtCore
from pcer_window import PcerWindow

class SystemForm(PcerWindow):

    back = QtCore.pyqtSignal()
    show_task = QtCore.pyqtSignal()
    group_box = None

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
        self.group_box = self.experiment.form_builder.build_system_form(system)

        #system_name = QLabel()
        #system_name.setText(system['name'])
        #self.vbox.addWidget(system_name)
        self.vbox.addWidget(self.group_box)

        #system_description = QLabel()
        #system_description.setText(system['description'])
        #self.vbox.addWidget(system_description)
        # --------------------------------------

        self.vbox.addStretch(1)
        self.vbox.addLayout(hbox)
        
        self.setWindowTitle('System presentation')

    def onShowTaskButtonClick(self):
        print("SystemForm.onShowTaskButtonClick")
        participant_id = self.experiment.participant_id
        system_id = self.experiment.session.getCurrentSystemId(participant_id)
        total_tasks = self.experiment.resource.getTasks(self.experiment.participant_group, system_id)
        if self.experiment.session.hasRemainingTasks(self.experiment.participant_id,total_tasks):
            self.show_task.emit()
        else:
            self.experiment.session.finishCurrentSystem(participant_id)
            self.popUpWarning('All tasks are completed for this system, Go back and start again.')

    def onBackButtonClick(self):
        print("SystemForm.onBackButtonClick")
        self.back.emit()

    def popUpWarning(self, msg):
        warning = QMessageBox()
        warning.setIcon(QMessageBox.Warning)
        warning.setText(msg)
        warning.setWindowTitle('Warning')
        warning.setStandardButtons(QMessageBox.Ok)
        warning.exec_()