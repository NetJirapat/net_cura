import time
import ctypes
import sys
sys.path.insert(0, "C:/cura_laser/resources/spice_x86/")

def main():

    laser = ctypes.CDLL("C:/Users/Laylase/Documents/Visual Studio 2015/Projects/my_spice/Debug/my_spice.dll")
    #laser = ctypes.CDLL("C:/my_spice.dll")
    #return 0

    err = laser.init_card()
    print(err)
    if err != 0:
        laser.GetErrorMessage.restype = ctypes.c_char_p
        laser.GetErrorMessage.argtype = [ctypes.c_int32]
        msgs = laser.GetErrorMessage(err)
        print("Err != 0 : " + str(type(msgs)))

    #laser.draw_rect()
    print("getSn : " + str(laser.getSn()))
    print("getVersion : " + str(laser.getVersion()))
    print("getDLLVersion : " + str(laser.getDLLVersion()))

    laser.test()
    time.sleep(3)

if __name__ == "__main__":
    print("Start !!!")
    main()
    print("END !!!")
