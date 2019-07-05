from participant_form import ParticipantForm
from system_form import SystemForm
from task_form import TaskForm

class ExperimentController:

    def __init__(self):
        self.window = None

    def show_participant_form(self):
    	if self.window is not None:
    		self.window.close()
        self.window = ParticipantForm()
        self.window.submit_info.connect(self.show_system_form)
        self.window.show()

    def show_system_form(self):
    	self.task_counter = 0
        self.window.close()
        self.window = SystemForm()
        self.window.back.connect(self.show_participant_form)
        self.window.show_task.connect(self.show_task_form)
        self.window.show()

    def show_task_form(self):
    	self.task_counter += 1
        self.window.close()
        self.window = TaskForm()
        self.window.submit_answer.connect(self.task_form_submit_answer)
        self.window.read_code.connect(self.show_src_navigator)
        self.window.show()

    def task_form_submit_answer(self):
    	print("submit_answer task_counter = {}".format(self.task_counter))
    	if self.task_counter < 3:
    		self.show_task_form()
    	else:
    		self.window.close()
    		self.show_system_form()

    def show_src_navigator(self):
    	print("show_src_navigator")
