import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from experiment_controller import ExperimentController

if __name__ == '__main__':
    app = QApplication(sys.argv)
    timer = QTimer()
    c = ExperimentController()
    c.show_participant_form()
    sys.exit(app.exec_())
