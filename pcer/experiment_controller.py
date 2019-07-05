from participant_form import ParticipantForm

class ExperimentController:

    def __init__(self):
        pass

    def show_participant_form(self):
        self.window = ParticipantForm()
        self.window.show()
