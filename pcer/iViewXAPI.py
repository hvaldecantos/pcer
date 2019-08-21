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
# import platform


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
    _fields_ = [("monitorSize",c_int),
                ("redGeometry",c_int),
                ("redHeightOverFloor",c_int),
                ("redInclAngle",c_int),
                ("redStimDist",c_int),
                ("redStimDistDepth",c_int),
                ("redStimDistHeight",c_int),
                ("setupName",c_char * 256),
                ("redStimHeightOverFloor",c_int),
                ("redStimX",c_int),
                ("redStimY",c_int),]

    def to_str(self):
        string = "monitorSize: " + str(self.monitorSize) + "\n" + \
                 "redGeometry: " + str(self.redGeometry) + "\n" + \
                 "redHeightOverFloor: " + str(self.redHeightOverFloor) + "\n" + \
                 "redInclAngle: " + str(self.redInclAngle) + "\n" + \
                 "redStimDist: " + str(self.redStimDist) + "\n" + \
                 "redStimDistDepth: " + str(self.redStimDistDepth) + "\n" + \
                 "redStimDistHeight: " + str(self.redStimDistHeight) + "\n" + \
                 "setupName: " + str(self.setupName) + "\n" + \
                 "redStimHeightOverFloor: " + str(self.redStimHeightOverFloor) + "\n" + \
                 "redStimX: " + str(self.redStimX) + "\n" + \
                 "redStimY: " + str(self.redStimY) + "\n"
        return string

class CGazeChannelQuality(Structure):
    _fields_ = [('gazeChannelQualityBinocular', c_double),
                ('gazeChannelQualityLeft', c_double),
                ('gazeChannelQualityRight', c_double)]
    def to_str(self):
        return ("Binocular: %f Left: %f Right: %f" % (self.gazeChannelQualityBinocular, self.gazeChannelQualityLeft, self.gazeChannelQualityRight))
