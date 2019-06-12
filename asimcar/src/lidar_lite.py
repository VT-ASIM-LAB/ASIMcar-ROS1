from smbus2 import SMBus
import time

class Lidar_Lite():
  def __init__(self, bus):
    self.bus = SMBus(bus)
    self.address = 0x62
    self.distWriteReg = 0x00
    self.distWriteVal = 0x04
    self.distReadReg1 = 0x8f
    self.distReadReg2 = 0x10
    self.velWriteReg = 0x04
    self.velWriteVal = 0x08
    self.velReadReg = 0x09
    self.updateTime = 0.005
  """
  def connect(self, bus):
    try:
      self.bus = SMBus(bus)
      time.sleep(0.5)
      return 0
    except:
      return -1
  """

  def writeAndWait(self, register, value):
    self.bus.write_byte_data(self.address, register, value);
    time.sleep(self.updateTime)

  def readAndWait(self, register):
    res = self.bus.read_byte_data(self.address, register)
    time.sleep(self.updateTime)
    return res

  def readDistAndWait(self, register):
    res = self.bus.read_i2c_block_data(self.address, register, 2)
    time.sleep(self.updateTime)
    return (res[0] << 8 | res[1])

  def getDistance(self):
    self.writeAndWait(self.distWriteReg, self.distWriteVal)
    dist = self.readDistAndWait(self.distReadReg1)
    return dist

  def getVelocity(self):
    self.writeAndWait(self.distWriteReg, self.distWriteVal)
    self.writeAndWait(self.velWriteReg, self.velWriteVal)
    vel = self.readAndWait(self.velReadReg)
    return self.signedInt(vel)

  def signedInt(self, value):
    if value > 127:
      return (256-value) * (-1)
    else:
      return value


