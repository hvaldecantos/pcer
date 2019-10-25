import sys
from PyQt5.QtWidgets import (QPushButton, QHBoxLayout)
from PyQt5 import QtCore
from pcer_window import PcerWindow
from functools import partial


class PretestForm(PcerWindow):

    submit_answer = QtCore.pyqtSignal()
    choice_combo_question_list = []
    group_box = None

    def __init__(self, experiment):
        super(PretestForm, self).__init__(experiment)


    def initUI(self):
        submitButton = QPushButton("Submit answer")
        submitButton.setStyleSheet('QPushButton {background-color: #fca395}')
        submitButton.clicked.connect(self.onSubmitButtonClick)

        self.group_box, self.choice_combo_question_list = self.experiment.form_builder.build_pretest_form(self.experiment)
        self.setExistingData()
        self.vbox.addWidget(self.group_box)

        for ccq_dict in self.choice_combo_question_list:
            cb = ccq_dict['combobox']
            cb.currentIndexChanged.connect(partial(self.choiceSelection, ccq_dict))

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(submitButton)

        self.vbox.addStretch(1)
        self.vbox.addLayout(hbox)
        self.setWindowTitle('Pretest')

    def setExistingData(self):
        current_pretest_data = self.experiment.session.getCurrentPretestState(self.experiment.participant_id)

        for question_id in current_pretest_data.keys():
            for question in self.choice_combo_question_list:
                if question_id == question['id']:
                    index = question['combobox'].findText(current_pretest_data[question_id]['answer'])
                    question['combobox'].setCurrentIndex(index)

    def areValidInputs(self):
        for ccq_dict in self.choice_combo_question_list:
            if ccq_dict['combobox'].currentText() == '--':
                return False
        return True

    def onSubmitButtonClick(self):
        print("PretestForm.onSubmitButtonClick")
        if self.areValidInputs():
            self.experiment.setPretestFinishedTrue()
            self.submit_answer.emit()
        else:
            self.popUpWarning('Enter all the answers')

    def choiceSelection(self,ccq_dict,i):
        print('Choice :',ccq_dict['combobox'].currentText(), ' is selected for question ',ccq_dict['question'])
        question = ccq_dict['question']
        choice = ccq_dict['combobox'].currentText()
        self.experiment.setPretestData(ccq_dict['id'], question, choice)
