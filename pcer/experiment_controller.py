from participant_form import ParticipantForm
from system_form import SystemForm
from task_form import TaskForm
from code_viewer import CodeViewer
from experiment import Experiment
from pcer_timer import PcerTimer

class ExperimentController:

    experiment = None
    timer = None

    def __init__(self):
        self.window = None
        self.experiment = Experiment()
        self.timer = PcerTimer(15)

    def show_participant_form(self):
    	self.timer.stop()
        if self.window is not None:
    		self.window.close()
        self.window = ParticipantForm(self.experiment)
        self.window.continue_with_the_experiment.connect(self.show_system_form)

        # the timer has to be added, although there is here a reference the
        # wrapped C/C++ object of type QTimer is deleted by pyqt
        self.window.addTimer(self.timer)
        self.timer.hide()

        self.window.show()

    def show_system_form(self):
        self.timer.stop()
        self.task_counter = 0
        self.window.close()
        self.window = SystemForm(self.experiment)
        self.window.back.connect(self.show_participant_form)
        self.window.show_task.connect(self.show_task_form)
        self.window.addTimer(self.timer)
        self.window.show()

    def show_task_form(self):
        self.timer.stop()
        self.task_counter += 1
        self.window.close()
        self.window = TaskForm(self.experiment)
        self.window.submit_answer.connect(self.task_form_submit_answer)
        self.window.read_code.connect(self.show_src_navigator)
        self.window.addTimer(self.timer)
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
        self.window.close()
        self.window = CodeViewer(self.experiment)
        self.window.back.connect(self.show_task_form)
        self.window.addTimer(self.timer)
        self.timer.start()
        self.window.show()
