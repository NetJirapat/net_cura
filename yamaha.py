import serial
import serial.tools.list_ports
import time

class Yamaha():
    def __init__(self):
        self.id = "DTA3660FA"
        self.port = ""
    def __del__(self):
        self.terminate()

    def terminate(self):
        if hasattr(self, 'ser'):
            if self.ser.is_open:
                self.ser.close()        
    
    def init(self, debug=False):
        ports = serial.tools.list_ports.comports()
        for port, desc, hwid in sorted(ports):
            if self.id in hwid:
                self.port = port
        if self.port is "":
            print("Yamaha device not found.")
            return False

        if debug:
            print("Yamaha port name : " + self.port)
        self.ser = serial.Serial(self.port,
                                 38400,
                                 bytesize=serial.EIGHTBITS,
                                 parity=serial.PARITY_ODD,
                                 stopbits=serial.STOPBITS_ONE,
                                 timeout=1)
        my_str = "@?D0.1\r\n"
        my_str_as_bytes = str.encode(my_str)
        self.ser.write(my_str_as_bytes)
        x = self.ser.read(100).decode()
        if not ("D0.1" in x and "OK" in x):
            return False
        self.clearError()
        self.setSpeed(25)
        return True
        
    def write(self, msg:str) -> str:
        str_as_bytes = str.encode(msg)
        self.ser.write(str_as_bytes)

    def read(self, cmd):
        t = time.time()
        x = ""
        while time.time()-t < 0.2:
            x = x + self.ser.read(50).decode()
            if cmd in x and "OK.1" in x:
                return x[x.find(cmd):]
        return ""
    def readAll(self):
        return self.ser.read(100).decode()

    def servo(self, status:bool):
        msg = "@SRVO"+str(int(status))+".1\r\n"
        #print("msg : " + msg)
        self.write(msg)
        #x = self.write("@SRVO0.1")
        #print("servo : " + x)
        return self.readAll()
    def breakServo(self, status:bool):
        msg = "@BRK"+str(int(status))+".1\r\n"
        x = self.write(msg)
        return self.readAll()
    def point(self, num:int, block:bool=False):
        msg = "@START"+str(num)+".1\r\n"
        print("point : " + msg)
        x = self.write(msg)
        if block:
            t = time.time()
            t2 = time.time()
            while True:
                status = self.statusOperation()
                if time.time() - t2 > 1.0:
                    print("status : " + str(status))
                    #print("Position : " + str(self.getPosition()))
                    t2 = time.time()
                if status == 0:
                    break
        return self.readAll()
    def gohome(self):        
        msg = "@ORG.1\r\n"
        x = self.write(msg)
        return self.readAll()
    def goPos(self, pos):
        realPos = int(pos*100)
        print('realPos : {}'.format(realPos))
        self.createPoint(50, realPos)
        self.point(50)
    def reset(self):  
        msg = "@RESET.1\r\n"
        x = self.write(msg)
        return self.readAll()
    def clearError(self):
        self.reset()
        self.breakServo(False)
        self.servo(True)
    def setSpeed(self, speed):
        self.write("@K10.1=" + str(speed) + "\r\n")
        return self.readAll()
    def createPoint(self, dest, pos):
        cmd = "@COPY200-" + str(dest) + "" + ".1\r\n"
        print("createPoint : " + cmd)
        self.write(cmd)
        self.pointEdit(dest, pos)
        return self.readAll()
    def pointEdit(self, num, pos):
        cmd = "@P" + str(num) + ".1=" + str(pos) + "\r\n"
        print("pointEdit : " + cmd)
        self.write(cmd)
        
    def getPosition(self, debug=False) -> int:
        self.write("@?D0.1\r\n")
        x = self.read("D0.1=")
        if x == "":
            return self.getPosition()
        if debug:
            print("x : " + x)
        x = x[5:x.find('\r')]
        #for k in x:
        #    print(str(int(k)) + " : " + k)
        return int(x)
    def statusOperation(self):
        self.write("@?D18.1\r\n")
        x = self.read("D18.1=")
        if x == "":
            return self.statusOperation()
        x = x[6:x.find('\r')]
        return int(x)

    def up(self):
        print("up")
        self.write("@JOG+.1\r\n")
    def down(self):
        print("down")
        self.write("@JOG-.1\r\n")
    def stop(self):
        print("stop")
        self.write("@STOP.1\r\n")

    def tmp(self):
        #print(self.ser.name)
        #print(self.ser.is_open)
        c=0
        cmd = [0,1,2,6,7,9,10,13,14,17,18]
        cmd_desc = ["Current position",
                    "Current speed",
                    "Electrical current",
                    "Position command",
                    "Speed command",
                    "Voltage value",
                    "Temperature",
                    "Current point number",
                    "Load rate",
                    "Machine reference",
                    "Operation status"]
        for i in range(len(cmd)):
            my_str = "@?D" + str(cmd[i]) + ".1\r\n"
            my_str_as_bytes = str.encode(my_str)
            self.ser.write(my_str_as_bytes)
            x="--"
            while len(x)>0:
                x = self.ser.read(100)
                c = c+1
                if len(x)>0:
                    x = x.decode().split()
                    print("[" + str(cmd[i]) + "] : " + x[0] + "\t" + cmd_desc[i])
                    #print(str(type(x)))
                    #print(str(len(x)))
        print("Loop ending ...")
        #self.ser.close()
        #print(self.ser.is_open)
