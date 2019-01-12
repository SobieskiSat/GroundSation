import sys
import yaml
from PyQt5 import QtWebEngineWidgets, QtCore
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QFrame,
QDialog, QApplication, QComboBox, QLabel, QCheckBox, QGridLayout, QFileDialog)
import matplotlib.pyplot as plt

#To be changed with GUI API

class OpenWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.btn_new_conection=QPushButton('Nowe Połączenie', self)
        self.btn_new_conection.move(20,40)
        self.btn_new_conection.clicked.connect(self.btn_new_conection_event)
        self.setGeometry(300, 300, 450, 350)
        self.setWindowTitle('Wybierz Akcję')
        self.show()

    def btn_new_conection_event(self):
        self.response='NC'
        self.close()

class ConfigureConnectionWindow(QWidget):
    def __init__(self, serials):
        super().__init__()
        self.initUI(serials)

    def initUI(self, serials):

        self.file=''

        self.port_label=QLabel('Port:')
        self.baudrate_label=QLabel('Baudrate:')
        self.timeout_label=QLabel('Timeout:')
        self.event_manager_box_label=QLabel('Use EventManager:')
        self.event_manager_file_label=QLabel('Set Log File:')
        self.positionX_label=QLabel('Map focus X:')
        self.positionY_label=QLabel('Map focus Y:')

        self.baudrate_edit=QLineEdit()
        self.positionX_edit=QLineEdit()
        self.positionY_edit=QLineEdit()
        self.baudrate_edit.setPlaceholderText('115200')
        self.timeout_edit=QLineEdit()
        self.event_manager_box=QCheckBox()
        self.event_manager_box.stateChanged.connect(self.event_manager_box_changed)

        self.port_box =QComboBox(self)
        for s in serials:
            self.port_box.addItem(s)

        self.btn_set_file=QPushButton('Choose File', self)
        self.btn_set_file.clicked.connect(self.file_dialog)
        self.btn_set_file.setEnabled(False)

        self.btn_connect=QPushButton('Connect', self)
        #self.btn_connect.move(150,200)
        self.btn_connect.clicked.connect(self.btn_connect_event)

        self.btn_load=QPushButton('Load Last Session', self)
        #self.btn_connect.move(150,200)
        self.btn_load.clicked.connect(self.btn_load_event)

        self.form_grid = QGridLayout()
        self.form_grid.setSpacing(10)

        self.form_grid.addWidget(self.port_label, 1, 0)
        self.form_grid.addWidget(self.port_box, 1, 1)
        self.form_grid.addWidget(self.baudrate_label, 2, 0)
        self.form_grid.addWidget(self.baudrate_edit, 2, 1)
        self.form_grid.addWidget(self.timeout_label, 3, 0)
        self.form_grid.addWidget(self.timeout_edit, 3, 1)
        self.form_grid.addWidget(self.event_manager_box_label, 4, 0)
        self.form_grid.addWidget(self.event_manager_box, 4, 1)
        self.form_grid.addWidget(self.event_manager_file_label, 5, 0)
        self.form_grid.addWidget(self.btn_set_file, 5, 1)
        self.form_grid.addWidget(self.positionX_label, 6, 0)
        self.form_grid.addWidget(self.positionX_edit, 6, 1)
        self.form_grid.addWidget(self.positionY_label, 7, 0)
        self.form_grid.addWidget(self.positionY_edit, 7, 1)
        self.form_grid.addWidget(self.btn_connect, 8, 0)
        self.form_grid.addWidget(self.btn_load, 8, 1)


        self.setLayout(self.form_grid)


        #print(SerialLoader.serials())
        self.setGeometry(300, 300, 450, 350)
        self.setWindowTitle('New Connection')
        self.show()

    def btn_connect_event(self):
        self.response={'port':str(self.port_box.currentText()),
        'port_num':self.port_box.currentIndex(),
        'baudrate':str(self.baudrate_edit.text()),
        'timeout':str(self.timeout_edit.text()),
        'use_event_manager':self.event_manager_box.checkState(),
        'file':self.file,
        'positionX':self.positionX_edit.text(),
        'positionY':self.positionY_edit.text()}
        with open('last_connection.yml', 'w') as outfile:
            yaml.dump(self.response, outfile, default_flow_style=False)
        self.close()

    def event_manager_box_changed(self):
        state=self.event_manager_box.checkState()
        self.btn_set_file.setEnabled(state)

    def file_dialog(self):
         file_name,a = QFileDialog.getOpenFileName(self, 'Open file', '/home')
         if file_name:
             self.file=file_name

    def btn_load_event(self):

        with open('last_connection.yml', 'r') as stream:
            session=yaml.load(stream)
            self.baudrate_edit.setText(str(session['baudrate']))
            self.timeout_edit.setText(str(session['timeout']))
            self.event_manager_box.setChecked(session['use_event_manager'])
            self.port_box.setCurrentText(str(session['port']))
            self.file=session['file']
            self.positionX_edit.setText(str(session['positionX']))
            self.positionY_edit.setText(str(session['positionY']))


class MainWidgetWindow(QWidget):
    def __init__(self, conf, labels):
        super().__init__()
        self.initUI(conf, labels)
    def initUI(self, conf, labels):
        self.labels={}
        self.conf=conf

        '''
        self.locationX_label=QLabel('Pozycja X:')
        self.locationY_label=QLabel('Pozycja Y:')
        self.height_label=QLabel('Wysokość:')
        self.speed_label=QLabel('Wysokość:')
        self.temperature_label=QLabel('Temperatura:')
        self.pressure_label=QLabel('Ciśnienie:')
        self.RRSI_label=QLabel('RRSI:')
        self.frequency_label=QLabel('Częstotliwość:')
        '''
        self.main_grid = QGridLayout()
        self.info_grid = QGridLayout()
        self.info_grid.setSpacing(10)
        elements=len(labels)
        if elements%2==0:
            elements=elements/2
        else:
            elements=(elements+1)/2
        for i in range(0,len(labels)):
            if i<elements:
                k=i
                j=0
            else:
                k=i-elements
                j=3
            self.labels[labels[i]['id']]={'text':QLabel(labels[i]['text']),
            'value':QLabel('-')}
            self.info_grid.addWidget(self.labels[labels[i]['id']]['text'], k+1, j)
            self.info_grid.addWidget(self.labels[labels[i]['id']]['value'], k+1, j+1)

        frame=QFrame()
        frame.setFrameShape(QFrame.VLine)
        self.info_grid.addWidget(frame, 1, 3, elements, 1)

        self.main_grid.addLayout(self.info_grid, 1,0)

        self.webView = QtWebEngineWidgets.QWebEngineView()
        self.webView.setUrl(QtCore.QUrl("D:\Projekty\Programowanide\CanSat\stacja\maps\map.html"))
        #self.webView.page.run
        #page().runJavaScript("[map.getBounds().getSouthWest().lat, map.getBounds().getSouthWest().lng, map.getBounds().getNorthEast().lat, map.getBounds().getNorthEast().lng]")
        self.main_grid.addWidget(self.webView, 1,1)
        self.webView.loadFinished.connect(self.webView_loaded_event)
        self.setLayout(self.main_grid)
        #self.map_functions()
        '''
        self.plot=plt.plot([1,2,3,4])
        self.plot.ylabel('some numbers')
        self.main_grid.addWidget(self.plot,2,1)
        '''
        self.input_grid=QGridLayout()

        self.setGeometry(300, 300, 590, 350)
        self.setWindowTitle('SobieskiSat')
        self.show()

    def update(self, data):
        posX=None
        posY=None
        rssi=None
        print(data)

        for d in data:

            for l_item, l_value in self.labels.items():
                if l_item == d['id']:
                    l_value['value'].setText(d['value'])

            print(d)
            if d['id']=='positionX':
                posX=d['value']
            if d['id']=='positionY':
                posY=d['value']
            if d['id']=='rssi':
                rssi=d['value']
        if posX!=None and posY!=None:
            self.map_add_point(posX, posY, rssi, '')


    def map_functions(self):
        #self.webView.page().runJavaScript('addPoint(50.05925, 19.92293, 13, "aaa")')
        self.webView.page().runJavaScript('alert("aa")')

    def map_add_point(self, posX, posY, signal, text):
        self.webView.page().runJavaScript('addPoint('+posX+', '+posY+', '+signal+', "'+text+'")')

    def resizeEvent(self, event):
        QWidget.resizeEvent(self, event)
        self.resize_map()

    def webView_loaded_event(self):
        self.webView_loaded=True
        self.webView.page().runJavaScript('init('+self.conf['positionX']+','+self.conf['positionY']+', 15)')
        self.resize_map()

    def resize_map(self):
        w=self.webView.frameSize().width()
        h=self.webView.frameSize().height()
        self.webView.page().runJavaScript('resizeMap("'+str(w)+'px","'+str(h)+'px")')
'''
stream = open('last_connection.yml', 'r')
print(yaml.load(stream))
print(stream)




app=QApplication(sys.argv)
win=OpenWindow()
app.exec_()
win=ConfigureConnectionWindow(['COM9','b'])
app.exec_()
win=MainWidgetWindow({'startX':'50.05925', 'startY':'19.92293'},[{'id':'height', 'text':'Wysokość:'}, {'id':'speed', 'text':'Prędkość:'}])
app.exec_()

print('ok')
'''
