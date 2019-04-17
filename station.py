from GUI.gui import *
from Modules.Communication import *
from Modules.EventManager import *
from Modules.Prediction import Predictor
import sys
from PyQt5.QtWidgets import QApplication
import threading
import time
import yaml

class Configurator:
    def __init__(self, file):
        self.file = file
        try:
            with open(file, 'r') as stream:
                self.data=yaml.load(stream)
        except Exception as e:
            print(e)

    def __setitem__(self, key, value):
        self.data[key]=value
        with open(self.file, 'w') as outfile:
            yaml.dump(self.data, outfile, default_flow_style=False)

    def __getitem__(self, key):
        return self.data[key]

    def get(self, key):
        return self.__getitem__(key)

structure = [
{'id': 'elevation', 'text':'Start elevation:' , 'num': 0},
{'id': 'time', 'text':'Time:' , 'num': 9},
{'id': 'rssi', 'text':'RSSI:' , 'num': 1},
{'id':'positionX' , 'text': 'Pozycja X:' , 'num': 2},
{'id': 'positionY', 'text': 'Pozycja Y:' , 'num': 3},
{'id':'altitude' , 'text':'Wysokość:' , 'num': 4},
{'id': 'pressure', 'text':'Ciśnienie:' , 'num': 5},
{'id': 'temperature', 'text':'Temperatura:' , 'num': 6},
{'id': 'pm25', 'text':'PM-2,5:' , 'num': 7},
{'id': 'pm10', 'text':'PM-10:' , 'num': 8}
]

conf = Configurator('config.yaml')
conf['labels']=structure
app = QApplication(sys.argv)
win = MainWidgetWindow(conf)
app.exec_()
