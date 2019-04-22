import serial
import serial.tools.list_ports
import time
import yaml
import copy


class DataCreator:
    def __init__(self, conf, obj):
        self.conf = conf
        self.obj = obj
        self.data=[]

    def new_radio(self):
        self._dataCounter=0
        self.radio_conf={
        'port':self.conf['port'],
        'baudrate':self.conf['baudrate'],
        'timeout':self.conf['timeout']
        }
        try:
            #print('aaasd')
            self.radio = Radio(self.conf['baudrate'], self.conf['port'], self.conf['timeout'])
        except Exception as e:
            print(e)

    def run_radio(self):
        if hasattr(self, 'radio'):
            try:
                #print('xxa')
                line=self.radio.readline()
                #self._raw_data_sever(line)
                if line!=None:
                    self.obj['rds'].write(line)
                    line = self.parser(line)
                    self.call(line)
            except Exception as e:
                print(e)


    def loop(self):
        while(True):
            while(self.obj['type']=='Radio'):
                self.run_radio()

    def _raw_data_sever(self, data):
        if('rds' in self.kwargs):
            self.kwargs['rds'](data)

    def parser(self, data):
        st = copy.deepcopy(self.conf['labels'])
        data=str(data[:-2])[2:-1]
        #print(len(st)==data.count('_'))
        if(len(st)==data.count('_')+2): #check if data is OK, THERE MUST BE 2
            data = data.split("_")
            data.append(str(self.obj['timer'].get_time()))
            for s in st:
                if s['num']!=0:
                    s['value']=data[s['num']-1]#set value of every structure (plus 1 => 0 is ignored by parser )

        self._dataCounter+=1
        return st


    def call(self, data):
        self.data = data

    def get(self):
        return self.data


class Radio:
    def __init__(self, baudrate = 115200, port='COM9', timeout=1, **kwargs):
        self.kwargs = kwargs
        self._log_manager('__init__', baudrate = baudrate, port=port,
        timeout=timeout, kwargs=kwargs)
        try:
            self.ser = serial.Serial(port, baudrate)
            self._log_manager('open_serial', baudrate = baudrate, port=port, timeout=timeout)
        except Exception as e:
            #self._log_manager('open_serial:exception', baudrate = baudrate, port=port,
            #timeout=timeout, exception=e)
            pass

    def readline(self):
        try:
            data_r=self.ser.readline()
            self._log_manager('readline:received', data=data_r)
            return data_r
        except Exception as e:
            pass
            #self._log_manager('readline:exception', exception=e)

    def _log_manager(self, action, **kwargs):
        if('event_manager' in self.kwargs):
            self.kwargs['event_manager'](action, kwargs=kwargs)


    def _set_dict_argument(self, list, id_key, id_value, value_key, value):
        for d in list:
            if d[id_key]==id_value:
                d[value_key]=value

    def close(self):
        if(hasattr(self, 'ser')):
            self._log_manager('close')
            self.ser.close()

    def __del__(self):
        self._log_manager('__del__')
        self.close()

class SerialLoader:
    def all_serials(self):
        return serial.tools.list_ports.comports()#{device, name, description, ...}
