import sys
from PyQt5.QtWidgets import QApplication
from experiment_controller import ExperimentController

if __name__ == '__main__':
    app = QApplication(sys.argv)
    c = ExperimentController()
    c.show_participant_form()
    sys.exit(app.exec_())
