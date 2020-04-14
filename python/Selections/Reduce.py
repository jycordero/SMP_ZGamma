#!/usr/bin/env python
# coding: utf-8

# In[2]:


import sys
import datetime


# In[3]:


projectdir = "/home/jcordero/CMS/JYCMCMS/SMP_ZG/"
sys.path.append(projectdir+"python")


# In[4]:


from scipy.optimize  import curve_fit, fsolve
from scipy.special   import erf, betainc, gamma

import array
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt 

from ROOT import TFile,TMVA,TH2F, TCanvas,TTree
from root_pandas import read_root


# # My Dependencies

# In[5]:


# My Dependencies
from Config            import Config
from Reader            import Reader
from Samples.Data      import Data
from Plotter.Helper    import Helper
from Plotter.Plotter   import Plotter
from Cuts.Cuts         import Cuts


# In[6]:


def dirStructure(figpath,Print = False):
    date = datetime.datetime.now()
    fileName = str(date.year) + str(date.month) + str(date.day) + "/"
    
    try:
        os.mkdir(figpath+fileName)    
    except:
        if Print:
            print("Directory "+fileName+ " already exist")
        
    try :
        os.mkdir(figpath+fileName+'ShowerShapeMVA/')
    except:
        if Print:
            print("Directory "+fileName+'ShowerShapeMVA/ already exist')
    
    dirSubStructure(figpath + fileName + "Stacked/", Print=Print)
    dirSubStructure(figpath + fileName + "Unstacked/", Print=Print)
    
    dirSubStructure(figpath + fileName + "nJets/", Print=Print)
    for i in range(5):
        dirSubStructure(figpath + fileName + "nJets/Stacked_nJets"+str(i)+"/", Print=Print)
        dirSubStructure(figpath + fileName + "nJets/Unstacked_nJets"+str(i)+"/", Print=Print)
    
    return figpath+fileName  

def dirSubStructure(path,Print):
    try:
        os.mkdir(path)
    except:
        if Print:
            print("Subdirectory for " + path + " already exists or failed.")
    
    try:
        os.mkdir(path+"log")
        os.mkdir(path+"log/Mult")
        os.mkdir(path+"linear")
        os.mkdir(path+"linear/Mult")
    except:
        if Print:
            print("Subdirectory for " + path + " already exists or failed.")


# In[7]:


def setConfiguration(selection,era):
    
    if   era == "2016":
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
            #SampleSet = "V4_phID_isConv"
            #SampleSet = "V4_phID_isConv_MINUIT"
            #SampleSet  = "V5_mediumID"
            #SampleSet  = "V6_lPhoton"
            SampleSet  = "V6_Accept"

            LoadVars = [
                'runNumber','evtNumber',
                'nPV','nPU','Rho', 'met',
                'genWeight','eventWeight','puWeight','triggerWeight','photonIDWeight',"photonIsConvWeight",
                'genPhotonFHPFS','genPhotonIPFS',
                'leptonOnePt','leptonOneEta','leptonOnePhi','leptonOneIso','leptonOneCharge',
                'leptonTwoPt','leptonTwoEta','leptonTwoPhi','leptonTwoIso','leptonTwoCharge',
                'photonOnePt','photonOneEta','photonOnePhi',
                'photonOneR9','photonOneMVA','photonOneERes','photonOneSieie',
                'photonOneHoverE','photonOneIneu','photonOneIph','photonOneIch',
                'photonOneSieip','photonOneSipip','photonOneSrr','photonOneE2x2','photonOneE5x5',
                'photonOneScEtaWidth','photonOneScPhiWidth',
                'photonOneScRawE','photonOnePreShowerE','photonOneScBrem',
                'genPhotonPt',
                'vetoDY','genIsoPass',
                'dileptonPt','dileptonEta','dileptonPhi','dileptonM',
                'llgPt','llgEta','llgPhi','llgM',
                'dileptonDEta','dileptonDPhi','dileptonDR',
                'l1PhotonDEta','l1PhotonDPhi','l1PhotonDR','l1PhotonM','l1PhotonPt',
                'l2PhotonDEta','l2PhotonDPhi','l2PhotonDR','l2PhotonM','l2PhotonPt',
                'dileptonPhotonDEta','dileptonPhotonDPhi','dileptonPhotonDR',
                'nMuons','nElectrons','nPhotons','nJets','nBJets',
                'passElectronVeto',
                ]          
        elif selection == "mumu":
            run = ['B','C','D','E','F']
            DataGen = 'rereco'
            #SampleSet = 'V1'
            #SampleSet = 'V2_puWeight'
            SampleSet = 'V2_puWeight_phID'

            LoadVars = [
                'runNumber','evtNumber',
                'nPV','nPU','Rho', 'met',
                'genWeight','eventWeight','puWeight','triggerWeight','photonIDWeight',"photonIsConvWeight",
                'genPhotonFHPFS','genPhotonIPFS',
                'leptonOnePt','leptonOneEta','leptonOnePhi','leptonOneIso','leptonOneCharge',
                'leptonTwoPt','leptonTwoEta','leptonTwoPhi','leptonTwoIso','leptonTwoCharge',
                'photonOnePt','photonOneEta','photonOnePhi',
                'photonOneR9','photonOneMVA','photonOneERes','photonOneSieie',
                'photonOneHoverE','photonOneIneu','photonOneIph','photonOneIch',
                'photonOneSieip','photonOneSipip','photonOneSrr','photonOneE2x2','photonOneE5x5',
                'photonOneScEtaWidth','photonOneScPhiWidth',
                'photonOneScRawE','photonOnePreShowerE','photonOneScBrem',
                'genPhotonPt',
                'vetoDY','genIsoPass',
                'dileptonPt','dileptonEta','dileptonPhi','dileptonM',
                'llgPt','llgEta','llgPhi','llgM',
                'dileptonDEta','dileptonDPhi','dileptonDR',
                'l1PhotonDEta','l1PhotonDPhi','l1PhotonDR','l1PhotonM','l1PhotonPt',
                'l2PhotonDEta','l2PhotonDPhi','l2PhotonDR','l2PhotonM','l2PhotonPt',
                'dileptonPhotonDEta','dileptonPhotonDPhi','dileptonPhotonDR',
                'nMuons','nElectrons','nPhotons','nJets','nBJets',
                'passElectronVeto',
                ]        
        elif selection == "ee":
            run = ['B','C','D','E','F']
            #run = ['D']
            DataGen = 'rereco'
            #SampleSet = 'EfficiencyCorrection/files_zee/CorrShower'
            SampleSet = 'EfficiencyCorrection/files_zee/V4_phID_isConv'

            LoadVars = [
                        #'runNumber','evtNumber',
                        'nPV',
                        'nPU',

                        #'genWeight',
                        'eventWeight','puWeight',
                        #'triggerWeight','photonIDWeight',
                        'photonOneEta',
                        #'leptonOneCharge','leptonTwoCharge',
                        #'photonOneMVA',
                        #'photonOneERes',

                        ############################# 

                        #'photonOneR9',
                        'photonOneSieie',
                        #'photonOneHoverE',

                        #'photonOneIneu','photonOneIph','photonOneIch',
                        #'photonOneSieip',
                        #'photonOneSipip',
                        #'photonOneSrr',
                        #'photonOneE2x2',
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
    elif era == "2018":
        if selection == "mumug":
            run = ['A','B','C','D']
            DataGen = 'rereco'
            #SampleSet = 'V1_trigBits'
            SampleSet = 'V2_trigBits_pu'

            LoadVars = [
                'runNumber','evtNumber',
                'nPV','nPU','Rho', 'met',
                'genWeight','eventWeight','puWeight','triggerWeight','photonIDWeight',"photonIsConvWeight",
                'genPhotonFHPFS','genPhotonIPFS',
                'leptonOnePt','leptonOneEta','leptonOnePhi','leptonOneIso','leptonOneCharge',
                'leptonTwoPt','leptonTwoEta','leptonTwoPhi','leptonTwoIso','leptonTwoCharge',
                'photonOnePt','photonOneEta','photonOnePhi',
                'photonOneR9','photonOneMVA','photonOneERes','photonOneSieie',
                'photonOneHoverE','photonOneIneu','photonOneIph','photonOneIch',
                'photonOneSieip','photonOneSipip','photonOneSrr','photonOneE2x2','photonOneE5x5',
                'photonOneScEtaWidth','photonOneScPhiWidth',
                'photonOneScRawE','photonOnePreShowerE','photonOneScBrem',
                'genPhotonPt',
                'vetoDY','genIsoPass',
                'dileptonPt','dileptonEta','dileptonPhi','dileptonM',
                'llgPt','llgEta','llgPhi','llgM',
                'dileptonDEta','dileptonDPhi','dileptonDR',
                'l1PhotonDEta','l1PhotonDPhi','l1PhotonDR','l1PhotonM','l1PhotonPt',
                'l2PhotonDEta','l2PhotonDPhi','l2PhotonDR','l2PhotonM','l2PhotonPt',
                'dileptonPhotonDEta','dileptonPhotonDPhi','dileptonPhotonDR',
                'nMuons','nElectrons','nPhotons','nJets','nBJets',
                'passElectronVeto',
                ] 
        elif selection == "elelg":
            run = ['A','B','C','D']
            DataGen = 'rereco'
            SampleSet = 'V1_trigBits'

            LoadVars = [
                'runNumber','evtNumber',
                'nPV','nPU','Rho', 'met',
                'genWeight','eventWeight','puWeight','triggerWeight','photonIDWeight',"photonIsConvWeight",
                'genPhotonFHPFS','genPhotonIPFS',
                'leptonOnePt','leptonOneEta','leptonOnePhi','leptonOneIso','leptonOneCharge',
                'leptonTwoPt','leptonTwoEta','leptonTwoPhi','leptonTwoIso','leptonTwoCharge',
                'photonOnePt','photonOneEta','photonOnePhi',
                'photonOneR9','photonOneMVA','photonOneERes','photonOneSieie',
                'photonOneHoverE','photonOneIneu','photonOneIph','photonOneIch',
                'photonOneSieip','photonOneSipip','photonOneSrr','photonOneE2x2','photonOneE5x5',
                'photonOneScEtaWidth','photonOneScPhiWidth',
                'photonOneScRawE','photonOnePreShowerE','photonOneScBrem',
                'genPhotonPt',
                'vetoDY','genIsoPass',
                'dileptonPt','dileptonEta','dileptonPhi','dileptonM',
                'llgPt','llgEta','llgPhi','llgM',
                'dileptonDEta','dileptonDPhi','dileptonDR',
                'l1PhotonDEta','l1PhotonDPhi','l1PhotonDR','l1PhotonM','l1PhotonPt',
                'l2PhotonDEta','l2PhotonDPhi','l2PhotonDR','l2PhotonM','l2PhotonPt',
                'dileptonPhotonDEta','dileptonPhotonDPhi','dileptonPhotonDR',
                'nMuons','nElectrons','nPhotons','nJets','nBJets',
                'passElectronVeto',
                ]          
        elif selection == "mumu":
            run = ['A','B','C','D']
            DataGen = 'rereco'
            SampleSet = 'V1_trigBits'

            LoadVars = [
                'runNumber','evtNumber',
                'nPV','nPU','Rho', 'met',
                'genWeight','eventWeight','puWeight','triggerWeight','photonIDWeight',"photonIsConvWeight",
                'genPhotonFHPFS','genPhotonIPFS',
                'leptonOnePt','leptonOneEta','leptonOnePhi','leptonOneIso','leptonOneCharge',
                'leptonTwoPt','leptonTwoEta','leptonTwoPhi','leptonTwoIso','leptonTwoCharge',
                'photonOnePt','photonOneEta','photonOnePhi',
                'photonOneR9','photonOneMVA','photonOneERes','photonOneSieie',
                'photonOneHoverE','photonOneIneu','photonOneIph','photonOneIch',
                'photonOneSieip','photonOneSipip','photonOneSrr','photonOneE2x2','photonOneE5x5',
                'photonOneScEtaWidth','photonOneScPhiWidth',
                'photonOneScRawE','photonOnePreShowerE','photonOneScBrem',
                'genPhotonPt',
                'vetoDY','genIsoPass',
                'dileptonPt','dileptonEta','dileptonPhi','dileptonM',
                'llgPt','llgEta','llgPhi','llgM',
                'dileptonDEta','dileptonDPhi','dileptonDR',
                'l1PhotonDEta','l1PhotonDPhi','l1PhotonDR','l1PhotonM','l1PhotonPt',
                'l2PhotonDEta','l2PhotonDPhi','l2PhotonDR','l2PhotonM','l2PhotonPt',
                'dileptonPhotonDEta','dileptonPhotonDPhi','dileptonPhotonDR',
                'nMuons','nElectrons','nPhotons','nJets','nBJets',
                'passElectronVeto',
                ]        
        elif selection == "ee":
            run = ['A','B','C','D']
            DataGen = 'rereco'
            #SampleSet = 'V1_trigBits'
            #SampleSet = 'EfficiencyCorrection/files_zee/CorrShower'
            SampleSet = 'EfficiencyCorrection/files_zee/V4_phID_isConv'

            LoadVars = [
                        #'runNumber','evtNumber',
                        'nPV',
                        'nPU',

                        #'genWeight',
                        'eventWeight','puWeight',
                        #'triggerWeight','photonIDWeight',
                        'photonOneEta',
                        #'leptonOneCharge','leptonTwoCharge',
                        #'photonOneMVA',
                        #'photonOneERes',

                        ############################# 

                        #'photonOneR9',
                        'photonOneSieie',
                        #'photonOneHoverE',

                        #'photonOneIneu','photonOneIph','photonOneIch',
                        #'photonOneSieip',
                        #'photonOneSipip',
                        #'photonOneSrr',
                        #'photonOneE2x2',
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
    
    pathMVA = "/home/jcordero/CMS/data/data_"+era+"/"+DataGen+"/SMP_ZG/Files/ShowerShapeMVA/"
    path    = "/home/jcordero/CMS/data/data_"+era+"/"+DataGen+"/SMP_ZG/Files/"+selection+"/"+SampleSet+"/"
    figpath = "/home/jcordero/CMS/data/JYCMCMS/SMP_ZG/figs/"+era+"/"+DataGen+"/"+selection+"/"
    pathSelection = "/home/jcordero/CMS/data/data_"+era+"/"+DataGen+"/SMP_ZG/Files/"+selection+"/"+SampleSet+"/Reduced"

    config = Config(
                    projectdir = projectdir,
                    path       = path,
                    era        = era,
                    DataGen    = DataGen,
                    run        = run,
                    selection  = selection,
                    LoadVars   = LoadVars,
                    )
    
    return config, pathMVA, path, figpath, pathSelection


# In[8]:


#selection = 'mumug'
#selection = 'elelg'
selection = 'ee'

#era = "2016"
era = "2017"
#era = "2018"

config, pathMVA, path, figpath, pathSelections = setConfiguration(selection,era)

figpath = dirStructure(figpath)   


Help    = Helper(era)
Help.SetPath(path)
Help.figpath = figpath

Plotter = Plotter()
Plotter.SetFig(Help.figpath)

Cut     = Cuts(path = Help.path)


# In[9]:


Read = Reader(config)


# In[ ]:


data = Read.read( reduce = False )


# In[ ]:





# # Analyser

# In[8]:


################################
#stacked = False
stacked = True

LOG = 'both'
log = False
#log = True

#phType = 'ISR'
#phType = 'FSR'
phType = ''


ShowerShapeCorrection = True
#ShowerShapeCorrection = False

if selection == "mumug" or selection == "elelg":
    lgmDR = True
elif selection == "ee":
    lgmDR = False

################

#Region = ''

#Region = 'A'
#Region = 'B'
#Region = 'C'
#Region = 'D'

#Region = 'Ap'
#Region = 'Bp'
#Region = 'Cp'
#Region = 'Dp'


#Region = 'AB'
#Region = 'CD'

#Region = 'Sig'
#Region = 'Inv Sig'

#Region = 'Sideband'
#Region = 'Compare'


#Region = ['Sig','IPFS']
#Region = ['Sig','noIPFS']
#Region = ['Inv Sig','IPFS']
#Region = ['Inv Sig','noIPFS']

################

Charge = 'oposite'
#Charge = 'same'
#Charge = ''

#customRange = True
customRange = False

weightCorrection = True
#weightCorrection = False

#StatInclude = False
StatInclude = True

MVA = False
#MVA = True

vetoDY = True
#vetoDY = False

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

######## CUTS ##############
Cut.PhaseSpace(
                data,
                phType = phType,
                Charge = Charge,
                Region = Region,
                Print  = Print,
                vetoDY = vetoDY,
                lgmDR  = lgmDR,
                MVA    = MVA,
              )

for d in data[:-1]:
    if not d.df.empty:
        d.AddCuts(np.array(d.df.nPU) > 0) 
        
#for d in data[:-1]:
#    if not d.df.empty:
#        d.AddCuts(np.array(d.df.photonOnePt) > 100)
###############################


# In[ ]:





# # ShowerShape

# In[9]:


from Corrections.ShowerShape import ShowerShape


# In[10]:


SS = ShowerShape(config)
SS.loadToGraph()


# In[11]:


inMVA = SS.SSCorrected(data)


# # BDT READ

# In[12]:


from Corrections.MVA import MVA


# In[13]:


MVA = MVA(config,SS.mva_to_ntuple)


# In[14]:


MVA.loadMVA()


# In[15]:


MVA.readMVA(data, inMVA)


# # Saving to Reduced CSV

# In[ ]:



##################################################
if type(Region) is not list and type(Region) is not np.ndarray:
    labelRegion = Region.replace(" ","")
else:
    labelRegion = ''
    for r in Region:
        labelRegion += r.replace(" ","")
##################################################

for d in data:
    print("---------"+d.name+"-----------")
    df = pd.DataFrame({name:d.GetWithCuts(name) for name in data[0].df.keys()})

    variable = 'weights'
    df[variable] = d.GetWithCuts(variable)

    df["ShowerShapeMVA_EE"] = MVA.BDT['EE'][d.name]
    df["ShowerShapeMVA_EB"] = MVA.BDT['EB'][d.name]

    df.to_csv(pathSelections+'/'+d.name+'_'+labelRegion+'.csv')


# # ------------- PLOTS

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


bins  = np.arange(-1,1.1,step=0.1)

bdt = {}
for phType in ['EB','EE']:
    bdt[phType] = []
    
    Cut.PhaseSpace(
                data,
                phType = '',
                Charge = Charge,
                Region = 'Sig',
                Print  = Print,
                MVA    = MVA,
              ) 
    
    for d,i in zip(data,range(len(data))):
        if not d.df.empty and d.name != 'DoubleMuon_2017':
            d.AddCuts(np.array(d.df.nPU) > 0)
        
        if phType == 'EB':
            Ind = np.abs(d.GetWithCuts('photonOneEta') < 1.4442)
        else:
            Ind = np.logical_and(np.abs(d.GetWithCuts('photonOneEta')) > 1.5666,
                                 np.abs(d.GetWithCuts('photonOneEta')) <= 2.5
                                )

        
        if len(BDT[phType][d.name]) != 0:
            bdtH,x = np.histogram(np.array(BDT[phType][d.name])[Ind],
                                 bins    = bins,
                                 weights = data[i].GetWithCuts('weights')[Ind]
                                )
        else:
            bdtH = np.zeros(len(bins)-1)
        bdt[phType].append(bdtH)


# In[ ]:


Name = [d.name for d in data]


# In[ ]:


for log in [True,False]:
    for phType in ['EB','EE']:
        Plotter.Plot_Bin(
                         VAR = bdt[phType], wei=bdt,
                         label = Name, colors = colors,
                         ranges           = [-1,1], 
                         bins             = bins,
                         var              = 'ShowerShapeMVA',
                         part             =  '',
                         signalInclude    = True,
                         stacked          = True,
                         density          = False,
                         log              = log,
                         Plotting         = True,
                         Blind            = True,
                         StatInclude      = False,
                         index            = phType,
                        );


# # -----------------------------------------------------

# # Openning file test 

# In[ ]:


if type(Region) is not list or type(Region) is not np.nbarray:
    labelRegion = Region.replace(" ","")
else:
    labelRegion = ''
    for r in Region:
        labelRegion += r.replace(" ","")

reduced = []
for d in data:
    print('-----'+d.name+'--------')
    reduced.append(pd.read_csv(pathSelections+'/'+d.name+'_'+labelRegion+'.csv'))


# # -----------------------------------------------------
