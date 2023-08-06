import os, psutil
import pandas as pd
from multiprocessing import shared_memory
from pathlib import Path

from SharedData.Logger import Logger
from SharedData.SharedDataFeeder import SharedDataFeeder
from SharedData.Metadata import Metadata
from SharedData.SharedDataRealTime import SharedDataRealTime
from SharedData.Utils import remove_shm_from_resource_tracker, cpp


class SharedData:

    INIT_MESSAGE_SENT = False
    PERSIST_SHARED_MEMORY = True

    def __init__(self, database, mode='rw', user='master'):

        if Logger.log is None:
            Logger('SharedData')

        if (os.name == 'posix') & (SharedData.PERSIST_SHARED_MEMORY):
            remove_shm_from_resource_tracker()

        self.database = database
        self.user = user

        self.s3read = False
        self.s3write = False
        if mode == 'r':
            self.s3read = True
            self.s3write = False
        elif mode == 'w':
            self.s3read = False
            self.s3write = True
        elif mode == 'rw':
            self.s3read = True
            self.s3write = True

        if (Logger.user != 'master') & (user == 'master'):
            self.s3write = False
            mode = 'r'

        self.save_local = (os.environ['SAVE_LOCAL'] == 'True')

        self.mode = mode

        # DATA DICTIONARY
        # SharedDataTimeSeries: data[feeder][period][tag] (date x symbols)
        # SharedDataFrame: data[feeder][period][date] (symbols x tags)
        self.data = {}

        # Symbols collections metadata
        self.metadata = {}

        # static metadata
        self.static = pd.DataFrame([])

        if not SharedData.INIT_MESSAGE_SENT:
            SharedData.INIT_MESSAGE_SENT = True
            Logger.log.debug('Initializing SharedData %s:%s DONE!' %
                (os.environ['USERNAME'], os.environ['COMPUTERNAME']))

    def __setitem__(self, feeder, value):
        self.data[feeder] = value

    def __getitem__(self, feeder):
        if not feeder in self.data.keys():
            self.data[feeder] = SharedDataFeeder(self, feeder)
        return self.data[feeder]
    
    def malloc(self,shm_name,create=False,size=None,overwrite=False,):
        ismalloc = False
        shm = None
        try:
            shm = shared_memory.SharedMemory(\
                name = shm_name,create=False)
            ismalloc = True
            if (overwrite) & (os.name=='posix'):
                self.free(shm_name)
                if (create) & (not size is None):
                    shm = shared_memory.SharedMemory(\
                        name=shm_name,create=True,size=size)
                    ismalloc = True
                elif (create) & (size is None):
                    raise Exception('SharedData malloc must have a size when create=True')
        except:
            if (create) & (not size is None):

                shm = shared_memory.SharedMemory(\
                    name=shm_name,create=True,size=size)
                ismalloc = True
            elif (create) & (size is None):
                raise Exception('SharedData malloc must have a size when create=True')

        # register process id access to memory
        if ismalloc:            
            fpath = Path(os.environ['DATABASE_FOLDER'])
            fpath = fpath/('shm/'+shm_name.replace('\\','/')+'.csv')
            os.makedirs(fpath.parent,exist_ok=True)
            pid = os.getpid()
            f = open(fpath, "a+")
            f.write(str(pid)+',')
            f.flush()
            f.close()

        return [shm, ismalloc]
    
    def free(self,shm_name):
        if os.name=='posix':
            try:
                shm = shared_memory.SharedMemory(\
                    name = shm_name,create=False)
                shm.close()
                shm.unlink()
                fpath = Path(os.environ['DATABASE_FOLDER'])
                fpath = fpath/('shm/'+shm_name.replace('\\','/')+'.csv')
                if fpath.is_file():
                    os.remove(fpath)
            except:
                pass

    @staticmethod
    def free(shm_name):
        if os.name=='posix':
            try:
                shm = shared_memory.SharedMemory(\
                    name = shm_name,create=False)
                shm.close()
                shm.unlink()
                fpath = Path(os.environ['DATABASE_FOLDER'])
                fpath = fpath/('shm/'+shm_name.replace('\\','/')+'.csv')
                if fpath.is_file():
                    os.remove(fpath)
            except:
                pass

    @staticmethod
    def list():
        folder = Path(os.environ['DATABASE_FOLDER'])/'shm'
        shm_names = pd.DataFrame()
        for root, _, filenames in os.walk(folder):
            for filename in filenames:
                if filename.endswith('.csv'):
                    fpath = os.path.join(root, filename)
                    shm_name = fpath.removeprefix(str(folder))[1:]
                    shm_name = shm_name.removesuffix('.csv')
                    shm_name = shm_name.replace('/','\\')
                    try:
                        shm = shared_memory.SharedMemory(\
                            name = shm_name,create=False)
                        shm_names.loc[shm_name,'size'] = shm.size
                        shm.close()                
                    except:
                        try:                    
                            if fpath.is_file():
                                os.remove(fpath)                    
                        except:
                            pass
        shm_names = shm_names.sort_index()
        return shm_names
    
    @staticmethod
    def freeall():
        shm_names = SharedData.list()
        for shm_name in shm_names.index:
            SharedData.free(shm_name)
    
    def subscriberealtime(self):
        SharedDataRealTime.subscribe(self)