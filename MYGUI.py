from importlib import import_module
from msvcrt import kbhit
from ntpath import join
from PyQt5 import QtCore, QtGui, QtWidgets
from printer import *
from GUI import Ui_MainWindow
import time, threading
speed = 10
p= Printer()
fdir = "C:/nstda/cura_laser/resources/"
p.laser.init()
p.base.init()
statusStop = False
statusThread = False
mark = 15


def clicked_get_info():
    print(p.laser.getAllInfo())

def clicked_get_laser_state():
    print('Laser state : ' + str(p.laser.checkState(True)))

def clicked_off():
    ui.on.setStyleSheet("background-color:#040f13;\n"
"border-radius: 50px;\n"
"border: 1px solid #fff;\n"
"")
    ui.off.setStyleSheet("background-color:#a60000;\n"
"border-radius: 50px;\n"
"border: 1px solid #fff;\n"
"")
    ui.standby.setStyleSheet("background-color:#040f13;\n"
"border-radius: 50px;\n"
"border: 1px solid #fff;\n"
"")
    ui.text.setText("3D PRINTER : OFF")
    print(p.laser.setState(0))
    
def clicked_standby(): 
    ui.on.setStyleSheet("background-color:#040f13;\n"
"border-radius: 50px;\n"
"border: 1px solid #fff;\n"
"")
    ui.off.setStyleSheet("background-color:#040f13;\n"
"border-radius: 50px;\n"
"border: 1px solid #fff;\n"
"")
    ui.standby.setStyleSheet("background-color:#9f9f00;\n"
"border-radius: 50px;\n"
"border: 1px solid #fff;\n"
"")
    ui.text.setText("3D PRINTER : STANDBY")
    print(p.laser.setState(1)) 
    
def clicked_on():
    ui.on.setStyleSheet("background-color:#608f47;\n"
"border-radius: 50px;\n"
"border: 1px solid #fff;\n"
"")
    ui.off.setStyleSheet("background-color:#040f13;\n"
"border-radius: 50px;\n"
"border: 1px solid #fff;\n"
"")
    ui.standby.setStyleSheet("background-color:#040f13;\n"
"border-radius: 50px;\n"
"border: 1px solid #fff;\n"
"")
    ui.text.setText("3D PRINTER : ON")
    #p.laser.setState(2)
    
def clicked_home():
    p.base.gohome()


def set_layer0():
    print("Set home : Start")
    s = "Set home : Start\n" 
    home = p.base.getPosition()
    p.base_layer_pos = []
    p.base_layer_name = []
    for i in range(10):
        #self.printer.base.createPoint(i+1, int(home-(i*10)))
        level = int(home-(i*15))
        p.base.createPoint(2*i+1, level-1000)
        p.base_layer_pos.append((level-1000)*0.01)
        p.base_layer_name.append("layer " + str(i+1) + ', -1mm')
        p.base.createPoint(2*i+2, level)
        p.base_layer_pos.append(level*0.01)
        p.base_layer_name.append("layer " + str(i+1))
        s += "layer " + str(i) + " = " + str(p.base_layer_pos[i]) + " mm.\n"
    p.base_layer_count = len(p.base_layer_pos)
    print("Set home : Finished")
    s += "Set home : Finished\n"
    ui.text.setText(s)
         
    ui.listWidget_platform.clear()
    print('self.baseList.size = ' + str(ui.listWidget_platform.size))
    print("self.printer.base_layer_count = " + str(p.base_layer_count))
    for i in range(p.base_layer_count):
        #s = "layer " + str(i) + " : " + str(self.printer.base_layer_pos[i]) + " mm."
        ui.listWidget_platform.insertItem(i, p.base_layer_name[i])  
    baseLayer()  
def refresh():
        print("ManualWindow refresh.")
        ui.listWidget_platform.clear()
        print("self.printer.base_layer_count = " + str(p.base_layer_count))
        for i in range(p.base_layer_count):
            #s = "layer " + str(i) + " : " + str(self.printer.base_layer_pos[i]) + " mm."
            ui.listWidget_platform.insertItem(i, p.base_layer_name[i])
def baseLayer():
    row = ui.listWidget_platform.currentRow()
    print("baseLayer : " + str(row))
    res = p.base.point(int(row)+1, True)
    print(res)
    get_current_position()   
                  
def clicked_load_GCode():
    gcode_file = "C:/nstda/cura_laser/resources/ear/layer_0.gcode"
    status = p.gcode.init(gcode_file)
    
    row = ui.listWidget_gcode.currentRow()
    print("gcodeRow : " + str(row))
    print("gcodeFile : " + fList[row])
    b = p.gcode_init(fdir + fList[row])
    if b:
        b = "True"
    else:
        b = "False"
    print("gcode loadding : " + b)
    ui.text.setText("gcode loadding : " + b)
    ui.gcodeStatus.setText("gcode loadding : " + b)  ##
    fList = getFileLists(fdir)
    for i in range(len(fList)):
        ui.listWidget_gcode.insertItem(i, fList[i])
        ###

def getFileLists(mypath):
        from os import listdir
        from os.path import isfile, join
        return [f for f in listdir(mypath) if isfile(join(mypath, f))]
    
#speed
def clicked_up():
    global speed
    speed = speed + 1
    if speed > 10:
        speed = 10
    updateSpeed()
def clicked_down():
    global speed
    speed = (speed - 1)
    if speed < 1:
        speed = 1
    updateSpeed()
def updateSpeed():
    ui.lineEdit_speed.setText(str(speed))
    p.base.setSpeed(speed)
    
def get_current_position(): #updatePos
    position_value = p.base.getPosition()*0.01
    ui.text.setText("Current Position : " + str(position_value) + "mm")
    ui.lineEdit_current_position.setText(str(position_value))

def clicked_set_value(): #goPos
    pos = float(ui.lineEdit_current_position.text())
    p.base.goPos(pos)
    get_current_position()

#parameter
def get_epfq():
    s = p.laser.getEpfq()
    #ui.text('epfq = ' + str(s))
    ui.lineEdit_epfq.setText(str(s))
    return s
def set_epfq():
    s = ui.lineEdit_epfq.text()
    p.laser.setStdfreq(s)
    ui.lineEdit_epfq.setText(str(get_epfq()))
def get_freq():
    s = p.laser.getFreq()
    #ui.text('freq = ' + str(s))
    ui.lineEdit_freq.setText(str(s))
    return s
def set_freq():
    s = ui.lineEdit_freq.text()
    p.laser.freq(s)
    ui.lineEdit_freq.setText(str(get_freq()))
def get_offtime():
    s = p.laser.getOfftime()
    #ui.text('freq = ' + str(s))
    ui.lineEdit_offtime.setText(str(s))
    return s
def set_offtime():
    s = ui.lineEdit_offtime.text()
    p.laser.freq(s)
    ui.lineEdit_offtime.setText(str(get_offtime()))
def get_gateext():
    s = p.laser.getGateext()
    ui.lineEdit_gateext.setText(str(s))
    return s
def set_gateext():
    s = ui.lineEdit_gateext.text()
    p.laser.setGateext(s)
    ui.lineEdit_gateext.setText(str(get_offtime()))
def get_XY_Gain():
    s = p.laser.getGateext()
    ui.lineEdit_XY_Gain.setText(str(s))
    return s
def set_XY_Gain():
    s = ui.lineEdit_XY_Gain.text()
    p.laser.setGateext(s)
    ui.lineEdit_XY_Gain.setText(str(get_offtime()))
"""
def get_mark_speed():  
    s = p.laser.getXXX()  #getXXX --> You have to add function setMarkSpeed in laserserail.py before open#mark_speed
    ui.lineEdit_mark_speed.setText(str(s))
    return s
def set_mark_speed():  
    s = ui.lineEdit_mark_speed.text() 
    p.laser.setXXX(s)  #setXXX --> You have to add function getMarkSpeed in laserserail.py before open#mark_speed
    ui.lineEdit_mark_speed.setText(str(get_offtime()))
"""
#execute
def execute():
    statusThread = True
    #p.execute_layer(0)
    p.exec_laser(True,mark)
    print("Laser Excuting...")
    time.sleep(0.01)
    s = p.head.card.read_status()
    print("before : " + bin(s) + ": s")
    print("before : " + bin(s)[8] + ": s")
    while bin(s)[8] != '1':
        if statusStop is True:
            break
        print(bin(s)[8] + ": s")
        s = p.head.card.read_status()                    
        time.sleep(1)
    p.laser.setState(1)
    p.exec_laser(False, mark)
    print("Layer finished.")
    statusThread = False
def executeThread():
    print('executeThread')
    if statusThread is False:
        statusStop = False
        excThread = threading.Thread(target=execute)
        excThread.start()
def executeStop():
    statusStop = True

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.Load_G_Code.clicked.connect(clicked_load_GCode)
    ui.off.clicked.connect(clicked_off)
    ui.standby.clicked.connect(clicked_standby)
    ui.on.clicked.connect(clicked_on)
    ui.home.clicked.connect(clicked_home)
    ui.get_current_position.clicked.connect(get_current_position)
    ui.set_layer0.clicked.connect(set_layer0)
    ui.up.clicked.connect(clicked_up)
    ui.down.clicked.connect(clicked_down)
    ui.set_value.clicked.connect(clicked_set_value)
    get_epfq()
    get_freq()
    get_offtime()
    get_gateext()
    get_XY_Gain()
    ui.Set_epfq.clicked.connect(set_epfq)
    ui.Set_freq.clicked.connect(set_freq)
    ui.Set_Offtime.clicked.connect(set_offtime)
    ui.Set_gateext.clicked.connect(set_gateext)
    ui.Set_XY_Gain.clicked.connect(set_XY_Gain)
    ui.start_printing.clicked.connect(executeThread)
    ui.stop_printing.clicked.connect(executeStop)
    MainWindow.show()
    sys.exit(app.exec_())