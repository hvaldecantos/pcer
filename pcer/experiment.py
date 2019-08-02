from session import Session
from resource import Resource
import random
from form_builder import FormBuilder

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
        pass

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
        tasks = None
        current_system_id = self.session.getCurrentSystemId(self.participant_id)
        print(current_system_id)

        # when reaching the task_form, there is a current_system_id in the session db

    def getExperimentalSystemFilenames(self):
        return self.resource.getExperimentalSystemFilenames(self.participant_group, self.session.getCurrentSystemId(self.participant_id))

    def getSourceCodePath(self):
         return self.getExperimentalSystem()['code'][self.participant_group]
