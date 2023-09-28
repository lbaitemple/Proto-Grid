
from serial.tools import list_ports
import re


class AllDevice:

  def __init__(self):
    self.devices={}
    enmu_ports = enumerate(list_ports.comports())
    port = []
    for n, (p, descriptor, hid) in enmu_ports:
    #print(p, descriptor, hid)
    #print(p)
      if re.findall(r"Ser", descriptor):
          print(p)
          port.append(p)

    for m in port:
        serial_commander = SerialCommander(m, 9600)  # Replace with your serial port and baud rate
        serial_commander.connect()
        time.sleep(2)
        serial_commander.send_command("*ID?")
        response = serial_commander.read_response()

        if (response == "houseload"):
            self.devices.append("household")
