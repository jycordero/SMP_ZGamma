
# coding: utf-8

# In[ ]:


from ROOT import TFile
from root_pandas import read_root
from Samples.ConfigData import ConfigData


# In[ ]:


class Data( ConfigData ):
    def __init__(self,path, name, file,chunksize=1):
        self.path = path
        self.name = name
        self.file = file
        self.chunksize = chunksize
        
    def __repr__(self):              
        return "file("+self.file+")"
       
    def __str__(self):
        msg= "DataFile(path="+self.path+",\n"             "         name="+self.name+")"
        return msg

    def __len__(self):
        return self.N()
    
    def __iter__(self):
        return iter(read_root(self.path,chunksize=self.chunksize))
    
    def _totalNameToBin(name):
        mapConv = {
                "Total":1
                    }
        return mapConv[name]
        
    def N(self):
        try:
            return self.Total() - 2*self.getBin(30)
        except:
            return self.Total()
        
    def Total(self):
        return self.getBin(1)
    
    def getBin(self,n):
        try:
            n = int(n)
        except:
            n = self._totalNameToBin(n)
        
        rootFile = TFile(self.path)
        if super().isData(self.name):
            name = self.name
        else:
            name = self.name.lower()
        Bin = int(rootFile.Get("TotalEvents_"+name).GetBinContent(n))
        rootFile.Close()
        return Bin
        

