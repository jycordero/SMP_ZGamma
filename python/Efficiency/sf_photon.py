#!/usr/bin/env python
# coding: utf-8

# In[1]:


import array
import numpy as np
from ROOT import TFile, TTree, TH2F


# In[8]:





# # Reader File

# In[2]:


NewOld = 'New/'

path = "/home/jcordero/CMS/JYCMCMS/SMP_ZG/python/Efficiency/zee/"
fileName = 'eff_photon_data.root'
#fileName = 'eff_photon_data_ExpFit.root'
fileData = TFile(path+fileName)

fileName = 'eff_photon.root'
fileMC = TFile(path+fileName)


# In[3]:


Data = fileData.Get('EGamma_eff')
MC   = fileMC.Get('EGamma_eff')


# In[ ]:





# # Scale Factor

# In[4]:


fileName = 'sf_photon.root'
file = TFile(path+fileName,'recreate')
tree = TTree('tree_SF','tree_SF')


# In[5]:


ptBins  = array.array('f',[0,20,40,50,90,150,500])
#ptBins  = array.array("f",[10,20,35,50,90,150,500])

#etaBins = array.array("f",[-2.5,-2,-1.566,-1.4442,-1.0,0,1.0,1.4442,1.566,2,2.5])
etaBins = array.array("f",[-2.5,-1.566,-1.4442,0,1.4442,1.566,2.5])

ptNBins, etaNBins  = len(ptBins)-1, len(etaBins)-1

hist2d = TH2F("SF","SF",
              ptNBins,ptBins,
              etaNBins,etaBins)

tree.Branch("sf",hist2d,"TH2F")
#hist2d.SetAxisRange(0,1,"Z")
hist2d.SetAxisRange(0,2,"Z")


# # Filling Hist

# In[6]:


SF = {}

ptBin,etaBin = 7,11
for i in range(1,ptBin):
    SF[i] = {}
    for j in range(1,etaBin):
        data = Data.GetBinContent(i,j)
        mc = MC.GetBinContent(i,j)
        #print(i,j,data,mc)
        if mc == 0:
            SF[i][j] = 1
        else:
            SF[i][j] = data/mc
        hist2d.SetBinContent(i,j,SF[i][j])
        tree.Fill()
file.Write()
file.Close()


# In[ ]:





# In[ ]:





# In[ ]:




