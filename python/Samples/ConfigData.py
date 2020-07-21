#!/usr/bin/env python
# coding: utf-8

# In[3]:


import os
import numpy as np
from Common.IO import openJson


# In[4]:


class ConfigData:
    dataNameRoot = ['Muon','Electron','EGamma','Gamma','EG']
    mergepath = "/home/jcordero/CMS/SMP_ZGamma/json/manage/"
    
    def isData(self,name):
        return np.sum([ d.lower() in name.lower() for d in self.dataNameRoot], dtype = np.bool)
        
    def Runs(self,era):
        return openJson(os.path.join(self.mergepath,'runs.json'))[era]
        
    def Diboson(self,era):
        return openJson(os.path.join(self.mergepath,'merge.json'))[era]["Diboson"]
        
    def DoubleMuon(self,era):
        return openJson(os.path.join(self.mergepath,'merge.json'))[era]["DoubleMuon"]
    
    def DoubleEG(self,era):
        return openJson(os.path.join(self.mergepath,'merge.json'))[era]["DoubleEG"]
    
    def Electron(self,era):
        return openJson(os.path.join(self.mergepath,'merge.json'))[era]["Electron"]
    


# In[7]:


if __name__ == '__main__':
    C = ConfigData()
    print(C.Diboson('2016'))
    print(C.DoubleMuon('2018'))
    print(C.Runs('2017'))
    print(C.SingleElectron('2018'))


# In[ ]:





# In[ ]:




