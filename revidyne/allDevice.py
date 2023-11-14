
from serial.tools import list_ports
from .serialcom import SerialCommander
import re, time


class AllDevice:

  def __init__(self, spd=9600):
    self.devices={}
    self.spd = spd
    enmu_ports = enumerate(list_ports.comports())
    port = []
    for n, (p, descriptor, hid) in enmu_ports:
      if re.findall(r"Ser", descriptor)  :
        if "wch" not in p:
            print(p)
            port.append(p)

    for m in port:
        serial_commander = SerialCommander(m, self.spd)  # Replace with your serial port and baud rate
        serial_commander.connect()
        time.sleep(2)
        serial_commander.send_command("*ID?")
        response = serial_commander.read_response()
        print(response)

        self.devices[response]=Device(response, port=m, spd=self.spd)            

  def getAllDevice(self):
    return self.devices
       


class Device:
  def __init__(self, name, port, spd=9600):
      self.port = port
      self.name = name

      mod = __import__('.revidyne', fromlist=[name])
      klass = getattr(mod, name)
      self.device=klass(port, spd)

  def getDevice(self):
     return self.device

