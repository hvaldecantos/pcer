import unittest
import os
from pcer.session import Session
from pcer.participant_already_exist_error import ParticipantAlreadyExistError
from pcer.participant_does_not_exist_error import ParticipantDoesNotExistError
from pcer.current_system_already_exist_error import CurrentSystemAlreadyExistError
from pcer.system_already_exist_error import SystemAlreadyExistError
from pcer.wrong_current_system_error import WrongCurrentSystemError
from pcer.current_task_already_exist_error import CurrentTaskAlreadyExistError
from pcer.no_current_system_available_error import NoCurrentSystemAvailableError
from pcer.unfinishable_system_error import UnfinishableSystemError
from datetime import datetime
import re

import json

class TestSession(unittest.TestCase):

    def setUp(self):
        self.session = Session("tinydbTestSession.json", "experiment")

    def tearDown(self):
        self.session.close()
        os.remove("tinydbTestSession.json")

    """ Participant tests
    """
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

    """ Trial (Experimental systems) tests
    """
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
                         re.findall(r"^\d{4}\-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.\d{1}", trial['timestamp_start'])
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

    def test_get_current_system_id_and_index(self):
        self.session.addParticipant('1001', 'oo')

        self.session.setCurrentSystemId('1001', 'clock', True)
        self.session.setCurrentTaskId('1001', 'clock', 'objsinteracts')
        # print(json.dumps(self.session.getParticipantStatus('1001'), indent=4, sort_keys=False))
        system_id, idx = self.session.getCurrentSystemIdAndIndex('1001')
        self.assertEqual(system_id, 'clock')
        self.assertEqual(idx, 0)

        self.session.finishCurrentTask('1001')
        self.session.finishCurrentSystem('1001')
        self.session.setCurrentSystemId('1001', 'menu', False)
        self.session.setCurrentTaskId('1001', 'menu', 'objsinteracts')
        system_id, idx = self.session.getCurrentSystemIdAndIndex('1001')
        self.assertEqual(system_id, 'menu')
        self.assertEqual(idx, 1)

        self.session.finishCurrentTask('1001')
        self.session.finishCurrentSystem('1001')
        self.session.setCurrentSystemId('1001', 'spell', False)
        self.session.setCurrentTaskId('1001', 'spell', 'objsinteracts')
        system_id, idx = self.session.getCurrentSystemIdAndIndex('1001')
        self.assertEqual(system_id, 'spell')
        self.assertEqual(idx, 2)

    def test_get_current_system_id_when_there_is_no_current_system(self):
        self.session.addParticipant('1001', 'oo')
        self.assertEqual(self.session.getCurrentSystemId('1001'), None)

    def test_get_current_system_id_with_invalid_participant_id(self):
        self.session.addParticipant('1001', 'oo')
        self.session.setCurrentSystemId('1001', 'clock', True)
        with self.assertRaises(ParticipantDoesNotExistError):
            self.session.getCurrentSystemId('5005')

    def test_finishing_a_current_system_when_there_is_no_current_system(self):
        self.session.addParticipant('1001', 'oo')
        with self.assertRaises(NoCurrentSystemAvailableError):
            self.session.finishCurrentSystem('1001')

        self.session.setCurrentSystemId('1001', 'clock', True)
        self.session.setCurrentTaskId('1001', 'clock', 'objsinteracts')
        self.session.finishCurrentTask('1001')
        self.session.finishCurrentSystem('1001')
        with self.assertRaises(NoCurrentSystemAvailableError):
            self.session.finishCurrentSystem('1001')

    def test_finish_current_system_when_it_has_a_task_not_finished(self):
        self.session.addParticipant('1001', 'oo')
        self.session.setCurrentSystemId('1001', 'clock', True)
        self.session.setCurrentTaskId('1001', 'clock', 'objsinteracts')
        with self.assertRaises(UnfinishableSystemError):
            self.session.finishCurrentSystem('1001')

    def test_get_finished_warmup_systems(self):
        self.session.addParticipant('1001', 'oo')
        self.session.setCurrentSystemId('1001', 'clock', isWarmup = True)

        self.session.setCurrentTaskId('1001', 'clock', 'objsinteracts')
        self.session.finishCurrentTask('1001')

        self.session.setCurrentTaskId('1001', 'clock', 'implfeats')
        self.session.finishCurrentTask('1001')

        self.session.setCurrentTaskId('1001', 'clock', 'execflow')
        self.session.finishCurrentTask('1001')

        self.session.setCurrentTaskId('1001', 'clock', 'changedobjs')
        self.session.finishCurrentTask('1001')

        self.assertEqual(self.session.getFinishedWarmupSystemIds('1001'), [])
        self.session.finishCurrentSystem('1001')
        self.assertEqual(self.session.getFinishedWarmupSystemIds('1001'), ['clock'])

        self.session.setCurrentSystemId('1001', 'store', isWarmup = True)
        self.assertEqual(self.session.getFinishedWarmupSystemIds('1001'), ['clock'])

        self.session.setCurrentTaskId('1001', 'store', 'execflow')
        self.session.finishCurrentTask('1001')
        self.assertEqual(self.session.getFinishedWarmupSystemIds('1001'), ['clock'])

        self.session.finishCurrentSystem('1001')
        self.assertEqual(self.session.getFinishedWarmupSystemIds('1001'), ['clock', 'store'])

    """ Task tests
    """
    def test_set_current_task_id(self):
        self.session.addParticipant('1001', 'oo')
        self.session.setCurrentSystemId('1001', 'clock', True)

        timestamp = str(datetime.now())
        self.session.setCurrentTaskId('1001', 'clock', 'objsinteracts')
        status = self.session.getParticipantStatus('1001')
        current_task = status['trials'][0]['tasks'][0]

        self.assertEqual(re.findall(r"^\d{4}\-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.", timestamp),
                         re.findall(r"^\d{4}\-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.", current_task['timestamp_start'])
                        )
        self.assertEqual(current_task['finished'], False)
        self.assertEqual(current_task['questionnaire'], {})
        self.assertEqual(current_task['task_id'], 'objsinteracts')

    def test_adding_a_new_task_to_an_invalid_participant_id(self):
        self.session.addParticipant('1001', 'oo')
        self.session.setCurrentSystemId('1001', 'clock', True)
        with self.assertRaises(ParticipantDoesNotExistError):
            self.session.setCurrentTaskId('1000', 'clock', 'objsinteracts')

    def test_adding_a_new_task_when_there_is_no_current_system(self):
        self.session.addParticipant('1001', 'oo')
        with self.assertRaises(NoCurrentSystemAvailableError):
            self.session.setCurrentTaskId('1001', 'clock', 'objsinteracts')

    def test_adding_a_new_task_to_a_wrong_system_id(self):
        self.session.addParticipant('1001', 'oo')
        self.session.setCurrentSystemId('1001', 'clock', True)
        with self.assertRaises(WrongCurrentSystemError):
            self.session.setCurrentTaskId('1001', 'menu', 'objsinteracts')
    
    def test_adding_a_task_when_there_is_a_current_task_already(self):
        self.session.addParticipant('1001', 'oo')
        self.session.setCurrentSystemId('1001', 'library', False)
        self.session.setCurrentTaskId('1001', 'library', 'objsinteracts')

        with self.assertRaises(CurrentTaskAlreadyExistError):
            self.session.setCurrentTaskId('1001', 'library', 'execflow')

    def test_finish_current_task(self):
        self.session.addParticipant('1001', 'oo')
        self.session.setCurrentSystemId('1001', 'library', False)
        self.session.setCurrentTaskId('1001', 'library', 'objsinteracts')
        status = self.session.getParticipantStatus('1001')
        current_task = status['trials'][0]['tasks'][0]
        self.assertEqual(current_task['finished'], False)
        self.session.finishCurrentTask('1001')
        self.assertEqual(current_task['finished'], True)

    def test_set_current_task_data(self):
        #working on simple way to test this
        pass

    def test_get_current_system_finished_tasks(self):
        self.session.addParticipant('1001', 'oo')
        finished_tasks = self.session.getCurrentSystemFinishedTasks('1001')
        self.assertEqual(len(finished_tasks), 0)

        self.session.setCurrentSystemId('1001', 'clock', True)
        finished_tasks = self.session.getCurrentSystemFinishedTasks('1001')
        self.assertEqual(len(finished_tasks), 0)

        self.session.setCurrentTaskId('1001', 'clock', 'objsinteracts')
        finished_tasks = self.session.getCurrentSystemFinishedTasks('1001')
        self.assertEqual(len(finished_tasks), 0)

        self.session.finishCurrentTask('1001')
        finished_tasks = self.session.getCurrentSystemFinishedTasks('1001')
        self.assertEqual(len(finished_tasks), 1)

        self.session.setCurrentTaskId('1001', 'clock', 'implfeats')
        self.session.finishCurrentTask('1001')
        finished_tasks = self.session.getCurrentSystemFinishedTasks('1001')
        self.assertEqual(len(finished_tasks), 2)

        self.session.setCurrentTaskId('1001', 'clock', 'execflow')
        self.session.finishCurrentTask('1001')
        finished_tasks = self.session.getCurrentSystemFinishedTasks('1001')
        self.assertEqual(len(finished_tasks), 3)

        self.session.setCurrentTaskId('1001', 'clock', 'changedobjs')
        self.session.finishCurrentTask('1001')
        finished_tasks = self.session.getCurrentSystemFinishedTasks('1001')
        self.assertEqual(len(finished_tasks), 4)

        self.session.finishCurrentSystem('1001')
        self.session.setCurrentSystemId('1001', 'spell', True)
        self.session.setCurrentTaskId('1001', 'spell', 'changedobjs')
        self.session.finishCurrentTask('1001')
        finished_tasks = self.session.getCurrentSystemFinishedTasks('1001')
        self.assertEqual(len(finished_tasks), 1)


    """ Code viewer data tests
    """
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


if __name__ == '__main__':
    unittest.main()
