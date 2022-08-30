#!/usr/bin/env python3
import laserserial

laser = laserserial.LaserSerial()

def main():
    global laser
    
    print(str(laser.init()))
    while True:
        msg = input("Enter cmd : ")
        if msg == 'q':
            break
        msg = msg + '\n'
        laser.ser.write(msg.encode('utf-8'))     # write a string
        while True:
            res = laser.ser.readline()
            if len(res) > 0:
                print(res)
            else:
                break
    '''
    msg = 'state 1'+'\n'
    ser.write(msg.encode('utf-8'))
    '''
    laser.ser.close()             # close port

if __name__ == "__main__":
    main()
