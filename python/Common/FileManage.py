#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import datetime


# In[ ]:


def Date():
    date = datetime.datetime.now()
    return str(date.year) + str(date.month) + str(date.day) + "/"

def CreateDir(figpath,sufix='', Print = False):
    try:
        os.mkdir(figpath+sufix)
        if Print: print("Dir "+figpath+sufix+" created")
    except:
        if Print:
            print("Directory "+figpath+sufix+ " already exist")   

def dirStructure(path,dictStruct,date=True,Print = False):
    if date:
        path = os.path.join(path,Date())
        CreateDir(path,Print=Print)
        
    for key in dictStruct:
        try:
            dirStructure(os.path.join(path,key),dictStruct[key],date=False,Print=Print)
        except:
            CreateDir(os.path.join(path,key),Print=Print)


# In[ ]:




