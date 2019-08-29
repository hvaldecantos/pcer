import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication, QLabel, QComboBox, QGroupBox, QMessageBox)
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
        submitButton.clicked.connect(self.onSubmitButtonClick)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(submitButton)

        self.group_box, self.choice_combo_question_list = self.experiment.form_builder.build_pretest_form(self.experiment)

        for ccq_dict in self.choice_combo_question_list:
            cb = ccq_dict['combobox']
            cb.currentIndexChanged.connect(partial(self.choiceSelection, ccq_dict))

        self.vbox.addWidget(self.group_box)
        self.vbox.addStretch(1)
        self.vbox.addLayout(hbox)
        self.setWindowTitle('Pretest')

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

    def popUpWarning(self, msg):
        warning = QMessageBox()
        warning.setIcon(QMessageBox.Warning)
        warning.setText(msg)
        warning.setWindowTitle('Warning')
        warning.setStandardButtons(QMessageBox.Ok)
        warning.exec_()