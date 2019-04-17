import sys
import yaml
import copy
import os
from PyQt5 import QtWebEngineWidgets, QtCore
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QFrame,
QDialog, QApplication, QComboBox, QLabel, QCheckBox, QGridLayout, QFileDialog,
QHBoxLayout, QVBoxLayout, QSplitter, QRadioButton, QButtonGroup)
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from random import randint#nie potrzebne

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


        self.logButttonGroup=QButtonGroup(self)
        self.port_label=QLabel('Port:')
        self.baudrate_label=QLabel('Baudrate:')
        self.timeout_label=QLabel('Timeout:')
        self.event_manager_box_label=QLabel('Use custom EventManager:')
        self.event_manager_file_label=QLabel('Set Log File:')
        self.positionX_label=QLabel('Map focus X:')
        self.positionY_label=QLabel('Map focus Y:')
        self.elevation_label=QLabel('Elevation (m.n.p.m):') #nowe

        self.baudrate_edit=QLineEdit()
        self.positionX_edit=QLineEdit()
        self.positionY_edit=QLineEdit()
        self.elevation_edit=QLineEdit() #nowe

        self.baudrate_edit.setText('115200') #to jest faktycznie wpisany tekst
        #self.baudrate_edit.setPlaceholderText('115200') #to jest taka podpowiedź w stylu co tam ma być
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
        self.form_grid.addWidget(self.elevation_label, 8, 0) #nowe
        self.form_grid.addWidget(self.elevation_edit, 8, 1) #nowe
        self.form_grid.addWidget(self.btn_connect, 9, 0)
        self.form_grid.addWidget(self.btn_load, 9, 1)



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
        'positionY':self.positionY_edit.text(),
        'elevation':self.elevation_edit.text()}
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
            self.elevation_edit.setText(str(session['elevation']))


class MainWidgetWindow(QWidget):
    def __init__(self, conf):
        super().__init__()
        self.dm=DataManager(1000)
        self.initUI(conf)

    def initUI(self, conf):
        self.labels={}
        self.conf=conf
        labels=conf['labels']
        labels[0].update({'value': conf.get("elevation") }) #dodawanie value do "elevation"
        items=['time/rssi','time/positionX','time/positionY','time/temperature','time/pressure','time/altitude','time/pm25','time/pm10']

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

        #menubar = self.menuBar()

        self.main_grid = QVBoxLayout()
        self.top_widget=QWidget()
        self.top_grid=QGridLayout()
        self.top_widget.setLayout(self.top_grid)
        self.bottom_widget=QWidget()
        self.bottom_grid=QGridLayout()
        self.bottom_widget.setLayout(self.bottom_grid)
        self.info_grid = QGridLayout()
        self.info_widget=QWidget()
        self.panel_grid=QGridLayout()
        self.option_grid=QGridLayout()
        self.panel_grid.addLayout(self.info_grid, 1, 0)
        self.panel_grid.addLayout(self.option_grid, 2, 0)
        self.info_widget.setLayout(self.panel_grid)

        self.top_splitter=QSplitter(QtCore.Qt.Horizontal)
        self.top_splitter.addWidget(self.info_widget)


        self.vertical_splitter=QSplitter(QtCore.Qt.Vertical)
        self.vertical_splitter.addWidget(self.top_splitter)
        self.vertical_splitter.addWidget(self.bottom_widget)
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
        cwd = os.getcwd()+"/maps/map.html"
        self.webView = QtWebEngineWidgets.QWebEngineView()
        self.webView.setUrl(QtCore.QUrl(cwd))    #MAPS PATH


        #self.webView.page.run
        #page().runJavaScript("[map.getBounds().getSouthWest().lat, map.getBounds().getSouthWest().lng, map.getBounds().getNorthEast().lat, map.getBounds().getNorthEast().lng]")
        self.top_grid.addWidget(self.webView, 1,1)
        self.left_plot=self.draw_plot('time', 'altitude', self.dm)
        self.right_plot=self.draw_plot('time', 'pressure', self.dm)
        self.bottom_grid.addWidget(self.left_plot.get_widget(), 1,0)
        self.bottom_grid.addWidget(self.right_plot.get_widget(), 1,1)
        self.webView.loadFinished.connect(self.webView_loaded_event)
        self.top_splitter.addWidget(self.webView)

        self.new_flight_button=QPushButton('New Flight', self)
        self.new_flight_button.clicked.connect(self.new_flight)
        self.center_map_button=QPushButton('Center Map', self)
        self.center_map_button.clicked.connect(self.center_map)
        self.option_grid.addWidget(self.new_flight_button, 1, 0)
        self.option_grid.addWidget(self.center_map_button, 1, 1)

        self.left_plot_box = QComboBox(self)
        self.left_plot_box.addItems(items) #dodawanie listy wykresów

        self.left_plot_box.currentIndexChanged.connect(self.change_plots)

        self.right_plot_box = QComboBox(self)
        self.right_plot_box.addItems(items) #dodawanie listy wykresów

        self.right_plot_box.currentIndexChanged.connect(self.change_plots)


        self.left_plot_box_label = QLabel('Left Plot')
        self.right_plot_box_label = QLabel('Right Plot')

        self.option_grid.addWidget(self.left_plot_box_label, 2, 0)
        self.option_grid.addWidget(self.left_plot_box, 2, 1)
        self.option_grid.addWidget(self.right_plot_box_label, 3, 0)
        self.option_grid.addWidget(self.right_plot_box, 3, 1)

        self.time_control = TimeControlWidget(self)
        self.panel_grid.addWidget(self.time_control, 3, 0)

        self.main_grid.addWidget(self.vertical_splitter)
        self.setLayout(self.main_grid)
        #self.map_functions()
        '''
        self.plot=plt.plot([1,2,3,4])
        self.plot.ylabel('some numbers')
        self.main_grid.addWidget(self.plot,2,1)
        '''
        self.vertical_splitter.splitterMoved.connect(self.resize_map)
        self.top_splitter.splitterMoved.connect(self.resize_map)
        self.input_grid=QGridLayout()

        self.setGeometry(300, 300, 590, 350)
        self.setWindowTitle('SobieskiSat')
        self.show()

    def new_flight(self):
        self.conf['dm'].new_save()

    def change_plots(self):


        left = self.left_plot_box.currentText()
        right = self.right_plot_box.currentText()
        left=left.split('/')
        right=right.split('/')

        self.left_plot.lx = left[0]
        self.left_plot.ly = left[1]
        self.right_plot.lx = right[0]
        self.right_plot.ly = right[1]

    def center_map(self):
        posX=str(self.dm.get_by_id('positionX', 1)[0])
        posY=str(self.dm.get_by_id('positionY', 1)[0])
        try:
            self.webView.page().runJavaScript('centerMap('+posX+', '+posY+')')
        except Exception as e:
            print(e)
    def update(self, datag):
        #print('xd')
        posX=None
        posY=None
        rssi=None
        data=copy.deepcopy(datag)
        #print(data)
        self.dm.add(data)
        for d in data:
            for l_item, l_value in self.labels.items():
                if l_item == d['id']:
                    l_value['value'].setText(d['value'])

            if d['id']=='positionX':
                posX=d['value']
            if d['id']=='positionY':
                posY=d['value']
            if d['id']=='rssi':
                rssi=d['value']
        if posX!=None and posY!=None:
            self.map_add_point(posX, posY, rssi, str(data))
        #print(' try plot')
        try:
            self.left_plot.update()
            self.right_plot.update()
        except Exception as e:
            print('Graf nie działa!!!'+str(e))
        try:
            predicts_num=50
            if(len(self.dm.get_by_id('positionX', predicts_num))==predicts_num):
                pred=self.conf['predictor'].predict([
                    self.dm.get_by_id('positionX', predicts_num),
                    self.dm.get_by_id('positionY', predicts_num),
                    self.dm.get_by_id('altitude', predicts_num)], float(self.conf.get("elevation"))) #nowe zmiana stałej 202 na stałą ustalaną podczas startu programu w gui.py
                try:
                    self.webView.page().runJavaScript('drawPrediction('+str(pred['x'])+', '+str(pred['y'])+', '+str(pred['r'])+')')
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)

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

    def draw_plot(self, typex, typey, dm):
        return PlotG(typex, typey, dm)

    def __del__(self):

        with open('log1a.yml', 'w') as outfile:
            yaml.dump(self.data, outfile, default_flow_style=False)



class PlotG:
    def __init__(self, lx, ly, dm):
        self.dm=dm
        self.fig = plt.Figure()#main figure
        self.canvas=FigureCanvas(self.fig)
        self.sp=self.fig.add_subplot(1,1,1)
        self.length=100

        self.lx=lx#list of x param
        self.ly=ly# y param
        #self.plot=[]#all subplots
    '''
    def update(self):
        print(self.sp)
        self.datax.append(randint(1,20))
        self.datay.append(self.datay[-1]+1)
        self.sp.clear()
        self.sp.plot( self.datay[-30:],self.datax[-30:])
        self.canvas.draw()
    '''



    def update(self):#updates plot on call
        self.sp.clear()
        tab=self.dm.get_by_id(self.ly, self.length)
        tab2=self.dm.get_by_id(self.lx, self.length)
        self.sp.plot(tab2, tab)
        #self.sp.plot(self.make_data(self.ly, data), self.make_data(self.lx, data))
        self.canvas.draw()

        #print('xdddd')

    def make_data(self, id, data):#converts whole data into list of nums of id
        pass

    def get_widget(self):
        self.widget=QWidget()
        self.widget_layout=QGridLayout()
        self.widget.setLayout(self.widget_layout)
        self.button_layout=QGridLayout()
        self.widget_layout.addWidget(self.canvas, 1, 0)
        self.widget_layout.addLayout(self.button_layout, 1, 1)
        self.zoomin_button=QPushButton('+', self.widget)
        self.zoomout_button=QPushButton('-',self.widget)
        self.save_button=QPushButton('S',self.widget)
        self.pause_button=QPushButton('||',self.widget)
        self.zoomin_button.setMaximumSize(30, 30)
        self.zoomout_button.setMaximumSize(30, 30)
        self.pause_button.setMaximumSize(30, 30)
        self.save_button.setMaximumSize(30, 30)
        self.zoomin_button.clicked.connect(self._zoomin)
        self.zoomout_button.clicked.connect(self._zoomout)
        self.button_layout.addWidget(self.zoomin_button, 1, 0)
        self.button_layout.addWidget(self.zoomout_button, 2, 0)
        self.button_layout.addWidget(self.pause_button, 3, 0)
        self.button_layout.addWidget(self.save_button, 4, 0)

        return self.widget

    def _zoomin(self):
        if self.length>100:
            self.length-=50

    def _zoomout(self):
        self.length+=50


class TimeControlWidget(QWidget):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.setFixedHeight(50)

        self.left_button =QPushButton('<<')
        self.left_button.setMaximumSize(30, 30)
        self.left_button.clicked.connect(self.left_button_pushed)
        self.grid.addWidget(self.left_button, 1, 0)

        self.back_button =QPushButton('<')
        self.back_button.setMaximumSize(30, 30)
        self.back_button.setCheckable(True)
        self.back_button.clicked.connect(self.left_button_pushed)
        self.grid.addWidget(self.back_button, 1, 1)

        self.pause_button =QPushButton('||')
        self.pause_button.setMaximumSize(30, 30)
        self.pause_button.setCheckable(True)
        self.pause_button.clicked.connect(self.left_button_pushed)
        self.grid.addWidget(self.pause_button, 1, 2)

        self.forward_button =QPushButton('>')
        self.forward_button.setMaximumSize(30, 30)
        self.forward_button.setCheckable(True)
        self.forward_button.clicked.connect(self.left_button_pushed)
        self.grid.addWidget(self.forward_button, 1, 3)

        self.right_button =QPushButton('>>')
        self.right_button.setMaximumSize(30, 30)
        self.right_button.clicked.connect(self.left_button_pushed)
        self.grid.addWidget(self.right_button, 1, 4)

    def left_button_pushed(self):
        pass



class DataManager:
    def __init__(self, max):
        self.max=max
        self.data=[]

    def add(self, line):
        if len(self.data)>=self.max:
            self.data.pop(0)
        #print(line)
        self.data.append(line)
        #print(self.data)

    def get_by_id(self, id, length):
        list=self.get_last(length)
        res=[]
        try:
            for l in list:
                for dic in l:
                    if(dic['id']==id):

                        res.append(float(dic['value']))
        except Exception as e:
            print(e)
        return res

    def get_last(self, length):
        #print('xas')
        try:
            #print(self.data[-len])
            return self.data[-length:]
        except Exception:
            pass

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
