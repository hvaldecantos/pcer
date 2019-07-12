from session import Session

class Experiment():
    
    participant_id = None
    participant_group = None
    current_system = None
    current_task = None
    session = None

    def __init__(self):
        self.session = Session('db.json', 'experiment')
        pass

    def addParticipant(self, p_id, p_group):
        print("Experiment.openParticipanSession")
        if not self.session.existParticipant(p_id):
            self.session.addParticipant(p_id, p_group)
            self.participant_id = p_id
            self.participant_group = p_group
        else:
            print("Participant already exist")

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
        pass
        # check the file structure
