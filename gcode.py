class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
class Gcode():
    def __init__(self):
        self.fname = ""
        self.layers = []
        self.file_handler = ""
        
    def init(self, fname:str, debug=False):
        self.fname = ""
        self.layers = []
        self.file_handler = ""
        f = open(fname, "r")
        datas = f.readlines()
        for d in datas:
            if "G0" in d or "G1" in d or 'LAYER:' in d:
                p = self.str2pnt(d)
                #print(str(p.x) + ", " + str(p.y))
                self.layers.append(p)
        if debug:
            print(datas)
        f.close()
        return True
    
    def str2pnt(self, msg:str) -> Point:
        msg = msg.split()
        p = Point(-1,-1)
        for k in msg:
            if 'X' in k:
                p.x = float(k[1:])
            elif 'Y' in k:
                p.y = float(k[1:])
        return p

    def layer2file(self, fname):
        f = open(fname, 'w')
        for x in self.layers:
            f.writelines(x)
        f.close()
    
    def layers_splitter(self, folder:str):
        l = -1
        print('type: {}, len: {}'.format(type(self.layers), len(self.layers)))
        for x in self.layers:
            print('x : type: {}'.format(type(x)))
            if "LAYER:" in x:
                new_l = self.get_layer_number(x)
                print("LAYER : " + str(new_l))
                if l is -1:
                    l = new_l
                    self.file_handler = open(folder+"layer_"+str(l)+".gcode", 'w')
                elif l != new_l:
                    self.file_handler.close()
                    l = new_l
                    self.file_handler = open(folder+"layer_"+str(l)+".gcode", 'w')
            elif "G0" in x or "G1" in x:
                self.file_handler.writelines(x)
        self.file_handler.close()

    def get_layer_number(self, msg:str) -> int:
        x = int(''.join(i for i in msg if i.isdigit()))
        return x
