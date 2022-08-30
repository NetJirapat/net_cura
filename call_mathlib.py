#!/usr/bin/env python3

import time
import ctypes

def main():

    #mymath = ctypes.CDLL("C:/Users/Laylase/Documents/Visual Studio 2015/Projects/math_dll/Debug/math_dll.dll")
    #mymath = ctypes.CDLL("C:/Users/Laylase/Documents/Visual Studio 2015/Projects/math_dll/x64/Debug/math_dll.dll")


    mymath.fibonacci_init(1, 1)

    for i in range(5):
        print("[" + str(i) + "] : ")
        print(mymath.fibonacci_index())
        print(mymath.fibonacci_current())
        print(mymath.fibonacci_next())
        print("--------------")

def main2():
    mymath = ctypes.CDLL("C:/Users/Laylase/Documents/Visual Studio 2015/Projects/math_int_lib/Debug/math_int_lib.dll")
    
    a = [1, 20, 3]
    b = [5, 4, 3]
    for i in range(len(a)):
        print(str(mymath.plus(a[i], b[i])) + ", " + str(mymath.minus(a[i], b[i])))
    
    math_f = ctypes.CDLL("C:/Users/Laylase/Documents/Visual Studio 2015/Projects/math_float_lib/Debug/math_float_lib.dll")
    for i in range(len(a)):
        print(str(math_f.plus_i(a[i], b[i])) + ", " + str(math_f.minus_i(a[i], b[i])))

    c = [1.1, 20.5, 3.75]
    d = [5.2, 4.6, 3.75]
    for i in range(len(c)):
        c[i] = ctypes.c_float(c[i])
        d[i] = ctypes.c_float(d[i])
        print(str(c[i]) + ", " + str(d[i]) + ", " + str(math_f.plus_f(c[i], d[i])) + ", " + str(math_f.minus_f(c[i], d[i])))        
    

if __name__ == "__main__":
    print("Start !!!")
    #main()
    main2()
    print("END !!!")
