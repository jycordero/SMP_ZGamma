
# coding: utf-8

# In[ ]:


from ROOT import TFile
from root_pandas import read_root


# In[ ]:


class DataFile:
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
        
    def N(self,n=1):
        rootFile = TFile(self.path)
        return int(rootFile.Get("TotalEvents_"+self.name.lower()).GetBinContent(n))
        
    def Total(self):
        return self.N()
    
    def getBin(self,n):
        try:
            n = int(n)
        except:
            n = self._totalNameToBin(n)
        
        return self.N(n)

