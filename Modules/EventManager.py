import time
import os

class Manager:
    def __init__(self, file, verbose=False):
        self.verbose = verbose
        try:
            self.file = open(file, 'a')
        except Exception as e:
            print('EM: Otwarcie Pliku '+str(file)+' nie powiodło się: '+str(e))

    def write_event(self, object, action,  **kwargs):
        localtime = time.asctime( time.localtime(time.time()))
        if(kwargs['kwargs'] == {}):
            com = str(localtime)+' '+str(object.__class__.__name__)+' '+str(action)+' '+'\n'
        else:
            com=str(localtime)+' '+str(object.__class__.__name__)+' '+str(action)+' '+str(kwargs)+'\n'
        try:
            self.file.write(com)
        except Exception:
            pass
        if(self.verbose==True):
            print(com)

    def __call__(self, object, action, **kwargs):
        self.write_event(object, action, kwargs = kwargs)

    def __del__(self):
        try:
            self.file.close()
        except Exception:
            pass

class DataSaver:
    def __init__(self, file):
        try:
            self.file = file
            self.file = open(self.file, 'a')
        except Exception as e:
            print('DataSever: Otwarcie Pliku '+str(file)+' nie powiodło się: '+str(e))

    def write(self, data):
        self.file.write(str(time.time())+'_'+str(data)+'\n')
        self.file.flush()
        # typically the above line would do. however this is used to ensure that the file is written
        os.fsync(self.file.fileno())

    def __call__(self, data):
        #print(data)
        self.write(data)

    def save(self):
        self.file.close()

    def __del__(self):
        pass

class DataManager:
    def __init__(self, path):
        self.path=''
        if path!=None:
            self.path=path
        self.prefix='/saves'
        self.path+=self.prefix
        self.new_save()

    def new_save(self):
        num=0
        while(os.path.isdir(self.path+'/'+str(num))):
            num+=1
        path=self.path+'/'+str(num)
        try:
            os.makedirs(path)
            #self.ds.save()
        except Exception as e:
            print(e)
        self.ds=DataSaver(path+'/raw.txt')
        self.em=Manager(path+'/em.txt', False)

    def finish(self):
        self.ds.__del__()
        self.em.__del__()
