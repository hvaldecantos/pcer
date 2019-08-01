from session import Session
from resource import Resource
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

    def getExperimentalSystem(self):
        # print("-----------")
        # print(self.resource.getWarmupSystems()[0])
        # print("-----------")
        system = None

        system_id = self.session.getCurrentSystemId(self.participant_id)
        print(system_id)

        if not system_id:
            if not self.session.isWarmupSystemFinished(self.participant_id):
                warmup_systems = self.resource.getWarmupSystems()
                random.shuffle(warmup_systems)
                system = warmup_systems[0] # there must be at least
            else:
                system = self.session.getCurrentSystemId(participant_id)
                if len(system) <= 0:
                    finished_systems = self.session.getFinishedExperimentalSystems(participant_id)
                    all_systems = self.resource.getExperimentalSystems()
                    remain_systems = all_systems - finished_systems
                    system = random.shuffle(remain_systems)[0]

            self.session.setCurrentSystemId(self.participant_id, system['id'])
        else:
            system = self.resource.getSystem(system_id)
        return system

        # return QPushButton("Current System")
