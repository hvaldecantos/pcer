from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication, QLabel, QComboBox, QGroupBox)
from PyQt5 import QtCore


class FormBuilder:

    def __init__(self):
        pass

    def build_pretest_form(self, experiment):
        pretests = experiment.resource.getPretests(experiment.participant_group)
        print('pretests')
        name = pretests['name']
        description = pretests['description']
        questions = pretests['questions']
        options = pretests['options']
        groupbox = QGroupBox(name)
        inner_vbox = QVBoxLayout()
        inner_vbox.addStretch(1)

        description_label = QLabel(description)
        for i in range(0,len(questions)):
            question_label = QLabel(questions[i])
            inner_vbox.addWidget(question_label)
            question_widgets.append(question_label)
            choiceCombo = QComboBox()
            for option in options:
                choiceCombo.addItem(option)
            inner_vbox.addWidget(choiceCombo)
    
        groupbox.setLayout(inner_vbox)
        return groupbox
    
