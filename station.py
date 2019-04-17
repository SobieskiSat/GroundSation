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

conf = Configurator('config.yaml')
conf['labels']=structure
app = QApplication(sys.argv)
win = MainWidgetWindow(conf)
app.exec_()
