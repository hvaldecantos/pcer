from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication, QLabel, QComboBox, QGroupBox)
from PyQt5 import QtCore
from PyQt5.QtGui import QFont

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
        choice_combo_question_list = []

        description_label = QLabel(description)
        for i in range(0,len(questions)):
            question_label = QLabel(questions[i])
            inner_vbox.addWidget(question_label)
            #question_widgets.append(question_label)
            choiceCombo = QComboBox()
            for option in options:
                choiceCombo.addItem(option)
            choice_combo_question_dict = {}
            choice_combo_question_dict['id'] = 'Q'+str(i+1)
            choice_combo_question_dict['question'] = questions[i]
            choice_combo_question_dict['combobox'] = choiceCombo
            choice_combo_question_list.append(choice_combo_question_dict)
            inner_vbox.addWidget(choiceCombo)

        groupbox.setLayout(inner_vbox)
        return groupbox, choice_combo_question_list

    def build_system_form(self, system):
        name = system['name']
        description = system['description']
        system_id = system['id']
        description_label = QLabel(description)
        description_label.setFont(QFont('Verdana', 12))
        group_box = QGroupBox(name)
        group_box.setFont(QFont('Arial', 16))
        inner_vbox = QVBoxLayout()
        inner_vbox.addWidget(description_label)
        group_box.setLayout(inner_vbox)
        return group_box

    def build_task_form(self, task):
        choice_combo_question_list = []
        task_id = task['id']
        name = task['name']
        description = task['description']
        questions = task['questions']
        options = task['options']
        description_label = QLabel(description)
        description_label.setFont(QFont('Verdana', 12))
        description_label.setWordWrap(True)
        group_box = QGroupBox(name)
        group_box.setFont(QFont('Arial', 16))
        inner_vbox = QVBoxLayout()
        inner_vbox.addWidget(description_label)
        inner_vbox.addStretch(1)
        inner_vbox.setSpacing(10);

        for i in range(0,len(questions)):
            question_label = QLabel(questions[i])
            question_label.setFont(QFont('Arial', 16))
            inner_vbox.addWidget(question_label)
            choiceCombo = QComboBox()
            choiceCombo.setFont(QFont('Verdana', 12))
            for option in options:
                choiceCombo.addItem(option)
            choice_combo_question_dict = {}
            choice_combo_question_dict['id'] = 'Q'+str(i+1)
            choice_combo_question_dict['question'] = questions[i]
            choice_combo_question_dict['combobox'] = choiceCombo
            choice_combo_question_list.append(choice_combo_question_dict)
            inner_vbox.addWidget(choiceCombo)
        group_box.setLayout(inner_vbox)
        return group_box, choice_combo_question_list


