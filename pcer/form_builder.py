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
        choice_combo_question_pair = []

        description_label = QLabel(description)
        for i in range(0,len(questions)):
            question_label = QLabel(questions[i])
            inner_vbox.addWidget(question_label)
            #question_widgets.append(question_label)
            choiceCombo = QComboBox()
            for option in options:
                choiceCombo.addItem(option)
            choice_combo_question_pair.append([questions[i], choiceCombo])
            inner_vbox.addWidget(choiceCombo)

        groupbox.setLayout(inner_vbox)
        return groupbox, choice_combo_question_pair

    def build_system_form(self, system):
        name = system['name']
        description = system['description']
        system_id = system['id']
        description_label = QLabel(description)
        group_box = QGroupBox(name)
        inner_vbox = QVBoxLayout()
        inner_vbox.addWidget(description_label)
        group_box.setLayout(inner_vbox)
        return group_box

    def build_task_form(self, task):
        choice_combo_question_pair = []
        task_id = task['id']
        name = task['name']
        description = task['description']
        questions = task['questions']
        options = task['options']
        description_label = QLabel(description)
        group_box = QGroupBox(name)
        inner_vbox = QVBoxLayout()
        inner_vbox.addWidget(description_label)
        for i in range(0,len(questions)):
            question_label = QLabel(questions[i])
            inner_vbox.addWidget(question_label)
            choiceCombo = QComboBox()
            for option in options:
                choiceCombo.addItem(option)
            choice_combo_question_pair.append([questions[i], choiceCombo])
            inner_vbox.addWidget(choiceCombo)
        group_box.setLayout(inner_vbox)
        return group_box, choice_combo_question_pair


