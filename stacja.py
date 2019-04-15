from GUI.gui import *
from Modules.Communication import *
from Modules.EventManager import *
from Modules.Prediction import Predictor
import sys
from PyQt5.QtWidgets import QApplication
import threading
import time



def main_window(app, conf):
    '''
    em=Manager(conf['file'])
    rds = DataSaver('dstest6.txt')#raw data sever
    '''
    dm=DataManager(None)
    em=dm.em
    rds=dm.ds
    predictor = Predictor()

    '''
    r=Radio(port=conf['port'], baudrate = conf['baudrate'],
    timeout=conf['timeout'], event_manager=em)
    '''
    radio={
    'port':conf['port'],
    'baudrate':conf['baudrate'],
    'timeout':conf['timeout']
    }

    structure = [
    {'id': 'elevation', 'text':'Start elevation:' , 'num': 0},
    {'id': 'time', 'text':'Time:' , 'num': 0},
    {'id': 'rssi', 'text':'RSSI:' , 'num': 1},
    {'id':'positionX' , 'text': 'Pozycja X:' , 'num': 2},
    {'id': 'positionY', 'text': 'Pozycja Y:' , 'num': 3},
    {'id':'altitude' , 'text':'Wysokość:' , 'num': 4},
    {'id': 'temperature', 'text':'Temperatura:' , 'num': 5},
    {'id': 'pressure', 'text':'Ciśnienie:' , 'num': 6},
    {'id': 'pm25', 'text':'PM-2,5:' , 'num': 7},
    {'id': 'pm10', 'text':'PM-10:' , 'num': 8}

    ]

    dr=DataReader(structure, radio, event_manager = em, rds=rds)
    conf['dm']=dm
    conf['labels']=structure
    conf['predictor']=predictor
    conf['time']=get_time
    win=MainWidgetWindow(conf)

    reader = threading.Thread(target=dr.keepReading, args=(True, ), kwargs={'call':win.update,})
    reader.start()
    app.exec_()

def call_update(data):
    print(data)

def get_time():
    return time.time()

def new_connection(app):
    serials=SerialLoader().all_serials()
    names=[]
    for s in serials:
        names.append(s.device)
    win=ConfigureConnectionWindow(names)
    app.exec_()
    if(win.response):
        main_window(app, win.response)
'''
r=Radio(port='COM11')
r.keepReading(condition=True, call=print)
'''

app = QApplication(sys.argv)
win = OpenWindow()
app.exec_()
if(win.response=='NC'):
    new_connection(app)
