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
        return self.data

    def __str__(self):
        return str(self.data)

def new_reader(info, call):
    if info['type'] == 'radio':
        radio={
        'port':info['port'],
        'baudrate':info['baudrate'],
        'timeout':info['timeout']
        }
        dr=DataReader(info['labels'], radio, event_manager = info['em'], rds=info['rds'])
        reader = threading.Thread(target=dr.keepReading, args=(True, ), kwargs={'call':call,})

conf = Configurator('config.yaml')
dm=DataManager(None)
em=dm.em
rds=dm.ds
print(conf)
conf['dm'] = dm
conf['rds'] = rds
conf['em'] = em
app = QApplication(sys.argv)
win = MainWidgetWindow(conf, new_reader)
app.exec_()
