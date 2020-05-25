#!/usr/bin/env python
# coding: utf-8

# In[1]:


from ROOT import TMVA,TH2F, TCanvas
import array
import pandas as pd

# My Dependencies
from Data      import *
from Helper    import *


# In[2]:


#DataGen = 'rereco'
DataGen = 'legacy'

selection = 'mumug'
#selection = 'elelg'

#SampleSet = 'HZG'
#SampleSet = 'WithMuonVeto'
#SampleSet = 'WithWJets'
if DataGen == 'legacy':
    #SampleSet = 'MatchZGpaper'
    #SampleSet = 'Rerun'
    SampleSet = 'Correction'
else:
    SampleSet = 'MatchZGpaper_newAna'
#SampleSet = 'ReRun'
#SampleSet = 'Z'

pathData    = "/home/jcordero/CMS/data_2016/"+DataGen+"/SMP_ZG/Files/"+selection+"/"+SampleSet+"/"
figpath = "/home/jcordero/CMS/JYCMCMS/SMP_ZG/figs/"+DataGen+"/"+selection+"/"

Help    = Helper()


# In[3]:


r = 'B'
DoubleLepton = Data(pathData+"DoubleMuon/","DoubleMuon_2016",trigger = r,data=True)


# In[4]:


data = [DoubleLepton]


# In[5]:


#path = "/eos/uscms/store/user/corderom/Corrections2016Rereco/"
#phVals = ["EE","EB"]
phVals = ["EE"]
path = ""
file = {}
reader = {}
for ph in phVals:
    file[ph] = "TMVAnalysis_BDT_"+ph+".weights.xml"
    reader[ph] = TMVA.Reader()


# In[6]:


varName= {
        "recoPhi"                :["photonOnePhi"],
        "r9"                     :["photonOneR9"],
        "sieieFull5x5"           :["photonOneSieie"],
        "sieipFull5x5"           :["photonOneSieip"],
        "e2x2Full5x5/e5x5Full5x5":["photonOneE2x2","photonOneE5x5"],
        "recoSCEta"              :["photonOneEta"],
        "rawE"                   :["photonOneScRawE"],
        "scEtaWidth"             :["photonOneScEtaWidth"],
        "scPhiWidth"             :["photonOneScPhiWidth"],
        "esEn/rawE"              :["photonOnePreShowerE","photonOneScRawE"],
        "esRR"                   :["photonOneSrr"],
        "rho"                    :["Rho"],
        }


# In[ ]:





# In[7]:



inMVA = {}
for d in data:
    for vr in varName:
        VARS = [d.GetWithCuts(v) for v in varName[vr]]
        if len(VARS) >1:
            inMVA[vr] = VARS[0]/VARS[1]
        else:
            inMVA[vr] = VARS[0]
        


# In[8]:


var = {}
for phType in phVals:
    var[ph] = {}
    #for vn in varName:
            #var[ph][vn] = (array.array('f',inMVA[vn]))
            #var[ph][vn] = (array.array('f',[0]))
            #reader[ph].AddVariable(vn, var[ph][vn])
            
    recoPhi                 = (array.array('f',[0]))
    r9                      = (array.array('f',[0]))
    sieieFull5x5            = (array.array('f',[0]))
    sieipFull5x5            = (array.array('f',[0]))
    e2x2Over5x5             = (array.array('f',[0]))
    recoSCEta               = (array.array('f',[0]))
    rawE                    = (array.array('f',[0]))
    scEtaWidth              = (array.array('f',[0]))
    scPhiWidth              = (array.array('f',[0]))
    esEnOverrawE            = (array.array('f',[0]))
    esRR                    = (array.array('f',[0]))
    rho                     = (array.array('f',[0]))

    reader[ph].AddVariable("recoPhi", recoPhi     )
    reader[ph].AddVariable("r9", r9          )
    reader[ph].AddVariable("sieieFull5x5", sieieFull5x5)
    reader[ph].AddVariable("sieipFull5x5", sieipFull5x5)
    reader[ph].AddVariable("e2x2Full5x5/e5x5Full5x5", e2x2Over5x5 )
    reader[ph].AddVariable("recoSCEta", recoSCEta   )
    reader[ph].AddVariable("rawE", rawE        )
    reader[ph].AddVariable("scEtaWidth", scEtaWidth  )
    reader[ph].AddVariable("scPhiWidth", scPhiWidth  )
    reader[ph].AddVariable("esEn/rawE", esEnOverrawE)
    reader[ph].AddVariable("esRR", esRR)
    reader[ph].AddVariable("rho", rho         )
            
    reader[ph].BookMVA("BDT",path+file[ph])        


# In[ ]:





# In[ ]:





# In[ ]:





# In[9]:


df = pd.DataFrame()
df.to_csv(figpath+"BDT.csv",'a')

N = list(varName.keys())

bdtOutput = []
for i in range(len(inMVA['r9'])):
    #for v in inMVA:
    #    var[ph][v] = (array.array('f',[inMVA[v][i]]))
    #    df[v] =  var[ph][v]
    
    
    recoPhi                 = inMVA[N[0]][i]
    r9                      = inMVA[N[1]][i]
    sieieFull5x5            = inMVA[N[2]][i]
    sieipFull5x5            = inMVA[N[3]][i]
    e2x2Over5x5             = inMVA[N[4]][i]
    recoSCEta               = inMVA[N[5]][i]
    rawE                    = inMVA[N[6]][i]
    scEtaWidth              = inMVA[N[7]][i]
    scPhiWidth              = inMVA[N[8]][i]
    esEnOverrawE            = inMVA[N[9]][i]
    esRR                    = inMVA[N[10]][i]
    rho                     = inMVA[N[11]][i]
    
    bdtOutput.append(reader[ph].EvaluateMVA("BDT"))
    #print([var['EE'][v] for v in inMVA] , bdtOutput[-1])
    print(bdtOutput[-1])
    
    
    
    


# In[10]:


bdtOutput


# In[ ]:


reader["EE"]


# In[ ]:


dir(reader["EE"])


# In[ ]:


reader["EE"].Dump()


# In[ ]:





# In[ ]:




