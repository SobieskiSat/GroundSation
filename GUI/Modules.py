import sys
import yaml
from PyQt5 import QtWebEngineWidgets, QtCore, QtGui
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QFrame,
QDialog, QApplication, QComboBox, QLabel, QCheckBox, QGridLayout, QFileDialog)
import matplotlib.pyplot as plt

#Work in progress

class DictReader:
    def __init__(self, dict, default):
        self.dict = dict
        self.default = default

    def get_value(self, key):
        if key in self.dict:
            return kwargs[key]
        elif key in self.default:
            return self.default[key]
        else:
            raise KeyError

    def __getitem__(self, key):
        return self.get_value(key)



class InfoTable:
    def __init__(self):
        self.grid = QGridLayout()
        self.tables=[]

    def add(self, id, text, **kwargs):
        text_lable=QLabel(str(text))
        type=QLabel
        if 'type' in kwargs:
            type=kwargs['type']()
        try:
            value=type()
        except Exception:
            print('Type Error')
        self.grid.addWidget(text_lable, len(self.tables)+1, 0)
        self.grid.addWidget(value, len(self.tables)+1, 1)
        self.tables.append({'id':id, 'text':text_lable, 'value':value, 'type': type})

    def text(self, id, value):
        for i in self.tables:
            if i['id']==id and i['type']==QLabel:
                i['value'].setText(value)

    def update(self, id):
        for i in self.tables:
            if i['id']==id:
                return i

    def __getitem__(self, key):
        return self.update(key)


    def __setitem__(self, key, item):
        self.text(key, item)



class GUIWindow(QWidget):
    def __init__(self, **kwargs):
        super().__init__()
        self.default_values={
        'win_width':300,
        'win_height':300,
        'win_posX':300,
        'win_posY':300,
        'win_title':'SobieskiSat',
        'win_incon':'logo.png'
        }
        self._initGUI(kwargs)

    def _init_kwargs_reader(self, key, kwargs):
        if key in kwargs:
            return kwargs[key]
        elif key in self.default_valuesa:
            return self.default_values[key]
        else:
            raise KeyError

    def _run(self):
        self.setLayout(self.layout)
        self.show()

    def _initGUI(self, kwargs):
        dr = DictReader(kwargs, self.default_values)
        self.setGeometry(dr['win_width'], dr['win_height'], dr['win_posX'], dr['win_posX'])
        self.setWindowTitle(dr['win_title'])
        self.setWindowIcon(QtGui.QIcon(dr['win_incon']))
        self.layout = QGridLayout()
        self.layout.setSpacing(10)
        try:
            self.initUI()
            self._run()
        except:
            pass


#Testing
class TheWindow(GUIWindow):
    def initUI(self):
        print('init')
        it=InfoTable()
        it.add('speed', 'Prędkość')
        value_lable=QLabel('-')
        self.layout.addLayout(it(), 1, 1)
        self.layout.addWidget(value_lable, 1, 0)
'''
app=QApplication(sys.argv)
win=TheWindow()
app.exec_()
'''
