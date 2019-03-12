import serial
import serial.tools.list_ports
import time
import yaml

class DataReader:
    def __init__(self, structure, radio, **kwargs):
        self.kwargs = kwargs
        self.structure = structure #structure of data received from satellite
        for s in self.structure: #check if every stucture has all attributes
            for p in ['id', 'text', 'num']:
                if not(p in s):
                    raise Exception('Not found "'+p+'" in "'+str(s)+'" structures')

        for p in ['baudrate', 'port', 'timeout']:#check if radio has all attributes
            if not( p in radio):
                raise Exception('Not found "'+p+'" in "'+str(radio)+'" radio')
        try: #open _log_manager
            self._log_manager('open_DataReader:open_log_manager', structure=structure, radio=radio, kwargs=kwargs)
        except Exception:
            raise Exception('Failed opening _log_manager in DataReader')
        try: #open radio
            self._log_manager('open_radio', radio=radio)
            self.radio = Radio(radio['baudrate'], radio['port'], radio['timeout'], event_manager = self._log_manager)
        except Exception:
            #self._log_manager('open_radio:exception', radio=radio)
            pass

        self._log_manager('open_DataReader:done')# log everything is OK

    def _log_manager(self, action, **kwargs):
        if('event_manager' in self.kwargs):
            self.kwargs['event_manager'](self, action, kwargs=kwargs)

    def _raw_data_sever(self, data):
        if('rds' in self.kwargs):
            self.kwargs['rds'](data)

    def keepReading(self, condition, interval=1, **kwargs):
        lastLine='RUN'
        if not ('second_condition' in kwargs):
            second_condition=True
        while(condition):
            if(second_condition):
                #line=self.radio.readline()
                line=b'80_50.4482155_21.7964096_0.0_28.02_1003.46_8.3_9.2\r\n'
                if lastLine!=line and ('call' in kwargs) and line!=None:
                    self._raw_data_sever(line)
                    line = self.parser(line, self.structure)
                    kwargs['call'](line)
                lastLine=line
        time.sleep(1)

    def parser(self, data, structure):
        st = self.structure
        data=str(data[:-2])[2:-1]
        if(len(st)==data.count('_')+1): #check if data is OK
            data = data.split("_")
            for s in st:
                s['value']=data[s['num']]#set value of every structure
        #print(st)
        return st

        #checksum --- to be added
    '''
    def __del__(self):
        with open('log.yml', 'w') as outfile:
            yaml.dump(self., outfile, default_flow_style=False)
    '''








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

    def keepReading(self, condition, interval=1, **kwargs):
        self.lines=[]
        self.lines.append('Opening:')
        while(condition):
            #line=self.readline()
            #line=b'80_50.4482155_21.7964096_0.0_28.02_1003.46_8.3_9.2\r\n'
            time.sleep(interval)
            if self.lines[-1]!=line and 'call' in kwargs and line!=None:
                line = self.parser(line)
                kwargs['call'](line)
            self.lines.append(line)

    def _set_dict_argument(self, list, id_key, id_value, value_key, value):
        for d in list:
            if d[id_key]==id_value:
                d[value_key]=value


    def parser(self, data):
        res=[{'id': 'rssi', 'text':'RSSI:' , 'value': '133'},
        {'id':'positionX' , 'text': 'Pozycja X:' , 'value': '50.05925'},
        {'id': 'positionY', 'text': 'Pozycja Y:' , 'value': '19.92293'},
        {'id':'altitude' , 'text':'Wysokość:' , 'value': '1134'},
        {'id': 'temperature', 'text':'Temperatura:' , 'value': '25'},
        {'id': 'pressure', 'text':'Ciśnienie:' , 'value': '1115'},
        {'id': 'pm25', 'text':'pm25:' , 'value': '133'},
        {'id': 'pm10', 'text':'pm10:' , 'value': '133'}]

        data=str(data[:-2])[2:-1]

        #print(data)

        data1=data.split("_")
        data=data1
        try:

            self._set_dict_argument(res, 'id', 'rssi', 'value', str(data[0]))
            self._set_dict_argument(res, 'id', 'temperature', 'value',str(data[4]))
            self._set_dict_argument(res, 'id', 'pressure', 'value', str(data[5]))
            self._set_dict_argument(res, 'id', 'positionX', 'value', str(data[1]))
            self._set_dict_argument(res, 'id', 'positionY', 'value', str(data[2]))
            self._set_dict_argument(res, 'id', 'altitude', 'value', str(data[3]))
            self._set_dict_argument(res, 'id', 'pm25', 'value', str(data[6]))
            self._set_dict_argument(res, 'id', 'pm10', 'value', str(data[7]))
        except Exception:
            pass
        #print(type(data))
        #print(data1)
        return res


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


#print(SerialLoader().all_serials())
'''
r=Radio()
r.keepReading(True,call=print)
'''
'''
with serial.Serial('COM9', 115200, timeout=1 ) as ser:

    print(ser.readline())

ser = serial.Serial
ser.baudrate = 115200
ser.port='COM9'
ser.open()
while(True):
    print(ser.read(256))
'''
