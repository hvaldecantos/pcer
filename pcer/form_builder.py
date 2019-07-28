from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication, QLabel, QComboBox, QGroupBox)
from PyQt5 import QtCore


class FormBuilder:

    def __init__(self):
        pass

    def build_pretest_form(self):
        groupbox = QGroupBox('Pretest')
        inner_vbox = QVBoxLayout()
        inner_vbox.addStretch(1)

        # < temporary code: this code should build from the
        # questions in the pretest.yml file, and more ...
        #groups_dir = os.listdir(self.experiment.resource.path)
        #os.path.join(groups_dir)
        #print('Path : ',self.experiment.resource.path+'\\'+participant_group+'\\'+)
        questions = ['qwe','asd','zxc','try']
        options = ['a','b','c','d']
        question_widgets = []
        answer_widgets = []
        print('Here')
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
    
