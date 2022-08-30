import ctypes

class Card():
    def __init__(self):
        self.card = ""
    
    def init(self):
        #self.card = ctypes.CDLL("C:/Users/Laylase/Documents/Visual Studio 2015/Projects/laser_rect_dll/Debug/laser_rect_dll.dll")
        #self.card = ctypes.CDLL("D:/Users/Laylase/Documents/Visual Studio 2015/Projects/laser_rect_dll/Debug/laser_rect_dll.dll")
        #self.card = ctypes.CDLL("D:/Users/Laylase/Documents/Visual Studio 2015/Projects/laser_rect_dll/x64/Debug/laser_rect_dll.dll")
        self.card = ""
        #self.card.init_card()
        return True

    def enable_laser(self, n):
        self.card.enable_laser(n)
    
    def laser_on(self, n, x):
        self.card.laser_on(n, x)