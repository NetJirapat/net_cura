import laserserial
import keyboard as key
import time


laser = laserserial.LaserSerial()

def main():
    global laser
    
    print(str(laser.init()))
    t = time.time()
    state = -1
    bCheck=False
    while True:
        if time.time()-t > 1.0:
            bIn = False
            if key.is_pressed('c'):
                break
            elif key.is_pressed('0'):
                laser.state(0)
                state = 0
                bIn=True
            elif key.is_pressed('1'):
                laser.state(1)
                state = 1
                bIn=True
            elif key.is_pressed('2'):
                laser.state(2)
                state = 2
                bIn=True
            if bIn:
                print('bIn')
                t = time.time()
                laser.readUntilOk()
                #laser.checkState()
                bCheck=True
                print('bIn-out')
        if bCheck:
            c = laser.checkState()
            if c == state:
                print('laser state = ' + str(c))
                print(time.time()-t)
                bCheck=False
        #print(laser.checkState())
        m = []
        laser.write('state?')
        m.append(laser.readLine())
        laser.write('is1?')
        m.append(laser.readLine())
        laser.write('imax?')
        m.append(laser.readLine())
        laser.write('ia1?')
        m.append(laser.readLine())
        laser.write('ta1?')
        m.append(laser.readLine())
        print(m)
    laser.terminate()

if __name__ == "__main__":
    main()
