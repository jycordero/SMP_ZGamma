#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
from Config import Config
from Reader import Reader


# In[2]:


sys.path.append("/home/jcordero/CMS/JYCMCMS/SMP_ZG/python")


# In[3]:


class Test (Config):
    pass


# In[4]:


T = Test(path = 'path', era = "2018", DataGen="rereco", selection = "mumug")


# In[5]:


C = Config(path = 'path', era = "2018", DataGen="rereco", selection = "mumug")


# In[7]:


read = Reader(C)


# In[ ]:





# In[ ]:





# In[ ]:




