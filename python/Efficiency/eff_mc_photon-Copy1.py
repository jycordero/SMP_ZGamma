#!/usr/bin/env python
# coding: utf-8

# In[74]:


from ROOT import TFile,TTree,TH2F
import array
import matplotlib.pyplot as plt
import numpy as np
from root_pandas import read_root 

import scipy.special as spc
from scipy.optimize import curve_fit


# In[75]:


def BinFormat(Bins,Type='ranges'):
    bins = []
    if Type == 'ranges':
        if type(Bins[0]) is np.ndarray or type(Bins[0]) is list:
            bins = Bins
        else:
            for i in np.arange(len(Bins)-1):
                bins.append([Bins[i],Bins[i+1]])
    elif Type == 'edges':
        if type(Bins[0]) is int or type(Bins[0]) is float:
            bins = Bins
        else:
            for b in Bins:
                bins.append(b[0])
            bins.append(Bins[-1][1])
        bins = array.array("f",bins)
        
    return bins

def BinIndex(Data,Low,Max):
    return np.logical_and(np.array(Data) >= Low, np.array(Data) <  Max)


# In[76]:


path = "/home/jcordero/CMS/JYCMCMS/SMP_ZG/python/Efficiency/files_zee/New/DYJets/"
fileName = "output_DYJets_v.root"
file = TFile(path+fileName,"read")


# In[77]:


Probe = file.Get("EGammaProbe")
Pass = file.Get("EGammaProbePass")

tree = file.Get("tree_dyjets")


# In[78]:


ptBins  = array.array('f',[0,20,40,50,90,150,500])
#ptBins  = array.array("f",[10,20,35,50,90,150,500])

etaBins = array.array("f",[-2.5,-2,-1.566,-1.4442,-1.0,0,1.0,1.4442,1.566,2,2.5])
#etaBins = array.array("f",[-2.5,-1.566,-1.4442,0,1.4442,1.566,2.5])

ptNBins,etaNBins = len(ptBins),len(etaBins)

ProbeCount , PassCount , eff = {},{},{}
for i in range(ptNBins):
    ProbeCount[i] , PassCount[i] , eff[i] = {}, {}, {}
    for j in range(etaNBins):
        ProbeCount[i][j] = Probe.GetBinContent(i,j)
        PassCount[i][j]  = Pass .GetBinContent(i,j)
        
        if ProbeCount[i][j] == 0:
            eff[i][j] = 0
        else:
            eff[i][j] = PassCount[i][j]/ProbeCount[i][j]


# In[ ]:





# In[79]:


fileOut = TFile("eff_photon.root","recreate")
tree = TTree("eff_photon","eff_photon")

ptNBins,etaNBins = len(ptBins)-1,len(etaBins)-1
hist2d = TH2F("EGamma_eff","Eff",
              ptNBins ,ptBins,
              etaNBins,etaBins)


tree.Branch("eff",hist2d,"TH2F")



'''
hist2d = TH2F("EGamma_eff","Eff",
              ptNBins,ptBinsDown,ptBinsUp
              etaNBins,etaBinsDown)
'''
for i in range(ptNBins+1):
    for j in range(etaNBins+1):
        #print(i,j)
        hist2d.SetBinContent(i,j,eff[i][j])
        tree.Fill()
fileOut.Write()
fileOut.Close()


# In[ ]:





# # Create Eff for MC

# In[80]:


NewOld = 'New/'


#path = "/home/jcordero/CMS/JYCMCMS/SMP_ZG/python/Efficiency/files_zee/"+NewOld+"SingleElectron/"
figpath = '/home/jcordero/CMS/JYCMCMS/SMP_ZG/python/Efficiency/'

var = ["dileptonProbeFailM","dileptonProbePassM",
      "leptonProbeFailPt","leptonProbePassPt",
      "leptonProbeFailEta","leptonProbePassEta",
       "vetoDY","genIsoPass","fromZ",
      ]


# In[ ]:





# In[81]:


#samples = ["DYJets","WJets"]
samples = ["DYJets"]
s = samples[0]

path = "/home/jcordero/CMS/JYCMCMS/SMP_ZG/python/Efficiency/files_zee/"+NewOld+s+"/"
fileName = "output_"+s+"_v.root"
dfMC = read_root(path+fileName,columns = var)


# In[ ]:





# In[82]:


ProbeType = "Pass"
part      = 'dileptonProbe'
variable  = 'M'
sample    = dfMC

ptBins, etaBins = BinFormat(ptBins,Type='ranges'),BinFormat(etaBins,Type='ranges')

Yields = {}
Yields[ProbeType] = {}

for j in np.arange(ptNBins):
    '''
    if j in BinEBEE:
        etaBINS = etaBinsEBEE
    else:
        etaBINS = etaBins
    '''
    Yields[ProbeType][j] = {}
    
    for i in np.arange(etaNBins):
    #for i in np.arange(len(etaBINS)):                 
        VAL = sample[part+ProbeType+variable]
        Ind = sample.vetoDY == False
        if samples == "DYJets":
            Ind = np.logical_and(Ind,sample.fromZ == True)
            #Ind = np.logical_and(Ind,sample.fromZ == False)

        Var = np.array(VAL[Ind])
        Pt  = sample['leptonProbe'+ProbeType+'Pt'][Ind]
        Eta = sample['leptonProbe'+ProbeType+'Eta'][Ind]


        ptInd  = BinIndex(Pt , ptBins [j][0], ptBins [j][1])
        #etaInd = BinIndex(Eta, etaBINS[i][0], etaBINS[i][1])
        etaInd = BinIndex(Eta, etaBins[i][0], etaBins[i][1])
        Ind    = np.logical_and(ptInd,etaInd)
        
        Yields[ProbeType][j][i] = np.sum(Ind)
#dfMC.leptonProbeFailPt


# In[56]:


ProbeType = "Fail"
part      = 'dileptonProbe'
variable  = 'M'
sample    = dfMC

ptBins, etaBins = BinFormat(ptBins,Type='ranges'),BinFormat(etaBins,Type='ranges')

Yields[ProbeType] = {}

for j in np.arange(ptNBins):
    '''
    if j in BinEBEE:
        etaBINS = etaBinsEBEE
    else:
        etaBINS = etaBins
    '''
    Yields[ProbeType][j] = {}
    
    for i in np.arange(etaNBins):
    #for i in np.arange(len(etaBINS)):                 
        VAL = sample[part+ProbeType+variable]
        Ind = sample.vetoDY == False
        if samples == "DYJets":
            Ind = np.logical_and(Ind,sample.fromZ == True)
            #Ind = np.logical_and(Ind,sample.fromZ == False)

        Var = np.array(VAL[Ind])
        Pt  = sample['leptonProbe'+ProbeType+'Pt'][Ind]
        Eta = sample['leptonProbe'+ProbeType+'Eta'][Ind]


        ptInd  = BinIndex(Pt , ptBins [j][0], ptBins [j][1])
        #etaInd = BinIndex(Eta, etaBINS[i][0], etaBINS[i][1])
        etaInd = BinIndex(Eta, etaBins[i][0], etaBins[i][1])
        Ind    = np.logical_and(ptInd,etaInd)
        
        Yields[ProbeType][j][i] = np.sum(Ind)
#dfMC.leptonProbeFailPt


# In[67]:


eff = {}
for j in np.arange(ptNBins):    
    eff[j] = {}
    for i in np.arange(etaNBins):
        eff[j][i] = Yields['Pass'][j][i]/(Yields['Pass'][j][i] + Yields['Fail'][j][i])


# In[68]:


eff


# In[72]:


len(dfMC.leptonProbeFailPt)/len(dfMC.leptonProbePassPt)


# In[66]:


print(ptNBins,etaNBins)


# In[ ]:




