#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np


# In[1]:


class ConfigData:
    data = ['Muon','Electron','EGamma','Gamma','EG']
    
    def isData(self,name):    
        return np.sum([ d.lower() in name.lower() for d in self.data], dtype = np.bool)
    
    @staticmethod
    def Runs(era):
        if '2018' in era :
            return ['A','B','C','D']
        elif '2017' in era:
            return ['B','C','D','E','F']
        elif '2016' in era:
            return ['B','C','D','E','F','G','H']
        
    @staticmethod
    def Diboson(era):
        if   '2018' in era:
            return ['WZTo2L2Q','ZZTo4L','WZTo3LNu']
        elif '2017' in era:
            return ['WWTo2L2Nu','WZTo2L2Q','WZTo3LNu','ZZTo2L2Nu','ZZTo2L2Q','ZZTo4L']
        elif '2016' in era:
            return ['WWTo2L2Nu','WZTo2L2Q','WZTo3LNu','ZZTo2L2Nu','ZZTo2L2Q','ZZTo4L']
        
    

