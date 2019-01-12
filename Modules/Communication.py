import serial
import serial.tools.list_ports
import time

class Radio:
    def __init__(self, baudrate = 115200, port='COM9', timeout=1, **kwargs):
        self.kwargs = kwargs
        self._log_manager('__init__', baudrate = baudrate, port=port,
        timeout=timeout, kwargs=kwargs)
        try:
            self.ser = serial.Serial(port, baudrate)
            self._log_manager('open_serial', baudrate = baudrate, port=port, timeout=timeout)
        except Exception as e:
            self._log_manager('open_serial:exception', baudrate = baudrate, port=port,
            timeout=timeout, exception=e)

    def readline(self):
        self._log_manager('readline:call')
        try:
            data_r=self.ser.readline()
            self._log_manager('readline:received', data=data_r)
            return data_r
        except Exception as e:
            self._log_manager('readline:exception', exception=e)

    def _log_manager(self, action, **kwargs):
        if('event_manager' in self.kwargs):
            self.kwargs['event_manager'](self, action, kwargs=kwargs)

    def keepReading(self, condition, interval=1, **kwargs):
        self.lines=[]
        self.lines.append('Opening:')
        while(condition):
            line=self.readline()
            #line=0
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
        res=[{'id': 'rssi', 'text':'RSSI:' , 'value': '0'},
        {'id': 'temperature', 'text':'Temperatura:' , 'value': '0'},
        {'id': 'pressure', 'text':'Ciśnienie:' , 'value': '0'},
        {'id':'positionX' , 'text': 'Pozycja X:' , 'value': '0'},
        {'id': 'positionY', 'text': 'Pozycja Y:' , 'value': '0'},
        {'id':'altitude' , 'text':'Wysokość:' , 'value': '0'}]

        data=str(data[:-2])[2:-1]

        #print(data)

        data=data.split("_")
        for i, r in enumerate(res):
            try:
                self._set_dict_argument(res, 'id', r['id'], 'value', data[i])
            except:
                self._log_manager('parser:exception', data=str(data), res=str(r))
        '''
        try:
            self._set_dict_argument(res, 'id', 'rssi', 'value', str(data[0]))
            self._set_dict_argument(res, 'id', 'temperature', 'value',str(data[1]))
            self._set_dict_argument(res, 'id', 'pressure', 'value', str(data[2]))
            self._set_dict_argument(res, 'id', 'positionX', 'value', str(data[3]))
            self._set_dict_argument(res, 'id', 'positionY', 'value', str(data[4]))
            self._set_dict_argument(res, 'id', 'altitude', 'value', str(data[5]))

        except Exception:
            pass
        '''
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
