import laserserial
import keyboard as key

laser = laserserial.LaserSerial()

def main():
    global laser
    
    laser.init()
    
    while True:
        if key.is_pressed('q'):
            break
        print('----- Start -----')
        x = 'State : ' + str(laser.getState())
        x = x + '\nis1 : ' + str(laser.getIs1())
        x = x + '\nimax : ' + str(laser.getImax())
        x = x + '\nia1 : ' + str(laser.getIa1())
        x = x + '\nta1 : ' + str(laser.getTa1())
        x = x + '\nepfq : ' + str(laser.getEpfq())
        x = x + '\nfreq : ' + str(laser.getFreq())
        x = x + '\nofftime : ' + str(laser.getOfftime())
        x = x + '\ngate_ext : ' + str(laser.getGateext())
        x = x + '\nerror : ' + str(laser.getErrors())
        x = x + '\nwarning : ' + str(laser.getWarnings())
        print(x)
        print('----- End -----')

if __name__ == "__main__":
    main()
