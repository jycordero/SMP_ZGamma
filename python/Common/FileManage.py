
# coding: utf-8

# In[1]:


import os
import datetime


# In[124]:


def Date():
    date = datetime.datetime.now()
    return "{:02d}{:02d}{:02d}".format(date.year,date.month,date.day)

def CreateDir(figpath,sufix='', Print = False):
    try:
        os.mkdir(figpath+sufix)
        if Print: print("Dir "+figpath+sufix+" created")
    except:
        if Print:
            print("Directory "+figpath+sufix+ " already exist or can't create")   

def dirStructure(path,dictStruct,date=True,Print = False):    
    for key in dictStruct:
        CreateDir(os.path.join(path,key),Print=Print)
        while type(dictStruct[key]) is not set and type(dictStruct[key]) is not str:
            dirStructure(os.path.join(path,key),subdic,Print=Print)
        else:
            if type(dictStruct[key]) is set:
                for subkey in dictStruct[key]:
                    CreateDir(os.path.join(path,key,subkey),Print=Print)
                    if date:
                        CreateDir(os.path.join(path,key,subkey,Date()),Print=Print)
            else:
                CreateDir(os.path.join(path,key,dictStruct[key],Date()),Print=Print)

