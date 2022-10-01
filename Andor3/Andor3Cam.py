'''
@Description:
@Author: F.O.X
@Date: 2020-03-08 00:01:00
@LastEditor: F.O.X
LastEditTime: 2022-10-01 08:04:23
'''

from andor3 import Andor3
import time


class Camera():
    def __init__(self, name):
        self.cam = Andor3()
        self.cam.ElectronicShutteringMode = 2
        self.encoding_modes = [x for x in range(self.cam.getEnumCount(
            'PixelEncoding')) if self.cam.isEnumIndexAvailable('PixelEncoding', x)]
        self.mode_names = [self.cam.getEnumStringByIndex(
            'PixelEncoding', x) for x in self.encoding_modes]
        self.start_time = 0
        self.exposing = False
        self.cooling_power = [0, 100, 50, 99, 99, -1, 999]

    def __del__(self):
        try:
            self.cam.close()
        except:
            pass

    @property
    def Connected(self):
        return self.cam.CameraPresent

    @Connected.setter
    def Connected(self, value):
        if value is True and self.Connected is False:
            self.cam.open()
        elif value is False and self.Connected is True:
            self.cam.close()
        else:
            pass

    # def SetImageArea(self):
    #     if (self.area[0] * self.binw) >= self.imagew:
    #         self.area[0] = (self.imagew / self.binw - 1)
    #     if self.area[1] * self.binh >= self.imageh:
    #         self.area[1] = self.imageh / self.binh - 1
    #     if (self.area[0] + self.area[2]) * self.binw > self.imagew:
    #         self.area[2] = self.imagew / self.binw
    #     if (self.area[1] + self.area[3]) * self.binh > self.imageh:
    #         self.area[3] = self.imageh / self.binh
    #     SetQHYCCDBinMode(self.cam, self.binw, self.binh)
    #     SetQHYCCDResolution(self.cam, *self.area)

    @property
    def BinX(self):
        return self.cam.AOIVBin

    @BinX.setter
    def BinX(self, value):
        self.cam.AOIVBin = int(value)

    @property
    def BinY(self):
        return self.cam.AOIHBin

    @BinY.setter
    def BinY(self, value):
        self.cam.AOIHBin = int(value)

    @property
    def NumX(self):
        return self.cam.AOIWidth

    @NumX.setter
    def NumX(self, value):
        if value > 0:
            self.cam.AOIWidth = int(value)

    @property
    def NumY(self):
        return self.cam.AOIHeight

    @NumY.setter
    def NumY(self, value):
        if value > 0:
            self.cam.AOIHeight = int(value)

    @property
    def StartX(self):
        return self.cam.AOILeft - 1

    @StartX.setter
    def StartX(self, value):
        if value >= 0 and value < self.NumX:
            self.cam.AOILeft = int(value) + 1

    @property
    def StartY(self):
        return self.cam.AOITop - 1

    @StartY.setter
    def StartY(self, value):
        if value >= 0 and value < self.NumY:
            self.cam.AOITop = int(value) + 1

    def StartExposure(self, exp, light=1):
        if self.cam.CameraAcquiring:
            self.cam.stop()
        self.cam.ExposureTime = exp
        self.cam.queueBuffer()
        self.cam.start()
        self.start_time = time.time()
        self.exposing = True

    @property
    def CameraState(self):
        if self.cam.CameraAcquiring:
            return 2
        elif self.cam.CameraStatus[0] > 4:
            return 5
        else:
            return 0

    @property
    def CameraXSize(self):
        return self.cam.SensorWidth

    @property
    def CameraYSize(self):
        return self.cam.SensorHeight

    @property
    def CanAbortExposure(self):
        return True

    @property
    def CanAsymmetricBin(self):
        return True

    @property
    def CanFastReadout(self):
        return False

    @property
    def CanGetCoolerPower(self):
        return False

    @property
    def CanPulseGuide(self):
        return False

    @property
    def CanSetCCDTemperature(self):
        return True

    @property
    def CanStopExposure(self):
        return True

    @property
    def CCDTemperature(self):
        return self.cam.SensorTemperature

    @property
    def CoolerOn(self):
        return self.cam.SensorCooling

    @CoolerOn.setter
    def CoolerOn(self, value):
        self.cam.SensorCooling = bool(value)

    @property
    def CoolerPower(self):
        return self.cooling_power[self.cam.TemperatureStatus[0]]

    # @CoolerPower.setter
    # def CoolerPower(self, value):
    #     if value >= 0 and value <= 100:
    #         SetQHYCCDParam(self.cam, CONTROL_ID.CONTROL_MANULPWM,
    #                        int(value * 255. / 100.))

    @property
    def HeatSinkTemperature(self):
        return self.cam.SensorTemperature

    @property
    def ImageReady(self):
        if self.exposing:
            try:
                self.buffer = self.cam.waitBuffer(timeout=0, copy=True)
                self.cam.stop()
                self.exposing = False
                return True
            except:
                return False
        else:
            return True

    @property
    def ImageArray(self):
        try:
            return self.cam.decode_image(self.buffer)[0]
        except:
            return None

    # @property
    # def ImageArrayVariant(self):
    #     return self.ImageArray

    @property
    def LastExposureDuration(self):
        return self.cam.ExposureTime

    @property
    def LastExposureStartTime(self):
        return self.start_time

    @property
    def MaxBinX(self):
        return self.cam.max('AOIVBin')

    @property
    def MaxBinY(self):
        return self.cam.max('AOIHBin')

    @property
    def MaxADU(self):
        if self.cam.BitDepth[0] == 1:
            return 65535
        elif self.cam.BitDepth[0] == 2:
            return 4294967295
        elif self.cam.BitDepth[0] == 0:
            return 4095
        else:
            return 0

    @property
    def PercentCompleted(self):
        progress = (time.time() - self.start_time)/self.cam.ExposureTime * 100
        return progress if progress < 100 else 100

    @property
    def PixelSizeX(self):
        return self.cam.PixelWidth

    @property
    def PixelSizeY(self):
        return self.cam.PixelHeight

    @property
    def ReadoutMode(self):
        return self.encoding_modes.index(self.cam.PixelEncoding[0])

    @property
    def ReadoutModes(self):
        return self.mode_names

    @ReadoutMode.setter
    def ReadoutMode(self, value):
        self.cam.PixelEncoding = self.encoding_modes[int(value)]

    @property
    def Gain(self):
        return self.cam.GainMode[1]

    # @property
    # def GainMax(self):
    #     return self.gain_max

    # @property
    # def GainMin(self):
    #     return self.gain_min

    # @property
    # def Gains(self):
    #     return list(range(self.gain_min, self.gain_max+1, self.gain_step))

    # @Gain.setter
    # def Gain(self, value):
    #     if int(value) <= self.GainMax and int(value) >= self.GainMin:
    #         SetQHYCCDParam(self.cam, CONTROL_ID.CONTROL_GAIN, int(value))

    # @property
    # def Offset(self):
    #     return int(GetQHYCCDParam(self.cam, CONTROL_ID.CONTROL_OFFSET))

    # @property
    # def OffsetMax(self):
    #     return self.offset_max

    # @property
    # def OffsetMin(self):
    #     return self.offset_min

    # @property
    # def Offsets(self):
    #     return list(range(self.offset_min, self.offset_max+1, self.offset_step))

    # @Offset.setter
    # def Offset(self, value):
    #     if int(value) <= self.OffsetMax and int(value) >= self.OffsetMin:
    #         SetQHYCCDParam(self.cam, CONTROL_ID.CONTROL_OFFSET, int(value))

    @property
    def SensorType(self):
        return "Monochrome"

    @property
    def SetCCDTemperature(self):
        return self.cam.TargetSensorTemperature

    @SetCCDTemperature.setter
    def SetCCDTemperature(self, value):
        if value < 45 and value > -55:
            self.cam.TargetSensorTemperature = int(value)
        else:
            raise ValueError("Invalid value")

    def AbortExposure(self):
        self.cam.stop()

    def StopExposure(self):
        self.cam.stop()

    @property
    def SensorName(self):
        return self.cam.SensorType

    @property
    def Name(self):
        return self.cam.CameraModel

    @property
    def Description(self):
        return f"{self.cam.CameraFamily} {self.cam.CameraModel} {self.cam.CameraName} {self.cam.InterfaceType} {self.cam.SerialNumber}"

    @property
    def DriverVersion(self):
        return self.cam.software_version

    @property
    def InterfaceVersion(self):
        return "3"

    # @property
    def DriverInfo(self):
        return self.cam.software_version

    # @property
    # def Debayer(self):
    #     return self.debayer

    # @Debayer.setter
    # def Debayer(self, value):
    #     if IsQHYCCDControlAvailable(self.cam, CONTROL_ID.CAM_COLOR) in [BAYER_ID.BAYER_GB, BAYER_ID.BAYER_GR, BAYER_ID.BAYER_BG, BAYER_ID.BAYER_RG]:
    #         SetQHYCCDDebayerOnOff(self.cam, value)
    #         self.debayer = value
    #         if value:
    #             self.stype = 1
    #         else:
    #             self.stype = 2

    # @property
    # def USBTraffic(self):
    #     return GetQHYCCDParam(self.cam, CONTROL_ID.CONTROL_USBTRAFFIC)

    # @USBTraffic.setter
    # def USBTraffic(self, value):
    #     SetQHYCCDParam(self.cam, CONTROL_ID.CONTROL_USBTRAFFIC, int(value))

    # @property
    # def DDR(self):
    #     return IsQHYCCDControlAvailable(self.cam, CONTROL_ID.CONTROL_DDR) == ERROR_ID.SUCCESS

    # @DDR.setter
    # def DDR(self, value):
    #     SetQHYCCDParam(self.cam, CONTROL_ID.CONTROL_DDR, bool(value))

    # @property
    # def RowOffset(self):
    #     return self.rowoffset

    # @property
    # def SupportedActions(self):
    #     return ['RowOffset']
