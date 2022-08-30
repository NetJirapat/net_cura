# https://www.yrginc.com/Catalog/PDF/CurrentManuals/CONTROLLER_E/TS_E_V2.03.pdf

import serial
import serial.tools.list_ports
import time
import yamaha

base = yamaha.Yamaha()

def main():
    global connected, base

    '''
    device_port=""
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in sorted(ports):
        if "DTA3660FA" in hwid:
            device_port = port
    if device_port is "":
        print("Yamaha device not found.")
        return False

    print("Yamaha port name : " + device_port)
    serial_port = serial.Serial(device_port,
                                38400,
                                bytesize=serial.EIGHTBITS,
                                parity=serial.PARITY_ODD,
                                stopbits=serial.STOPBITS_ONE,
                                timeout=1)
    '''
    if not base.init():
        print("Can't find Yamaha device.")
        return False

    #base.tmp()


    while(True):
        msg = input("Enter cmd : ")
        if msg is 'q':
            break
        elif msg.isnumeric():
            res = base.point(int(msg))
            print(res)
        elif msg is 'v':
            res = base.servo(False)
            print(res)
        elif msg is 'V':
            res = base.servo(True)
            print(res)
        elif msg is 'b':
            res = base.breakServo(False)
            print(res)
        elif msg is 'B':
            res = base.breakServo(True)
            print(res)
        elif msg is 's':
            #serial_port.write(str.encode("@?D0.1\r\n"))
            res = base.write("@?D0.1\r\n")
            print(res)
        elif msg != "":
            #for x in msg:
            #    print(str(ord(x)) + str(" : ") + str(x))
            #serial_port.write(str.encode(msg+"\r\n"))
            res = base.write(msg+"\r\n")
            print(res)
    
    
        '''
        while serial_port.inWaiting()>0:
            data_str = serial_port.read(serial_port.inWaiting()).decode('ascii')
            print(data_str, end='')
            time.sleep(0.01)
        '''
    base.terminate()

    '''
    while (True):
        # NB: for PySerial v3.0 or later, use property `in_waiting` instead of function `inWaiting()` below!
        if (ser.inWaiting()>0): #if incoming bytes are waiting to be read from the serial input buffer
            data_str = ser.read(ser.inWaiting()).decode('ascii') #read the bytes and convert from binary array to ASCII
            print(data_str, end='') #print the incoming string without putting a new-line ('\n') automatically after every print()
        #Put the rest of your code you want here
        time.sleep(0.01) # Optional: sleep 10 ms (0.01 sec) once per loop to let other threads on your PC run during this time. 

	my_str = "@?D0.1\r\n"
	my_str_as_bytes = str.encode(my_str)
	self.ser.write(my_str_as_bytes)
	x = self.ser.read(100).decode()
	if not ("D0.1" in x and "OK" in x):
		return False
	return True
    '''

if __name__ == "__main__":
    main()