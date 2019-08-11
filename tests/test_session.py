import unittest
import os
from pcer.session import Session
from pcer.participant_already_exist_error import ParticipantAlreadyExistError
from pcer.participant_does_not_exist_error import ParticipantDoesNotExistError
from pcer.current_system_already_exist_error import CurrentSystemAlreadyExistError
from pcer.system_already_exist_error import SystemAlreadyExistError
from pcer.wrong_current_system_error import WrongCurrentSystemError
from pcer.current_task_already_exist_error import CurrentTaskAlreadyExistError
from datetime import datetime
import re


class TestSession(unittest.TestCase):

    def setUp(self):
        self.session = Session("tinydbTestSession.json", "experiment")

    def tearDown(self):
        self.session.close()
        os.remove("tinydbTestSession.json")

    def test_add_participant(self):
        self.assertEqual(len(self.session.db.all()), 0)
        self.assertEqual(self.session.existParticipant('1001'), False)

        self.session.addParticipant('1001', 'oo')
        self.assertEqual(self.session.existParticipant('1001'), True)
        self.assertEqual(len(self.session.db.all()), 1)
        
        self.session.addParticipant('1002', 'oo')
        self.assertEqual(len(self.session.db.all()), 2)

    def test_participant_already_exists(self):
        self.session.addParticipant('1001', 'oo')
        with self.assertRaises(ParticipantAlreadyExistError):
            self.session.addParticipant('1001', 'oo')

    def test_initial_participant_status(self):
        self.session.addParticipant('1001', 'oo')
        status = self.session.getParticipantStatus('1001')

        initial_status = {u'trials': [],
                          u'group': u'oo',
                          u'id': u'1001',
                          u'warmup_finished': False,
                          u'experiment_finished': False,
                          u'pretest_data': {},
                          u'current_opened_filename': None,
                          u'scroll_displacements': {},
                          u'filenames_order': []}

        self.assertEqual(status, initial_status)

    def test_experimental_system_existance(self):
        self.session.addParticipant('1001', 'oo')
        self.assertFalse(self.session.existExperimentalSystem('1001', 'library'))
        self.session.setCurrentSystemId('1001', 'library', False)
        self.assertTrue(self.session.existExperimentalSystem('1001', 'library'))

    def test_adding_a_new_trial_system(self):
        self.session.addParticipant('1001', 'oo')
        
        timestamp = str(datetime.now())
        self.session.setCurrentSystemId('1001', 'library', False)
        status = self.session.getParticipantStatus('1001')
        trial = status['trials'][0]

        self.assertEqual(re.findall(r"^\d{4}\-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.\d{1}", timestamp),
                         re.findall(r"^\d{4}\-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.\d{1}", trial['timestamp'])
                        )
        self.assertEqual(trial['finished'], False)
        self.assertEqual(trial['tasks'], [])
        self.assertEqual(trial['system_id'], 'library')
        self.assertEqual(trial['warmup'], False)

    def test_adding_a_new_trial_with_a_system_id_that_already_exists(self):
        self.session.addParticipant('1001', 'oo')
        self.session.setCurrentSystemId('1001', 'library', False)
        with self.assertRaises(SystemAlreadyExistError):
            self.session.setCurrentSystemId('1001', 'library', False)

    def test_adding_a_new_trial_system_to_a_invalid_participant_id(self):
        self.session.addParticipant('1001', 'oo')
        with self.assertRaises(ParticipantDoesNotExistError):
            self.session.setCurrentSystemId('5005', 'library', False)

    def test_adding_a_new_trial_system_when_there_is_a_current_system_already(self):
        self.session.addParticipant('1001', 'oo')
        self.session.setCurrentSystemId('1001', 'library', False)
        with self.assertRaises(CurrentSystemAlreadyExistError):
            self.session.setCurrentSystemId('1001', 'menu', False)

    def test_get_current_system_id(self):
        self.session.addParticipant('1001', 'oo')
        self.session.setCurrentSystemId('1001', 'clock', True)
        self.assertEqual(self.session.getCurrentSystemId('1001'), 'clock')

    def test_get_current_system_id_when_there_is_no_current_system(self):
        self.session.addParticipant('1001', 'oo')
        self.assertEqual(self.session.getCurrentSystemId('1001'), None)

    def test_get_current_system_id_with_invalid_participant_id(self):
        self.session.addParticipant('1001', 'oo')
        self.session.setCurrentSystemId('1001', 'clock', True)
        with self.assertRaises(ParticipantDoesNotExistError):
            self.session.getCurrentSystemId('5005')

    def test_set_current_task_id(self):
        self.session.addParticipant('1001', 'oo')
        self.session.setCurrentSystemId('1001', 'clock', True)

        timestamp = str(datetime.now())
        self.session.setCurrentTaskId('1001', 'clock', 'objsinteracts')
        status = self.session.getParticipantStatus('1001')
        current_task = status['trials'][0]['tasks'][0]

        self.assertEqual(re.findall(r"^\d{4}\-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.", timestamp),
                         re.findall(r"^\d{4}\-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.", current_task['timestamp'])
                        )
        self.assertEqual(current_task['finished'], False)
        self.assertEqual(current_task['questionnaire'], {})
        self.assertEqual(current_task['task_id'], 'objsinteracts')

    def test_adding_a_new_task_to_a_invalid_participant_id(self):
        self.session.addParticipant('1001', 'oo')
        self.session.setCurrentSystemId('1001', 'clock', True)
        with self.assertRaises(ParticipantDoesNotExistError):
            self.session.setCurrentTaskId('1000', 'clock', 'objsinteracts')

    def test_adding_a_new_task_to_a_wrong_system_id(self):
        self.session.addParticipant('1001', 'oo')
        with self.assertRaises(WrongCurrentSystemError):
            self.session.setCurrentTaskId('1001', 'clock', 'objsinteracts')

        self.session.setCurrentSystemId('1001', 'clock', True)
        with self.assertRaises(WrongCurrentSystemError):
            self.session.setCurrentTaskId('1001', 'menu', 'objsinteracts')
    
    def test_adding_a_task_when_there_is_a_current_task_already(self):
        self.session.addParticipant('1001', 'oo')
        self.session.setCurrentSystemId('1001', 'library', False)
        self.session.setCurrentTaskId('1001', 'library', 'objsinteracts')

        with self.assertRaises(CurrentTaskAlreadyExistError):
            self.session.setCurrentTaskId('1001', 'library', 'execflow')

    def test_scroll_displacement_data(self):
        self.session.addParticipant('1001', 'oo')
        self.assertEqual(self.session.getScrollDisplacements('1001'), {})

        self.session.setScrollDisplacements('1001', {'filename1.java': 126})
        displacements = self.session.getScrollDisplacements('1001')
        self.assertEqual(displacements['filename1.java'], 126)

    def test_current_opened_filenamed(self):
        self.session.addParticipant('1001', 'oo')
        self.assertEqual(self.session.getCurrentOpenedFilename('1001'), None)

        self.session.setCurrentOpenedFilename('1001', 'filename1.java')
        current_opened_filename = self.session.getCurrentOpenedFilename('1001')
        self.assertEqual(current_opened_filename, 'filename1.java')

    def test_finish_current_task(self):
        self.session.addParticipant('1001', 'oo')
        self.session.setCurrentSystemId('1001', 'library', False)
        self.session.setCurrentTaskId('1001', 'library', 'objsinteracts')
        status = self.session.getParticipantStatus('1001')
        current_task = status['trials'][0]['tasks'][0]
        self.session.finishCurrentTask('1001')
        self.assertEqual(current_task['finished'], True)

    def test_set_current_task_data(self):
        #working on simple way to test this
        pass

    def test_get_finished_task(self):
        self.session.addParticipant('1001', 'oo')
        self.session.setCurrentSystemId('1001', 'library', False)
        #self.session.setCurrentTaskId('1001', 'library', 'objsinteracts')
        self.assertEqual(self.session.getFinishedTasks('1001'), [])

        task_list1 = [
                        {
                            "timestamp": "2019-08-08 15:58:41.128000",
                            "finished": True,
                            "questionnaire": {
                                "Q1": {
                                    "answer": "dk",
                                    "question": "The Timer role-player object requires a Clock role-player object to update its time."
                                },
                                "Q3": {
                                    "answer": "dk",
                                    "question": "A Clock role-player object invokes update on another Clock role-player object."
                                },
                                "Q2": {
                                    "answer": "dk",
                                    "question": "A Clock role-player object uses a Timer role-player object to update its time."
                                }
                            },
                            "task_id": "objsinteracts"
                        }
                    ]
        self.session.addParticipant('1002', 'oo')
        self.session.setCurrentSystemId('1002', 'library', False)
        self.session.setCurrentTaskId('1002', 'library', 'objsinteracts')
        self.session.finishCurrentTask('1002')
        self.assertEqual(self.session.getFinishedTasks('1002'), task_list1)

        task_list2 = [
                        {
                            "timestamp": "2019-08-08 15:58:41.128000",
                            "finished": False,
                            "questionnaire": {
                                "Q1": {
                                    "answer": "dk",
                                    "question": "The Timer role-player object requires a Clock role-player object to update its time."
                                },
                                "Q3": {
                                    "answer": "dk",
                                    "question": "A Clock role-player object invokes update on another Clock role-player object."
                                },
                                "Q2": {
                                    "answer": "dk",
                                    "question": "A Clock role-player object uses a Timer role-player object to update its time."
                                }
                            },
                            "task_id": "objsinteracts"
                        }]
        self.session.addParticipant('1003', 'oo')
        self.session.setCurrentSystemId('1003', 'library', False)
        self.session.setCurrentTaskId('1003', 'library', 'objsinteracts')
        self.assertEqual(self.session.getFinishedTasks('1003'), [])

if __name__ == '__main__':
    unittest.main()
