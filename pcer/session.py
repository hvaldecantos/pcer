from tinydb import TinyDB, Query
from participant_already_exist_error import ParticipantAlreadyExistError
from participant_does_not_exist_error import ParticipantDoesNotExistError
from current_system_already_exist_error import CurrentSystemAlreadyExistError
from system_already_exist_error import SystemAlreadyExistError
from current_task_already_exist_error import CurrentTaskAlreadyExistError
from wrong_current_system_error import WrongCurrentSystemError
from no_current_system_available_error import NoCurrentSystemAvailableError
from unfinishable_system_error import UnfinishableSystemError
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

    def getCurrentSystemIdAndIndex(self, participant_id):
        current_system_id = None
        trial_index = None

        trials = self.getTrials(participant_id)

        for i in range(len(trials)):
            if trials[i]['finished'] == False:
                current_system_id = trials[i]['system_id']
                trial_index = i
                break

        return current_system_id, trial_index

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
                "timestamp_start": str(datetime.now()),
                "timestamp_end": None,
                "finished": False,
                "tasks": [],
                "system_id": system_id, 
                "warmup": isWarmup,
            }
        )
        self.db.update({'trials': trials}, self.participant.id == participant_id)

    def finishCurrentSystem(self, participant_id):
        current_system_id = self.getCurrentSystemId(participant_id)
        if not current_system_id: raise NoCurrentSystemAvailableError(participant_id)
        current_task_id = self.getCurrentTaskId(participant_id)
        if current_task_id: raise UnfinishableSystemError(current_system_id, "The 'system_id': '%s' cannot be finished with the unfinished 'task_id': '%s'." % (current_system_id, current_task_id))
        tasks = self.getTasks(participant_id, current_system_id)
        if len(tasks) == 0: raise UnfinishableSystemError(current_system_id, "You cannot finished a system with no tasks")

        trials = self.getTrials(participant_id)

        for t in trials:
            if t['system_id'] == current_system_id:
                t['finished'] = True
                break

        self.db.update({'trials': trials}, self.participant.id == participant_id)

    def getTasks(self, participant_id, system_id):
        tasks = None
        trials = self.getTrials(participant_id)
        for t in trials:
            if t['system_id'] == system_id:
                tasks = t['tasks']
                break
        return tasks

    def getCurrentTask(self, participant_id):
        current_task = None
        current_system_id = self.getCurrentSystemId(participant_id)
        tasks = self.getTasks(participant_id, current_system_id)
        for t in tasks:
            if t['finished'] == False:
                current_task = t
                break
        return current_task

    def getCurrentTaskId(self, participant_id):
        current_task_id = None
        task = self.getCurrentTask(participant_id)
        if task: current_task_id = task['task_id']
        return current_task_id

    def setCurrentTaskId(self, participant_id, system_id, task_id):
        current_system_id, i = self.getCurrentSystemIdAndIndex(participant_id)
        if not current_system_id: raise NoCurrentSystemAvailableError(participant_id)
        if current_system_id != system_id: raise WrongCurrentSystemError(system_id)

        current_task_id = self.getCurrentTaskId(participant_id)
        if current_task_id: raise CurrentTaskAlreadyExistError(system_id, task_id)

        trials = self.getTrials(participant_id)
        tasks = self.getTasks(participant_id, system_id)

        tasks.append(
            {
                "timestamp_start": str(datetime.now()),
                "finished": False, 
                "questionnaire": { },
                "task_id": task_id
            }
        )

        trials[i]['tasks'] = tasks
        self.db.update({'trials': trials}, self.participant.id == participant_id)

    def finishCurrentTask(self, participant_id):
        current_system_id = self.getCurrentSystemId(participant_id)
        current_task_id = self.getCurrentTaskId(participant_id)
        trials = self.getTrials(participant_id)
        print('Setting task to finished')
        for t in trials:
            if t['system_id'] == current_system_id:
                for task in t['tasks']:
                    if task['task_id'] == current_task_id:
                        task['finished'] = True
                        task['timestamp_end'] = str(datetime.now())
                        break
        self.db.update({'trials': trials}, self.participant.id == participant_id)

    def setCurrentTaskData(self, answers, participant_id):
        current_system_id = self.getCurrentSystemId(participant_id)
        current_task_id = self.getCurrentTaskId(participant_id)

        trials = self.getTrials(participant_id)
        for t in trials:
            if t['system_id'] == current_system_id:
                for task in t['tasks']:
                    if task['task_id'] == current_task_id:
                        task['questionnaire'] = answers
        self.db.update({'trials': trials}, self.participant.id == participant_id)

    def getFinishedTasks(self, participant_id):
        current_task_id = None
        trials = self.getTrials(participant_id)
        finished_tasks = []
        for t in trials:
            if t['finished'] == False:
                tasks = t['tasks']
                break
        for t in tasks:
            if t['finished'] == True:
                finished_tasks.append(t)
        return finished_tasks

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
