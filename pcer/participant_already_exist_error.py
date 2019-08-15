class ParticipantAlreadyExistError(Exception):
    def __init__(self, participant_id, msg=None):
        self.msg = msg
        if msg is None:
            self.msg = ("Participant 'id': '%s' already exist in the DB." % participant_id)
        super(ParticipantAlreadyExistError, self).__init__(self.msg)
        self.participant_id = participant_id
