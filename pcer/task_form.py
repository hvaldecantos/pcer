import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication, QMessageBox, QLabel)
from PyQt5 import QtCore
from pcer_window import PcerWindow
from functools import partial

class TaskForm(PcerWindow):

    submit_answer = QtCore.pyqtSignal()
    read_code = QtCore.pyqtSignal()
    choice_combo_question_list = []
    group_box = None

    def __init__(self, experiment):
        super(TaskForm, self).__init__(experiment)

    def initUI(self):
        submitButton = QPushButton("Submit answer")
        readButton = QPushButton("Read code")

        submitButton.clicked.connect(self.onSubmitButtonClick)
        readButton.clicked.connect(self.onReadButtonClick)

        system = self.experiment.getExperimentalSystem()
        self.group_box_system = self.experiment.form_builder.build_system_form(system)

        task = self.experiment.getExperimentalTask()
        self.group_box, self.choice_combo_question_list = self.experiment.form_builder.build_task_form(task)

        self.setExistingData()

        self.vbox.addWidget(self.group_box_system)
        self.vbox.addWidget(QLabel(""))
        self.vbox.addWidget(self.group_box)

        for ccq_dict in self.choice_combo_question_list:
            cb = ccq_dict['combobox']
            cb.currentIndexChanged.connect(partial(self.choiceSelection, ccq_dict))

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(submitButton)
        hbox.addWidget(readButton)

        self.vbox.addStretch(1)
        self.vbox.addLayout(hbox)
        self.setWindowTitle('Task presentation')

    def setExistingData(self):
        current_task_data = self.experiment.session.getCurrentTaskState(self.experiment.participant_id)
        if current_task_data.keys() > 0:
            for question_id in current_task_data.keys():
                for question in self.choice_combo_question_list:
                    if question_id == question['id']:
                        index = question['combobox'].findText(current_task_data[question_id]['answer'])
                        question['combobox'].setCurrentIndex(index)
        else:
            print('No existing session')

    def areValidInputs(self):
        for ccq_dict in self.choice_combo_question_list:
            if ccq_dict['combobox'].currentText() == '--':
                return False
        return True

    def onSubmitButtonClick(self):
        if self.areValidInputs():
            self.experiment.finishCurrentTask()
            print("TaskForm.onSubmitButtonClick")
            self.submit_answer.emit()
        else:
            self.popUpWarning('Please answer all questions')

    def onReadButtonClick(self):
        print("TaskForm.onReadButtonClick")
        self.read_code.emit()

    def choiceSelection(self,ccq_dict,i):
        print('Choice :',ccq_dict['combobox'].currentText(), ' is selected for question ',ccq_dict['question'])
        question = ccq_dict['question']
        choice = ccq_dict['combobox'].currentText()
        self.experiment.setTaskData(ccq_dict['id'], question, choice)

    def popUpWarning(self, msg):
        warning = QMessageBox()
        warning.setIcon(QMessageBox.Warning)
        warning.setText(msg)
        warning.setWindowTitle('Warning')
        warning.setStandardButtons(QMessageBox.Ok)
        warning.exec_()
