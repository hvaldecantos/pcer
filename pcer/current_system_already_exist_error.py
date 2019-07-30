class CurrentSystemAlreadyExistError(Exception):
    def __init__(self, system_id, msg=None):
        self.msg = msg
        if msg is None:
            self.msg = ("There is already a current system 'system_id' : %s in the DB." % system_id)
        super(CurrentSystemAlreadyExistError, self).__init__(msg)
        self.system_id = system_id
