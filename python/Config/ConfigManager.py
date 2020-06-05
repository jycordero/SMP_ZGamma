
# coding: utf-8

# In[2]:


import os
from Common import IO
from Common.ProjectManage import ProjectManage


# In[9]:


class ConfigManager( ProjectManage ):
    def __init__(self):
        self.jsonpath = "/home/jcordero/CMS/SMP_ZGamma/json/"
        self.structpath = os.path.join(self.jsonpath,"manage/")
        
    
    def _getDirStruct(self):
        return IO.openDict(os.path.join(self.structpath,"dirstructure.json"))
    
    def _getDirFigStruct(self):
        return IO.openDict(os.path.join(self.structpath,"figstructure.json"))
    
    def CreateProject(self,path,Print=False):
        super().dirStructure(path,self._getDirStruct(),date=True,Print=Print)
        
    def CreateFigStructure(self,path,Print=False):
        super().dirStructure(path,self._getDirFigStruct(),date=False,Print=Print)
        
    def latestDir(self,era,selection):
        return IO.openJson(os.path.join(self.jsonpath,"data","conf.json"))[era][selection]
        
    def legacy(self,era):
        if   '2016' in era : return 'legacy'
        elif '2017' in era : return 'rereco'
        elif '2018' in era : return 'rereco'

