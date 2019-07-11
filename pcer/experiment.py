from session import Session

class Experiment():
    
    participant_id = None
    experimental_system = None
    experimental_task = None
    session = None

    def __init__(self):
        self.session = Session('db.json', 'experiment')
        pass

    def addParticipant(self, id, group):
        print("Experiment.openParticipanSession")
        if not self.session.existParticipant(id):
            self.session.addParticipant(id, group)
        else:
            print("Participant already exist")
        

    def openParticipanSession(self, id):
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
