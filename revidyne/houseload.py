import serial
from .serialcom import SerialCommander
import time
from traitlets import HasTraits, observe, Instance, Int

inPrompts = {'getAll': ["Kilowatt capacity: ", "Current KW level: ", "Load allocated: ", \
                        "Difference between allocated and used KW: ", "Carbon value: ",  \
                        "Renewability: ", "Current Power: "] ,
           'getLoads': ["h1 load: ", "h2 load: ", "h3 load: ", "h4 load: "],
            'getLoadVal':  ["Combined load: "] ,
             'getKW':         ["KW: "],
              'getCarbon': ["Carbon emission in ton: "]}

class houseload(HasTraits, SerialCommander):
    h1 = Int()
    h2 = Int()
    h3 = Int()
    h4 = Int()
    def __init__(self, COM, SP):
        self.cmdMenu = {}
        self.cmds = {}
        self.port = COM
        self.baud_rate = SP
        super(houseload, self).connect()
        time.sleep(2)
        self.set_up_cmds()

    def set_up_cmds(self):

        #self.send_command("getCommands")
        #cmd_name = self.read_response()

        super(houseload, self).send_command("getCommands")
        cmd_name = super(houseload, self).read_response()
        
        while cmd_name != "eoc":
            super(houseload, self).send_command(cmd_name)
            cmd_name = super(houseload, self).read_response()
            print(cmd_name)
            num_of_output = 0
            num_of_input = 0
            special_index = -1  
            # Index of the first special char: ">" means cmd needs input, "<" means cmd has output

            if ">" in cmd_name:
                special_index = cmd_name.index(">")
                num_of_output = int(cmd_name[special_index + 1:])
            if "<" in cmd_name:
                special_index = cmd_name.index("<")
                num_of_input = int(cmd_name[special_index + 1:])

            if special_index != -1:
                cmd_name = cmd_name[:special_index]

            curr_cmd = Cmd(cmd_name, num_of_input, num_of_output)
            self.cmds[cmd_name] = curr_cmd         
          

    def call(self, cmd_name):
        if cmd_name not in self.cmds:
            print(f"ERROR: '{cmd_name}' is not in cmd menu")
            return

        curr_cmd = self.cmds[cmd_name]

        if curr_cmd.in_arg == 0 and curr_cmd.out_arg == 0:
            self.send_command(cmd_name)
        elif curr_cmd.in_arg != 0:
            self.read_cmd_message(cmd_name)
        elif cmd_name == "setLoad":
            self.set_load()
        elif cmd_name == "setVolts":
            self.set_volts()
        elif cmd_name == "setMot":
            self.set_mot()
        elif cmd_name == "setKp":
            self.set_kp()
        elif cmd_name == "setKi":
            self.set_ki()
        elif cmd_name == "setKd":
            self.set_kd()

    @observe('h1', 'h2', 'h3', 'h4')
    def setlimits(self, value):
        self.send_command(f"setLimits\n{self.h1}\n{self.h2}\n{self.h3}\n{self.h4}")

    def setLimits(self, h1, h2, h3, h4):
        self.h1 = h1
        self.h2 = h2
        self.h3 = h3
        self.h4 = h4
        self.send_command(f"setLimits\n{self.h1}\n{self.h2}\n{self.h3}\n{self.h4}")


    def read_cmd_message(self, cmd_name):
        if cmd_name not in self.cmds:
            print(f"ERROR: '{cmd_name}' is not in cmd menu")
            return

        count = self.cmds[cmd_name].in_arg
        self.send_command(cmd_name)
        time.sleep(0.1)  # Wait for response to be received
        cnt=0
        for _ in range(count):
            response = self.read_response()
            print(inPrompts[cmd_name][cnt], response)
            cnt=cnt+1

class Cmd:
    def __init__(self, name, in_arg, out_arg):
        self.name = name
        self.in_arg = in_arg
        self.out_arg = out_arg

#generator = GeneratorObj("/dev/cu.usbserial-110", 9600)
#generator.setup()  # Replace with your COM port and baud rate
#generator.call("init")
#generator.call("runRange")
# Call other commands as needed
#generator.call("off")  # For example, turning off the generator
