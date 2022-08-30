#!/usr/bin/env python3
import serial

def main():
    #print( sum([x+35 if x>60 else x+25 for x in [35,78,56,92,45,56,98,250,60,300]]) )
    ser = serial.Serial('/dev/ttyUSB0')  # open serial port
    print(ser.name)         # check which port was really used
    ser.write(b'hello')     # write a string
    ser.close()             # close port

if __name__ == "__main__":
    main()
