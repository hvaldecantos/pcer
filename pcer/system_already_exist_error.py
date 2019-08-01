class SystemAlreadyExistError(Exception):
    def __init__(self, system_id, msg=None):
        self.msg = msg
        if msg is None:
            self.msg = ("There is already a trial with a 'system_id': %s in the DB." % (system_id))
        super(SystemAlreadyExistError, self).__init__(msg)
        self.system_id = system_id
