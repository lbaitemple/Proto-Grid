
from serial.tools import list_ports
from .serialcom import SerialCommander
import re, time


class AllDevice:

  def __init__(self):
    self.devices={}
    enmu_ports = enumerate(list_ports.comports())
    port = []
    for n, (p, descriptor, hid) in enmu_ports:
      if re.findall(r"Ser", descriptor):
          print(p)
          port.append(p)

    for m in port:
        serial_commander = SerialCommander(m, 9600)  # Replace with your serial port and baud rate
        serial_commander.connect()
        time.sleep(2)
        serial_commander.send_command("*ID?")
        response = serial_commander.read_response()
        print(response)

        self.devices[response]=Device(response, port=m, spd=9600)            

  def getAllDevice(self):
    return self.devices
       


class Device:
  def __init__(self, name, port, spd=9600):
      self.port = port
      self.name = name

      mod = __import__('.revdyn', fromlist=[name])
      klass = getattr(mod, name)
      self.device=klass(port, spd)

  def getDevice(self):
     return self.device

