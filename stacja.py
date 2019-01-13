from GUI.gui import *
from Modules.Communication import *
from Modules.EventManager import *
import sys
from PyQt5.QtWidgets import QApplication
import threading



def main_window(app, conf):
    em=Manager(conf['file'])#new EventManager
    r=Radio(port=conf['port'], baudrate = conf['baudrate'],
    timeout=conf['timeout'], event_manager=em)#new Radio
    labels=[{'id':'positionX' , 'text': 'Pozycja X:'},
    {'id': 'positionY', 'text': 'Pozycja Y:'},
    {'id':'altitude' , 'text':'Wysokość:'},
    {'id': 'temperature', 'text':'Temperatura:'},
    {'id': 'pressure', 'text':'Ciśnienie:'},
    {'id': 'rssi', 'text':'RSSI:'}]#labels to display
    win=MainWidgetWindow(conf, labels)
    reader = threading.Thread(target=r.keepReading, args=(True, ), kwargs={'call':win.update})#radio reader Thread
    reader.start()
    app.exec_()


def new_connection(app):
    serials=SerialLoader().all_serials() #find all serial ports
    names=[] #names of serials (COM9)
    for s in serials:
        names.append(s.device)
    win=ConfigureConnectionWindow(names)
    app.exec_()
    if(win.response):#on connent
        main_window(app, win.response)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = OpenWindow()
    app.exec_()
    if(win.response=='NC'): #new connection
        new_connection(app)
