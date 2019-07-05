from participant_form import ParticipantForm
from system_form import SystemForm

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
        self.window.close()
        self.window = SystemForm()
        self.window.back.connect(self.show_participant_form)
        self.window.show()


