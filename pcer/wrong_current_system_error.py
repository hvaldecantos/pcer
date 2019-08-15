class WrongCurrentSystemError(Exception):
    def __init__(self, system_id, msg=None):
        self.msg = msg
        if msg is None:
            self.msg = ("You are trying to add a current task into a non-current system 'system_id': '%s'." % system_id)
        super(WrongCurrentSystemError, self).__init__(self.msg)
        self.system_id = system_id
