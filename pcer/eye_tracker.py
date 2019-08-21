from iViewXAPI import CCalibration, CSample, CSystem, CAccuracy, CRedGeometry, CGazeChannelQuality
import ctypes
import platform

class ET:

    def __init__(self):

        if(platform.system() != "Windows"):
            raise Exception("Your OS system is not supported for eye tracking yet.")

        if platform.architecture()[0] == '64bit':
            self.iViewXAPI = ctypes.windll.LoadLibrary("iViewXAPI64.dll")
        else:
            self.iViewXAPI = ctypes.windll.LoadLibrary("iViewXAPI.dll")

        print("------------------ Make UDP connection ---------------------------\n")
        self.iViewXAPI.iV_Connect(ctypes.c_char_p('192.168.74.1'), ctypes.c_int(4444), ctypes.c_char_p('192.168.74.2'), ctypes.c_int(5555))
        # print('Set tracking mode\n')
        # self.iViewXAPI.SetTrackingMode()

    def getDeviseInfo(self):
        print("------------------- Devise Information         -------------------\n")
        # name = (ctypes.c_char * 64)
        name = ctypes.c_char_p()
        name.value = "hola mundo"

        print(self.iViewXAPI.iV_GetDeviceName(ctypes.byref(name)))
        print("Devise Name: ", name.value)
        print(self.iViewXAPI.iV_GetSerialNumber(ctypes.byref(name)))
        print("Serial numb: ", name.value)

        systemData = CSystem(0, 0, 0, 0, 0, 0, 0, 0)

        res = self.iViewXAPI.iV_GetSystemInfo(ctypes.byref(systemData))
        print("iV_GetSystemInfo result: " + str(res))
        print(systemData.to_str())

        res = self.iViewXAPI.iV_GetTrackingMode(ctypes.byref(name))
        print("Tracking mode: ", name.value)

    def getGeometryInfo(self):
        print("------------------- RED Geometry information   -------------------\n")
        redGeometry = CRedGeometry(0, 0, 0, 0, 0, 0, 0, "empty", 0, 0, 0)
        self.iViewXAPI.iV_GetCurrentREDGeometry(ctypes.byref(redGeometry))
        print(redGeometry.to_str())

    def getGeometryProfiles(self):
        print("------------------- Geometry profiles information ----------------\n")
        maxSize = ctypes.c_int()
        # names = ctypes.c_char * 256
        names = ctypes.c_char_p()
        self.iViewXAPI.iV_GetGeometryProfiles(ctypes.byref(maxSize), ctypes.byref(names))
        # self.iViewXAPI.iV_GetGeometryProfiles(ctypes.byref(maxSize, names]))
        # print("Max size: %d, profile names: %s" % (str(maxSize), str(names)))

    def calibrate(self):
        print("------------------- Setting up the calibration -------------------\n")
        calibrationData = CCalibration(5,   # ("method", c_int),  select calibration method (default: 5) a bit mask is used to specify a new calibration workflow. 0, 1, 2, 5, 9 or 13 calibration points are possible
                                       1,   # ("visualization", c_int), draw calibration/validation by API (default: 1)
                                       0,   # ("displayDevice", c_int), set display device [0: primary device (default), 1: secondary device]
                                       0,   # ("speed", c_int), set calibration/validation speed [0: slow (default), 1: fast]
                                       0,   # ("autoAccept", c_int), set calibration/validation point acceptance [2: full-automatic, 1: semi-automatic (default), 0: manual]
                                       20,  # ("foregroundBrightness", c_int), set calibration/validation target brightness [0..255] (default: 250)
                                       239, # ("backgroundBrightness", c_int), set calibration/validation background brightness [0..255] (default: 220)
                                       1,   # ("targetShape", c_int), set calibration/validation target shape [IMAGE = 0, CIRCLE1 = 1, CIRCLE2 = 2 (default), CROSS = 3]
                                       10,   # ("targetSize", c_int), set calibration/validation target size in pixel (minimum: 10 pixels, default: 20 pixels
                                       b"") # ("targetFilename", c_char * 256), selectcustomcalibration/validationtarget(onlyiftargetShape=0)

        self.iViewXAPI.iV_ShowAccuracyMonitor()
        self.iViewXAPI.iV_SetupCalibration(ctypes.byref(calibrationData))
        self.iViewXAPI.iV_Calibrate()
        self.iViewXAPI.iV_Validate()

    def getAccuracyData(self, show_image = 0):
        print("------------------- Accuracy data after validation   -------------\n")
        accuracyData = CAccuracy(0, 0, 0, 0)
        self.iViewXAPI.iV_GetAccuracy(ctypes.byref(accuracyData), show_image)
        result = accuracyData.to_dict()
        print(result)
        return result

    def getGazeChannelQuality(self):
        print("------------------- Gaze Channel Quality Information -------------\n")
        channelQuality = CGazeChannelQuality(1.0, 1.1, 1.2)
        self.iViewXAPI.iV_GetGazeChannelQuality(ctypes.byref(channelQuality))
        print(channelQuality.to_str())

    def plugg(self, editor):
        from ctypes import WINFUNCTYPE
        @WINFUNCTYPE(None, CSample)
        def sample_callback(sample):
            try:
                editor.gazeMoveEvent((sample.leftEye.gazeX + sample.rightEye.gazeX)/2,
                                     (sample.leftEye.gazeY + sample.rightEye.gazeY)/2)
            except Exception as e:
                print("========>", e)
                pass

        self.call_back_function =  sample_callback
        print('Set callback function\n')
        self.iViewXAPI.iV_SetSampleCallback(self.call_back_function)

    def unplugg(self):
        self.iViewXAPI.iV_SetSampleCallback(None)

    def __del__(self):
        print('Disconnect eye tracker\n')
        self.iViewXAPI.iV_Disconnect()
