from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5 import QtCore

class PcerTimer(QLabel):

	timeout_signal = QtCore.pyqtSignal()

	minute = None
	second = None

	def __init__(self):
		super(PcerTimer, self).__init__()

		self.timer = QTimer(self)
		self.timer.timeout.connect(self.timerEvent)

	def setTime(self, minutes, seconds):
		self.minute = minutes
		self.second = seconds
		self.setText("%02d:%02d" % (self.minute, self.second))

	def decreaseOneSecond(self):
		self.second = self.second - 1
		if(self.timeIsOver()): self.timout_event()
		if(self.second < 0):
			if(self.minute <= 0):
				self.second = 0
			else:
				self.minute = self.minute - 1
				self.second = 59

	def timerEvent(self):
		self.decreaseOneSecond()
		self.setText("%02d:%02d" % (self.minute, self.second))

	def timout_event(self):
		self.setText("%02d:%02d" % (self.minute, self.second))
		self.timeout_signal.emit()

	def timeIsOver(self):
		return (self.minute == 0 and self.second == 0)

	def start(self):
		self.timer.start(1000)

	def stop(self):
		self.timer.stop()
