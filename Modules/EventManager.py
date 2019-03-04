import time

class Manager:
    def __init__(self, file, verbose=False):
        try:
            self.file = open(file, 'a')
            self.verbose = verbose
        except Exception as e:
            print('EM: Otwarcie Pliku '+str(file)+' nie powiodło się: '+str(e))

    def write_event(self, object, action,  **kwargs):
        localtime = time.asctime( time.localtime(time.time()))
        if(kwargs['kwargs'] == {}):
            com = str(localtime)+' '+str(object.__class__.__name__)+' '+str(action)+' '+'\n'
        else:
            com=str(localtime)+' '+str(object.__class__.__name__)+' '+str(action)+' '+str(kwargs)+'\n'
        self.file.write(com)
        if(self.verbose==True):
            print(com)

    def __call__(self, object, action, **kwargs):
        self.write_event(object, action, kwargs = kwargs)

    def __del__(self):
        self.file.close()

class DataSaver:
    def __init__(self, file):
        try:
            self.file = file
            self.file = open(self.file, 'a')
        except Exception as e:
            print('DataSever: Otwarcie Pliku '+str(file)+' nie powiodło się: '+str(e))

    def write(self, data):
        self.file.write(str(time.time())+'_'+str(data)+'\n')

    def __call__(self, data):
        self.write(data)

    def __del__(self):
        self.file.close()
