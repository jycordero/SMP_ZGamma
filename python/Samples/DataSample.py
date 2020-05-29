
# coding: utf-8

# In[ ]:


from glob import glob
import os
import numpy as np


# In[ ]:


from Common.CommonHelper import CommonHelper
from Common.StackList import StackList
from Samples.DataFile import DataFile


# In[ ]:


class DataSample( StackList ):
    def __init__(self,path,name,era,chunksize=1):
        self.path = os.path.join(path, name) #/PATHTODATA/SAMPLE
        self.name = name
        self.era  = era
        self.chunksize = chunksize
        self.confpath = "/home/jcordero/CMS/SMP_ZGamma/json/data/"
        
        StackList.__init__(self, self._loadFiles() )
   
    def _loadFiles(self):
        DataFiles = []
        for files in self._getFiles():
            filename = files.split("/")[-1]
            DataFiles.append( DataFile(files, self.name, filename, self.chunksize) )
        return DataFiles
    
    def _getFiles(self):
        return glob(os.path.join(self.path,"output*[!v_0]*"))

    def getLumi(self,era):
        return CommonHelper.Read.openJson(self.confpath+"lumi.json")[era]
    
    def getXsec(self,process,era=None):
        try:
            return CommonHelper.Read.openJson(self.confpath+"xsec.json")[process][era]
        except:
            return CommonHelper.Read.openJson(self.confpath+"xsec.json")[process]
        
    def getSF(self,data=False):
        if(self.N() != 0 and not data):
            return(1e3*self.getXsec(self.name,self.era)*self.getLumi(self.era)/self.N())
        else: 
            return(1)
    
    def N(self):
        return np.sum([istck.N() for istck in self.stack])
    
    def Total(self):
        return self.N()
       

