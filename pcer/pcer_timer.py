from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QTime, QTimer

class PcerTimer(QLabel):

	def __init__(self, minutes):
		super(PcerTimer, self).__init__()

		self.timer = QTimer(self)
		self.timer.timeout.connect(self.timerEvent)

		self.time = QTime(0, minutes, 0)

		self.setText(self.time.toString("mm:ss"))

	def timerEvent(self):
		self.setText(self.time.toString("mm:ss"))
		self.time = self.time.addSecs(-1)

	def start(self):
		self.timer.start(1000)
		self.timerEvent()

	def stop(self):
		self.timer.stop()
