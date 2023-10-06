import serial
from .serialcom import SerialCommander
import time
from traitlets import HasTraits, observe, Instance, Int, Float


inPrompts = {'getAll': ["Kilowatt capacity: ", "Current KW level: ", "Load allocated: ", \
                        "Difference between allocated and used KW: ", "Carbon value: ",  \
                        "Renewability: ", "Current Power: "] ,
           'getLoads': ["h1 load: ", "h2 load: ", "h3 load: ", "h4 load: "],
            'getLoadVal':  ["Combined load: "] ,
             'getKW':         ["KW: "],
              'getCarbon': ["Carbon emission in ton: "]}

class generator(HasTraits, SerialCommander):
    Kd = Float()
    Ki = Float()
    Kp = Float()
    Mot = Int()
    Volts = Int()
    load = Int()


    def __init__(self, COM, SP):
        self.cmdMenu = {}
        self.cmds = {}
        self.port = COM
        self.baud_rate = SP
        super(generator, self).connect()
        time.sleep(2)
        self.set_up_cmds()

    def set_up_cmds(self):

        #self.send_command("getCommands")
        #cmd_name = self.read_response()

        super(generator, self).send_command("getCommands")
        cmd_name = super(generator, self).read_response()
        
        while cmd_name != "eoc":
            super(generator, self).send_command(cmd_name)
            cmd_name = super(generator, self).read_response()
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
          

    def call(self, cmd_name, returnValue=False):
        if cmd_name not in self.cmds:
            print(f"ERROR: '{cmd_name}' is not in cmd menu")
            return

        curr_cmd = self.cmds[cmd_name]

        if curr_cmd.in_arg == 0 and curr_cmd.out_arg == 0:
            self.send_command(cmd_name)
        elif curr_cmd.in_arg != 0:
            return self.read_cmd_message(cmd_name, returnValue)
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


    @observe('Kd')
    def setkd(self, value):
        self.send_command(f"setKd\n{self.Kd}")

    def setKd(self, kd):
        self.send_command(f"setKd\n{kd}")


    @observe('Ki')
    def setki(self, value):
        self.send_command(f"setKi\n{self.Ki}")

    def setKi(self, ki):
        self.send_command(f"setKi\n{ki}")
        self.Ki = ki


    @observe('Kp')
    def setkp(self, value):
        self.send_command(f"setKp\n{self.Kp}")

    def setKp(self, kp):
        self.send_command(f"setKp\n{kp}")
        self.Kp = kp


    @observe('Mot')
    def setmot(self, value):
        self.send_command(f"setMot\n{self.Mot}")

    def setMot(self, mot):
        self.send_command(f"setMot\n{mot}")
        self.Mot = mot

    @observe('Volts')
    def setvolts(self, value):
        self.send_command(f"setVolts\n{self.Volts}")

    def setVolts(self, volts):
        self.send_command(f"setVolts\n{volts}")
        self.Volts = volts


    @observe('load')
    def setLoad(self, value):
        self.send_command(f"setLoad\n{self.load}")

    def setLoad(self, ld):
        self.send_command(f"setLoad\n{ld}")
        self.load = ld

    def read_cmd_message(self, cmd_name, returnValue=False):
        if cmd_name not in self.cmds:
            print(f"ERROR: '{cmd_name}' is not in cmd menu")
            return

        count = self.cmds[cmd_name].in_arg
        self.send_command(cmd_name)
        time.sleep(0.1)  # Wait for response to be received
        cnt=0
        data=[None] *count
        for _ in range(count):
            response = self.read_response()
            if (returnValue==False):
                print(inPrompts[cmd_name][cnt], response)
            data[cnt]=response
            cnt=cnt+1
        return data

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
