class ParticipantDoesNotExistError(Exception):
    def __init__(self, participant_id, msg=None):
        self.msg = msg
        if msg is None:
            self.msg = ("Participant 'id': '%s'does not exist in the DB." % participant_id)
        super(ParticipantDoesNotExistError, self).__init__(self.msg)
        self.participant_id = participant_id
