from GUI.gui import *
from Modules.Communication import *
from Modules.EventManager import *
import sys
from PyQt5.QtWidgets import QApplication
import threading



def main_window(app, conf):
    em=Manager(conf['file'])
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
    {'id': 'rssi', 'text':'RSSI:' , 'num': None},
    {'id':'positionX' , 'text': 'Pozycja X:' , 'num': None},
    {'id': 'positionY', 'text': 'Pozycja Y:' , 'num': None},
    {'id':'altitude' , 'text':'Wysokość:' , 'num': None},
    {'id': 'temperature', 'text':'Temperatura:' , 'num': None},
    {'id': 'pressure', 'text':'Ciśnienie:' , 'num': None},
    {'id': 'pm25', 'text':'PM-2,5:' , 'num': None},
    {'id': 'pm10', 'text':'PM-10:' , 'num': None}
    ]

    dr=DataReader(structure, radio, event_manager = em)
    win=MainWidgetWindow(conf,[{'id': 'rssi', 'text':'RSSI:' , 'value': None},
    {'id':'positionX' , 'text': 'Pozycja X:' , 'value': None},
    {'id': 'positionY', 'text': 'Pozycja Y:' , 'value': None},
    {'id':'altitude' , 'text':'Wysokość:' , 'value': None},
    {'id': 'temperature', 'text':'Temperatura:' , 'value': None},
    {'id': 'pressure', 'text':'Ciśnienie:' , 'value': None},
    {'id': 'pm25', 'text':'PM-2,5:' , 'value': None},
    {'id': 'pm10', 'text':'PM-10:' , 'value': None}
    ])
    
    reader = threading.Thread(target=dr.keepReading, args=(True, ), kwargs={'call':print})
    reader.start()
    app.exec_()

def call_update(data):
    print(data)

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
