#!/usr/bin/env python
# coding: utf-8

# In[1]:


## Python dependencies 
import matplotlib.pyplot as plt
import matplotlib.colors as col
import numpy as np
import pandas as pd


# In[44]:


from scipy.optimize  import curve_fit
from scipy.special   import erf, betainc, gamma
from scipy           import asarray as ar,exp
from numpy.random    import uniform
from scipy           import stats
from scipy.integrate import simps

from root_pandas import read_root 

# External Dependencies
from ROOT import TFile, TTree,Double, TGraph


# In[3]:


# My Dependencies
#from Samples.Data      import Data
from Plotter.Helper    import Helper
from Data import Data
from Helper import Helper

import Samples
import Plotter


# In[ ]:





# In[4]:


import os, datetime


# In[5]:


from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
from sklearn.model_selection import train_test_split


# In[6]:


def dirStructure(figpath):
    date = datetime.datetime.now()
    fileName = str(date.year) + str(date.month) + str(date.day) + "/"
    
    try:
        os.mkdir(figpath+fileName)    
    except:
        print("Directory "+fileName+ " already exist")

    
    dirSubStructure(figpath + fileName + "Stacked/")
    dirSubStructure(figpath + fileName + "Unstacked/")
    
    dirSubStructure(figpath + fileName + "nJets/")
    for i in range(5):
        dirSubStructure(figpath + fileName + "nJets/Stacked_nJets"+str(i)+"/")
        dirSubStructure(figpath + fileName + "nJets/Unstacked_nJets"+str(i)+"/")
    
    return figpath+fileName  

def dirSubStructure(path):
    try:
        os.mkdir(path)
    except:
        print("Subdirectory for " + path + " already exists or failed.")
    
    try:
        os.mkdir(path+"log")
        os.mkdir(path+"log/Mult")
        os.mkdir(path+"linear")
        os.mkdir(path+"linear/Mult")
    except:
        print("Subdirectory for " + path + " already exists or failed.")


# In[7]:


#selection = 'mumug'
#selection = 'elelg'
selection = 'ee'

era = "2017"

if era == "2016":
    run = ['B','C','D','E','F','G','H']
    #DataGen = 'rereco'
    DataGen = 'legacy'
    if DataGen == 'legacy':
        #SampleSet = 'MatchZGpaper'
        #SampleSet = 'Rerun'
        SampleSet = 'Correction'
    else:
        SampleSet = 'MatchZGpaper_newAna'
elif era == "2017":
    if selection == "mumug":
        run = ['B','C','D','E','F']
        DataGen = 'rereco'
        #SampleSet = 'V1'
        #SampleSet = 'V2_puWeight'
        SampleSet = 'V2_puWeight_phID'
    elif selection == "mumu":
        run = ['B','C','D','E','F']
        DataGen = 'rereco'
        #SampleSet = 'V1'
        #SampleSet = 'V2_puWeight'
        SampleSet = 'V2_puWeight_phID'
    elif selection == "ee":
        #run = ['B','C','D','E','F']
        run = ['D']
        DataGen = 'rereco'
        SampleSet = 'EfficiencyCorrection/files_zee/CorrShower'

path    = "/home/jcordero/CMS/data_"+era+"/"+DataGen+"/SMP_ZG/Files/"+selection+"/"+SampleSet+"/"
figpath = "/home/jcordero/CMS/JYCMCMS/SMP_ZG/figs/"+era+"/"+DataGen+"/"+selection+"/"

figpath = dirStructure(figpath)


# In[24]:


#file = TFile(figpath+"trans_ShowerShape.root","read")
file = TFile("/home/jcordero/CMS/JYCMCMS/SMP_ZG/figs/2017/rereco/ee/2019122/trans_ShowerShape.root","read")
print(file)


# In[25]:


file.cd()
graph = file.Get("trans_R9_EB")
#graph = file.Get("photonOneR9_EB")
print(graph)


# In[26]:


graph.Draw("APL")


# In[29]:


graph.Eval(0.3)


# In[30]:


dir(graph)


# In[46]:


graph.Eval(Double(0.3))


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




