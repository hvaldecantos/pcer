import unittest
import os
from pcer.experiment import Experiment
import re


class TestSession(unittest.TestCase):

    def setUp(self):
        self.experiment = Experiment()

    def test_active_participant(self):
        self.assertFalse(self.experiment.hasActiveParticipant())
        self.experiment.setCurrentParticipant('1234', 'dci')
        self.assertTrue(self.experiment.hasActiveParticipant())

if __name__ == '__main__':
    unittest.main()
