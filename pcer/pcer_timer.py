from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QTime, QTimer

class PcerTimer(QLabel):

	def __init__(self, minutes):
		super(PcerTimer, self).__init__()

		timer = QTimer(self)
		timer.timeout.connect(self.timerEvent)
		timer.start(1000)

		self.time = QTime(0, minutes, 0)

		self.timerEvent()

	def timerEvent(self):
		self.setText(self.time.toString("mm:ss"))
		self.time = self.time.addSecs(-1)
