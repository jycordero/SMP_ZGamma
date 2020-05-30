
# coding: utf-8

# In[1]:


import os
from glob import glob


# In[2]:


#from dask.distributed import Client, progress
#client = Client(threads_per_worker=4, n_workers=20)


# In[3]:


import numpy as np
import pandas as pd
#from dask import delayed
#from dask import compute

from root_pandas import read_root 
from ROOT import TFile


# In[4]:


'''
from guppy import hpy
h = hpy()
print(h.heap())
''';


# In[5]:


import matplotlib.pyplot as plt


# In[6]:


from Common.CommonHelper  import CommonHelper
from Samples.DataStack    import DataStack
from Samples.DataSample   import DataSample
from Samples.Event        import Event
from Samples.DataFile     import DataFile
from Plotter.Histo        import Histo
from Plotter.HistoSample  import HistoSample
from Plotter.HistoVar     import HistoVar


# In[7]:


def getSamplesPath(path):
    return glob(os.path.join(path,"*[!.][!s][!h]"))

def getSampleFromPath(path):
    return path.split("/")[-1]

def getFileFromPath(path):
    return path.split("/")[-1]

def getFiles(path,sample):
    return glob(os.path.join(path,sample,"output*[!v_0]*"))


# In[8]:


def isPathEmpty(path,samp):
    file = glob(os.path.join(path, getSampleFromPath(samp),"output*"))
    if file:
        return False
    else:
        return True


# In[9]:


def SampleLoop(Sample, HStack):
    for file in Sample:
        for i,iEvent in enumerate(file):
            event = Event(iEvent)

            for histo in HStack:
                #print(histo.name)
                histo.fill( event.value(histo.name),
                            event.value('eventWeight')*Sample.getSF())
    return HStack


# In[10]:


path = "/home/jcordero/CMS/data/data_2018/rereco/SMP_ZG/Files/mumug/VDask/"
chuncksize = 5000
era = "2018"

dataFiles  = ['DoubleMuon']
dataFiles += ['DoubleMuon_'+era+run for era in ['2016','2017','2018'] for run in ['A','B','C','D','E','F','G','Histo']]


# In[11]:


DStack = DataStack()

for samp in getSamplesPath(path):
    if not isPathEmpty(path,samp) :
        if getSampleFromPath(samp) not in dataFiles:
            DStack.append( DataSample(path, getSampleFromPath(samp), era, chuncksize) )
    


# In[12]:


def Var2PlotDict(part,var,ph):
    VarDict = []
    dirstruc = {}
    for p in part:
        for v in var:
            for gm in ph:
                VarDict.append({
                                "part":p,
                                "var":v,
                                "ph":gm
                                })
                
    return VarDict
    
def Var2Plot():
    PartVar = []
    VarDict = []
    
    parts = ["photonOne","leptonOne","leptonTwo","dilepton","llg"]
    var = ["Pt"]
    ph = [""]
    #ph = ["","_EE","_EB"]
    PartVar += [p+v+gm for p in parts for v in var for gm in ph]
    VarDict += Var2PlotDict(parts,var,ph)    
    
    parts = ["dilepton","llg"]
    var = ["M"]
    ph = [""]
    #ph = ["","_EE","_EB"]
    PartVar += [p+v+gm for p in parts for v in var for gm in ph]
    VarDict += Var2PlotDict(parts,var,ph)    
    
    parts = ["photonOne","leptonOne","leptonTwo"]
    var = ["Eta","Phi"]
    ph = [""]
    #ph = ["","_EE","_EB"]
    PartVar += [p+v+gm for p in parts for v in var for gm in ph]
    VarDict += Var2PlotDict(parts,var,ph)    
    
    parts = ["dilepton","dileptonPhoton","l1Photon","l2Photon"]
    var = ["DR","DEta","DPhi"]
    ph = [""]
    PartVar += [p+v+gm for p in parts for v in var for gm in ph]
    VarDict += Var2PlotDict(parts,var,ph)
    
    return PartVar,VarDict


# In[13]:


def HVarStackckIni():
    HVarStack = HistoVar()
    _,vardict = Var2Plot()
    
    for var in vardict:
        #print(var)
        HVarStack.append(Histo(variable = var))
        
    return HVarStack


# In[14]:



HSampleStack = HistoSample()
for sample in DStack.getSamples():
    print(sample)
    HSampleStack.append(SampleLoop(DStack[sample], HVarStackckIni()),name = sample)
    #HSampleStack.append(delayed(SampleLoop)(DStack[sample], HVarStack))
#compute(*HSampleStack)


# In[15]:


fig,ax = HSampleStack.plot(variable="dileptonM",log=True)
#HSampleStack.plot(log=True)
#HSampleStack.plot(log=False)


# In[16]:


VV = ['WZTo2L2Q','ZZTo4L','WZTo3LNu']
HSampleStack.merge(VV,name ="VV")


# In[17]:


HSampleStack.name


# In[18]:


#HSampleStack.plot(variable="dileptonM",log=True)
HSampleStack.plot(variable="dileptonM",log=False)


# In[19]:


HSampleStack['ZGToLLG'].plot(variable='photonOnePt')


# In[ ]:


#np.sum(HSampleStack[smp] for smp in HSampleStack.name)
for hsmpstck in HSampleStack:
    hsmpstck.Print = True


# In[ ]:


HSampleStack['DYJets'].Print


# In[ ]:


#M['photonOnePt'].values
#M['photonOnePt'].plot()


# In[ ]:


M = HSampleStack['DYJets']+HSampleStack['ZGToLLG']


# In[ ]:


HSampleStack['DYJets']['photonOnePt'].plot()
HSampleStack['ZGToLLG']['photonOnePt'].plot()


# In[ ]:


M['photonOnePt'].plot()
#M['photonOnePt'].values
#HSampleStack['DYJets']['photonOnePt']+HSampleStack['ZGToLLG']['photonOnePt']


# In[ ]:


print(HSampleStack['DYJets']['photonOnePt'].values,
      HSampleStack['ZGToLLG']['photonOnePt'].values)


# In[ ]:


(HSampleStack['DYJets']['photonOnePt'] + HSampleStack['ZGToLLG']['photonOnePt']).values


# In[ ]:


HSampleStack.getProperties()


# In[ ]:


for idy, izg in zip(HSampleStack['DYJets'],HSampleStack['ZGToLLG']):
    print((idy + izg).values)
    m = (idy + izg)
    print(m.values)
    print()


# In[ ]:


type(HSampleStack['DYJets']+HSampleStack['ZGToLLG'])


# In[ ]:


for d in HSampleStack['DYJets']:
    print(type(d))


# In[ ]:


['photonOnePt', 'leptonOnePt', 'leptonTwoPt', 'dileptonPt', 'llgPt', 'dileptonM', 'llgM', 'photonOneEta', 'photonOnePhi', 'leptonOneEta', 'leptonOnePhi', 'leptonTwoEta', 'leptonTwoPhi', 'dileptonDR', 'dileptonDEta', 'dileptonDPhi', 'dileptonPhotonDR', 'dileptonPhotonDEta', 'dileptonPhotonDPhi', 'l1PhotonDR', 'l1PhotonDEta', 'l1PhotonDPhi', 'l2PhotonDR', 'l2PhotonDEta', 'l2PhotonDPhi', 'photonOnePt', 'leptonOnePt', 'leptonTwoPt', 'dileptonPt', 'llgPt', 'dileptonM', 'llgM', 'photonOneEta', 'photonOnePhi', 'leptonOneEta', 'leptonOnePhi', 'leptonTwoEta', 'leptonTwoPhi', 'dileptonDR', 'dileptonDEta', 'dileptonDPhi', 'dileptonPhotonDR', 'dileptonPhotonDEta', 'dileptonPhotonDPhi', 'l1PhotonDR', 'l1PhotonDEta', 'l1PhotonDPhi', 'l2PhotonDR', 'l2PhotonDEta', 'l2PhotonDPhi', 'photonOnePt', 'leptonOnePt', 'leptonTwoPt', 'dileptonPt', 'llgPt', 'dileptonM', 'llgM', 'photonOneEta', 'photonOnePhi', 'leptonOneEta', 'leptonOnePhi', 'leptonTwoEta', 'leptonTwoPhi', 'dileptonDR', 'dileptonDEta', 'dileptonDPhi', 'dileptonPhotonDR', 'dileptonPhotonDEta', 'dileptonPhotonDPhi', 'l1PhotonDR', 'l1PhotonDEta', 'l1PhotonDPhi', 'l2PhotonDR', 'l2PhotonDEta', 'l2PhotonDPhi']

