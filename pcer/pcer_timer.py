from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5 import QtCore

class PcerTimer(QLabel):

	timeout_signal = QtCore.pyqtSignal()

	minute = None
	second = None

	def __init__(self, minutes):
		super(PcerTimer, self).__init__()

		self.timer = QTimer(self)
		self.timer.timeout.connect(self.timerEvent)

		self.minute = 0
		self.second = minutes

		self.setText("%02d:%02d" % (self.minute, self.second))

	def countDownBySecond(self):
		self.second = self.second - 1
		if(self.second < 0):
			self.minute = self.minute - 1
			self.second = 59
		if(self.minute < 0):
			self.timout_event()

	def timerEvent(self):
		self.setText("%02d:%02d" % (self.minute, self.second))
		self.countDownBySecond()

	def timout_event(self):
		self.timeout_signal.emit()

	def timeIsOver(self):
		return (self.minute < 0)

	def start(self):
		self.timer.start(1000)
		self.timerEvent()

	def stop(self):
		self.timer.stop()
