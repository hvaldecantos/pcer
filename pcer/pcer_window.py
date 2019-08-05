import yaml
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QVBoxLayout, QStatusBar, QLabel
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
        self.statusBar = QStatusBar()
        self.statusBar.setSizeGripEnabled(False)
        self.statusBar.insertWidget(0, QLabel("Message 1"))
        self.statusBar.insertWidget(1, QLabel("Message 2"))
        self.vbox.addWidget(self.statusBar)
        self.statusBar.setStyleSheet("background: rgba(250, 250, 250)")

    def addTimer(self, timer):
        self.statusBar.insertPermanentWidget(2, timer)
        timer.show()

    def centerOnScreen (self):
        resolution = QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))
        print(resolution.height())
