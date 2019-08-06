from tinydb import TinyDB, Query
from participant_already_exist_error import ParticipantAlreadyExistError
from participant_does_not_exist_error import ParticipantDoesNotExistError
from current_system_already_exist_error import CurrentSystemAlreadyExistError
from system_already_exist_error import SystemAlreadyExistError
from current_task_already_exist_error import CurrentTaskAlreadyExistError
from wrong_current_system_error import WrongCurrentSystemError
from datetime import datetime


class Session():
    
    db = None
    participant = None
    
    def __init__(self, path, name):
        self.db = TinyDB(path, sort_keys=False, indent=4, default_table = name)
        self.participant = Query()

    def close(self):
        self.db.close()

    def existParticipant(self, id):
        return len(self.db.search(self.participant.id == id)) > 0

    def addParticipant(self, id, group):
        if self.existParticipant(id): 
            raise ParticipantAlreadyExistError(id)

        self.db.insert(
            {
                'id': id,
                'group': group,
                'warmup_finished': False,
                'experiment_finished': False,
                'trials': [],
                'pretest_data': {},
                'current_opened_filename': None,
                'scroll_displacements': {},
                'filenames_order': []
            }
        )

    def getParticipantStatus(self, id):
        status = self.db.search(self.participant.id == id)
        if len(status) <= 0: raise ParticipantDoesNotExistError(id)
        else: return status[0]

    def isWarmupSystemFinished(self, participant_id):
        return self.getParticipantStatus(participant_id)['warmup_finished']
    
    def getTrials(self, participant_id):
        status = self.getParticipantStatus(participant_id)
        return status['trials']

    def getCurrentSystemId(self, participant_id):
        current_system_id = None
        trials = self.getTrials(participant_id)
        for t in trials:
            if t['finished'] == False:
                current_system_id = t['system_id']
        return current_system_id

    def existExperimentalSystem(self, participant_id, system_id):
        trials = self.getTrials(participant_id)
        for t in trials:
            if t['system_id'] == system_id:
                return True
        return False

    def setCurrentSystemId(self, participant_id, system_id, isWarmup):
        current_system_id = self.getCurrentSystemId(participant_id)
        if self.existExperimentalSystem(participant_id, system_id): raise SystemAlreadyExistError(system_id)
        if current_system_id: raise CurrentSystemAlreadyExistError(current_system_id)

        trials = self.getTrials(participant_id)
        trials.append(
            {
                "timestamp": str(datetime.now()), 
                "finished": False,
                "tasks": [],
                "system_id": system_id, 
                "warmup": isWarmup
            }
        )
        self.db.update({'trials': trials}, self.participant.id == participant_id)

    def getCurrentTaskId(self, participant_id):
        current_task_id = None
        trials = self.getTrials(participant_id)
        for t in trials:
            if t['finished'] == False:
                tasks = t['tasks']
                break

        for t in tasks:
            if t['finished'] == False:
                current_task_id = t['task_id']
                break            
        return current_task_id

    def setCurrentTaskId(self, participant_id, system_id, task_id):

        current_system_id = self.getCurrentSystemId(participant_id)
        if current_system_id != system_id: raise WrongCurrentSystemError(system_id)

        current_task_id = self.getCurrentTaskId(participant_id)
        if current_task_id: raise CurrentTaskAlreadyExistError(system_id, task_id)

        trials = self.getTrials(participant_id)

        trial_index = None
        tasks = None
        for i in range(len(trials)):
             if trials[i]['system_id'] == system_id:
                tasks = trials[i]['tasks']
                trial_index = i
                break

        tasks.append(
            {
                "timestamp": str(datetime.now()), 
                "finished": False, 
                "answers": { }, 
                "task_id": task_id
            }
        )

        trials[trial_index]['tasks'] = tasks
        self.db.update({'trials': trials}, self.participant.id == participant_id)

    def setPretestData(self, pretest_data, participant_id):
        self.db.update({'pretest_data': pretest_data}, self.participant.id == participant_id)

    def getScrollDisplacements(self, participant_id):
        status = self.getParticipantStatus(participant_id)
        return status['scroll_displacements']

    def setScrollDisplacements(self, participant_id, displacement_dict):
        self.db.update({'scroll_displacements': displacement_dict}, self.participant.id == participant_id)

    def getCurrentOpenedFilename(self, participant_id):
        status = self.getParticipantStatus(participant_id)
        return status['current_opened_filename']

    def setCurrentOpenedFilename(self, participant_id, filename):
        self.db.update({'current_opened_filename': filename}, self.participant.id == participant_id)

    def setFilenamesOrder(self, participant_id, filename_list):
        self.db.update({'filenames_order': filename_list}, self.participant.id == participant_id)

    def getFilenamesOrder(self, participant_id):
        status = self.getParticipantStatus(participant_id)
        return status['filenames_order']