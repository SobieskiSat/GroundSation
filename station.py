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
        self.data = {}
        try:
            with open(file, 'r') as stream:
                self.data=yaml.load(stream)
        except Exception as e:
            print(e)

    def __setitem__(self, key, value):
        self.data[key]=value
        self.save()

    def save(self):
        #print(self.data)
        with open(self.file, 'w') as outfile:
            yaml.dump(self.data, outfile, default_flow_style=False)

    def __getitem__(self, key):
        return self.data[key]

    def get(self, key):
        return self.__getitem__(key)

    def update(self, new):
        self.data.update(new)
        self.save()

    def all(self):
        return copy.deepcopy(self.data)

    def __str__(self):
        return str(self.data)

def new_reader(conf, obj, call):
    if conf['type'] == 'radio':
        radio={
        'port':conf['port'],
        'baudrate':conf['baudrate'],
        'timeout':conf['timeout']
        }
        dr=DataReader(conf['labels'], radio, event_manager = obj['em'], rds=obj['rds'])
        reader = threading.Thread(target=dr.keepReading, args=(True, ), kwargs={'call':call,})
        reader.start()

conf = Configurator('config.yaml')
dm=DataManager(None)
obj={'dm':dm, 'em':dm.em, 'rds':dm.ds, 'reader':new_reader}
app = QApplication(sys.argv)
win = MainWidgetWindow(conf, obj)
app.exec_()
