from iViewXAPI import iViewXAPI, CCalibration, CSample, CSystem, CAccuracy, CRedGeometry, CGazeChannelQuality, WINFUNCTYPE
from ctypes import *
import ctypes

class ET:
    # call_back_function = None

    def __init__(self):

        # @WINFUNCTYPE(None, CSample)
        # def sample_callback(sample):
        #     try:
        #         ex.gazeMoveEvent((sample.leftEye.gazeX + sample.rightEye.gazeX)/2,
        #                          (sample.leftEye.gazeY + sample.rightEye.gazeY)/2)
        #     except Exception as e:
        #         print("========>", e)
        #         pass

        # self.call_back_function =  sample_callback
        print('Make UDP connection\n')
        iViewXAPI.iV_Connect(c_char_p('192.168.74.1'), c_int(4444), c_char_p('192.168.74.2'), c_int(5555))
        # print('Set tracking mode\n')
        # iViewXAPI.SetTrackingMode()

    def getDeviseInfo(self):
        print("------------------- Devise Information         -------------------\n")
        # name = (c_char * 64)
        name = c_char_p()
        name.value = "hola mundo"

        print(iViewXAPI.iV_GetDeviceName(byref(name)))
        print("Devise Name: ", name.value)
        print(iViewXAPI.iV_GetSerialNumber(byref(name)))
        print("Serial numb: ", name.value)

        systemData = CSystem(0, 0, 0, 0, 0, 0, 0, 0)

        res = iViewXAPI.iV_GetSystemInfo(byref(systemData))
        print("iV_GetSystemInfo result: " + str(res))
        print(systemData.to_str())

        res = iViewXAPI.iV_GetTrackingMode(byref(name))
        print("Tracking mode: ", name.value)

    def getGeometryInfo(self):
        print("------------------- RED Geometry information   -------------------\n")
        redGeometry = CRedGeometry(0, 0, 0, 0, 0, 0, 0, "empty", 0, 0, 0)
        iViewXAPI.iV_GetCurrentREDGeometry(byref(redGeometry))
        print(redGeometry.to_str())

    def getGeometryProfiles(self):
        print("------------------- Geometry profiles information ----------------\n")
        maxSize = c_int()
        # names = c_char * 256
        names = c_char_p()
        iViewXAPI.iV_GetGeometryProfiles(byref(maxSize), byref(names))
        # iViewXAPI.iV_GetGeometryProfiles(byref(maxSize, names]))
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

        iViewXAPI.iV_ShowAccuracyMonitor()
        iViewXAPI.iV_SetupCalibration(byref(calibrationData))
        iViewXAPI.iV_Calibrate()
        iViewXAPI.iV_Validate()

    def getAccuracyData(self, show_image = 0):
        print("------------------- Accuracy data after validation   -------------\n")
        accuracyData = CAccuracy(0, 0, 0, 0)
        iViewXAPI.iV_GetAccuracy(byref(accuracyData), show_image)
        result = accuracyData.to_dict()
        print(result)
        return result

    def getGazeChannelQuality(self):
        print("------------------- Gaze Channel Quality Information -------------\n")
        channelQuality = CGazeChannelQuality(1.0, 1.1, 1.2)
        iViewXAPI.iV_GetGazeChannelQuality(byref(channelQuality))
        print(channelQuality.to_str())

    def plugg(self, editor):
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
        iViewXAPI.iV_SetSampleCallback(self.call_back_function)

    def unplugg(self):
        iViewXAPI.iV_SetSampleCallback(None)

    def __del__(self):
        print('Disconnect eye tracker\n')
        iViewXAPI.iV_Disconnect()
