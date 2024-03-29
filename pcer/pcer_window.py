import yaml
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QVBoxLayout, QStatusBar, QMessageBox
from PyQt5 import QtCore
from pcer_timer import PcerTimer
import time

class PcerWindow(QWidget):

    experiment = None
    vbox = None
    statusBar = None
    start = None

    def __init__(self, experiment):
        super(PcerWindow, self).__init__()
        if self.start is None:
            self.start = time.time()
        self.experiment = experiment
        self.vbox = QVBoxLayout()
        self.statusBar = QStatusBar()
        self.setParticipantIdGroupInStatusBar(experiment.participant_id, experiment.participant_group)
        self.initBaseUI()

        self.initUI() # invokes method in subclass
        self.setStatusBar()
        self.setLayout(self.vbox)

    def initBaseUI(self):
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        with open("config.yml", "r") as stream:
            try:
                self.config = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        self.width = self.config['window_size']['width']
        self.height = self.config['window_size']['height']
        self.setFixedSize(self.width, self.height)
        self.centerOnScreen()

    def setStatusBar(self):
        self.statusBar.setSizeGripEnabled(False)
        self.vbox.addWidget(self.statusBar)
        self.statusBar.setStyleSheet("background: rgba(250, 250, 250)")

    def setParticipantIdGroupInStatusBar(self, id, group):
        self.statusBar.showMessage("[ID: " + str(id) + " - Group: " + str(group) + "]")

    def addTimer(self, timer):
        self.statusBar.insertPermanentWidget(0, timer)
        timer.show()

    def centerOnScreen (self):
        resolution = QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))
        print("Monitor resolution: %d (w) x %d (h)" % (resolution.width(), resolution.height()))

    def popUpWarning(self, msg):
        warning = QMessageBox()
        warning.setIcon(QMessageBox.Warning)
        warning.setText(msg)
        warning.setWindowTitle('Warning')
        warning.setStandardButtons(QMessageBox.Ok)
        warning.exec_()
