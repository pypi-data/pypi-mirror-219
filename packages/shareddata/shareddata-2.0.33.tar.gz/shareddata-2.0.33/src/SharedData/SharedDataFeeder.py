import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import time

from SharedData.Metadata import Metadata
from SharedData.Logger import Logger
from SharedData.SharedDataPeriod import SharedDataPeriod
from SharedData.SharedDataTable import SharedDataTable

class SharedDataFeeder():

    dense_datasets = {'W1':'weekly','D1':'daily','M15':'15 min','M1':'1 min'}
    
    def __init__(self, sharedData, feeder):
        self.feeder = feeder
        self.sharedData = sharedData    
        self.database = sharedData.database        
        
        # DATA DICTIONARY
        # data[period][tag]
        self.data = {}     
    
    def __setitem__(self, dataset, value):
        if not dataset in self.data.keys():
            if (dataset in SharedDataFeeder.dense_datasets.keys()):
                period = dataset
                self.data[period] = value
            else:
                self.data[dataset] = SharedDataTable(self, dataset, value)            
        return self.data[dataset]
                
    def __getitem__(self, dataset):
        if not dataset in self.data.keys():            
            if (dataset in SharedDataFeeder.dense_datasets.keys()):                
                period = dataset
                self.data[period] = SharedDataPeriod(self, period)
            else:
                self.data[dataset] = SharedDataTable(self, dataset)

        if (dataset in SharedDataFeeder.dense_datasets.keys()):
            return self.data[dataset]    
        else:
            return self.data[dataset].records
    
    def create_table(self,dataset,names,formats,size,overwrite=False):
        self.data[dataset] = SharedDataTable(\
            self,dataset,names=names,formats=formats,size=size,overwrite=overwrite)
        return self.data[dataset].records
    
    def load_table(self,dataset,size=None):
        self.data[dataset] = SharedDataTable(self,dataset,size=size)
        return self.data[dataset].records