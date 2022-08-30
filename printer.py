import yamaha
import card
import laserserial
import gcode
import ctypes

class Printer():
    def __init__(self):
        self.base = yamaha.Yamaha()
        self.head = card.Card()
        self.laser = laserserial.LaserSerial()
        self.gcode = gcode.Gcode()
        self.base_layer_count = 0
        self.base_layer_pos = []
        self.base_layer_name = []
        self.exec_gain = 300
    
    def init(self, fname):
        res = ["Card init : ", "Laser init : ", "Base init : ", "G-Code init : "]
        self.init_status = [False, False, False, False]
        if (not (self.head is '')) and self.card_init():
            self.init_status[0] = True
        if (not (self.laser is '')) and self.laser_init():
            self.init_status[1] = True
        if self.base_init():
            self.init_status[2] = True
        if self.gcode_init(fname):
            self.init_status[3] = True
        
        for i in range(len(res)):
            res[i] = res[i] + self.b2str(self.init_status[i])
        
        if (not (self.laser is '')):
            self.laser_home_position()
        return res

    def get_execGain(self):
        return self.exec_gain
    def set_execGain(self, g):
        self.exec_gain = g
    def execute_layer(self, layer, mark=150.0):
        print("----- execute_layer : " + str(layer) + " : start -----")
        self.laser_home_position()
        print("Moving base to layer " + str(layer) + '.')
        res = self.base.point(layer+1, True)
        print("Base finished. Position : " + str(self.base.getPosition()*0.01) + " mm.")

        strLayer = str(i).zfill(3)
        print("Layer Loading : " + str(strLayer))
        fname = "C:/cura_laser/resources/gcodeHere/" + strLayer + ".gcode"
        print(fname)
        self.gcode_init(fname)
        print('Layer load finished.')

        self.exec_laser(True, mark)
        print("Laser Excuting...")
        time.sleep(0.01)
        s = self.head.card.read_status()
        #print("before : " + bin(s)[8] + ": s")
        while bin(s)[8] != '1':
            #print(bin(s)[8] + ": s")
            s = self.head.card.read_status()                    
            time.sleep(1)
        self.laser.setState(1)
        self.laser_home_position()
        print("----- execute_layer : " + str(layer) + " : end -----")
        
    def b2str(self, b):
        if b:
            return "Pass"
        return "Not found."
        
    def base_init(self):
        if not self.base.init():
            print("Base init failed.")
            return False
        print("Base init passed.")
        return True

    def laser_init(self):
        if not self.laser.init(True):
            print("Laser init failed.")
            return False
        print("Laser init passed.")
        return True

    def card_init(self):
        if not self.head.init():
            print("Head init failed.")
            return False
        print("Head init passed.")
        return True

    def gcode_init(self, fname):
        if not self.gcode.init(fname):
            print("Gcode init failed.")
            return False
        print("Gcode init passed.")
        return True
    
    def laser_home_position(self):
        self.head.card.start_list(True)
        self.head.enable_laser(True)
        self.head.card.add_point(0, 0)
        self.head.enable_laser(False)
        self.head.card.start_list(False)
        res = self.head.card.read_status()
        self.laser.setState(1)
        self.head.card.exec_list(True)

    def exec_laser(self, status:bool, k=300, mark=150.0):
        k = int(self.exec_gain)
        step_period = ctypes.c_ushort(60)
        jump_del = ctypes.c_ushort(300)
        mark_del = ctypes.c_ushort(300)
        poly_del = ctypes.c_ushort(50)
        laser_off_del = ctypes.c_ushort(300)
        laser_on_del = ctypes.c_ushort(200)
        t1 = ctypes.c_ushort(320)
        t2 = ctypes.c_ushort(200)
        t3 = ctypes.c_ushort(0)
        self.head.card.setDelays(step_period, jump_del, mark_del, poly_del, laser_off_del, laser_on_del, t1, t2, t3)

        jump = 1831.1
        jump = 180.0
        self.head.card.set_speed(ctypes.c_double(1831.1), ctypes.c_double(150.0)) # jump, mark

        x = []
        y = []
        for i in range(len(self.gcode.layers)):
            x.append(self.gcode.layers[i].x)
            y.append(self.gcode.layers[i].y)
        xx = [min(x), max(x), self.avg(x)]
        yy = [min(y), max(y), self.avg(y)]
        print("x : " + str(xx))
        print("y : " + str(yy))

        xt = []
        yt = []
        for i in range(len(self.gcode.layers)):
            x = ((self.gcode.layers[i].x-xx[0]) * k -10000)
            y = ((self.gcode.layers[i].y-yy[0]) * k -10000)
            xt.append(x)
            yt.append(y)
        xx = [min(xt), max(xt), self.avg(xt)]
        yy = [min(yt), max(yt), self.avg(yt)]
        print("x : " + str(xx))
        print("y : " + str(yy))

        if status:
            self.head.card.start_list(True)
            self.head.enable_laser(True)
            #self.head.laser_on(True)
            self.head.card.start_laser_manually(ctypes.c_bool(True))
        
            for i in range(len(self.gcode.layers)):
                x = ((self.gcode.layers[i].x-xx[0]) * k -10000)
                y = ((self.gcode.layers[i].y-yy[0]) * k -10000)
                self.head.card.add_point(int(x),int(y))
                for i in range(10):
                    self.head.card.delay_one_ms()

            #self.head.laser_on(False)
            self.head.enable_laser(False)
            self.head.card.start_list(False)
            res = self.head.card.read_status()
            self.laser.setState(2)
            self.laser.getAllInfo()
            self.head.card.exec_list(True)        
        else:
            self.laser.setState(1)
            self.laser.getAllInfo()
            self.head.card.exec_list(False)
            res = 'stop completed.'
        return res

    def avg(self, lst):
        return sum(lst) / len(lst)
