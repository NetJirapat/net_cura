import os
import gcode

gcode = gcode.Gcode()

fname = "C:/cura_laser/resources/PM_Strip_with_holes-Body.gcode"
fout = "C:/cura_laser/resources/strip_holes/"

def main():
    if not os.path.exists(fout):
        os.mkdir(fout)

    if not gcode_init(fname, debug=True):
        return False

    gcode.layers_splitter(fout)

def gcode_init(fname, debug=False):
    global gcode
    if not gcode.init(fname, debug):
        print("Gcode init failed.")
        return False
    print("Gcode init passed.")
    return True

if __name__ == "__main__":
    main()
