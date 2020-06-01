#!/usr/bin/env python
# coding: utf-8

# In[1]:


from Common import IO
from Common.ProjectManage import ProjectManage


# In[2]:


class ConfigManager( ProjectManage ):
    def __init__(self):
        self.structpath = "/home/jcordero/CMS/SMP_ZGamma/json/manage/"
    
    def _getDirStruct(self):
        return IO.openDict(self.structpath+"dirstruct.json")
    
    def CreateProject(self,path,date=True,Print=False):
        super().dirStructure(path,self._getDirStruct(),date,Print)

