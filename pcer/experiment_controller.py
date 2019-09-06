from participant_form import ParticipantForm
from system_form import SystemForm
from task_form import TaskForm
from code_viewer import CodeViewer
from pretest_form import PretestForm
from end_form import EndForm
from experiment import Experiment
from pcer_timer import PcerTimer
from eye_tracker import ET
import yaml

class ExperimentController:

    experiment = None
    timer = None
    et = None

    def __init__(self):
        self.window = None
        self.experiment = Experiment()
        self.timer = PcerTimer()
        config = yaml.load(open("config.yml"), Loader = yaml.SafeLoader)
        self.tracking_device = config['tracker']['device']
        self.time_limit_minutes = config['time_limit']['minutes']
        self.time_limit_seconds = config['time_limit']['seconds']
        if self.tracking_device == "eye tracker":
            self.et = ET()

    def show_participant_form(self):
    	self.timer.stop()
        if self.window is not None:
    		self.window.close()
        self.window = ParticipantForm(self.experiment)
        self.window.continue_with_the_experiment.connect(self.show_system_or_pretest_or_end)
        self.window.calibrate_eye_tracker.connect(self.start_calibration)

        # the timer has to be added, although there is here a reference the
        # wrapped C/C++ object of type QTimer is deleted by pyqt
        self.window.addTimer(self.timer)
        self.timer.hide()

        self.window.show()

    def start_calibration(self):
        self.et.calibrate()
        result = self.et.getAccuracyData()
        self.experiment.session.addETCalibrationAccuracy(self.experiment.participant_id, result)

    def show_system_form(self):
        self.timer.stop()
        self.window.close()
        self.window = SystemForm(self.experiment)
        self.window.back.connect(self.show_participant_form)
        self.window.show_task.connect(self.show_task_form)
        self.timer.setTime(self.time_limit_minutes, self.time_limit_seconds)
        self.window.addTimer(self.timer)
        self.timer.hide()
        self.window.show()

    def show_task_form(self):
        self.timer.stop()
        self.window.close()
        self.window = TaskForm(self.experiment, self.timer)
        self.window.submit_answer.connect(self.task_form_submit_answer)
        self.window.read_code.connect(self.show_src_navigator)
        self.window.addTimer(self.timer)
        self.window.show()

    def show_system_or_pretest_or_end(self):
        if(self.experiment.isWarmupSystemsFinished() and not self.experiment.isPretestFinished()):
            self.show_pretest_form()
        elif(self.experiment.isExperimentFinished()):
            self.show_end_message()
        else:
            self.show_system_form()

    def show_end_message(self):
        self.timer.stop()
        self.window.close()
        self.window = EndForm(self.experiment)
        self.window.back.connect(self.show_participant_form)
        self.window.addTimer(self.timer)
        self.timer.hide()
        self.window.show()
        print("The exoeriment is finished")

    def task_form_submit_answer(self):
        participant_id = self.experiment.participant_id
        system_id = self.experiment.session.getCurrentSystemId(participant_id)
        total_tasks = self.experiment.resource.getTasks(self.experiment.participant_group, system_id)
        if self.experiment.session.hasRemainingTasks(participant_id, total_tasks):
            self.show_task_form()
        else:
            self.experiment.finishCurrentSystem()
            self.show_system_or_pretest_or_end()

    def show_pretest_form(self):
        self.timer.stop()
        self.window.close()
        self.window = PretestForm(self.experiment)
        self.window.submit_answer.connect(self.show_system_form)
        self.window.addTimer(self.timer)
        self.timer.hide()
        self.window.show()

    def show_src_navigator(self):
        print("show_src_navigator")
        self.window.close()
        self.window = CodeViewer(self.experiment, self.et, self.timer)
        self.window.back.connect(self.show_task_form)
        self.window.addTimer(self.timer)
        self.timer.start()
        self.window.show()
