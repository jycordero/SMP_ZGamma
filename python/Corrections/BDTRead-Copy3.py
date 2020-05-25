#!/usr/bin/env python
# coding: utf-8

# In[1]:


from ROOT import TMVA,TH2F, TCanvas
import array, sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 

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

#pathData    = "/home/jcordero/CMS/data_2016/"+DataGen+"/SMP_ZG/Files/"+selection+"/"+SampleSet+"/"
path    = "/home/jcordero/CMS/data_2016/"+DataGen+"/SMP_ZG/Files/"+selection+"/"+SampleSet+"/"
figpath = "/home/jcordero/CMS/JYCMCMS/SMP_ZG/figs/"+DataGen+"/"+selection+"/"

Help    = Helper()


# In[3]:


# --------------------------------------
#  Data
# ---------------------------------------

run = ['B','C','D','E','F','G','H']
if selection   == 'mumug':
    DoubleLepton = [Data(path+"DoubleMuon/","DoubleMuon_2016",trigger = r,data=True) for r in run]
elif selection == 'elelg':
    DoubleLepton = [Data(path+"DoubleEG/","DoubleEG_2016",trigger = r,data=True) for r in run]

#################################
Leptons = DoubleLepton[0]
for i in np.arange(len(DoubleLepton[1:])):
    Leptons =   Leptons + DoubleLepton[1]
    del DoubleLepton[1]    


# In[4]:


trigger    = "_v"
DYJets     = Data(path +      "DYJets/",     "DYJets", trigger)

if DataGen == "legacy":
    ZG     = Data(path + "ZGToLLG/", "ZGToLLG", trigger)
    WJets  = Data(path + "WJets/","WJets", trigger)
    TT     = Data(path +   "TTTo2L2Nu/",  "TTTo2L2Nu", trigger)
elif DataGen == "rereco":
    ZG     = Data(path + "ZG_ZToLL/", "ZG_ZToLL", trigger)
    TT     = Data(path +          "TT/",         "TT", trigger)
    W1Jets = Data(path + "W1JetsToLNu/","W1JetsToLNu", trigger)
    W2Jets = Data(path + "W2JetsToLNu/","W2JetsToLNu", trigger)
    W3Jets = Data(path + "W2JetsToLNu/","W3JetsToLNu", trigger)
    W4Jets = Data(path + "W3JetsToLNu/","W4JetsToLNu", trigger)

WWTo2L2Nu  = Data(path +   "WWTo2L2Nu/",  "WWTo2L2Nu", trigger)

ZZTo2L2Nu  = Data(path +   "ZZTo2L2Nu/",  "ZZTo2L2Nu", trigger)
ZZTo2L2Q   = Data(path +    "ZZTo2L2Q/",   "ZZTo2L2Q", trigger)
ZZTo4L     = Data(path +      "ZZTo4L/",     "ZZTo4L", trigger)

WZTo2L2Q   = Data(path +    "WZTo2L2Q/",   "WZTo2L2Q", trigger)
WZTo3LNu   = Data(path +    "WZTo3LNu/",   "WZTo3LNu", trigger)

#ZG_veto    = Data(path +      "DYJets/",     "DYJets", trigger)
# ---------------------------------------
# Understanding the Z Peak
#ZPeak = Data("ZPeak_WminusH_HToZG_WToAll/", "ZPeak_WminusH_","HLT_IsoMu24_v")


# In[5]:


print(' +++ Merging Data Samples')
#Leptons = DoubleLepton[0] + DoubleLepton[1] + DoubleLepton[2] + DoubleLepton[3] + DoubleLepton[4] + DoubleLepton[5] + DoubleLepton[6]

print(' +++ Merging MC Samples')
if DataGen == "rereco":
    WJets = W1Jets + W2Jets + W3Jets + W3Jets

WW = WWTo2L2Nu
ZZ = ZZTo2L2Nu + ZZTo2L2Q + ZZTo4L
WZ = WZTo2L2Q + WZTo3LNu

VV = WWTo2L2Nu + ZZTo2L2Nu + ZZTo2L2Q + ZZTo4L + WZTo2L2Q + WZTo3LNu



print('--Done')


# In[6]:


import copy
dataSelect = 'ALL'
#dataSelect = 'DY Only'
#dataSelect = 'DYVeto'
#dataSelect = 'DY ZG'
#dataSelect = 'DY ZG Comp'
#dataSelect = 'no ZG'
#dataSelect = 'DY Compare'


if   dataSelect == 'ALL':
    data        = [  WJets,         VV,     TT,   DYJets,        ZG,      Leptons]
    listSamples = [ 'WJets',      'VV',   'TT', 'DYJets',      'ZG', 'DoubleMuon']
    legend      = [ 'WJets',      'VV',   'TT', 'DYJets',      'ZG', 'DoubleMuon']
    colors      = [     'b',    'cyan',    'r', 'purple', 'magenta',          'k']
    dataFlag    = [   False,     False,  False,    False,     False,         True]
    combFlag    = [   False,     False,  False,    False,     False,         True]
elif dataSelect == 'VV Separate':
    data        = [  DYJets,   WJets,       TT,       WW,      ZZ,       WZ,       ZG,    Leptons]
    listSamples = ['DYJets', 'WJets',      'TT',    'WW',    'ZZ',     'WZ',      'ZG', 'DoubleMuon']
    legend      = ['DYJets', 'WJets',      'TT',    'WW',    'ZZ',     'WZ',      'ZG', 'DoubleMuon']
    colors      = [  'cyan',     'r',  'purple',    'grey',  'teal', 'orange', 'magenta',          'k']
    dataFlag    = [   False,   False,     False,   False,   False,    False,     False,         True]
    combFlag    = [   False,   False,     False,   False,   False,    False,     False,         True]
elif dataSelect == 'DY Only':    
    data        = [  DYJets, Leptons]
    listSamples = ['DYJets', 'DoubleMuon']
    legend      = ['DYJets', 'DoubleMuon']
    colors      = [  'cyan', 'k']
    dataFlag    = [   False, True]
    combFlag    = [   False, True]
elif dataSelect == 'DY Compare':    
    DYJets_SideBand = copy.deepcopy(DYJets)
    
    data        = [  DYJets,DYJets_SideBand, Leptons]
    listSamples = ['DYJets','DYJets', 'DoubleMuon']
    legend      = ['DYJets', 'DYJets','DoubleMuon']
    colors      = [  'cyan', 'magenta','k']
    dataFlag    = [   False, False, True]    
    combFlag    = [   False, False, True]   
    
    data[0].name = 'DYJets_Sig'
    data[1].name = 'DYJets_SideBand'
elif dataSelect == 'DYVeto':
    data        = [  DYJets,   WJets,       TT,       WW,      ZZ,       WZ,       ZG_veto,    Leptons]
    listSamples = ['DYJets', 'WJets',      'TT',    'WW',    'ZZ',     'WZ',      'ZG', 'DoubleMuon']
    legend      = ['DYJets', 'WJets',      'TT',    'WW',    'ZZ',     'WZ',      'ZG', 'DoubleMuon']
    colors      = [  'cyan',     'r',  'purple',    'grey',  'teal', 'orange', 'magenta',          'k']
    dataFlag    = [   False,   False,     False,   False,   False,    False,     False,         True]
    combFlag    = [   False,   False,     False,   False,   False,    False,     False,         True]
elif dataSelect == 'DY ZG':
    data        = [  DYJets,      ZG,    Leptons]
    listSamples = ['DYJets',      'ZG', 'DoubleMuon']
    legend      = ['DYJets',      'ZG', 'DoubleMuon']
    colors      = [  'cyan',      'magenta',          'k']
    dataFlag    = [   False,     False,         True]
    combFlag    = [   False,     False,         True]
elif dataSelect == 'DY ZG Comp':    
    data        = [  ZG_veto,      ZG,    Leptons]
    listSamples = ['DYJets',      'ZG', 'DoubleMuon']
    legend      = ['DYJets',      'ZG', 'DoubleMuon']
    colors      = [  'cyan',      'magenta',          'k']
    dataFlag    = [   False,     False,         True]
    combFlag    = [   False,     False,         True]
elif dataSelect == 'no ZG':
    data        = [  WJets,         VV,     TT,   DYJets,     Leptons]
    listSamples = [ 'WJets',      'VV',   'TT', 'DYJets','DoubleMuon']
    legend      = [ 'WJets',      'VV',   'TT', 'DYJets','DoubleMuon']
    colors      = [     'b',    'cyan',    'r', 'purple',         'k']
    dataFlag    = [   False,     False,  False,    False,        True]
    combFlag    = [   False,     False,  False,    False,        True]

ind = []
for i in range(len(data)):
    if len(data[i].df.columns) <= 1:
        continue
    else: 
        ind.append(i)

data        = [data[i]        for i in ind]
listSamples = [listSamples[i] for i in ind]
legend      = [legend[i]      for i in ind]
colors      = [colors[i]      for i in ind]
dataFlag    = [dataFlag[i]    for i in ind]
combFlag    = [combFlag[i]    for i in ind]

for i in range(len(data)):
    print(i,data[i].name,colors[i])    


# # Cuts

# In[7]:


def STD_Cuts(
            data,
            phType = 'ISR',
            Charge ='oposite',
            Print = False,
            MVA   = False,
            ):
    
    [d.ResetCuts() for d in data]
    #---------------------------- CUTS ------------------------------------ CUTS -----------------------
    # The proper cut
    DYJets .AddCuts(np.array(DYJets.df.vetoDY)==False)
    #ZG_veto.AddCuts(np.array(ZG_veto.df.vetoDY)==True )


    for d in data:
        #d.AddCuts(np.array(d.df.photonOnePt)>10)
        if Print:
            print('-----------------',d.name,'--------------')
            print('----Total----')
            print(sum(d.cuts))

        #if(DataGen == "legacy"):
        #    d.AddCuts(np.array(d.df.genIsoPass == True))
        #    if Print:
        #        print('----genIsoPass----')
        #        print(sum(d.cuts))
        
        d.AddCuts(np.array(d.df.l1PhotonDR) > 0.7)
        d.AddCuts(np.array(d.df.l2PhotonDR) > 0.7)
        if Print:
            print('----DR cuts ----')
            print(sum(d.cuts))

        
        if phType == 'ISR':
            # 2 Body to get ISR
            d.AddCuts(np.array(d.df.llgM)+np.array(d.df.dileptonM) > 185)
        elif phType == 'FSR' :
            # 3 Body to get FSR
            d.AddCuts(np.array(d.df.llgM)+np.array(d.df.dileptonM) < 185)
        if Print:
            print('----Mass cuts ----')  
            print(sum(d.cuts))

        if MVA:
            d.AddCuts(np.array(d.df.photonOneMVA > 0.2))
        if Print:
            print('----MVA cuts ----')  
            print(sum(d.cuts))
        #d.AddCuts(np.array(d.df.nJets)==0)
        #d.AddCuts(np.array(d.df.nJets)==1)
        #d.AddCuts(np.array(d.df.nJets)>1)
        #d.AddCuts(np.array(d.df.photonOneIph) > 0.6)

        # MVA CUT
        #d.AddCuts(np.array(d.df.photonOneMVA) > 0.5)
        #d.AddCuts(np.array(d.df.photonOneMVA)-5*np.array(d.df.photonOneHoverE) -0.6 > 0)


        
        if Charge == 'oposite':
            d.AddCuts(np.array(d.df.leptonOneCharge) != np.array(d.df.leptonTwoCharge))
        elif Charge == 'same':
            d.AddCuts(np.array(d.df.leptonOneCharge) == np.array(d.df.leptonTwoCharge))
        if Print:
            print('----Charge cuts ----')
            print(sum(d.cuts))
            
def PhaseSpace(
                data,
                phType = 'ISR',
                Charge = 'oposite',
                Region = '',
                Print  = False,
                MVA    = False,
              ):   
    
    STD_Cuts( data, phType = phType, Charge = Charge, Print = Print , MVA = MVA)
    
    for d in data:            
        if Print:
            print('-------'+d.name+'-------')
            print('----- Standard Region')
            print(sum(d.cuts))
    
        if Region == 'Sig':            
            if Print:
                print('-------'+d.name+'-------')
                print('----- Total')
                print(sum(d.cuts))
            SigRegion = np.logical_or(
                                      np.array(d.df.photonOneIch_EB) < 2.0,
                                      np.array(d.df.photonOneIch_EE) < 1.5 
                                     )
            d.AddCuts(SigRegion)
            #d.AddCuts()
            
            if Print:
                print('----- Signal Region')
                print(sum(d.cuts))
        elif Region == 'Sideband':
            if Print:
                print('-------'+d.name+'-------')
                print('----- Total')
                print(sum(d.cuts))
            SideBandRegion = np.logical_or(
                                      np.array(d.df.photonOneIch_EB) >= 2.0,
                                      np.array(d.df.photonOneIch_EE) >= 1.5 
                                     )
            d.AddCuts(SideBandRegion)
            #d.AddCuts()
            
            if Print:
                print('----- Signal Region')
                print(sum(d.cuts))            
        elif Region == 'Compare':
            print(d.name)
            if d.name == 'DYJets_Sig':
                SigRegion = np.logical_or(
                                          np.array(d.df.photonOneIch_EB) < 2.0,
                                          np.array(d.df.photonOneIch_EE) < 1.5 
                                         )
                d.AddCuts(SigRegion)
                
            elif d.name == 'DYJets_SideBand':
                SideBandRegion = np.logical_or(
                                      np.array(d.df.photonOneIch_EB) >= 2.0,
                                      np.array(d.df.photonOneIch_EE) >= 1.5 
                                     )
                d.AddCuts(SideBandRegion)


# # ReWeight

# In[8]:


def GetMCPU():
    ########### MC Scenario ##################
    PU = np.array([
                    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 
                    11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 
                    21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 
                    31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 
                    41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 
                    51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 
                    61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 
                    71, 72, 73, 74]
                    )
    PUmc = np.array([
                    1.78653e-05 ,2.56602e-05 ,5.27857e-05 ,8.88954e-05 ,
                    0.000109362 ,0.000140973 ,0.000240998  ,0.00071209  ,
                    0.00130121  ,0.00245255  ,0.00502589   ,0.00919534  ,
                    0.0146697   ,0.0204126   ,0.0267586    ,0.0337697   ,
                    0.0401478   ,0.0450159   ,0.0490577    ,0.0524855   ,
                    0.0548159   ,0.0559937   ,0.0554468    ,0.0537687   ,
                    0.0512055   ,0.0476713   ,0.0435312    ,0.0393107   ,
                    0.0349812   ,0.0307413   ,0.0272425    ,0.0237115   ,
                    0.0208329   ,0.0182459   ,0.0160712    ,0.0142498   ,
                    0.012804    ,0.011571    ,0.010547     ,0.00959489  ,
                    0.00891718  ,0.00829292  ,0.0076195    ,0.0069806   ,
                    0.0062025   ,0.00546581  ,0.00484127   ,0.00407168  ,
                    0.00337681  ,0.00269893  ,0.00212473   ,0.00160208  ,
                    0.00117884  ,0.000859662 ,0.000569085  ,0.000365431 ,
                    0.000243565 ,0.00015688  ,9.88128e-05  ,6.53783e-05 ,
                    3.73924e-05 ,2.61382e-05 ,2.0307e-05   ,1.73032e-05 ,
                    1.435e-05   ,1.36486e-05 ,1.35555e-05  ,1.37491e-05 ,
                    1.34255e-05 ,1.33987e-05 ,1.34061e-05  ,1.34211e-05 ,
                    1.34177e-05 ,1.32959e-05 ,1.33287e-05]
                    )
    
    return PU,PUmc

def GetDataPU(xsec='69p2'):
    pileupFile = 'pileup_sf_2016_'+xsec+'mb.root'
    file = TFile('/home/jcordero/CMS/data_2016/'+DataGen+'/SMP_ZG/Files/'+pileupFile)
    puTree = file.Get('pileup')
    PUdata = []
    for pu in puTree:
        PUdata.append(pu)
    return PUdata

def GetPUweight(xsec='69p2'):
    
    ### Get Distributions ##
    PU,PUmc= GetMCPU()
    PUdata = GetDataPU(xsec)
    
    ### Normalize ###
    PUmc   = np.array(PUmc)/sum(PUmc)        
    PUdata = np.array(PUdata)/sum(PUdata)
    
    return PU,PUdata/PUmc,PUdata,PUmc,

def SF_ratio(
             xsec1='65',
             xsec2='69p2',
            ):
    pu,r1,r1d,r1m = GetPUweight(xsec = xsec1)
    pu,r2,r2d,r2m = GetPUweight(xsec = xsec2)
    rScale = r1/r2
    rScale[np.isnan(rScale)] = np.ones(sum(np.isnan(rScale)))

    puWeight = []
    for d in data[:-1]:
        puW = np.ones(len(d.df.nPU))
        print('--------------',d.name)
        print(len(d.df.nPU))
        for i in range(len(pu)-2):
            mask = np.logical_and(np.array(d.df.nPU) > pu[i], np.array(d.df.nPU) <= pu[i+1])        
            puW[mask] = np.ones(np.sum(mask))*rScale[i]
        puWeight.append(puW)
    return puWeight


# In[9]:


################################
#stacked = False
stacked = True

LOG = 'both'
log = False
#log = True

weightCorrection = True 
#weightCorrection = False
xsec1='65'
#xsec2='67'
#xsec2='70'
xsec2='69p2'

#phType = 'ISR'
#phType = 'FSR'
phType = ''

Region = 'Sig'
#Region = 'Sideband'
#Region = 'Compare'
#Region = ''

Charge = 'oposite'
#Charge = 'same'

#customRange = True
customRange = False

MVA = False
#MVA = True

Print = False
#Print = True
###############################
if stacked:
    Fol  = 'Stacked'
    stackLab  = ''
    histtype  = 'stepfilled'
    density   = False
    linewidth = 1
else:
    Fol  = 'Unstacked'
    stackLab  = ''
    histtype  = 'step'
    density   = True
    #density = False
    linewidth = 1.7
###############################    
if log:
    stackFol = Fol+'/log'
else:
    stackFol = Fol+'/linear'
###############################

######## CUTS ##############
PhaseSpace(
            data,
            phType = phType,
            Charge = Charge,
            Region = Region,
            Print  = Print,
            MVA    = MVA,
          )
#for d in data:
#    d.AddCuts(np.array(d.df.photonOneMVA)>0.2)
###############################


# In[10]:


if weightCorrection:
    reWeight = []
    puWeight = SF_ratio(xsec1=xsec1,xsec2=xsec2)
    for i in range(len(data[:-1])):
        reWeight.append(data[i].weight*puWeight[i])


# In[ ]:





# In[ ]:





# In[ ]:





# In[11]:


#path = "/eos/uscms/store/user/corderom/Corrections2016Rereco/"
#phVals = ["EE","EB"]
phVals = ["EE"]
path = ""
file = {}
reader = {}
for ph in phVals:
    file[ph] = "TMVAnalysis_BDT_"+ph+".weights.xml"
    reader[ph] = TMVA.Reader()


# In[12]:


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


# In[13]:



inMVA = {}
for d in data:
    inMVA[d.name] = {}
    for vr in varName:
        VARS = [d.GetWithCuts(v) for v in varName[vr]]
        if len(VARS) >1:
            inMVA[d.name][vr] = VARS[0]/VARS[1]
        else:
            inMVA[d.name][vr] = VARS[0]
        


# In[14]:


var = {}
for phType in phVals:
    var[ph] = {}
    for vn in varName:
            var[ph][vn] = array.array('f',[0])
            reader[ph].AddVariable(vn, var[ph][vn])
    reader[ph].BookMVA("BDT",path+file[ph])        


# In[ ]:





# In[ ]:





# In[ ]:





# In[56]:


len(inMVA['DYJets']['recoPhi'])


# In[15]:


BDT = {}
for d in data:
    print('---------------',d.name,'--------------')
    BDT[d.name] = []
    for i in range(len(inMVA[d.name]["recoPhi"])):
        for v in inMVA[d.name]:
            if i == 0:
                print('----',v)
            var[ph][v][0] = inMVA[d.name][v][i]
        BDT[d.name].append(reader[ph].EvaluateMVA("BDT"))
        #if i == 1000:
        #    break


# In[52]:


print(len(data[-3].df.photonOneMVA))
print(len(BDT[data[-3].name]))


# In[ ]:


#ptBins = [20, 25, 30, 35, 45, 55, 65, 75, 85, 95, 120, 1000]
ptBins = [20, 25, 30, 35, 45, 55]
var = 'photonOnePt'
Ind = {}

for d in data:
    Ind[d.name] = []
    for i in np.arange(len(ptBins[:-1])):
        ptInd = np.logical_and(
                            np.array(d.GetWithCuts(var)) >= ptBins[i], 
                            np.array(d.GetWithCuts(var)) <  ptBins[i+1]
                          )
        #etaInd = np.logical_and(
        #                        np.array(sample['photonOneEta']) >= etaBins[i], 
        #                        np.array(sample['photonOneEta']) <  etaBins[i+1]
        #      v                )

        #Ind = np.logical_and(ptInd,etaInd)
        Ind[d.name].append(ptInd)
        
        


# In[ ]:





# In[ ]:


ranges,bins = [-1,1],40
figx, figy = 24,19
nx , ny    = 3,4
ptBins = [20, 25, 30, 35, 45, 55]

for log in [True,False]:
    row, col   = 0,0

        
    pathFile = "/home/jcordero/CMS/JYCMCMS/SMP_ZG/python/Corrections/"
    if log:
        fileName = "ShowerShapeMVA_log"
    else:
        fileName = "ShowerShapeMVA"
    fig = plt.figure(figsize=(figx,figy))
    for i in np.arange(len(ptBins)-1):
        if i != 0:
            if i%ny == 0:
                row += 1
                col = 0  
        
        ax = plt.subplot2grid((nx*4,ny),(row*4,col),rowspan = 3, colspan = 1)    
        mc = plt.hist(
                        [np.array(BDT[d.name])[Ind[d.name][i]] for d in data[:-1]],
                        range    = ranges,
                        bins     = bins,
                        weights  = [d.GetWithCuts('weights')[Ind[d.name][i]] for d in data[:-1]],
                        histtype = 'stepfilled',
                        color    = colors[:-1],
                        stacked  = True,
                        label    = legend[:-1]
                        )
        plt.grid(linestyle='--')

        ax = plt.gca()
        y3,x3 =np.histogram(
                            np.array(BDT[data[-1].name])[Ind[data[-1].name][i]],
                            range    = ranges,
                            bins     = bins,
                           )
        x3b = (x3[1:len(x3)] + x3[0:-1])/2
        ax.errorbar(x3b,
                    y3,
                    xerr      = np.diff(x3)/2,yerr = np.sqrt(y3),
                    color     ='k',
                    marker    ='o',
                    linestyle ='',
                    label     = legend[-1]
                   )
        if log:
            ax.set_yscale('log')
        plt.grid(linestyle='--')

        plt.title('MVA score | Pt [' + str(ptBins[i])+','+str(ptBins[i+1])+']')
        plt.ylabel('# Counts')
        plt.xlabel('ShowerShape MVA')
        plt.legend()
        lim = ax.get_xlim()
        
        ax = plt.subplot2grid((nx*4,ny),(row*4+3,col),rowspan = 1, colspan = 1)    
        
        ymc = mc[0][-1]
        plt.errorbar(
                        x3b,
                        y3/ymc - 1,
                        yerr      = y3/ymc*np.sqrt(1/y3+1/ymc),
                        color     = 'k',
                        marker    = 'o',
                        linestyle = '',
                        linewidth = 1.5
                        )
        ax.grid(linestyle = '--')
        ax.set_xlim(lim)
        ax.set_ylim([-1,1])
        col += 1
        
        plt.tight_layout()
    fig.savefig(figpath+'ShowerShapeMVA/'+fileName+'.png')
    plt.show()


# In[25]:


folderMVA = 'MVA_scores'
for d,i in zip(data,np.arange(len(data))):
    
    df = pd.DataFrame({'MVA':BDT[d.name]})
    df.to_csv(folderMVA+'/MVA_'+legend[i]+'.csv')


# In[58]:


print(len(data[1].GetWithCuts('photonOneMVA')),
      len(BDT[data[1].name])
     )


# # ----------------- IOIOIOOIOIOO--------------

# In[ ]:


################################
#stacked = False
stacked = True

LOG = 'both'
log = False
#log = True

weightCorrection = True 
#weightCorrection = False
xsec1='65'
#xsec2='67'
#xsec2='70'
xsec2='69p2'

#phType = 'ISR'
#phType = 'FSR'
phType = ''

#Region = 'Sig'
Region = 'Sideband'
#Region = 'Compare'
#Region = ''

Charge = 'oposite'
#Charge = 'same'

#customRange = True
customRange = False

MVA = False
#MVA = True

Print = False
#Print = True
###############################
if stacked:
    Fol  = 'Stacked'
    stackLab  = ''
    histtype  = 'stepfilled'
    density   = False
    linewidth = 1
else:
    Fol  = 'Unstacked'
    stackLab  = ''
    histtype  = 'step'
    density   = True
    #density = False
    linewidth = 1.7
###############################    
if log:
    stackFol = Fol+'/log'
else:
    stackFol = Fol+'/linear'
###############################

######## CUTS ##############
PhaseSpace(
            data,
            phType = phType,
            Charge = Charge,
            Region = Region,
            Print  = Print,
            MVA    = MVA,
          )
#for d in data:
#    d.AddCuts(np.array(d.df.photonOneMVA)>0.2)
###############################


# In[ ]:





# In[ ]:


ranges,bins = [-1,1],40
#figx, figy = 24,19
figx, figy = 10,8
log        = True
dataSample = 'DYJets'
color      = 'purple'

#fig = plt.figure(figsize=(figx,figy))
pathFile = "/home/jcordero/CMS/JYCMCMS/SMP_ZG/python/Corrections/"
if log:
    fileName = "ShowerShapeMVA_log.png"
else:
    fileName = "ShowerShapeMVA.png"

for d in data:
    if d.name == dataSample:
        for i in np.arange(len(ptBins)-1):
            #plt.subplot(3,4,i+1)
            fig = plt.figure(figsize=(figx,figy))
            plt.hist(
                    #[np.array(BDT[d.name])[Ind[d.name][i]] for d in data[:-1]],
                    np.array(BDT[d.name])[Ind[d.name][i]] ,
                    range    = ranges,
                    bins     = bins,
                    #weights  = [d.GetWithCuts('weights')[Ind[d.name][i]] for d in data[:-1]],
                    weights  = d.GetWithCuts('weights')[Ind[d.name][i]],
                    histtype = 'stepfilled',
                    #color    = colors[:-1],
                    color    = color,
                    stacked  = True,
                    label    = dataSample
                    )
            plt.grid(linestyle='--')

            ax = plt.gca()

            if log:
                ax.set_yscale('log')
            plt.grid(linestyle='--')

            plt.title('MVA score | Pt [' + str(ptBins[i])+','+str(ptBins[i+1])+']')
            plt.ylabel('# Counts')
            plt.xlabel('ShowerShape MVA')
            plt.legend()

            fig.savefig(figpath+'ShowerShapeMVA/'+dataSample+'_'+fileName+'_'+str(ptBins[i])+'_'+str(ptBins[i+1])+'.png')
            plt.show()


# In[ ]:


ranges,bins = [-1,1],40
#figx, figy = 24,19
figx, figy = 10,8
log        = True
dataSample = 'ZGToLLG'
color      = 'magenta'

#fig = plt.figure(figsize=(figx,figy))
pathFile = "/home/jcordero/CMS/JYCMCMS/SMP_ZG/python/Corrections/"
if log:
    fileName = "ShowerShapeMVA_log.png"
else:
    fileName = "ShowerShapeMVA.png"

for d in data:
    if d.name == dataSample:
        for i in np.arange(len(ptBins)-1):
            #plt.subplot(3,4,i+1)
            fig = plt.figure(figsize=(figx,figy))
            plt.hist(
                    #[np.array(BDT[d.name])[Ind[d.name][i]] for d in data[:-1]],
                    np.array(BDT[d.name])[Ind[d.name][i]] ,
                    range    = ranges,
                    bins     = bins,
                    #weights  = [d.GetWithCuts('weights')[Ind[d.name][i]] for d in data[:-1]],
                    weights  = d.GetWithCuts('weights')[Ind[d.name][i]],
                    histtype = 'stepfilled',z
                    #color    = colors[:-1],
                    color    = color,
                    stacked  = True,
                    label    = dataSample
                    )
            plt.grid(linestyle='--')

            ax = plt.gca()

            if log:
                ax.set_yscale('log')
            plt.grid(linestyle='--')

            plt.title('MVA score | Pt [' + str(ptBins[i])+','+str(ptBins[i+1])+']')
            plt.ylabel('# Counts')
            plt.xlabel('ShowerShape MVA')
            plt.legend()

            fig.savefig(figpath+'ShowerShapeMVA/'+dataSample+'_'+fileName+'_'+str(ptBins[i])+'_'+str(ptBins[i+1])+'.png')
            plt.show()


# In[ ]:




