import sys
import yaml
from PyQt5 import QtWebEngineWidgets, QtCore, QtGui
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QFrame,
QDialog, QApplication, QComboBox, QLabel, QCheckBox, QGridLayout, QFileDialog)
import matplotlib.pyplot as plt

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

    def add(self, id, text):
        text_lable=QLabel(str(text))
        value_lable=QLabel('-')
        self.grid.addWidget(text_lable, len(self.tables)+1, 0)
        self.grid.addWidget(value_lable, len(self.tables)+1, 1)
        self.tables.append({'id':id, 'text':textlable, 'value':value_lable})

    def update(self, id, value):
        for i in self.tables:
            if i['id']==id:
                i['value'].setText(value)

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
        self._initUI(kwargs)

    def _init_kwargs_reader(self, key, kwargs):
        if key in kwargs:
            return kwargs[key]
        elif key in self.default_valuesa:
            return self.default_values[key]
        else:
            raise KeyError

    def _initUI(self, kwargs):
        dr = DictReader(kwargs, self.default_values)
        self.setGeometry(dr['win_width'], dr['win_height'], dr['win_posX'], dr['win_posX'])
        self.setWindowTitle(dr['win_title'])
        self.setWindowIcon(QtGui.QIcon(dr['win_incon']))
        self.layout = QGridLayout()
        self.layout.setSpacing(10)
        self.setLayout(self.layout)
        try:
            self.initUI()
        except:
            pass


class TheWindow(GUIWindow):
    def initUI(self):
        it=InfoTable()
        it.add('speed', 'Prędkość')
        value_lable=QLabel('-')
        self.layout.addLayout(it, 1,1)
        self.layout.addWidget(value_lable, 1,0)

app=QApplication(sys.argv)
win=TheWindow()
win.show()
app.exec_()
