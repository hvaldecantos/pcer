# -----------------------------------------------------------------------
#
# (c) Copyright 1997-2016, SensoMotoric Instruments GmbH
# 
# Permission  is  hereby granted,  free  of  charge,  to any  person  or
# organization  obtaining  a  copy  of  the  software  and  accompanying
# documentation  covered  by  this  license  (the  "Software")  to  use,
# reproduce,  display, distribute, execute,  and transmit  the Software,
# and  to  prepare derivative  works  of  the  Software, and  to  permit
# third-parties to whom the Software  is furnished to do so, all subject
# to the following:
# 
# The  copyright notices  in  the Software  and  this entire  statement,
# including the above license  grant, this restriction and the following
# disclaimer, must be  included in all copies of  the Software, in whole
# or  in part, and  all derivative  works of  the Software,  unless such
# copies   or   derivative   works   are   solely   in   the   form   of
# machine-executable  object   code  generated  by   a  source  language
# processor.
# 
# THE  SOFTWARE IS  PROVIDED  "AS  IS", WITHOUT  WARRANTY  OF ANY  KIND,
# EXPRESS OR  IMPLIED, INCLUDING  BUT NOT LIMITED  TO THE  WARRANTIES OF
# MERCHANTABILITY,   FITNESS  FOR  A   PARTICULAR  PURPOSE,   TITLE  AND
# NON-INFRINGEMENT. IN  NO EVENT SHALL  THE COPYRIGHT HOLDERS  OR ANYONE
# DISTRIBUTING  THE  SOFTWARE  BE   LIABLE  FOR  ANY  DAMAGES  OR  OTHER
# LIABILITY, WHETHER  IN CONTRACT, TORT OR OTHERWISE,  ARISING FROM, OUT
# OF OR IN CONNECTION WITH THE  SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# -----------------------------------------------------------------------
# iViewXAPI.py
#
# Demonstrates features of iView API 
# Defines structures 
# Loads iViewXAPI.dll / iViewXAPI64.dll
# This script shows how to set up an experiment with Python 2.7.1 (with ctypes Library) 


from ctypes import Structure, c_char, c_char_p, c_int, c_double, c_longlong, byref

#===========================
#       Struct Definitions
#===========================

class CSystem(Structure):
    _fields_ = [("samplerate", c_int),
    ("iV_MajorVersion", c_int),
    ("iV_MinorVersion", c_int),
    ("iV_Buildnumber", c_int),
    ("API_MajorVersion", c_int),
    ("API_MinorVersion", c_int),
    ("API_Buildnumber", c_int),
    ("iV_ETDevice", c_int)]

    def to_str(self):
        string = "Samplerate: " + str(self.samplerate) + "\n" + \
                 "iViewX Version: " + str(self.iV_MajorVersion) + "." + str(self.iV_MinorVersion) + "." + str(self.iV_Buildnumber)  + "\n" + \
                 "iViewX API Version: " + str(self.API_MajorVersion) + "." + str(self.API_MinorVersion) + "." + str(self.API_Buildnumber)  + "\n" + \
                 "iV_ETDevice: " + str(self.iV_ETDevice) + "\n"
        return string

class CCalibration(Structure):
    _fields_ = [("method", c_int),
    ("visualization", c_int),
    ("displayDevice", c_int),
    ("speed", c_int),
    ("autoAccept", c_int),
    ("foregroundBrightness", c_int),
    ("backgroundBrightness", c_int),
    ("targetShape", c_int),
    ("targetSize", c_int),
    ("targetFilename", c_char * 256)]

class CEye(Structure):
    _fields_ = [("gazeX", c_double),
    ("gazeY", c_double),
    ("diam", c_double),
    ("eyePositionX", c_double),
    ("eyePositionY", c_double),
    ("eyePositionZ", c_double)]

class CSample(Structure):
    _fields_ = [("timestamp", c_longlong),
    ("leftEye", CEye),
    ("rightEye", CEye),
    ("planeNumber", c_int)]

class CEvent(Structure):
    _fields_ = [("eventType", c_char),
    ("eye", c_char),
    ("startTime", c_longlong),
    ("endTime", c_longlong),
    ("duration", c_longlong),
    ("positionX", c_double),
    ("positionY", c_double)]

class CAccuracy(Structure):
    _fields_ = [("deviationLX",c_double),
                ("deviationLY",c_double),
                ("deviationRX",c_double),
                ("deviationRY",c_double)]
    def to_str(self):
        return ("LX: %f, LY: %f, RX: %f, RY: %f" % (self.deviationLX, self.deviationLY, self.deviationRX, self.deviationRY))

    def to_dict(self):
        result = {}
        result['LX'] = self.deviationLX
        result['LY'] = self.deviationLY
        result['RX'] = self.deviationRX
        result['RY'] = self.deviationRY
        return result

class CRedGeometry(Structure):

    _fields_ = [
        ('redGeometry', c_int),
        ('monitorSize', c_int),
        ('setupName', c_char * 256),
        ('stimX', c_int),
        ('stimY', c_int),
        ('stimHeightOverFloor', c_int),
        ('redHeightOverFloor', c_int),
        ('redStimDist', c_int),
        ('redInclAngle', c_int),
        ('redStimDistHeight', c_int),
        ('redStimDistDepth', c_int)]

    def to_str(self):
        string = "redGeometry: " + str(self.redGeometry) + "\n" + \
                 "monitorSize: " + str(self.monitorSize) + "\n" + \
                 "setupName: " + str(self.setupName) + "\n" + \
                 "stimX: " + str(self.stimX) + "\n" + \
                 "stimY: " + str(self.stimY) + "\n" + \
                 "stimHeightOverFloor: " + str(self.stimHeightOverFloor) + "\n" + \
                 "redHeightOverFloor: " + str(self.redHeightOverFloor) + "\n" + \
                 "redStimDist: " + str(self.redStimDist) + "\n" + \
                 "redInclAngle: " + str(self.redInclAngle) + "\n" + \
                 "redStimDistHeight: " + str(self.redStimDistHeight) + "\n" + \
                 "redStimDistDepth: " + str(self.redStimDistDepth) + "\n"
        return string

class CGazeChannelQuality(Structure):
    _fields_ = [('gazeChannelQualityBinocular', c_double),
                ('gazeChannelQualityLeft', c_double),
                ('gazeChannelQualityRight', c_double)]
    def to_str(self):
        return ("Binocular: %f Left: %f Right: %f" % (self.gazeChannelQualityBinocular, self.gazeChannelQualityLeft, self.gazeChannelQualityRight))

RET_VALUE = {}
RET_VALUE[1] = 'RET_SUCCESS'
RET_VALUE[2] = 'RET_NO_VALID_DATA'
RET_VALUE[3] = 'RET_CALIBRATION_ABORTED'
RET_VALUE[4] = 'RET_SERVER_IS_RUNNING'
RET_VALUE[5] = 'RET_CALIBRATION_NOT_IN_PROGRESS'
RET_VALUE[11] = 'RET_WINDOW_IS_OPEN'
RET_VALUE[12] = 'RET_WINDOW_IS_CLOSED'
RET_VALUE[100] = 'ERR_COULD_NOT_CONNECT'
RET_VALUE[101] = 'ERR_NOT_CONNECTED'
RET_VALUE[102] = 'ERR_NOT_CALIBRATED'
RET_VALUE[103] = 'ERR_NOT_VALIDATED'
RET_VALUE[104] = 'ERR_EYETRACKING_APPLICATION_NOT_RUNNING'
RET_VALUE[105] = 'ERR_WRONG_COMMUNICATION_PARAMETER'
RET_VALUE[111] = 'ERR_WRONG_DEVICE'
RET_VALUE[112] = 'ERR_WRONG_PARAMETER'
RET_VALUE[113] = 'ERR_WRONG_CALIBRATION_METHOD'
RET_VALUE[114] = 'ERR_CALIBRATION_TIMEOUT'
RET_VALUE[115] = 'ERR_TRACKING_NOT_STABLE'
RET_VALUE[121] = 'ERR_CREATE_SOCKET'
RET_VALUE[122] = 'ERR_CONNECT_SOCKET'
RET_VALUE[123] = 'ERR_BIND_SOCKET'
RET_VALUE[124] = 'ERR_DELETE_SOCKET'
RET_VALUE[131] = 'ERR_NO_RESPONSE_FROM_IVIEWX'
RET_VALUE[132] = 'ERR_INVALID_IVIEWX_VERSION'
RET_VALUE[133] = 'ERR_WRONG_IVIEWX_VERSION'
RET_VALUE[171] = 'ERR_ACCESS_TO_FILE'
RET_VALUE[181] = 'ERR_SOCKET_CONNECTION'
RET_VALUE[191] = 'ERR_EMPTY_DATA_BUFFER'
RET_VALUE[192] = 'ERR_RECORDING_DATA_BUFFER'
RET_VALUE[193] = 'ERR_FULL_DATA_BUFFER'
RET_VALUE[194] = 'ERR_IVIEWX_IS_NOT_READY'
RET_VALUE[201] = 'ERR_IVIEWX_NOT_FOUND'
RET_VALUE[202] = 'ERR_IVIEWX_PATH_NOT_FOUND'
RET_VALUE[203] = 'ERR_IVIEWX_ACCESS_DENIED'
RET_VALUE[204] = 'ERR_IVIEWX_ACCESS_INCOMPLETE'
RET_VALUE[205] = 'ERR_IVIEWX_OUT_OF_MEMORY'
RET_VALUE[211] = 'ERR_CAMERA_NOT_FOUND'
RET_VALUE[212] = 'ERR_WRONG_CAMERA'
RET_VALUE[213] = 'ERR_WRONG_CAMERA_PORT'
RET_VALUE[220] = 'ERR_COULD_NOT_OPEN_PORT'
RET_VALUE[221] = 'ERR_COULD_NOT_CLOSE_PORT'
RET_VALUE[222] = 'ERR_AOI_ACCESS'
RET_VALUE[223] = 'ERR_AOI_NOT_DEFINED'
RET_VALUE[250] = 'ERR_FEATURE_NOT_LICENSED'
RET_VALUE[300] = 'ERR_DEPRECATED_FUNCTION'
RET_VALUE[400] = 'ERR_INITIALIZATION'
RET_VALUE[401] = 'ERR_FUNC_NOT_LOADED'
