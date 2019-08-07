from session import Session
from resource import Resource
import random
from form_builder import FormBuilder
import json


class Experiment():
    
    participant_id = None
    participant_group = None
    current_system = None
    current_task = None
    session = None
    resource = None
    pretest_data = {}

    def __init__(self):
        self.session = Session('db.json', 'experiment')
        self.resource = Resource()
        self.form_builder = FormBuilder()
        pass

    def hasActiveParticipant(self):
        return self.participant_id != None and participant_group != None

    #Added new function setCurrent participant for modularity
    def setCurrentParticipant(self,p_id, p_group=None):
        self.participant_id = p_id
        self.participant_group = p_group

    def addParticipant(self, p_id, p_group):
        print("Experiment.openParticipanSession")
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

    def getNextTask(self):
        random.shuffle(tasks)
        next_task = tasks[0]
        return next_task

    def getGroups(self):
        return self.resource.getGroups()

    def setPretestData(self,question, choice):
        if choice != '--':
            self.pretest_data[question] = choice
        else:
            del self.pretest_data[question]
        self.session.setPretestData(self.pretest_data, self.participant_id)

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

    def getExperimentalSystem(self):
        # print("-----------")
        # print(self.resource.getWarmupSystems()[0])
        # print("-----------")
        system = None

        current_system_id = self.session.getCurrentSystemId(self.participant_id)
        print(current_system_id)

        if not current_system_id:
            if not self.session.isWarmupSystemFinished(self.participant_id):
                warmup_systems = self.resource.getWarmupSystems()
                random.shuffle(warmup_systems)
                system = warmup_systems[0] # there must be at least one

            # else:
            #     finished_systems = self.session.getFinishedExperimentalSystems(participant_id):
            #     all_systems = self.resource.getExperimentalSystems()
            #     remaining_systems = all_systems - finished_systems
            #     system = random.shuffle(remaining_systems)[0]

            self.session.setCurrentSystemId(self.participant_id, system['id'], system['warmup'])
        else:
            system = self.resource.getSystem(current_system_id)
        return system

    def getExperimentalTasks(self):
        task = None
        next_task = None
        current_system_id = self.session.getCurrentSystemId(self.participant_id)
        print('current_system_id : ',current_system_id)
        current_task_id = self.session.getCurrentTaskId(self.participant_id)
        print('current_task_id : ',current_task_id)
        #Total tasks
        tasks = self.resource.getTasks(self.participant_group, current_system_id)
        finished_tasks = []
        remaning_tasks = []
        print('Total tasks :------- ',json.dumps(tasks, indent=4, sort_keys=False))
        if not current_task_id:
            print('No current Task')
            finished_tasks = self.session.getFinishedTasks(self.participant_id)
            print('finished_tasks :------ ',json.dumps(finished_tasks, indent=4, sort_keys=False))
            remaning_tasks = [task for task in tasks if task not in finished_tasks]
            print(remaning_tasks)
            print('remaning_tasks : ',len(remaning_tasks))
            next_task = self.getNextTask(remaning_tasks)
            self.current_task = next_task
            print('next tasks is : ',next_task)
            current_task_id = next_task['id']
            print('current_task_id : ',current_task_id)
            self.session.setCurrentTaskId(self.participant_id, current_system_id, current_task_id)
        else:
            pass
        return self.current_task

    def getExperimentalSystemFilenames(self):
        return self.resource.getExperimentalSystemFilenames(self.participant_group, self.session.getCurrentSystemId(self.participant_id))

    def getSourceCodePath(self):
         return self.getExperimentalSystem()['code'][self.participant_group]
