
# coding: utf-8

# In[1]:


from Common import IO
from Common.ProjectManage import ProjectManage


# In[2]:


class ConfigManager( ProjectManage ):
    def __init__(self):
        self.structpath = "/home/jcordero/CMS/SMP_ZGamma/json/manage/"
    
    def _getDirStruct(self):
        return IO.openDict(self.structpath+"dirstructure.json")
    
    def _getDirFigStruct(self):
        return IO.openDict(self.structpath+"figstructure.json")
    
    def CreateProject(self,path,Print=False):
        super().dirStructure(path,self._getDirStruct(),date=True,Print=Print)
        
    def CreateFigStructure(self,path,Print=False):
        super().dirStructure(path,self._getDirFigStruct(),date=False,Print=Print)
        
        
    def legacy(self,era):
        if   '2016' in era : return 'legacy'
        elif '2017' in era : return 'rereco'
        elif '2018' in era : return 'rereco'

