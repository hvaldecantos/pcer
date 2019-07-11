from tinydb import TinyDB, Query

class Session():
    
    db = None
    participant = None
    
    def __init__(self, path, name):
        self.db = TinyDB(path, sort_keys=False, indent=4, default_table = name)
        self.participant = Query()

    def existParticipant(self, id):
        return len(self.db.search(self.participant.id == id)) > 0

    def addParticipant(self, id, group):
        self.db.insert({'id': id, 'group': group})
