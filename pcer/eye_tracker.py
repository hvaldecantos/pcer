from iViewXAPI import CCalibration, CSample, CSystem, CAccuracy, CRedGeometry, CGazeChannelQuality, RET_VALUE
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

    def getdeviceInfo(self):
        print("------------------- device Information         -------------------\n")

        tracking_mode = ctypes.c_int
        tracking_mode = 0
        res = self.iViewXAPI.iV_GetTrackingMode(tracking_mode)
        print("Tracking mode: ", tracking_mode, " result: ", RET_VALUE[res])

        # name = (ctypes.c_char * 64)
        class CName(ctypes.Structure):
            _fields_ = [("name", ctypes.c_char * 64)]
        # name = ctypes.c_char_p()
        # name.value = "hola mundo"
        name = CName()

        res = self.iViewXAPI.iV_GetDeviceName(ctypes.byref(name))
        print("device Name  : ", name.name, " result: ", RET_VALUE[res])


        # name = ctypes.c_char * 64
        res = self.iViewXAPI.iV_GetSerialNumber(ctypes.byref(name))
        print("Serial number: ", name.name, " result: ", RET_VALUE[res])

        # name = "123456789012345678901234567890"
        # print(self.iViewXAPI.iV_GetDeviceName(name))
        # print("device Name: ", name)

        systemData = CSystem(0, 0, 0, 0, 0, 0, 0, 0)

        res = self.iViewXAPI.iV_GetSystemInfo(ctypes.byref(systemData))
        print("iV_GetSystemInfo result: " + RET_VALUE[res])
        print(systemData.to_str())

        res = self.iViewXAPI.iV_GetTrackingMode(ctypes.byref(name))
        print("Tracking mode: ", name.name, " result: ", RET_VALUE[res])

    def getGeometryInfo(self):
        print("------------------- RED Geometry information   -------------------\n")
        # redGeometry = CRedGeometry(0, 0, 0, 0, 0, 0, 0, "empty", 0, 0, 0)
        redGeometry = CRedGeometry(0, 0, "empty", 0, 0, 0, 0, 0, 0, 0, 0)
        self.iViewXAPI.iV_GetCurrentREDGeometry(ctypes.byref(redGeometry))
        print(redGeometry.to_str())

        # redGeometry = CRedGeometry(0, 19, "hector", 474, 297, 0, 0, 0, 0, 0, 0)
        # self.iViewXAPI.iV_SetREDGeometry(ctypes.byref(redGeometry))

        # self.iViewXAPI.iV_GetCurrentREDGeometry(ctypes.byref(redGeometry))
        # print(redGeometry.to_str())

    def getGeometryProfiles(self):
        print("------------------- Geometry profiles information ----------------\n")
        # class CName(ctypes.Structure):
        #     _fields_ = [("name", ctypes.c_char * 64)]

        maxSize = ctypes.c_int()
        # maxSize = 2
        # names = ctypes.c_char * 256
        names = ctypes.c_char_p()
        self.iViewXAPI.iV_GetGeometryProfiles(maxSize, names)
        # self.iViewXAPI.iV_GetGeometryProfiles(ctypes.byref(maxSize), ctypes.byref(names))
        # self.iViewXAPI.iV_GetGeometryProfiles(ctypes.byref(maxSize, names]))
        print("Max size: %s, profile names: %s" % (str(maxSize), str(names)))

        maxSize = 126
        names = '                                        '
        self.iViewXAPI.iV_GetGeometryProfiles(maxSize, names)
        print("Max size: %s, profile names: %s" % (str(maxSize), str(names)))

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

        res = self.iViewXAPI.iV_SetupCalibration(ctypes.byref(calibrationData))
        print("iV_SetupCalibration res = ", res)
        res = self.iViewXAPI.iV_Calibrate()
        print("iV_Calibrate res = ", res)
        res = self.iViewXAPI.iV_Validate()
        print("iV_Validate res = ", res)
        res = self.iViewXAPI.iV_ShowAccuracyMonitor()
        print("iV_ShowAccuracyMonitor res = ", res)

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
                                     (sample.leftEye.gazeY + sample.rightEye.gazeY)/2,
                                     (sample.leftEye.diam + sample.rightEye.diam)/2)
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

# et = ET()
# et.getdeviceInfo()
# et.getGeometryInfo()
# et.getGeometryProfiles()
