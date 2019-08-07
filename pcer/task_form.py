import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication)
from PyQt5 import QtCore
from pcer_window import PcerWindow
from functools import partial

class TaskForm(PcerWindow):

    submit_answer = QtCore.pyqtSignal()
    read_code = QtCore.pyqtSignal()
    group_box = None

    def __init__(self, experiment):
        super(TaskForm, self).__init__(experiment)

    def initUI(self):
        submitButton = QPushButton("Submit answer")
        readButton = QPushButton("Read code")

        submitButton.clicked.connect(self.onSubmitButtonClick)
        readButton.clicked.connect(self.onReadButtonClick)

        task = self.experiment.getExperimentalTasks()
        self.group_box, self.choice_combo_question_pair = self.experiment.form_builder.build_task_form(task)
        self.vbox.addWidget(self.group_box)

        for ccq_pair in self.choice_combo_question_pair:
            cb = ccq_pair[1]
            cb.currentIndexChanged.connect(partial(self.choiceSelection, ccq_pair))

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        
        hbox.addWidget(submitButton)
        hbox.addWidget(readButton)

        self.vbox.addStretch(1)
        self.vbox.addLayout(hbox)
        
        self.setWindowTitle('Task presentation')

    def onSubmitButtonClick(self):
        self.experiment.finishCurrentTask()
        print("TaskForm.onSubmitButtonClick")
        self.submit_answer.emit()

    def onReadButtonClick(self):
        print("TaskForm.onReadButtonClick")
        self.read_code.emit()

    def choiceSelection(self,ccq_pair,i):
        print('Choice :',ccq_pair[1].currentText(), ' is selected for question ',ccq_pair[0])
        question = ccq_pair[0]
        choice = ccq_pair[1].currentText()
        self.experiment.setTaskData(question, choice)
