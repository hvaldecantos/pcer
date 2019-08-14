class CurrentTaskAlreadyExistError(Exception):
    def __init__(self, system_id, task_id, msg=None):
        self.msg = msg
        if msg is None:
            self.msg = ("There is already a current task 'task_id': '%s' for 'system_id': '%s' in the DB." % (task_id, system_id))
        super(CurrentTaskAlreadyExistError, self).__init__(self.msg)
        self.system_id = system_id
        self.task_id = task_id
