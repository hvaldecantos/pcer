from tinydb import TinyDB, Query
from participant_already_exist_error import ParticipantAlreadyExistError

class Session():
    
    db = None
    participant = None
    
    def __init__(self, path, name):
        self.db = TinyDB(path, sort_keys=False, indent=4, default_table = name)
        self.participant = Query()

    def existParticipant(self, id):
        return len(self.db.search(self.participant.id == id)) > 0

    def addParticipant(self, id, group):
        if self.existParticipant(id):
            raise ParticipantAlreadyExistError(id)
        self.db.insert({'id': id, 'group': group, 'warmup_finished': False, 'experiment_finished': False, 'current_system_id': None})

    def getParticipantStatus(self, id):
    	return self.db.search(self.participant.id == id)

    def isWarmupSystemFinished(self, participant_id):
        return self.getParticipantStatus(participant_id)[0]['warmup_finished']

    def getCurrentSystemId(self, participant_id):
        return self.getParticipantStatus(participant_id)[0]['current_system_id']

    def setCurrentSystemId(self, participant_id, system_id):
        self.db.update({'current_system_id': system_id}, self.participant.id == participant_id)
