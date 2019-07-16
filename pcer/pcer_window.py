import yaml
from PyQt5.QtWidgets import QWidget, QDesktopWidget
from PyQt5 import QtCore

class PcerWindow(QWidget):

    experiment = None

    def __init__(self, experiment):
        super(PcerWindow, self).__init__()
        self.experiment = experiment

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

    def centerOnScreen (self):
        resolution = QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))
        print(resolution.height())
