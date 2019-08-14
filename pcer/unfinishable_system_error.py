class UnfinishableSystemError(Exception):
    def __init__(self, system_id, msg=None):
        self.msg = msg
        if msg is None:
            self.msg = ("The 'system_id': '%s' cannot be finished." % system_id)
        super(UnfinishableSystemError, self).__init__(msg)
        self.system_id = system_id
