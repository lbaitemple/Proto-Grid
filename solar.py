import serial
from serial.tools import list_ports
enmu_ports = enumerate(list_ports.comports())
port = []

for n, (p, descriptor, hid) in enmu_ports:
    print(p, descriptor, hid)
    print(p)
    if descriptor == "USB-Serial Controller D":
        port.append(p)

print(port)
port = "/dev/cu.usbserial-11240" 
serial = serial.Serial()
serial.port = port
serial.baudrate = 9600
serial.timeout = 1
