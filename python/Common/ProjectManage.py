#!/usr/bin/env python
# coding: utf-8

# In[1]:


from Common.FileManage import Date, CreateDir, dirStructure


# In[2]:


class ProjectManage:
    def Date(self):
        return Date()

    def CreateDir(self,figpath,sufix='', Print = False):
        return CreateDir(figpath,sufix, Print )

    def dirStructure(self, path,dictStruct,date=True,Print = False):
        return dirStructure(path,dictStruct,date,Print )


# In[ ]:





# In[ ]:





# In[ ]:




