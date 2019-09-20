from PyQt5.QtWidgets import (QVBoxLayout, QLabel, QComboBox, QGroupBox)
from PyQt5.QtGui import QFont
import yaml

class FormBuilder:

    def __init__(self):
        config = yaml.load(open("config.yml"), Loader = yaml.SafeLoader)
        self.font_type = config['form']['font']['type']
        self.title_size = config['form']['font']['title_size']
        self.title_bold = config['form']['font']['title_bold']
        self.description_size = config['form']['font']['description_size']
        self.end_title = config['form']['end']['title']
        self.end_msg = config['form']['end']['message']

    def getTitleFont(self, bold = True):
        font = QFont(self.font_type)
        font.setFixedPitch(True)
        font.setPixelSize(self.title_size)
        font.setBold(self.title_bold and bold)
        return font

    def getDescriptionFont(self):
        font = QFont(self.font_type)
        font.setFixedPitch(True)
        font.setPixelSize(self.description_size)
        font.setBold(False)
        return font

    def build_pretest_form(self, experiment):
        pretests = experiment.resource.getPretests(experiment.participant_group)
        name = pretests['name']
        description = pretests['description']
        questions = pretests['questions']
        options = pretests['options']

        groupbox = QGroupBox(name)
        groupbox.setFont(self.getTitleFont())
        inner_vbox = QVBoxLayout()
        inner_vbox.addStretch(1)
        choice_combo_question_list = []

        description_label = QLabel(description)
        description_label.setFont(self.getDescriptionFont())
        for i in range(0,len(questions)):
            question_label = QLabel(questions[i])
            question_label.setFont(self.getTitleFont(False))
            inner_vbox.addWidget(question_label)
            #question_widgets.append(question_label)
            choiceCombo = QComboBox()
            choiceCombo.setFont(self.getDescriptionFont())
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
        description_label.setWordWrap(True)
        description_label.setFont(self.getDescriptionFont())
        group_box = QGroupBox(name)
        group_box.setFont(self.getTitleFont())
        inner_vbox = QVBoxLayout()
        inner_vbox.addWidget(description_label)
        group_box.setLayout(inner_vbox)
        return group_box

    def build_end_message(self):
        name = self.end_title
        description = self.end_msg
        description_label = QLabel(description)
        description_label.setWordWrap(True)
        description_label.setFont(self.getDescriptionFont())
        group_box = QGroupBox(name)
        group_box.setFont(self.getTitleFont())
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
        description_label.setFont(self.getDescriptionFont())
        description_label.setWordWrap(True)
        group_box = QGroupBox(name)
        group_box.setFont(self.getTitleFont())
        inner_vbox = QVBoxLayout()
        inner_vbox.addWidget(description_label)
        inner_vbox.addWidget(QLabel(""))
        inner_vbox.addStretch(1)
        inner_vbox.setSpacing(10);

        for i in range(0,len(questions)):
            question_label = QLabel(questions[i])
            question_label.setFont(self.getTitleFont(False))
            question_label.setWordWrap(True)
            inner_vbox.addWidget(question_label)
            choiceCombo = QComboBox()
            choiceCombo.setFont(self.getDescriptionFont())
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
