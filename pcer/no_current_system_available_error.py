class NoCurrentSystemAvailableError(Exception):
    def __init__(self, participant_id, msg=None):
        self.msg = msg
        if msg is None:
            self.msg = ("There is no current system for Participant 'id' : %s in the DB." % participant_id)
        super(NoCurrentSystemAvailableError, self).__init__(msg)
        self.participant_id = participant_id
