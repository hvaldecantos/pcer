import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication, QLabel, QComboBox, QGroupBox)
from PyQt5 import QtCore
from pcer_window import PcerWindow
from functools import partial


class PretestForm(PcerWindow):

    submit_answer = QtCore.pyqtSignal()
    choice_combo_question_pair = []
    group_box = None

    def __init__(self, experiment):
        super(PretestForm, self).__init__(experiment)


    def initUI(self):
        submitButton = QPushButton("Submit answer")
        submitButton.clicked.connect(self.onSubmitButtonClick)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(submitButton)

        self.group_box, self.choice_combo_question_pair = self.experiment.form_builder.build_pretest_form(self.experiment)

        for ccq_pair in self.choice_combo_question_pair:
            cb = ccq_pair[1]
            cb.currentIndexChanged.connect(partial(self.choiceSelection, ccq_pair))

        self.vbox.addWidget(self.group_box)
        self.vbox.addStretch(1)
        self.vbox.addLayout(hbox)
        self.setWindowTitle('Pretest')

    def onSubmitButtonClick(self):
        print("PretestForm.onSubmitButtonClick")
        self.submit_answer.emit()

    def choiceSelection(self,ccq_pair,i):
        print('Choice :',ccq_pair[1].currentText(), ' is selected for question ',ccq_pair[0])
        question = ccq_pair[0]
        choice = ccq_pair[1].currentText()
        self.experiment.setPretestData(question, choice)
