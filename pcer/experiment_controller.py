from participant_form import ParticipantForm
from system_form import SystemForm

class ExperimentController:

    def __init__(self):
        pass

    def show_participant_form(self):
        self.participant_form = ParticipantForm()
        self.participant_form.to_system_form.connect(self.show_system_form)
        self.participant_form.show()

    def show_system_form(self):
        self.system_form = SystemForm()
        self.participant_form.close()
        self.system_form.to_participant_form.connect(self.show_participant_form)
        self.system_form.show()


