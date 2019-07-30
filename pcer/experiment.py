from session import Session
from resource import Resource
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication)
import random

class Experiment():
    
    participant_id = None
    participant_group = None
    current_system = None
    current_task = None
    session = None
    resource = None

    def __init__(self):
        self.session = Session('db.json', 'experiment')
        self.resource = Resource()
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
