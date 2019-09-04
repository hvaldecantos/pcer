from session import Session
from resource import Resource
import random
from form_builder import FormBuilder
import json


class Experiment():
    
    participant_id = None
    participant_group = None
    current_system_id = None
    current_task_id = None
    session = None
    resource = None

    def __init__(self, db_filename = 'db.json'):
        self.session = Session(db_filename, 'experiment')
        self.resource = Resource()
        self.form_builder = FormBuilder()
        pass

    def hasActiveParticipant(self):
        return self.participant_id != None and self.participant_group != None

    def setCurrentParticipant(self,p_id, p_group=None):
        self.participant_id = p_id
        self.participant_group = p_group

    def addParticipant(self, p_id, p_group):
        self.session.addParticipant(p_id, p_group)
        self.setCurrentParticipant(p_id, p_group)

    def getParticipantStatus(self, p_id):
        return self.session.getParticipantStatus(p_id)

    def openParticipanSession(self, p_id):
        print("Experiment.openParticipanSession")
        pass

    def saveParticipanSession(self):
        pass

    def getNextSystemDescription(self):
        pass

    def finishCurrentTask(self):
        self.session.finishCurrentTask(self.participant_id)

    def getGroups(self):
        return self.resource.getGroups()

    def setPretestData(self,question_id, question, choice):
        pretest_data = self.session.getCurrentPretestState(self.participant_id)
        if choice != '--':
            pretest_data[question_id] = {}
            pretest_data[question_id]['question'] = question
            pretest_data[question_id]['answer'] = choice
        else:
            del pretest_data[question_id]
        self.session.setPretestData(pretest_data, self.participant_id)

    def setTaskData(self,question_id, question, choice):
        current_task_data = self.session.getCurrentTaskState(self.participant_id)
        if choice != '--':
            current_task_data[question_id] = {}
            current_task_data[question_id]['question'] = question
            current_task_data[question_id]['answer'] = choice
        else:
            del current_task_data[question_id]
        self.session.setCurrentTaskData(current_task_data, self.participant_id)

    def getScrollDisplacement(self, filename):
        return self.session.getScrollDisplacements(self.participant_id)[filename]

    def setScrollDisplacement(self, filename, scroll_displacement):
        displacements = self.session.getScrollDisplacements(self.participant_id)
        displacements[filename] = scroll_displacement
        self.session.setScrollDisplacements(self.participant_id, displacements)

    def clearScrollDisplacements(self):
        self.session.setScrollDisplacements(self.participant_id, {})

    def getCurrentOpenedFilename(self):
        return self.session.getCurrentOpenedFilename(self.participant_id)

    def setCurrentOpenedFilename(self, filename):
        self.session.setCurrentOpenedFilename(self.participant_id, filename)

    def clearCurrentOpenedFilename(self):
        self.session.setCurrentOpenedFilename(self.participant_id, None)

    def isWarmupSystemsFinished(self):
        warmup_systems = self.resource.getWarmupSystems()
        finished_warmup_systems =  self.session.getFinishedWarmupSystemIds(self.participant_id)

        for ws in warmup_systems:
            if not (ws['id'] in finished_warmup_systems):
                return False
        return True

    def isExperimentFinished(self):
        return self.session.isExperimentFinished(self.participant_id)

    def setExperimentFinishedTrue(self):
        self.session.setExperimentFinishedTrue(self.participant_id)

    def isPretestFinished(self):
        return self.session.isPretestFinished(self.participant_id)

    def setPretestFinishedTrue(self):
        self.session.setPretestFinishedTrue(self.participant_id)

    def getRemainingExperimentalSystems(self):
        finished_systems = self.session.getFinishedSystemIds(self.participant_id)
        all_systems = self.resource.getExperimentalSystems()
        remaining_systems = [s for s in all_systems if s['id'] not in finished_systems]
        return remaining_systems

    def hasRemainingExperimentalSystems(self):
        return len(self.getRemainingExperimentalSystems()) > 0

    def finishCurrentSystem(self):
        self.session.finishCurrentSystem(self.participant_id)
        if(not self.hasRemainingExperimentalSystems()):
            self.setExperimentFinishedTrue()

    def getExperimentalSystem(self):
        system = None
        current_system_id = self.session.getCurrentSystemId(self.participant_id)

        if not current_system_id:
            self.clearCurrentOpenedFilename()
            self.clearCurrentExperimentalSystemFilenamesOrder()
            self.clearScrollDisplacements()
            if not self.isWarmupSystemsFinished():
                warmup_systems = self.resource.getWarmupSystems()
                finished_warmup_systems =  self.session.getFinishedWarmupSystemIds(self.participant_id)
                remaining_warmup_systems = [s for s in warmup_systems if s['id'] not in finished_warmup_systems]
                random.shuffle(remaining_warmup_systems)
                system = remaining_warmup_systems[0]
            else:
                remaining_systems = self.getRemainingExperimentalSystems()

                random.shuffle(remaining_systems)
                system = remaining_systems[0]
            self.current_system_id = system['id']
            self.session.setCurrentSystemId(self.participant_id, system['id'], system['warmup'])
        else:
            self.current_system_id = current_system_id
            system = self.resource.getSystem(current_system_id)
        return system

    def getExperimentalTask(self):
        task = None
        current_system_id = self.session.getCurrentSystemId(self.participant_id)
        current_task_id = self.session.getCurrentTaskId(self.participant_id)

        if not current_task_id:
            tasks = self.resource.getTasks(self.participant_group, current_system_id)
            finished_tasks = self.session.getCurrentSystemFinishedTasks(self.participant_id)
            remaining_tasks = [task for task in tasks if task['id'] not in [f_task['task_id'] for f_task in finished_tasks]]
            random.shuffle(remaining_tasks)
            task = remaining_tasks[0]
            self.current_task_id = task['id']
            self.session.setCurrentTaskId(self.participant_id, current_system_id, task['id'])
        else:
            self.current_task_id = current_task_id
            task = self.resource.getTask(self.participant_group, current_system_id, current_task_id)
        return task

    def getCurrentExperimentalSystemFilenames(self):
        filenames = self.session.getFilenamesOrder(self.participant_id)
        if len(filenames) == 0:
            filenames = self.resource.getCurrentExperimentalSystemFilenames(self.participant_group, self.session.getCurrentSystemId(self.participant_id))
            random.shuffle(filenames)
            self.session.setFilenamesOrder(self.participant_id, filenames)
        return filenames

    def clearCurrentExperimentalSystemFilenamesOrder(self):
        self.session.setFilenamesOrder(self.participant_id, [])

    def getSourceCodePath(self):
         return self.getExperimentalSystem()['code'][self.participant_group]
