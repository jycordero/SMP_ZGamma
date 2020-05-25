#!/usr/bin/env python
# coding: utf-8

# In[1]:


## Python dependencies 
import matplotlib as mlp
import matplotlib.pyplot as plt
import matplotlib.colors as col
import numpy as np
import pandas as pd


# In[ ]:





# In[2]:


from numpy.random    import uniform
from root_pandas import read_root 

# External Dependencies
from ROOT import TFile, TTree


# In[3]:


# My Dependencies
#from Samples.Data      import Data
from Plotter.Helper    import Helper
from Data import Data
from Helper import Helper

#import Samples
import Plotter


# In[ ]:





# In[4]:


import os, datetime


# In[ ]:





# In[5]:


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


# In[6]:


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
        #SampleSet = 'V2_puWeight_phID'
        #SampleSet = 'V4_phID_isConv'
        SampleSet = 'V4_phID_isConv_MINUIT'
    elif selection == "mumu":
        run = ['B','C','D','E','F']
        DataGen = 'rereco'
        #SampleSet = 'V1'
        #SampleSet = 'V2_puWeight'
        SampleSet = 'V2_puWeight_phID'
    elif selection == "ee":
        run = ['B','C','D','E','F']
        DataGen = 'rereco'
        #SampleSet = 'EfficiencyCorrection/files_zee/CorrShower'
        SampleSet = 'EfficiencyCorrection/files_zee/V4_phID_isConv'

path    = "/home/jcordero/CMS/data_"+era+"/"+DataGen+"/SMP_ZG/Files/"+selection+"/"+SampleSet+"/"
figpath = "/home/jcordero/CMS/JYCMCMS/SMP_ZG/figs/"+era+"/"+DataGen+"/"+selection+"/"

figpath = dirStructure(figpath)

Help    = Plotter.Helper.Helper()
#Help    = Helper()

LoadVars = [
            #'runNumber','evtNumber',
            'nPV',
            'nPU',
            
            #'genWeight',
            'eventWeight','puWeight',
            #'triggerWeight','photonIDWeight',
            'photonOneEta',
            #'l1PhotonDR','l2PhotonDR',
            #'leptonOneCharge','leptonTwoCharge',
            #'photonOneMVA',
            #'photonOneERes',
    
            ############################# 
    
            'photonOneR9',
            #'photonOneSieie',
            'photonOneHoverE',
    
            #'photonOneIneu','photonOneIph','photonOneIch',
            #'photonOneSieip',
            #'photonOneSipip',
            #'photonOneSrr',
            #'photonOneE2x2',
            #'photonOneR9',
            #'photonOneE5x5',
            #'photonOneScEtaWidth',
            #'photonOneScPhiWidth',
            #'photonOneScRawE',
            #'photonOnePhi',
            #'photonOnePreShowerE',
            #'photonOneScBrem',
            #'Rho',
            ##############################
            #'genPhotonPt',
            #'vetoDY',
            #'genIsoPass',
            #'passElectronVeto',
            'ProbeIDPass','ProbeWorstPass',
            ]


# In[7]:


print(path,'\n',
      era,'\n',
      run,
     )


# In[8]:


# --------------------------------------
#  Data
# ---------------------------------------
if selection   == 'mumug':
    DoubleLepton = [Data(path+"DoubleMuon/","DoubleMuon_"+era,trigger = r,era = era,data=True, var = LoadVars) for r in run]
elif selection == 'elelg':
    DoubleLepton = [Data(path+"DoubleEG/","DoubleEG_"+era,trigger = r,era = era, data=True, var = LoadVars) for r in run]
elif selection == 'ee':
    #SingleLepton = [Data(path+"SingleElectron/","Electron_"+era,trigger = r,era = era, data=True, var = LoadVars) for r in run]
    SingleLepton = [Data(path+"SingleElectron/","Electron_"+era,trigger = r,era = '2017_RunD', data=True, var = LoadVars) for r in run]
    
    
#if selection   == 'mumug':
#    DoubleLepton = [Samples.Data.Data(path+"DoubleMuon/","DoubleMuon_"+era,trigger = r,data=True) for r in run]
#elif selection == 'elelg':
#    DoubleLepton = [Samples.Data.Data(path+"DoubleEG/","DoubleEG_"+era,trigger = r,data=True) for r in run]


# In[9]:


if selection   == 'mumug':
    Leptons = DoubleLepton[0]
    for i in np.arange(len(DoubleLepton[1:])):
        Leptons =   Leptons + DoubleLepton[1]
        del DoubleLepton[1]
elif selection == "mumu":
    Leptons = DoubleLepton[0]
    for i in np.arange(len(DoubleLepton[1:])):
        Leptons =   Leptons + DoubleLepton[1]
        del DoubleLepton[1]
elif selection == "ee":
    Leptons = SingleLepton[0]
    for i in np.arange(len(SingleLepton[1:])):
        Leptons =   Leptons + SingleLepton[1]
        del SingleLepton[1]


# In[10]:


DYJets     = Data(path +      "DYJets/",     "DYJets", "_v", era = '2017', var = LoadVars)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[11]:


import copy
#dataSelect = 'ALL'
dataSelect = 'DY Only'
#dataSelect = 'noTT'
#dataSelect = 'DYVeto'
#dataSelect = 'DY ZG'
#dataSelect = 'DY ZG Comp'
#dataSelect = 'no ZG'
#dataSelect = 'DY Compare'


if   dataSelect == 'ALL':
    data        = [  WJets,         VV,     TT,   DYJets,        ZG,      Leptons]
    listSamples = [ 'WJets',      'V-V',   'TT', 'DYJets',      'ZG', 'Data']
    #legend      = [ 'WJets',      'V-V',   'TT', 'DYJets',      'ZG', 'DoubleMuon']
    legend      = [ ' WJets',   '   V-V', '    TT', 'DYJets',  '    ZG', 'Data']
    #colors      = [     'b',    'cyan',    'r', 'purple', 'magenta',          'k']
    colors      = [     'cornflowerblue',    'lightskyblue',    'lightcoral', 'plum',     'pink',          'k']
    dataFlag    = [   False,     False,  False,    False,     False,         True]
    combFlag    = [   False,     False,  False,    False,     False,         True]
elif dataSelect == "noTT":
    data        = [  WJets,         VV,   DYJets,        ZG,      Leptons]
    listSamples = [ 'WJets',      'VV', 'DYJets',      'ZG', 'DoubleMuon']
    legend      = [ 'WJets',      'VV', 'DYJets',      'ZG', 'DoubleMuon']
    colors      = [     'b',    'cyan', 'purple', 'magenta',          'k']
    dataFlag    = [   False,     False,    False,     False,         True]
    combFlag    = [   False,     False,    False,     False,         True]
elif dataSelect == 'VV Separate':
    data        = [  DYJets,   WJets,       TT,       WW,      ZZ,       WZ,       ZG,    Leptons]
    listSamples = ['DYJets', 'WJets',      'TT',    'WW',    'ZZ',     'WZ',      'ZG', 'DoubleMuon']
    legend      = ['DYJets', 'WJets',      'TT',    'WW',    'ZZ',     'WZ',      'ZG', 'DoubleMuon']
    colors      = [  'cyan',     'r',  'purple',    'grey',  'teal', 'orange', 'magenta',          'k']
    dataFlag    = [   False,   False,     False,   False,   False,    False,     False,         True]
    combFlag    = [   False,   False,     False,   False,   False,    False,     False,         True]
elif dataSelect == 'DY Only':    
    data        = [  DYJets, Leptons]
    listSamples = ['DYJets',  'Data']
    legend      = ['DYJets',  'Data']
    colors      = [  'plum',     'k']
    dataFlag    = [   False,    True]
    combFlag    = [   False,    True]
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
    listSamples = [ 'WJets',      'V-V',   'TT', 'DYJets','Data']
    legend      = [ 'WJets',      'V-V',   'TT', 'DYJets','Data']
    colors      = [     'cornflowerblue',    'lightskyblue',    'lightcoral', 'plum', 'k']
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


# In[12]:




showershapeVar = [
'R9','HoverE',
'Sieie','Sieip','Sipip','Srr',
'E2x2','E5x5',
'ScEtaWidth','ScPhiWidth',
'ScRawE','PreShowerE','ScBrem',
'Ineu','Iph','Ich',
'ERes',
   ]

#showershapeVar = ['photonOne'+v for v in showershapeVar]


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[13]:


def GetPUweight(era = '2016', xsec='69p2'):
    
    ### Get Distributions ##
    PU,PUmc = GetMCPU(era)
    PUdata  = GetDataPU(era,xsec)
    
    ### Normalize ###
    PUmc   = np.array(PUmc)/sum(PUmc)        
    PUdata = np.array(PUdata)/sum(PUdata)
    
    return PU,PUdata[:len(PUmc)]/PUmc,PUdata,PUmc,


# In[14]:


def GetDataPU(era = '2016',xsec='69p2'):
    pileupFile = 'pileup_sf_'+era+'_'+xsec+'mb.root'
    file = TFile('/home/jcordero/CMS/data_'+era+'/'+DataGen+'/SMP_ZG/Files/'+pileupFile)
    puTree = file.Get('pileup')
    PUdata = []
    for pu in puTree:
        PUdata.append(pu)
    return PUdata


# In[15]:


def GetMCPU(era = '2016',Flag = True):
    ########### MC Scenario ##################
    
    if era == '2016':
        # mix_2016_25ns_Moriond17MC_PoissonOOTPU_cfi.py
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
    elif era == '2017':
        # Extracted from noTrig DYJets MC
        if Flag:
            PU = np.array([ 
                             0.,  1.,  2.,  3.,  4.,  5.,  6.,  7.,  8.,  9., 10., 11., 12.,
                            13., 14., 15., 16., 17., 18., 19., 20., 21., 22., 23., 24., 25.,
                            26., 27., 28., 29., 30., 31., 32., 33., 34., 35., 36., 37., 38.,
                            39., 40., 41., 42., 43., 44., 45., 46., 47., 48., 49., 50., 51.,
                            52., 53., 54., 55., 56., 57., 58., 59., 60., 61., 62., 63., 64.,
                            65., 66., 67., 68., 69., 70., 71., 72., 73., 74., 75., 76., 77.,
                            78., 79., 80., 81., 82., 83., 84., 85., 86., 87., 88., 89., 90.,
                            91., 92., 93., 94., 95., 96., 97., 98., 99.
                            ])
            PUmc = np.array([
                            2.50071521e-02, 9.32138697e-04, 1.34349382e-03, 1.55653761e-03,
                            1.45496351e-03, 1.43526107e-03, 1.27835150e-03, 1.15729683e-03,
                            2.21869955e-03, 1.72671527e-03, 2.28850123e-03, 3.35718143e-03,
                            4.92791900e-03, 6.68134795e-03, 9.10044445e-03, 1.17060042e-02,
                            1.45309977e-02, 1.75059783e-02, 1.99916815e-02, 2.23530463e-02,
                            2.41402001e-02, 2.53499037e-02, 2.62041645e-02, 2.67175374e-02,
                            2.74284230e-02, 2.83532398e-02, 2.89839400e-02, 2.93689364e-02,
                            2.91766601e-02, 2.90470411e-02, 2.88956340e-02, 2.90606641e-02,
                            2.90281817e-02, 2.85503530e-02, 2.82879200e-02, 2.75466820e-02,
                            2.62923374e-02, 2.50091934e-02, 2.40847315e-02, 2.32438276e-02,
                            2.14996286e-02, 1.96380581e-02, 1.77144071e-02, 1.59592475e-02,
                            1.44335061e-02, 1.32091144e-02, 1.20550570e-02, 1.16780036e-02,
                            1.13855288e-02, 1.11553119e-02, 1.13355627e-02, 1.13423077e-02,
                            1.12138868e-02, 1.12709972e-02, 1.11441738e-02, 1.12494754e-02,
                            1.10476141e-02, 1.08218347e-02, 1.03416985e-02, 9.49174212e-03,
                            8.46104682e-03, 7.27566069e-03, 5.91352943e-03, 4.90768406e-03,
                            3.81464205e-03, 3.17125069e-03, 2.79472984e-03, 2.00325951e-03,
                            1.47187034e-03, 1.02776656e-03, 7.73232257e-04, 6.06693338e-04,
                            3.89700182e-04, 3.41109691e-04, 3.04988540e-04, 2.55155551e-04,
                            1.94095718e-04, 1.72041404e-04, 1.62678304e-04, 3.32811588e-04,
                            3.62454007e-04, 2.83644223e-04, 1.80738880e-04, 2.56708672e-04,
                            1.23362162e-04, 1.57264569e-04, 8.94597549e-05, 2.03769442e-04,
                            1.75902018e-04, 1.12046568e-04, 5.72879681e-05, 4.00705152e-05,
                            5.28061053e-06, 2.49386817e-05, 2.00130702e-05, 1.53980828e-04,
                            6.65623177e-06, 1.37562123e-05, 4.82798677e-05
                            ])
        # mix_2017_25ns_UltraLegacy_PoissonOOTPU_cfi.py
        else:
            PU = np.array([
                             0,  1,  2,  3,  4,  5,  6,  7,  8,  9,
                            10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                            20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
                            30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
                            40, 41, 42, 43, 44, 45, 46, 47, 48, 49,
                            50, 51, 52, 53, 54, 55, 56, 57, 58, 59,
                            60, 61, 62, 63, 64, 65, 66, 67, 68, 69,
                            70, 71, 72, 73, 74, 75, 76, 77, 78, 79,
                            80, 81, 82, 83, 84, 85, 86, 87, 88, 89,
                            90, 91, 92, 93, 94, 95, 96, 97, 98
                            ])
            PUmc = np.array([
                            1.1840841518e-05, 3.46661037703e-05, 8.98772521472e-05, 7.47400487733e-05, 0.000123005176624,
                            0.000156501700614, 0.000154660478659, 0.000177496185603, 0.000324149805611, 0.000737524009713,
                            0.00140432980253, 0.00244424508696, 0.00380027898037, 0.00541093042612, 0.00768803501793,
                            0.010828224552, 0.0146608623707, 0.01887739113, 0.0228418813823, 0.0264817796874,
                            0.0294637401336, 0.0317960986171, 0.0336645950831, 0.0352638818387, 0.036869429333,
                            0.0382797316998, 0.039386705577, 0.0398389681346, 0.039646211131, 0.0388392805703,
                            0.0374195678161, 0.0355377892706, 0.0333383902828, 0.0308286549265, 0.0282914440969,
                            0.0257860718304, 0.02341635055, 0.0213126338243, 0.0195035612803, 0.0181079838989,
                            0.0171991315458, 0.0166377598339, 0.0166445341361, 0.0171943735369, 0.0181980997278,
                            0.0191339792146, 0.0198518804356, 0.0199714909193, 0.0194616474094, 0.0178626975229,
                            0.0153296785464, 0.0126789254325, 0.0100766041988, 0.00773867100481, 0.00592386091874,
                            0.00434706240169, 0.00310217013427, 0.00213213401899, 0.0013996000761, 0.000879148859271,
                            0.000540866009427, 0.000326115560156, 0.000193965828516, 0.000114607606623, 6.74262828734e-05,
                            3.97805301078e-05, 2.19948704638e-05, 9.72007976207e-06, 4.26179259146e-06, 2.80015581327e-06,
                            1.14675436465e-06, 2.52452411995e-07, 9.08394910044e-08, 1.14291987912e-08, 0.0,
                            0.0, 0.0, 0.0, 0.0, 0.0,
                            0.0, 0.0, 0.0, 0.0, 0.0,
                            0.0, 0.0, 0.0, 0.0, 0.0,
                            0.0, 0.0, 0.0, 0.0, 0.0,
                            0.0, 0.0, 0.0, 0.0
                            ])
    elif era == '2018':
        # mix_2018_25ns_UltraLegacy_PoissonOOTPU_cfi.py
        PU = np.array([
                        0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                        10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                        20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
                        30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
                        40, 41, 42, 43, 44, 45, 46, 47, 48, 49,
                        50, 51, 52, 53, 54, 55, 56, 57, 58, 59,
                        60, 61, 62, 63, 64, 65, 66, 67, 68, 69,
                        70, 71, 72, 73, 74, 75, 76, 77, 78, 79,
                        80, 81, 82, 83, 84, 85, 86, 87, 88, 89,
                        90, 91, 92, 93, 94, 95, 96, 97, 98
                        ])
        PUmc = np.array([
                        8.89374611122e-07, 1.1777062868e-05, 3.99725585118e-05, 0.000129888015252, 0.000265224848687,
                        0.000313088635109, 0.000353781668514, 0.000508787237162, 0.000873670065767, 0.00147166880932,
                        0.00228230649018, 0.00330375581273, 0.00466047608406, 0.00624959203029, 0.00810375867901,
                        0.010306521821, 0.0129512453978, 0.0160303925502, 0.0192913204592, 0.0223108613632,
                        0.0249798930986, 0.0273973789867, 0.0294402350483, 0.031029854302, 0.0324583524255,
                        0.0338264469857, 0.0351267479019, 0.0360320204259, 0.0367489568401, 0.0374133183052,
                        0.0380352633799, 0.0386200967002, 0.039124376968, 0.0394201612616, 0.0394673457109,
                        0.0391705388069, 0.0384758587461, 0.0372984548399, 0.0356497876549, 0.0334655175178,
                        0.030823567063, 0.0278340752408, 0.0246009685048, 0.0212676009273, 0.0180250593982,
                        0.0149129830776, 0.0120582333486, 0.00953400069415, 0.00738546929512, 0.00563442079939,
                        0.00422052915668, 0.00312446316347, 0.00228717533955, 0.00164064894334, 0.00118425084792,
                        0.000847785826565, 0.000603466454784, 0.000419347268964, 0.000291768785963, 0.000199761337863,
                        0.000136624574661, 9.46855200945e-05, 6.80243180179e-05, 4.94806013765e-05, 3.53122628249e-05,
                        2.556765786e-05, 1.75845711623e-05, 1.23828210848e-05, 9.31669724108e-06, 6.0713272037e-06,
                        3.95387384933e-06, 2.02760874107e-06, 1.22535149516e-06, 9.79612472109e-07, 7.61730246474e-07,
                        4.2748847738e-07, 2.41170461205e-07, 1.38701083552e-07, 3.37678010922e-08, 0.0,
                        0.0, 0.0, 0.0, 0.0, 0.0,
                        0.0, 0.0, 0.0, 0.0, 0.0,
                        0.0, 0.0, 0.0, 0.0, 0.0,
                        0.0, 0.0, 0.0, 0.0
                        ])

    return PU,PUmc


# In[16]:


def SF_ratio(
             era = '2016',
             xsec1='65',
             xsec2='69p2',
            ):
    pu,r1,r1d,r1mc = GetPUweight(era = era, xsec = xsec1)
    pu,r2,r2d,r2mc = GetPUweight(era = era, xsec = xsec2)
    
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


# In[ ]:





# In[17]:


def GetStatUncertainty(bins, counts, scale):
    x = []
    x.append(bins[0])
    for i in np.arange(1,len(bins)-1):
        x.append(bins[i])
        x.append(bins[i])
    x.append(bins[-1])

    statUn = np.sqrt(counts)
    statsUp, statsDown = [],[]
    count = []
    for i in np.arange(len(counts)):
        count.append(counts[i])
        count.append(counts[i])
        
        statsUp.append(statUn[i]*scale[i])
        statsUp.append(statUn[i]*scale[i])
        
        statsDown.append(statUn[i]*scale[i])
        statsDown.append(statUn[i]*scale[i])
        
    count     =     np.array(count)
    statsUp   =   np.array(statsUp)
    statsDown = np.array(statsDown)
    return x,count,statsUp, statsDown


# In[18]:


def UnStackHist(hist):
    UnHist = []
    UnHist.append(hist[0])
    for i in np.arange(1,len(hist)):
        UnHist.append(hist[i] - hist[i-1])
    return UnHist


# In[19]:


def GET_StatUncertainty(data,hist,var,bins):
    if len(var)>2:
        part,var,ph = var[0],var[2],'_'+var[1]
    else:
        part,var,ph= var[0],var[1],''
    var = part+var+ph
    
    VAL = hist[-1]
    hist = UnStackHist(hist)
    bins = np.array(bins)
    
    xc = (bins[:-1]+bins[1:])/1
    for i in np.arange(len(hist)-1):
        scale = []
        for j in np.arange(len(bins)-1):
            Ind = np.logical_and(data[i].GetWithCuts(var) > bins[j], data[i].GetWithCuts(var) <= bins[j+1])
            #weightPerBin.append(np.sum(d.GetWithCuts('weights')[Ind]))
            if np.sum(Ind) == 0:
                scale.append(1)
            else:
                weightOverYield = np.sum(data[i].GetWithCuts('weights')[Ind])/np.sum(Ind)
                scale.append(weightOverYield)
                     
        if i == 0:
            x,value, Up, Down = GetStatUncertainty(xc,hist[i],scale)
            statsUp   = Up
            statsDown = Down
        else:
            x,value, Up, Down = GetStatUncertainty(xc,hist[i],scale)
            statsUp   += Up
            statsDown += Down              
    x,value, Up, Down = GetStatUncertainty(bins,VAL,scale)
    
    return x,value,statsUp, statsDown


# In[20]:


def GET_RangeBins(Ks,
                  Blind    = True,
                  Plotting = True, 
                 ):
    ##########################
    if len(Ks)>2:
        part,var,ph = Ks[0],Ks[2],'_'+Ks[1]
    else:
        part,var,ph= Ks[0],Ks[1],''

    
    if   var == 'R9':
        ranges = [0.85,1]
        bins = 100
    elif var == 'HoverE':
        ranges = [0.0001,0.15]
        bins = 100
    elif var == 'Sieie':
        ranges = Help.plotOpsAll[0]['range'][var][part+ph]
        bins = 100
    elif var == 'S4':
        ranges = [0,1.1]
        bins = 40
    elif var == "Rho":
        if ph == "_EB":
            ranges = [0,60]
            bins   = 50
        else:
            ranges = [0,60]
            bins   = 50
    elif var == "ScBrem":
        if ph == "_EB":
            ranges = [0,30]
            bins   = 30
        else:
            ranges = [0,15]
            bins   = 15
    elif var == "ScRawE":
        ranges = [0,700]
        bins = 200
    elif var == "Eta":
        ranges = [-3,3]
        bins   = 50
    elif var == "Phi":
        ranges = [-3.6,3.6]
        bins   = 50
    ###########################
    elif var == 'nJets':
        ranges = [0,7]
        bins   = 7
    elif var == 'Pt':
        if not Blind:
            if part == 'photonOne' and Plotting:
                ranges = Help.plotOpsAll[0]['range'][var][part+ph]
                bins   = Help.plotOpsAll[0]['bins'][var][part+ph][:-1]
            else:
                ranges = Help.plotOpsAll[0]['range'][var][part+ph]
                bins   = Help.plotOpsAll[0]['bins'][var][part+ph]
        elif part == 'photonOne':
            ranges = [15,80]
            bins   = [15,20,25,30,35,45,55]           
        else:
            ranges = Help.plotOpsAll[0]['range'][var][part+ph]
            bins   = Help.plotOpsAll[0]['bins'][var][part+ph]
    elif var == 'M':
        if not Blind:
            if part == 'llg' and Plotting:
                ranges = Help.plotOpsAll[0]['range'][var][part+ph]
                bins   = Help.plotOpsAll[0]['bins'][var][part+ph][:-1]
            else:
                ranges = Help.plotOpsAll[0]['range'][var][part+ph]
                bins   = Help.plotOpsAll[0]['bins'][var][part+ph]
        elif part == 'llg' :
            ranges = [50,135]
            bins   = [50,  85,  95,  110,  135,  170,  210,  270]            
        else:
            ranges = Help.plotOpsAll[0]['range'][var][part+ph]
            bins   = Help.plotOpsAll[0]['bins'][var][part+ph]
    else:
        #ranges = Help.plotOpsAll[0]['range'][var][part+ph]
        #bins   = Help.plotOpsAll[0]['bins'][var][part+ph]
        ranges = Help.ranges[var][part+ph]
        bins   = Help.bins[var][part+ph]
    ##########################
    
    '''
    #### VERY QUICK TEST #####
    if var == 'M':
        if part == 'llg':
            ranges = [50,150]
            #bins   = [50,  85,  95,  110,  135,  170,  210,  270]            
            #bins = 30
            bins = int((ranges[1]-ranges[0])/3.5)
        elif part == 'dilepton':
            ranges = [50,120]
            #bins   = [50,  85,  95,  110,  135,  170,  210,  270]            
            #bins = 30
            bins = int((ranges[1]-ranges[0])/2)
    elif var == 'Eta':
        if part == 'photonOne':
            ranges = [-3,3]
            bins = 50
    if var == 'met':
        ranges = [0,170]
        bins = 50
    if var == 'Pt':
        if part == 'photonOne':
            ranges = [0,80]
            bins = int((ranges[1]-ranges[0])/2)
            
    ''';
    
    
    return ranges,bins


# In[21]:


def GET_WeiVAR(data,Ks,weightCorrection = True):
    if len(Ks)>2:
        part,var,ph = Ks[0],Ks[2],'_'+Ks[1]
    else:
        part,var,ph= Ks[0],Ks[1],''
     
    
    if weightCorrection:
        # MODIFICATIONS
        #wei = [np.array(reWeight[i][data[i].cuts])/(np.array(data[i].df.photonIDWeight)[data[i].cuts]) for i in range(len(data[:-1]))]
        #wei.append(data[-1].GetWithCuts('weight')//(np.array(data[-1].df.photonIDWeight)[data[-1].cuts]))
        
        wei = [np.array(reWeight[i][data[i].cuts]) for i in range(len(data[:-1]))]
        wei.append(data[-1].GetWithCuts('weight'))
    else:
        # ORIGINAL
        wei = [d.GetWithCuts('weight') for d in data]
    
    VAR = [d.GetWithCuts(part+var+ph) for d in data]        
        
    return wei,VAR


# In[ ]:





# In[22]:


def PlotDataMC(
                ax,
                lims,
                Data,Sig,Bkg,
                ranges,bins,mag=1,
                signalInclude=True,
                log = False,
                ):
    
    Bkg = Bkg[:len(Data[0])]
    try:
        Sig = Sig[:len(Data[0])]
    except:
        Sig = Sig
    
    if not signalInclude:
        h = Bkg+Sig/mag
        rDataMC = Data[1]/(Bkg+Sig/mag) - 1 
    else:
        h = np.array(Bkg)
        rDataMC = Data[1]/Bkg - 1 

    ax.errorbar(
                Data[0], rDataMC[:len(Data[0])],
                yerr      = Data[1]/h*np.sqrt(1/Data[1]+1/h),
                color     = 'k',
                marker    = 'o',
                linestyle = '',
                linewidth = 1.5
               )    
    plt.grid(linestyle='--')
    
    ax.set_ylabel(r'$\frac{Data}{MC}-1$')
    ax.set_xlim(lims[0])
    ax.set_ylim(lims[1])
    if log:
        ax.set_yscale('log')
    return rDataMC[:len(Data[0])]


# In[23]:


def PlotData(
            ax,
            Data,
            ranges,
            bins,
            log = False,
            ):

    y3,x3 =np.histogram(
                        Data,
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
    ax.legend(prop={'size': 10})
    
    xlim = ax.get_xlim()
    ax.set_ylabel('# Counts')
    #ax.set_xlabel(var)
    #plt.legend()
    if log:
        ax.set_yscale('log')
        
    return x3,np.array(y3),x3b,xlim


# In[24]:


def Plot(data,
         var,
         part             =  '',
         signalInclude    = False,
         stacked          = True,
         density          = False,
         log              = False,
         weightCorrection = True,
         Plotting         = True,
         Blind            = True,
        ):

    
    
    k = part+'_'+var
    Ks = k.split('_')
    
    ##########################
    
    ranges,bins = GET_RangeBins(Ks,Blind=False,Plotting=Plotting)
    wei   ,VAR  = GET_WeiVAR   (data,Ks, weightCorrection=weightCorrection )
    label = [legend[i] + ' Yield '+ str(int(np.sum(data[i].GetWithCuts('weights')))) for i in np.arange(len(data))]
    
    ##########################
    
    if stacked:
        histtype = 'stepfilled'
    else:
        histtype = 'step'
        
    ##########################
    
    if not signalInclude:
        N = 2
    else:
        N = 1
        
    ###########################################################

    fig = plt.figure(figsize=(10,10))
    plt.subplot2grid((4,1),(0,0),rowspan = 3, colspan = 1)

    #for w,da in zip(wei,VAR):
    #    print(len(w),len(da))
    h_bg = plt.hist(
                    VAR[:-N],
                    range     = ranges,
                    bins      = bins,
                    histtype  = histtype,
                    stacked   = stacked,
                    weights   = wei[:-N],
                    #label     = legend[:-N],
                    label     = label[:-N],
                    color     = colors[:-N],
                    density   = density,
                    linewidth = linewidth,
                    )
        
    plt.grid(linestyle='--')
    plt.legend()

    ##########################
    
    if stacked:
        ##########################
        if not signalInclude:
            h_sig = plt.hist(
                                VAR[-N],
                                range     = ranges,
                                bins      = bins,
                                histtype  = histtype,
                                stacked   = stacked,
                                #label     = legend[-N]+" x"+str(mag),
                                label     = label[-N]+" x"+str(mag),
                                color     = colors[-N],
                                weights   = np.array(wei[-N])*mag,
                                density   = density,
                                linewidth = 1.5,
                                #alpha = 0.5,
                                )
        else:
            h_sig = h_bg[-N]
            
        if type(bins) is float or type(bins) is int:
            step = (ranges[1]-ranges[0])/bins
            bins = np.array([ranges[0]+i*step for i in np.arange(bins+1)])   
        
        #x,value,statUp,statDown = GET_StatUncertainty(data, hist = h_bg[0], var=Ks, bins = bins)
        #ax = plt.gca()
        #ax.fill_between(x,value-statDown,value+statUp,facecolor='lightgrey',color = 'grey',hatch='/////',alpha=0.6,label='MC stat')
        ##########################
        if not density:
            #---------------------
            #---- Ploting the Data    
            #---------------------
            ax = plt.gca()
            # Blind the data Plot
            ranges,bins = GET_RangeBins(Ks,Blind=True,Plotting=Plotting)
            
            x3,y3,x3b,xlim = PlotData(ax,VAR[-1],ranges,bins,log)
            ax.set_xlabel(var)
            
            #------------------------
            #---- Ploting the Data/MC    
            #-------------------------
            plt.subplot2grid((4,1),(3,0),rowspan = 1, colspan = 1)    
            ax = plt.gca()
            
            # Data/MC  y-RANGE
            ylim = [-0.5,0.5]
            if type(h_bg[0]) == list:
                Bkg = h_bg[0][-1]
            else:
                Bkg = h_bg[0]
                
            rDataMC = PlotDataMC(ax,
                       lims    = [xlim, ylim],
                       Data    = [x3b, y3],
                       #Bkg     = h_bg[0][-1],
                       Bkg     = Bkg,
                       Sig     = h_sig[0],
                       ranges  = ranges,
                       bins    = bins,
                      )
    
    plt.tight_layout()
    plt.show()
    fig.savefig(figpath+stackFol+'/'+var+'_'+part+stackLab+".png")
    
    try:
        return x3,y3,Bkg,h_sig[0],rDataMC
    except:
        return False


# In[25]:


def Plot_Mult(
              data,
              var,
              part             = ['lepton1','lepton2','photon1','dilep','dilepgm'],
              signalInclude    = False,
              figDim           = [2,3],
              customRange      = False,
              stacked          = True,
              log              = False,
              weightCorrection = True,
              Blind            = True,
              Plotting         = True,
             ):

    
    nx,ny = figDim[0],figDim[1]
    
    ##########################
    if not signalInclude:
        N = 2
    else:
        N = 1
    ##########################
    if stacked:
        histtype = 'stepfilled'
    else:
        histtype = 'step'
    ##########################
    
    htemp = []
    row,col =0 , 0
    
    
    fig = plt.figure(figsize = (6*ny, 6*nx))
    
    for j,k in zip(range(len(part)),part):    
        K = k+'_'+var
        Ks = K.split('_')
        
        ##########################
        
        ranges,bins = GET_RangeBins(Ks, Blind=False,Plotting=Plotting)
        wei, VAR    = GET_WeiVAR(data, Ks, weightCorrection=weightCorrection )
        label = [legend[i] + ' Yield '+ str(int(np.sum(data[i].GetWithCuts('weights')))) for i in np.arange(len(data))]

        ##########################
        
        nx,ny = figDim[0],figDim[1]
    
        if j != 0:
            if j%ny == 0:
                row += 1
                col = 0  
    
        ax = plt.subplot2grid((nx*4,ny),(row*4,col),rowspan = 3, colspan = 1)    
        title_lab = k        


    
        
        h_bg = ax.hist(
                        VAR[:-N],                            
                        histtype  = histtype,
                        range     = ranges,
                        bins      = bins,
                        stacked   = stacked,
                        color     = colors[:-N],
                        weights   = wei[:-N],
                        #label     = legend,
                        label     = label,
                        density   = density,
                        linewidth = linewidth,
                        )
        htemp.append(h_bg)
        ax.set_title(title_lab)
        ax.set_xlabel(var)
        ax.grid(linestyle='--')
        ax.legend(prop={'size':10})

        #----------------------------------------------------------------
        #----------------------------------------------------------------
        if stacked:
            if not signalInclude:
                h_sig = ax.hist(
                                VAR[-N],
                                bins      = bins,
                                range     = ranges,
                                histtype  = Help.plotOpsAll[-N]['histtype'],
                                stacked   = Help.plotOpsAll[-N]['stacked'],
                                color     = colors[-N],
                                weights   = wei[-N],
                                #label     = legend[-N] + "x"+str(mag),
                                label     = label[-N] + "x"+str(mag),
                                linewidth = 2
                                )
                ax.legend(prop={'size': 10})
            else:
                h_sig = h_bg[0][-1]
            
            if type(bins) is float or type(bins) is int:
                step = (ranges[1]-ranges[0])/bins
                bins = np.array([ranges[0]+i*step for i in np.arange(bins+1)])   
            x,value,statUp,statDown = GET_StatUncertainty(data, hist = h_bg[0], var=Ks, bins = bins)
            ax = plt.gca()
            ax.fill_between(x,value-statDown,value+statUp,facecolor='lightgrey',color = 'grey',hatch='/////',alpha=0.6,label='MC stat')
            
            #---------------------
            #---- Ploting the Data    
            #---------------------
            ax = plt.gca()
            # Blind the data Plot
            ranges,bins = GET_RangeBins(Ks,Blind=True,Plotting=Plotting)
            
            x3,y3,x3b,xlim = PlotData(ax,VAR[-1],ranges,bins,log)
            ax.set_xlabel(var)
            
            #------------------------
            #---- Ploting the Data/MC    
            #-------------------------
            ax1 = plt.subplot2grid((nx*4,ny),(row*4+3,col),rowspan = 1, colspan = 1)    
            
            # Data/MC  y-RANGE
            ylim = [-0.5,0.5]
            PlotDataMC(ax1,
                       lims    = [xlim, ylim],
                       Data    = [x3b, y3],
                       Bkg     = h_bg[0][-1],
                       Sig     = h_sig[0],
                       ranges  = ranges,
                       bins    = bins,
                      )
            
        col+=1
        if log:
            ax.set_yscale('log')
        #########################################################
        
    
    fig.tight_layout()
    plt.show()
    fig.savefig(figpath+stackFol+'/Mult/'+var+stackLab+".png")


# In[ ]:





# In[26]:


def STD_Cuts(
            data,
            phType = 'ISR',
            Charge ='oposite',
            Print  = False,
            MVA    = False,
            vetoDY = True,
            ):
    
    [d.ResetCuts() for d in data]
    #---------------------------- CUTS ------------------------------------ CUTS -----------------------

    for d in data:
        #d.AddCuts(np.array(d.df.photonOnePt)>10)
        if Print:
            print('-----------------',d.name,'--------------')
            print('----Total----')
            print(np.sum(d.cuts))
            
        #-------------------------------------------
        if vetoDY and  d.name == 'DYJets':
            d.AddCuts(np.array(d.df.vetoDY)==False)
            
        #-------------------------------------------
        d.AddCuts(np.array(d.df.l1PhotonDR) > 0.7)
        d.AddCuts(np.array(d.df.l2PhotonDR) > 0.7)
        if Print:
            print('----DR cuts ----')
            print(np.sum(d.cuts))
            
        #-------------------------------------------
        if phType == 'ISR':
            # 2 Body to get ISR
            d.AddCuts(np.array(d.df.llgM)+np.array(d.df.dileptonM) > 185)
        elif phType == 'FSR' :
            # 3 Body to get FSR
            d.AddCuts(np.array(d.df.llgM)+np.array(d.df.dileptonM) < 185)
        if Print:
            print('----Mass cuts ----')  
            print(np.sum(d.cuts))
            
        #-------------------------------------------
        if MVA:
            #d.AddCuts(np.array(d.df.photonOneMVA <= 0.2))
            d.AddCuts(np.array(d.df.photonOneMVA > 0.2))
        if Print:
            print('----MVA cuts ----')  
            print(np.sum(d.cuts))
            
        #-------------------------------------------
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
                vetoDY = True,
              ):   
    
    STD_Cuts( data, phType = phType, Charge = Charge, Print = Print , MVA = MVA, vetoDY = vetoDY)
    
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


# In[ ]:





# In[ ]:





# In[27]:


mlp.rcParams['axes.grid']       = True
mlp.rcParams['axes.titlesize']  = 24
mlp.rcParams['axes.labelsize']  = 20

mlp.rcParams['xtick.labelsize'] = 16
mlp.rcParams['ytick.labelsize'] = 16

mlp.rcParams['legend.fontsize'] = 13


# In[ ]:





# In[ ]:





# In[ ]:





# In[28]:


if 'S4' in LoadVars:
    for d in data:
        d.df["photonOneS4"] = d.df.photonOneE2x2/d.df.photonOneE5x5
        d.df["photonOneS4_EE"] = d.df.photonOneE2x2_EE/d.df.photonOneE5x5_EE
        d.df["photonOneS4_EB"] = d.df.photonOneE2x2_EB/d.df.photonOneE5x5_EB

################################
#stacked = False
stacked = True

#Blind  = False
Blind  = True

#Plotting = True
Plotting = True

LOG = 'both'
log = False
#log = True

#weightCorrection = True 
weightCorrection = False
#xsec1, xsec2 = '65','69p2'
#xsec1, xsec2 = '69p2','69p2'
xsec1, xsec2 = '70','69p2'
#xsec1, xsec2 = '71p5','69p2'
#xsec1, xsec2 = '72p4','69p2'


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

#vetoDY = False
vetoDY = True

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
#PhaseSpace(
#            data,
#            phType = phType,
#            Charge = Charge,
#            Region = Region,
#            Print  = Print,
#            MVA    = MVA,
#            vetoDY = vetoDY,
#          )


##############################
for d in data[:-1]:
    d.AddCuts(np.array(d.df.nPU) > 0)    
print(np.sum(d.cuts))
if 'Sieip' in LoadVars or 'Sipip' in LoadVars:
    for d in data:
        d.AddCuts(np.array(d.df.photonOneSieip) < 0.15)     
        d.AddCuts(np.array(d.df.photonOneSipip) < 0.15)    
if 'Hover' in LoadVars:
    for d in data:
        d.AddCuts(np.array(d.df.photonOneHover) < 1)     
print(np.sum(d.cuts))        
for d in data:
    d.AddCuts(np.array(d.df.ProbeIDPass)    == True)    
    d.AddCuts(np.array(d.df.ProbeWorstPass) == True)    
###############################

#for d in data:
#    d.AddCuts(np.array(d.df.dileptonPt > 30))
#    d.AddCuts(np.array(d.df.dileptonPt < 30))

#for d in data:
#    d.AddCuts(np.array(d.df.dileptonPt < 18))


#for d in data:
#    d.AddCuts(np.logical_and(np.array(d.df.dileptonM > 75),np.array(d.df.dileptonM < 85)))

#for d in data:
#    d.AddCuts(np.array(d.df.photonOnePt > 30))


# In[29]:


'''
if weightCorrection:
    reWeight = []
    #puWeight = Samples.Helper.PUSF_ratio(xsec1=xsec1,xsec2=xsec2)
    puWeight = SF_ratio(era=era, xsec1=xsec1, xsec2=xsec2)
    for i in range(len(data[:-1])):
        reWeight.append(data[i].weight*puWeight[i])
else:
    reWeight = []
    puWeight = SF_ratio(era=era, xsec1=xsec1, xsec2=xsec2)
    puWeight = [1 for _ in puWeight]
    for i in range(len(data[:-1])):
        reWeight.append(data[i].weight*puWeight[i]) 
'''        


# In[30]:


showershapeVar[:3]


# In[31]:


showershapeVar[3:6]


# In[32]:


showershapeVar[8:10]


# In[33]:


showershapeVar[10:12]


# In[34]:


showershapeVar[12]


# In[37]:


for log in [True,False]:
    ###############################    
    if log:
        stackFol = Fol+'/log'
    else:
        stackFol = Fol+'/linear'
    ###############################
    P = {}


    #var = showershapeVar[3:6]
    #var = ['S4']
    #var = showershapeVar[8:10]
    #var = showershapeVar[10:12]
    #var = showershapeVar[12:14]
    #var = ['Sipip']
    
    #var = ['Sieip','Srr']
    #var = ['R9','Sipip']
    #var = ['Sieie','Hover']
    #var = ['E2x2','E5x5']
    #var = ['ScEtaWidth','ScPhiWidth']
    #var = ['ScRawE', 'PreShowerE']
    #var = ['ScBrem','Rho']
    #var = ['Eta','Phi']
    #var = ['ScRawE']
    #var = ['Sieie']
    
    var = ['R9',
           'HoverE',
          ]
    
    for p in ['_EE','_EB']:
        for v in var:
            
            if v == 'Rho':
                part = p
            else:
                part = 'photonOne'+p
            
            
            print('----------------'+str(v)+'----------------')
            P[v+p] = Plot(
                        data,
                        var              = v,
                        part             = part,
                        signalInclude    = True,
                        stacked          = stacked,
                        density          = density,
                        log              = log,
                        weightCorrection = weightCorrection,
                        Blind            = Blind,
                        Plotting         = Plotting,
                        )


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[38]:


import array
from ROOT import TGraph, TFile, TCanvas,Double,gROOT


# In[43]:


graph = {}

xs = {}

linewidth = 1.7

#fileTrans = TFile(figpath+"trans_ShowerShape.root")
#fileTrans.cd()
for gm in ['EE','EB']:
    for v in var:
        
        if v == 'Srr':
            if gm == 'EB':
                continue
        
        gROOT.Reset()
        
        if v == "Rho":
            VAR = v+'_'+gm
        else:
            VAR = 'photonOne'+v+'_'+gm
            
        #ranges = [0,1]
        if   v == 'R9':
            ranges = [0.85,1]
            bins = 40
        elif v == 'HoverE':
            ranges = [0,0.2]
            bins   = 40
        elif v == 'Sieie':
            if gm == 'EE':
                ranges = [0.015,0.035]
                bins = 40
            else:
                ranges = [0.005,0.015]
                bins = 40            
        elif v == 'Sieip':
            if gm == 'EE':
                ranges = [-0.0004,0.0004]
                bins = 40
            else:
                ranges = [-0.0001,0.0001]
                bins = 40
        elif v == 'Sipip':
            if gm == 'EE':
                ranges = [0.015,0.07]
                bins = 40
            else:
                ranges = [0.01,0.03]
                bins = 40
        elif v == 'Srr':
            if gm == 'EE':
                ranges = [0.01,30]
                bins = 70
        elif v == "S4":
            ranges = [0,1.1]
            bins = 40
        elif v == "ScRawE":
            ranges = [0,700]
            bins = 200
        elif v == "ScEtaWidth":
            ranges = [0,0.05]
            bins   = 30
        elif v == "ScPhiWidth":
            ranges = [0,0.15]
            bins   = 30
        elif v == "PreShowerE":
            ranges = [0.01,50]
            bins = 80
        elif v == "Rho":
            if gm == "EB":
                ranges = [0,60]
                bins   = 50
            else:
                ranges = [0,60]
                bins   = 50
        elif v == "ScBrem":
            if gm == "EB":
                ranges = [0,30]
                bins   = 30
            else:
                ranges = [0,15]
                bins   = 15
        elif v == "Eta":
            ranges = [-3,3]
            bins   = 50
        elif v == "Phi":
            ranges = [-3.6,3.6]
            bins   = 50
        print(VAR)
        
        fileTrans = TFile(figpath+"trans_ShowerShape_"+v+"_"+gm+".root","recreate")
        fileTrans.cd()
        
        c1 = TCanvas(VAR,VAR,200,20,700,500)
        c1.SetFillColor(0)
        c1.SetGrid()

        
        singleElec = np.sort(data[-1].GetWithCuts(VAR))
        singleElec = singleElec[:-np.sum(np.isnan(singleElec))]

        dyjets  = np.sort(data[0].GetWithCuts(VAR))
        dyjets  = dyjets[:-np.sum(np.isnan(dyjets))]
        

        if v == 'Sieip':
            singleElec = singleElec[singleElec < 1]
        
        
        x, y  = array.array('d'), array.array('d')
        hx,hxCorr = [],[]
        
        Nmc   = len(dyjets)
        Ndata = len(singleElec)
        N = 1000
        
        for i in np.arange(0,N):
            Aveg_Data = np.mean(singleElec[i*int(Ndata/N):(i+1)*int(Ndata/N)])
            Aveg_MC   = np.mean(dyjets    [i*int(Nmc  /N):(i+1)*int(Nmc  /N)])

            hx    .append(Aveg_Data)
            hxCorr.append(Aveg_MC  )
            
            if not np.isnan(Aveg_MC) and not np.isnan(Aveg_Data):
                x.append(Aveg_MC)
                y.append(Aveg_Data)

        xs[v+'_'+gm] = hx
        
        graph[VAR] = TGraph(N, x, y)

        graph[VAR].SetLineColor( 2 )
        graph[VAR].SetLineWidth( 0 )
        graph[VAR].SetMarkerColor( 4 )
        graph[VAR].SetMarkerStyle( 21 )
        graph[VAR].SetTitle(VAR)
        graph[VAR].GetXaxis().SetTitle( 'MC' )
        graph[VAR].GetYaxis().SetTitle( 'Data' )
        graph[VAR].Draw("AP")
        c1.Update()

        graph[VAR].Write('trans_'+v+'_'+gm)
        fileTrans.Write()


        xb = np.arange(min(hxCorr),max(hxCorr),step = (max(hxCorr)-min(hxCorr))/100)

        '''
        plt.figure(figsize=(10,10))
        plt.plot(xb,      h,color = 'b',linestyle = '-',label = 'MC corr')
        plt.plot(xb,P[v][1],color = 'k',marker = 'x',linewidth =0, label = 'data')
        plt.legend()
        ax = plt.gca()
        xlim = ax.get_xlim()
        ax.xaxis.set_ticks(np.arange(xlim[0],xlim[1],step=((xlim[1]-xlim[0])/10)))
        ax.grid(linestyle='--')
        ''';

        fig = plt.figure(figsize=(10,10))
        plt.plot(xb, xb,color = 'r',linestyle = '-',linewidth=linewidth)
        
        xCorr = [graph[VAR].Eval(xi) for xi in xb]
        #plt.plot(hx, hxCorr,color = 'b',marker = 'x',linewidth = 0,)
        plt.plot(xb, xCorr,color = 'b',linewidth=linewidth)
        
        plt.title('MC')
        plt.xlabel(v+'_'+gm)
        plt.ylabel('Data ')
        

        ax = plt.gca()
        if gm == 'EE':      
            #xlim = [0.013,0.036]
            xlim = ranges
            ax.set_xlim(xlim)
            ax.set_ylim
            (xlim)
        elif gm == 'EB':
            #xlim = [0.0025,0.015]
            xlim = ranges
            ax.set_xlim(xlim)
            ax.set_ylim(xlim)
        #ax.xaxis.set_ticks(np.arange(xlim[0],xlim[1],step=((xlim[1]-xlim[0])/10)))
        ax.grid(linestyle='--')
        fig.savefig(figpath+VAR+'_Corr.png')
        
    fileTrans.Close()


# In[40]:


#np.sum(np.array(xs['Sieip_EB']) > 1)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[44]:


for gm in ['EE','EB']:
    for v in var:
        if v == "Rho":
            VAR = v+'_'+gm
        else:
            VAR = 'photonOne'+v+'_'+gm
        
        for i in np.arange(len(data)):
            data[i].ResetCuts()
        i = 0
        data[i].AddCuts(data[i].df.nPU > 0)


        test = []
        ind = np.logical_not(np.isnan(data[0].GetWithCuts(VAR)))
        ind = np.logical_and(ind,np.logical_not(np.isinf(data[0].GetWithCuts("weight"))))
        for t in data[0].GetWithCuts(VAR)[ind]: 
            test.append(graph[VAR].Eval(t))

        ##############################################################


        #ranges = [0,1]
        if   v == 'R9':
            ranges = [0.85,1]
            bins = 40
        elif v == 'HoverE':
            ranges = [0,0.2]
            bins = 40
        elif v == 'Sieie':
            if gm == 'EE':
                ranges = [0.015,0.035]
                bins = 40
            else:
                ranges = [0.005,0.015]
                bins = 40            
        elif v == 'Sieip':
            if gm == 'EE':
                ranges = [-0.0004,0.0004]
                bins = 40
            else:
                ranges = [-0.0001,0.0001]
                bins = 40
        elif v == 'Sipip':
            if gm == 'EE':
                ranges = [0.015,0.07]
                bins = 40
            else:
                ranges = [0.01,0.03]
                bins = 40
        elif v == 'Srr':
            if gm == 'EE':
                ranges = [0.01,30]
                bins = 70
        elif v == "S4":
            ranges = [0,1.1]
            bins = 40
        elif v == "ScRawE":
            ranges = [0,700]
            bins = 200
        elif v == "ScEtaWidth":
            ranges = [0,0.05]
            bins   = 40
        elif v == "ScPhiWidth":
            ranges = [0,0.15]
            bins   = 40
        elif v == "PreShowerE":
            ranges = [0.01,50]
            bins = 80
        elif v == "Rho":
            if gm == "EB":
                ranges = [0,60]
                bins   = 50
            else:
                ranges = [0,60]
                bins   = 50
        elif v == "ScBrem":
            if gm == "EB":
                ranges = [0,30]
                bins   = 30
            else:
                ranges = [0,15]
                bins   = 15
        elif v == "Eta":
            ranges = [-3,3]
            bins   = 50
        elif v == "Phi":
            ranges = [-3.6,3.6]
            bins   = 50

        print(ranges,bins)
            
        fig = plt.figure(figsize=(10,10))
        histo = np.histogram(
                            data[1].GetWithCuts(VAR),
                            range    = ranges,
                            bins     = bins,
                            )

        plt.plot(
                (histo[1][:-1]+histo[1][1:])/2,histo[0],
                label      = 'data',
                marker     = 'x',
                markersize = 5,
                color      = 'k',
                linewidth  = 0,
                )

        plt.hist(
                test,
                range    = ranges,
                bins     = bins,
                #weights  = np.array(data[0].GetWithCuts("weights"))[ind]*1.08,
                weights  = np.array(data[0].GetWithCuts("weights"))[ind],
                histtype = 'step',
                linewidth = linewidth,
                label    = 'MC corr'
                )

        plt.hist(
                data[0].GetWithCuts(VAR),
                range    = ranges,
                bins     = bins,
                weights  = np.array(data[0].GetWithCuts("weights")),
                histtype = 'step',
                linewidth = linewidth,
                label    = 'MC'
                )
        plt.title(VAR)
        plt.xlabel(v)
        if v == 'HoverE':
            ax = plt.gca()
            ax.set_yscale('log')
        plt.legend()
        plt.grid(linestyle='--')
        plt.show()
        
        fig.savefig(figpath+VAR+'_Distr.png')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




