from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5 import QtCore

class PcerTimer(QLabel):

	timeout_signal = QtCore.pyqtSignal()

	minute = None
	second = None
	experiment = None

	def __init__(self, experiment):
		super(PcerTimer, self).__init__()
		self.experiment = experiment
		self.timer = QTimer(self)
		self.timer.timeout.connect(self.timerEvent)

	def setTime(self, time):
		self.minute = time['minute']
		self.second = time['second']
		self.setText("%02d:%02d" % (self.minute, self.second))

	def decreaseOneSecond(self):
		self.second = self.second - 1
		if(self.timeIsOver()):
			self.timout_event()
		if(self.second < 0):
			if(self.minute <= 0):
				self.second = 0
			else:
				self.minute = self.minute - 1
				self.second = 59
		self.experiment.setTimerTime({'minute': self.minute, 'second': self.second})

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
