import unittest
import os
from pcer.experiment import Experiment
from pcer.participant_already_exist_error import ParticipantAlreadyExistError

class TestExperiment(unittest.TestCase):

    def setUp(self):
        self.experiment = Experiment("tinydbTestExperiment.json")

    def tearDown(self):
        self.experiment.session.close()
        os.remove("tinydbTestExperiment.json")

    def test_active_participant(self):
        self.assertFalse(self.experiment.hasActiveParticipant())
        self.experiment.setCurrentParticipant('1234', 'dci')
        self.assertTrue(self.experiment.hasActiveParticipant())

    def test_add_participants(self):
        self.assertFalse(self.experiment.hasActiveParticipant())
        self.experiment.addParticipant('1234', 'dci')
        self.assertTrue(self.experiment.hasActiveParticipant())
        with self.assertRaises(ParticipantAlreadyExistError):
            self.experiment.addParticipant('1234', 'dci')


    def test_get_experimental_system_filenames(self):
        self.experiment.addParticipant('1234', 'dci')
        system = self.experiment.getExperimentalSystem()

        filenames = self.experiment.getExperimentalSystemFilenames()
        filenames_resource = self.experiment.resource.getExperimentalSystemFilenames(self.experiment.participant_group, system['id'])

        for filename in filenames:
            self.assertTrue(filename in filenames_resource)

    def test_clear_experimental_system_filenames(self):
        self.experiment.addParticipant('1234', 'dci')
        system = self.experiment.getExperimentalSystem() # adds a system in trials

        filenames = self.experiment.getExperimentalSystemFilenames()
        self.assertTrue(len(filenames) > 0)

        filenames_session = self.experiment.session.getFilenamesOrder(self.experiment.participant_id)
        self.assertTrue(len(filenames_session) > 0)

        self.experiment.clearExperimentalSystemFilenames()

        filenames_session = self.experiment.session.getFilenamesOrder(self.experiment.participant_id)
        self.assertTrue(len(filenames_session) == 0)


if __name__ == '__main__':
    unittest.main()
