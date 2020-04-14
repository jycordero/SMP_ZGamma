#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import datetime
import os
import importlib


# In[2]:


projectdir = "/home/jcordero/CMS/JYCMCMS/SMP_ZG/"
sys.path.append(projectdir + "python")


# In[3]:


from ROOT import TFile,TTree,TH2F,gROOT,gStyle,TCanvas
from root_pandas import read_root 

import array
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import scipy.stats   as stat
from scipy.optimize import curve_fit
from scipy.optimize import minimize


# In[4]:


from iminuit import Minuit
from pprint import pprint


# # My Dependencies

# In[5]:


from Config import Config
from Reader import Reader
from Samples.Data import Data
from Samples.DataStack import DataStack
from Samples.DataStack import DataStackTest
import Efficiency.Efficiency as Efficiency
from Plotter.Plotter import Plotter
from Common.CommonHelper import CommonHelper


# In[ ]:





# # Functions

# In[6]:


def setConfiguration(selection,era):
    
    if   era == "2016":
        #run = ['B','C','D','E','F','G','H']    
        run = ['C','D','E','F','G','H']    
        DataGen = 'legacy'
        #path = "/home/jcordero/CMS/data/data_"+era+"/"+DataGen+"/SMP_ZG/Files/ee/"+SampleSet+"/DYJets/"
        if selection == "mumug":
            SampleSet = "MatchZGpaper/"
        elif selection == "elelg":
            SampleSet = "MatchZGpaper/"
        elif selection == "ee":
            SampleSet = "/EfficiencyCorrection/files_zee/TagProbe_noTrig/"
    elif era == "2017":
        run = ['B','C','D','E','F']
        #run = ['D']
        DataGen = 'rereco'
        #SampleSet = 'EfficiencyCorrection/files_zee/CorrShower'
        if selection == "mumug":
            #SampleSet = 'V1'
            #SampleSet = 'V2_puWeight'
            #SampleSet = 'V2_puWeight_phID'
            #SampleSet = "V4_phID_isConv"
            #SampleSet = "V4_phID_isConv_MINUIT"
            #SampleSet  = "V5_mediumID"
            #SampleSet  = "V6_lPhoton"
            SampleSet  = "V6_Accept/"  
        elif selection == "elelg":
            #SampleSet = 'V1'
            #SampleSet = 'V2_puWeight'
            #SampleSet = 'V2_puWeight_phID'
            #SampleSet = "V4_phID_isConv"
            #SampleSet = "V4_phID_isConv_MINUIT"
            #SampleSet  = "V5_mediumID"
            #SampleSet  = "V6_lPhoton"
            SampleSet  = "V6_Accept/"   
        elif selection == "mumu":
            #SampleSet = 'V1'
            #SampleSet = 'V2_puWeight'
            SampleSet = 'V2_puWeight_phID/'
        elif selection == "ee":
            SampleSet = 'EfficiencyCorrection/files_zee/V4_phID_isConv/'
    elif era == "2018":
        run = ['A','B','C','D']
        DataGen = 'rereco'
        if selection == "mumug":
            #SampleSet = 'V1_trigBits'
            SampleSet = 'V2_trigBits_pu/'
        elif selection == "elelg":
            SampleSet = 'V2_trigBits_pu/'
        elif selection == "mumu":
            SampleSet = 'V2_trigBits_pu/'
        elif selection == "ee":
            SampleSet = 'EfficiencyCorrection/files_zee/V2_trigBits_pu/'

    path = "/home/jcordero/CMS/data/data_"+era+"/"+DataGen+"/SMP_ZG/Files/"+selection+"/"+SampleSet
    
    pathMVA = "/home/jcordero/CMS/data/data_"+era+"/"+DataGen+"/SMP_ZG/Files/ShowerShapeMVA/"
    #path    = "/home/jcordero/CMS/data/data_"+era+"/"+DataGen+"/SMP_ZG/Files/"+selection+"/"+SampleSet+"/"
    figpath = "/home/jcordero/CMS/JYCMCMS/SMP_ZG/figs/"+era+"/"+DataGen+"/"+selection+"/"
    pathSelection = "/home/jcordero/CMS/data/data_"+era+"/"+DataGen+"/SMP_ZG/Files/"+selection+"/"+SampleSet+"Reduced"

    '''
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
    ''';
    
    ## REDUCED
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


# # FIT

# In[7]:


def GoodGuess(i,j,Ni,Nj,tries,p0):
    if   len(p0) == 4:
        ####################################
        if i == 2 or i == 7:
            return False
        else:
            p0 = [np.random.rand()*1e6,   np.random.rand()*1e4, np.random.rand()*1e5,   np.random.rand()*1e4]

        ####################################
        if j == Nj-1 or j == Nj-2:
            #p0 = [1e5,   1e3, 1e5,   1e3]
            #p0 = [1e6,   1e6, 1e6,   1e6]
            p0 = [1e2,   2e2, 1e2,   2e2]
        else:
            p0 = [np.random.rand()*1e4,   np.random.rand()*1e3, np.random.rand()*1e3,   np.random.rand()*1e3]
        ####################################
        if tries == 100:
            print('Reach Maximum tries')
            return False
    elif len(p0) == 12:
        ####################################
        if i == 2 or i == 7:
            return False
        else:
            p0 = [
                np.random.rand()*1e6,   np.random.rand()*1e4, np.random.rand()*1e5,   np.random.rand()*1e4,
                np.random.rand()*60, np.random.rand()*10, np.random.rand()*200,   np.random.rand()*10,
                np.random.rand()*60, np.random.rand()*10, np.random.rand()*200,  np.random.rand()*10
                ]

        ####################################
        if j == Nj-1 or j == Nj-2:
            p0 = [
                    #1e5,   1e5, 1e5,   1e5,
                    1e2,   2e2, 1e2,   2e2,
                    1, -0.1, 1, 0.1,
                    1, -0.1, 1, 0.1
                    ]
        else:
            p0 = [
                np.random.rand()*1e4,   np.random.rand()*1e3, np.random.rand()*1e3,   np.random.rand()*1e3,
                np.random.rand()*60, -np.random.rand()*10, np.random.rand()*200,   np.random.rand()*10,
                np.random.rand()*60, -np.random.rand()*10, np.random.rand()*200,   np.random.rand()*10
                ]
        ####################################
        if tries == 1000:
            print('Reach Maximum tries')
            return False
    elif len(p0) == 14:
        ####################################
        if i == 2 or i == 7:
            return False
        else:
            p0 = [
                np.random.rand()*1e6,   np.random.rand()*1e4, np.random.rand()*1e5,   np.random.rand()*1e4,
                np.random.rand()*3, np.random.rand()*3, np.random.rand()*120,
                np.random.rand()*0.05, np.random.rand()*3,
                np.random.rand()*3, np.random.rand()*3, np.random.rand()*120,
                np.random.rand()*0.05, np.random.rand()*3,
                ]

        ####################################
        if j == Nj-1 or j == Nj-2:
            p0 = [
                5e3,   13e3, 5,   13,
                2, 2, 87,
                0.03, 0,
                2, 2, 87,
                0.03, 0,
                ]
        else:
            p0 = [
                np.random.rand()*1e6,   np.random.rand()*1e4, np.random.rand()*1e5,   np.random.rand()*1e4,
                np.random.rand()*3, np.random.rand()*3, np.random.rand()*120,
                np.random.rand()*0.05, np.random.rand()*3,
                np.random.rand()*3, np.random.rand()*3, np.random.rand()*120,
                np.random.rand()*0.05, np.random.rand()*3,
                ]
    elif len(p0) == 18:
        if i == 2 or i == 7:
            return False
        else:
            p0 = [
                np.random.rand()*1e6,   np.random.rand()*1e4, np.random.rand()*1e5,   np.random.rand()*1e4,
                # Pass
                np.random.rand()*2,   np.random.rand()*2, np.random.rand()*30,
                np.random.rand()*1e5, np.random.rand()*1e5, np.random.rand()*200,   np.random.rand()*10,
                #Fail
                np.random.rand()*2,   np.random.rand()*2, np.random.rand()*60,
                np.random.rand()*1e5, np.random.rand()*1e5, np.random.rand()*200,  np.random.rand()*10
                ]
        ###########################
        if j == Nj-1 or j == Nj-2:
            p0 = [
                    2e4,   5e3, 1e4,   1e3,
                    #Pass
                    1, 1, 20,
                    1, -2, 100,   -0.03,
                    # Fail
                    1, 1, 50,
                    1e2, 1e2, 100,   -0.03,
                    ]
        else:
            p0 = [
                np.random.rand()*1e6,   np.random.rand()*1e4, np.random.rand()*1e5,   np.random.rand()*1e4,
                # Pass
                np.random.rand()*2,   np.random.rand()*2, np.random.rand()*30,
                np.random.rand()*1e5, np.random.rand()*1e5, np.random.rand()*200,   np.random.rand()*10,
                #Fail
                np.random.rand()*2,   np.random.rand()*2, np.random.rand()*60,
                np.random.rand()*1e5, np.random.rand()*1e5, np.random.rand()*200,  np.random.rand()*10
                ]          

    return p0


# # Main Functionality

# In[8]:


def Plot(ax,
         Var,
         ranges, bins, color,
         DataMC='mc',
         tempType='KDE'
        ):
    
        
        if type(bins) is np.ndarray or type(bins) is list:
            hist = np.histogram(
                                Var,
                                range    = ranges,
                                bins     = bins,
                                )
            hist = ax.hist(
                            bins[:-1],
                            histtype = 'step',
                            range    = ranges,
                            weights  = hist[0]/np.diff(bins),
                            bins     = bins,
                            color    = color,
                            label    = 'HIST', 
                            )
        else:
            hist = ax.hist(
                            Var,
                            histtype = 'step',
                            range    = ranges,
                            bins     = bins,
                            color    = color,
                            label    = 'HIST', 
                            #density  = True,
                            )
        
        xc = (hist[1][:-1]+hist[1][1:])/2
        hist[0][np.isnan(hist[0])] = 0
        
        #######
        if   tempType == 'KDE':
            try:
                kde       = stat.gaussian_kde(dataset = Var)    
                template  = kde(xc)
                ratio     = np.sum(template)/np.sum(hist[0])
            except:
                template = xc*0
                ratio    = 1
        elif tempType == 'HIST':
                template = hist[0]
                ratio    = 1
            
        
        ax.plot(xc,template/ratio,'k--',label = 'KDE')
        ax.grid(linestyle = '--')
        ax.legend()
        
        return template, ratio


# In[9]:


def EffGrid(sample,
            part         = 'dilepton',
            variable     = 'M',
            DataMC       = 'mc',
            samples      = '',
            ProbeType    = 'Pass',
            IDPass       = True,
            ptBins       = array.array("f",[0,20,35,50,90,150,500]), 
            etaBins      = array.array("f",[-2.5,-2,-1.566,-1.4442,-1.0,0,1.0,1.4442,1.566,2,2.5]),
            Abs          = False, 
            isConv       = False,
            ranges       = [60,120],
            bins         =  60, # Should be ranges[1]-ranges[0]
            tempType     = 'KDE',
            BinEBEE      = None,
           ):
    #### Array Outputs
    template,ratios = {},{}
    
    ### Eta Bin formating
    etaBinsEBEE    = [[0,1.4442],[1.566,2.5]]
    etaBins,ptBins = BinFormat(etaBins), BinFormat(ptBins)
    etaNBin,ptNBin = len(etaBins),len(ptBins)

    ### Ploting variable
    if ProbeType == "Pass":
        color = 'C0'
    else:
        color = 'C1' 
    
    figx, figy = etaNBin, ptNBin

    fig = plt.figure(figsize=(figy*3,figx*4))
    for j in np.arange(ptNBin):
        if j in BinEBEE:
            etaBINS = etaBinsEBEE
        else:
            etaBINS = etaBins

        template[j],ratios[j] = {},{}
        for i in np.arange(len(etaBINS)):                 
            VAL = sample[part+variable]
            if IDPass:
                if ProbeType == "Pass":
                    Ind = sample["ProbeIDPass"] == True
                    Ind = np.logical_and(Ind,sample["ProbeISOPass"]   == True)
                    Ind = np.logical_and(Ind,sample["ProbeWorstPass"] == True)
                    Ind = np.logical_and(Ind,sample["ProbeSigPass"]   == True)
                    if isConv:
                        Ind = np.logical_and(Ind,sample["ProbeIsConv"]    == True)
                    
                else:
                    if isConv:
                        Ind = sample["ProbeIDPass"] == True
                        Ind = np.logical_and(Ind,sample["ProbeISOPass"]   == True)
                        Ind = np.logical_and(Ind,sample["ProbeWorstPass"] == True)
                        Ind = np.logical_and(Ind,sample["ProbeSigPass"]   == True)

                        Ind = np.logical_and(Ind,sample["ProbeIsConv"]    == False)
                    else:
                        Ind = sample["ProbeIDPass"] == False
                        Ind = np.logical_or(Ind,sample["ProbeISOPass"]   == False)
                        Ind = np.logical_or(Ind,sample["ProbeWorstPass"] == False)
                        Ind = np.logical_or(Ind,sample["ProbeSigPass"]   == False)


            else:
                if ProbeType == "Pass":
                    Ind = sample["ProbeIDPass"] == True
                else:
                    Ind = sample["ProbeIDPass"] == False    
            
            
            Var = np.array(VAL[Ind])
            Pt  = sample['leptonTwoPt'][Ind]
            Eta = sample['leptonTwoEta'][Ind]

            ptInd  = BinIndex(Pt , ptBins [j][0], ptBins [j][1], Abs = Abs)
            etaInd = BinIndex(Eta, etaBINS[i][0], etaBINS[i][1], Abs = Abs)
            Ind    = np.logical_and(ptInd,etaInd)


            ij = ptNBin*i + (j+1)     
            plt.subplot(etaNBin, ptNBin, ij)
            ax = plt.gca()

            TEMP, RATIO = Plot(
                                ax       = ax,
                                Var      = Var[Ind],
                                ranges   = ranges,
                                bins     = bins,
                                color    = color,
                                DataMC   = DataMC,
                                tempType = tempType,
                                )
                    
            template[j][i] = TEMP
            ratios[j][i]   = RATIO
            
        

            if j == 0:
                ax.set_ylabel('Eta ['+str(round(etaBINS[i][0],2))+','+str(round(etaBINS[i][1],2))+']'  )        
            if i == 0:
                ax.set_title('Pt ['+str(ptBins[j][0])+','+str(ptBins[j][1])+']' )
                
    

    
    plt.tight_layout()
    plt.show()
    #fig.savefig('/home/jcordero/CMS/MEH/zee/'+'zee_'+DataMC+'/'+samples+'_'+ProbeType+'_PeakMap.png')
    if isConv:
        fig.savefig(figpath+DataMC+samples+'_'+ProbeType+'_PeakMap_isConv.png')
    else:
        fig.savefig(figpath+DataMC+samples+'_'+ProbeType+'_PeakMap.png')
    
    return template,ratios


# In[10]:


def EffMC(
            sample,
            part      = 'dilepton',
            variable  = 'M',
            ptBins    = array.array("f",[0,20,35,50,90,150,500]), 
            etaBins   = array.array("f",[-2.5,-2,-1.566,-1.4442,-1.0,0,1.0,1.4442,1.566,2,2.5]),
            Abs       = False, 
            isConv    = False,
            ranges    = [60,120],
            bins      =  60, # Should be ranges[1]-ranges[0]
            BinEBEE   = None,
            ProbeType = 'Pass',
            ):
    #### Array Outputs
    Yield = {}
    
    ### Eta Bin formating
    etaBinsEBEE    = [[0,1.4442],[1.566,2.5]]
    etaBins,ptBins = BinFormat(etaBins), BinFormat(ptBins)
    etaNBin,ptNBin = len(etaBins),len(ptBins)
    
    for j in np.arange(ptNBin):
        Yield[j] = {}
        if j in BinEBEE:
            etaBINS = etaBinsEBEE
        else:
            etaBINS = etaBins

        #template[j],ratios[j] = {},{}
        for i in np.arange(len(etaBINS)):                 
            VAL = sample[part+variable]
            if ProbeType == "Pass":
                Ind = sample["ProbeIDPass"] == True
                Ind = np.logical_and(Ind,sample["ProbeISOPass"]   == True)
                Ind = np.logical_and(Ind,sample["ProbeWorstPass"] == True)
                Ind = np.logical_and(Ind,sample["ProbeSigPass"]   == True)
                if isConv:
                    Ind = np.logical_and(Ind,sample["ProbeIsConv"]   == True)
            else:
                if isConv:
                    Ind = sample["ProbeIDPass"] == True
                    Ind = np.logical_and(Ind,sample["ProbeISOPass"]   == True)
                    Ind = np.logical_and(Ind,sample["ProbeWorstPass"] == True)
                    Ind = np.logical_and(Ind,sample["ProbeSigPass"]   == True)
                
                    Ind = np.logical_and(Ind,sample["ProbeIsConv"] == False)
                else:
                    Ind = sample["ProbeIDPass"] == False
                    Ind = np.logical_or(Ind,sample["ProbeISOPass"]   == False)
                    Ind = np.logical_or(Ind,sample["ProbeWorstPass"] == False)
                    Ind = np.logical_or(Ind,sample["ProbeSigPass"]   == False)
                
        
            
            
            Var = np.array(VAL[Ind])
            Pt  = sample['leptonTwoPt'][Ind]
            Eta = sample['leptonTwoEta'][Ind]

            ptInd  = BinIndex(Pt , ptBins [j][0], ptBins [j][1],Abs=Abs)
            etaInd = BinIndex(Eta, etaBINS[i][0], etaBINS[i][1],Abs=Abs)
            Ind    = np.logical_and(ptInd,etaInd)
            
            Yield[j][i] = np.sum(Ind)
            
    return Yield


# In[ ]:





# # Extract Data

# In[11]:


#era = "2016"
era = "2017"
#era = "2018"

selection = "ee"
#selection = "mumug"
#selection = "elelg"

config, pathMVA, path, figpath, pathSelections = setConfiguration(selection,era)

config.LoadVars = [
                    "genWeight","eventWeight",
                    "dileptonM",
                   "leptonOnePt","leptonOneEta",
                   "leptonTwoPt","leptonTwoEta",
                   "vetoDY","genIsoPass",
                   "ProbeIDPass","ProbeISOPass","ProbeWorstPass","ProbeSigPass","ProbeIsConv"
                   #"ProbePass",
                   #"TagFromZ","ProbeFromZ",
                  ]
#config.run = ["B"]

Help   = CommonHelper
Read   = Reader(Config = config, Print = False)
Plot   = Plotter(Config = config)
EffAna = Efficiency.Efficiency(Config = config)


# In[ ]:





# In[12]:


Plot.Test()


# In[13]:


data = Read.read()
dataS = DataStack(data)


# In[ ]:





# In[ ]:





# # Extract MC

# In[14]:


#################
binsSelected = "Plots"
#binsSelected = "Optimized"
#binsSelected = "Hien"

EffAna.loadBins(Type = "BinSet1")
print(EffAna)


# In[15]:


#################
S = "DYJets"
#S = "WJets"
sample = dataS[S]    


# In[16]:



tempType = 'HIST'
#tempType = 'KDE'

#Abs = True
Abs = False

#isConv = True
isConv = False

ptBins = EffAna.bins["pt"]
etaBins = EffAna.bins["etaAbs"]

ptBins = Help.Plot.BinFormat(ptBins)
etaBins = Help.Plot.BinFormat(etaBins)

etaBinsEBEE    = [[0,1.4442],[1.566,2.5]]
#################
BinEBEE = [len(ptBins)-1]
#################

normalBin = True
#normalBin = False

ranges = [60,120]
if normalBin:
    bins   = int((ranges[1] - ranges[0] )/2)
    step = (ranges[-1]-ranges[0])/float(bins)
    bins = [ranges[0]+step*i for i in range(bins)]
else:
    bins = [60,65,70,75,80,82,84,86,87,88,89,90,91,92,93,94,96,98,100,105,110,115,120]
weight = np.diff(bins)
binMult = 2
xc = (np.array(bins[:-1])+np.array(bins[1:]))/binMult
x = xc




    


# In[ ]:





# In[ ]:





# In[17]:


part = "dilepton"
var  = "M"


ProbeType = "Pass"
#ProbeType = "Fail"
VAR = part+var

filters = ["ProbeIDPass","ProbeISOPass","ProbeWorstPass","ProbeSigPass"]
if ProbeType == "Pass":
    Ind = EffAna.getIndex(dataS[S], filters = filters, flag = True)
else:
    Ind = EffAna.getIndex(dataS[S], filters = filters, flag = False)

###############################
Pass = np.histogram(
                np.array(dataS[S][VAR][Ind]),
                range    = ranges,
                bins     = bins,
                )

plt.figure()
plt.hist(
        bins[:-1],
        weights = Pass[0]/weight,
        range    = ranges,
        bins  = bins,
        histtype = 'step',
        color    = 'C0',
        )
plt.grid(linestyle = '--')
plt.ylabel(r'Events')
plt.xlabel(part+var)
plt.title('Probe '+ProbeType  )
plt.show()
###############################

#ProbeType = "Pass"
ProbeType = "Fail"
VAR = part+var
if ProbeType == "Pass":
    Ind = EffAna.getIndex(dataS[S], filters = filters, flag = True)
    if isConv:
        Ind = np.logical_and(Ind,sample["ProbeIsConv"] == True)
else:
    Ind = EffAna.getIndex(dataS[S], filters = filters, flag = False)
    if isConv:
        Ind = np.logical_or(Ind,sample["ProbeIsConv"] == False)
    
Fail = np.histogram(
                np.array(dataS[S][VAR][Ind]),
                range    = ranges,
                bins     = bins,
                )
plt.figure()
plt.hist(
        bins[:-1],
        weights  = Fail[0]/weight,
        range    = ranges,
        bins     = bins,
        histtype = 'step',
        color    = 'C1',
        )

plt.grid(linestyle = '--')
plt.ylabel(r'Events/1 GeV')
plt.xlabel(part+var)
plt.title('Probe '+ProbeType  )
plt.show()

###############################


# In[ ]:





# In[18]:


Plot.Plot(dataS,
          var = "M", part = "dilepton",
          signalInclude = True, density = False
         );


# # MC EFF

# In[19]:


probe = "leptonTwo"
tag = "leptonOne"

part = "dilepton"
var = "M"

filters = ["ProbeIDPass","ProbeISOPass","ProbeWorstPass","ProbeSigPass"]
for d in dataS:
    print('---',d.name)
    Ind = EffAna.getIndex(d, filters = filters, flag = True)
    d.AddCuts(Ind)
    
PassMC = EffAna.GetYields(
                        dist1 = dataS[S].GetWithCuts(probe+"Pt"),
                        dist2 = dataS[S].GetWithCuts(probe+"Eta"),
                        bins1 = {"pt": EffAna.bins["pt"] },
                        bins2 = {"eta": EffAna.bins["eta"] },
                        )


for d in dataS:
    d.ResetCuts()
    
for d in dataS:
    print('---',d.name)
    Ind = EffAna.getIndex(d, filters = filters, flag = False)
    d.AddCuts(Ind)
    
FailMC = EffAna.GetYields(
                        dist1 = dataS[S].GetWithCuts(probe+"Pt"),
                        dist2 = dataS[S].GetWithCuts(probe+"Eta"),
                        bins1 = {"pt": EffAna.bins["pt"] },
                        bins2 = {"eta": EffAna.bins["eta"] },
                        )


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[21]:


print(
    np.sum(dataS['DYJets'].df["ProbeIsConv"] == True),
    np.sum(dataS['DYJets'].df["ProbeIsConv"] == False),
    np.sum(dataS['DYJets'].df["ProbeIsConv"] == True)/float(np.sum(dataS['DYJets'].df["ProbeIsConv"] == False)+np.sum(dataS['DYJets'].df["ProbeIsConv"] == True)),
    
    )


# In[22]:


effMC,effMCStat = {},{}
for j in  PassMC:
    effMC[j], effMCStat[j] = {},{}
    for i in  PassMC[j]:
        if PassMC[j][i] + FailMC[j][i] != 0:
            effMC[j][i] = float(PassMC[j][i])/(PassMC[j][i] + FailMC[j][i])
            effMCStat[j][i] = effMC[j][i]*np.sqrt(1/float(PassMC[j][i]) + 1/float(PassMC[j][i] + FailMC[j][i]))
        else:
            effMC[j][i] = 0
            effMCStat[j][i] = 0


# In[23]:


EffAna.eff(PassMC,FailMC)


# In[ ]:


if isConv:
    fileOut = TFile(figpath+binsSelected+"/isConv/"+"eff_photon_mc.root","recreate")
else:
    fileOut = TFile(figpath+binsSelected+"/ID/"+"eff_photon_mc.root","recreate")
tree = TTree("eff_photon","eff_photon")

gStyle.SetOptStat(0)
#################################################

ptBins, etaBins = BinFormat(ptBins,Type='edges'),BinFormat(etaBins,Type='edges')

ptNBins,etaNBins = len(ptBins)-2, len(etaBins)-1
histDraw = TH2F("EGamma_eff","Eff",
              ptNBins ,ptBins,
              etaNBins,etaBins)


ptNBins,etaNBins = len(ptBins)-1, len(etaBins)-1
hist2d = TH2F("EGamma_eff","Eff",
              ptNBins ,ptBins,
              etaNBins,etaBins)

ptNBins,etaNBins = len(ptBins)-2, len(etaBins)-1
statDraw = TH2F("EGamma_eff_draw_stat","Eff",
              ptNBins ,ptBins,
              etaNBins,etaBins)


ptNBins,etaNBins = len(ptBins)-1, len(etaBins)-1
stat2d = TH2F("EGamma_eff_stat","Eff",
              ptNBins ,ptBins,
              etaNBins,etaBins)



etaBins = BinFormat(etaBins)
#################################################
tree.Branch("eff",hist2d,"TH2F")


for j in range(ptNBins):
    hist2d.GetZaxis().SetRangeUser(0.6,1.1)
    if j in BinEBEE:
        etaBINS = etaBinsEBEE
    else:
        etaBINS = etaBins
        
    if len(etaBINS) > 2:
        for i in np.arange(len(etaBINS)):
            hist2d.SetBinContent(int(j)+1, int(i)+1, effMC[j][i])
            histDraw.SetBinContent(int(j)+1, int(i)+1, effMC[j][i])
            
            stat2d.SetBinContent(int(j)+1, int(i)+1, effMCStat[j][i])
            statDraw.SetBinContent(int(j)+1, int(i)+1, effMCStat[j][i])
            tree.Fill()
    else:
        for i in range(len(etaBins)):
            if np.abs(np.average(etaBins[i])) > 1.566:
                EFF = effMC[j][0]
                EFFStat = effMCStat[j][0]
            elif np.abs(np.average(etaBins[i])) < 1.4442:
                EFF = effMC[j][1]
                EFFStat = effMCStat[j][1]
                I = 2
            else:
                EFF = 0
                EFFStat = 0
            #print(j,i,I,eff[j][I])
            hist2d.SetBinContent(int(j)+1, int(i)+1, EFF)
            histDraw.SetBinContent(int(j)+1, int(i)+1, EFF)
            
            stat2d.SetBinContent(int(j)+1, int(i)+1, EFFStat)
            statDraw.SetBinContent(int(j)+1, int(i)+1, EFFStat)
            tree.Fill()
hist2d.GetZaxis().SetRangeUser(0.6,0.95)
    
fileOut.Write()


# In[ ]:


c = TCanvas()
if isConv:
    hist2d.GetZaxis().SetRangeUser(0.93,0.955)
else:
    hist2d.GetZaxis().SetRangeUser(0.55,0.95)
hist2d.Draw("COLZ text")
c.SetLogx()
c.Draw()


# In[ ]:





# In[ ]:


c = TCanvas()
histDraw.SetTitle("T&P Efficiency MC")
if isConv:
    histDraw.GetZaxis().SetRangeUser(0.93,0.955)
else:
    histDraw.GetZaxis().SetRangeUser(0.55,0.95)
    
histDraw.GetXaxis().SetTitle('pt')
histDraw.GetYaxis().SetTitle(r'\eta')

statDraw.SetBarOffset(-0.15)
statDraw.Draw("text same")

histDraw.Draw("COLZ text")
c.SetLogx()
if isConv:
    c.SaveAs(figpath+binsSelected+"/isConv/"+"EFF_mc_photonID.png")
else:
    c.SaveAs(figpath+binsSelected+"/ID/"+"EFF_mc_photonID.png")
c.Draw()


# In[ ]:


c = TCanvas()
statDraw.SetTitle("T&P Uncertainties Data")
if isConv:
    statDraw.GetZaxis().SetRangeUser(0.0005,0.01)
else:
    statDraw.GetZaxis().SetRangeUser(0,0.006)

statDraw.GetXaxis().SetTitle('pt')
statDraw.GetYaxis().SetTitle(r'\eta')
statDraw.Draw("colz text")
if isConv:
    c.SaveAs(figpath+binsSelected+"/isConv/"+"EFF_UNC_mc_photonID.png")
else:
    c.SaveAs(figpath+binsSelected+"/ID/"+"EFF_UNC_mc_photonID.png")
c.SetLogx()
c.Draw()


# In[ ]:


fileOut.Close()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# # MC PASS

# In[ ]:


IDPass = False
PassFail = 'Pass'
MC[PassFail] = {}


S = 'DYJets'
print('------------------------',S,'------------------------')
MC[PassFail][S] = EffGrid( 
                    sample      = dfMC[S],
                    part        = 'dilepton',
                    variable    = 'M',
                    DataMC      = 'mc',
                    samples     = S,
                    ProbeType   = 'Pass',
                    IDPass      = IDPass,
                    etaBins     = etaBins,
                    ptBins      = ptBins,
                    Abs         = Abs,
                    isConv      = isConv,
                    ranges      = ranges,
                    bins        = bins,
                    tempType    = tempType,
                    BinEBEE     = BinEBEE,
                  )



S = 'WJets'
print('------------------------',S,'------------------------')
MC[PassFail][S] = EffGrid( 
                    sample      = dfMC[S],
                    part        = 'dilepton',
                    variable    = 'M',
                    DataMC      = 'mc',
                    samples     = S,
                    ProbeType   = 'Pass',
                    IDPass      = IDPass,
                    etaBins     = etaBins,
                    ptBins      = ptBins,
                    Abs         = Abs,
                    isConv      = isConv,
                    ranges      = ranges,
                    bins        = bins,
                    tempType    = tempType,
                    BinEBEE     = BinEBEE,
                  )



# # MC Fail

# In[ ]:


IDPass = False
PassFail = 'Fail'
MC[PassFail] = {}

S = 'WJets'
print('------------------------',S,'------------------------')
MC[PassFail][S] = EffGrid( 
                    sample      = dfMC[S],
                    part        = 'dilepton',
                    variable    = 'M',
                    DataMC      = 'mc',
                    samples     = S,
                    ProbeType   = 'Fail',
                    IDPass      = IDPass,
                    etaBins     = etaBins,
                    ptBins      = ptBins,
                    Abs         = Abs,
                    isConv      = isConv,
                    ranges      = ranges,
                    bins        = bins,
                    tempType    = tempType,
                    BinEBEE     = BinEBEE,
                  )

S = 'DYJets'
print('------------------------',S,'------------------------')
MC[PassFail][S] = EffGrid( 
                    sample      = dfMC[S],
                    part        = 'dilepton',
                    variable    = 'M',
                    DataMC      = 'mc',
                    samples     = S,
                    ProbeType   = 'Fail',
                    IDPass      = IDPass,
                    etaBins     = etaBins,
                    ptBins      = ptBins,
                    Abs         = Abs,
                    isConv      = isConv,
                    ranges      = ranges,
                    bins        = bins,
                    tempType    = tempType,
                    BinEBEE     = BinEBEE,
                  )


# # DATA Pass

# In[ ]:


IDPass   = True
PassFail = 'Pass'
Data[PassFail] = EffGrid( 
                        sample       = df,
                        part         = 'dilepton',
                        variable     = 'M',
                        DataMC       = 'data',
                        samples      = '',
                        ProbeType    = 'Pass',
                        IDPass       = IDPass,
                        etaBins      = etaBins,
                        ptBins       = ptBins,
                        Abs          = Abs,
                        isConv       = isConv,
                        ranges       = ranges,
                        bins         = bins,
                        tempType     = tempType,
                        BinEBEE      = BinEBEE,
                        )


# # DATA Fail

# In[ ]:


IDPass   = True
PassFail = 'Fail'
Data[PassFail] = EffGrid( 
                        sample      = df,
                        part        = 'dilepton',
                        variable    = 'M',
                        DataMC      = 'data',
                        samples     = '',
                        ProbeType   = 'Fail',
                        IDPass      = IDPass,
                        etaBins     = etaBins,
                        ptBins      = ptBins,
                        Abs         = Abs,
                        isConv      = isConv,
                        ranges      = ranges,
                        bins        = bins,
                        tempType    = tempType,
                        BinEBEE     = BinEBEE,    
                        )


# # Fitting

# In[ ]:


def T(NSigPass, NBkgPass, NSigFail,NBkgFail, 
      alphaPass, betaPass, peakPass, gammaPass,
      alphaFail, betaFail, peakFail, gammaFail,
       MCPass, MCFail
     ):
    x = np.arange(0,len(MCPass))
    
    Pass = list(Template(NSigPass, NBkgPass, 
                         MCPass  , RooCMSShape(x,*(alphaPass, betaPass, peakPass, gammaPass)))) 
    
    Fail = list(Template(NSigFail, NBkgFail, 
                         MCFail, RooCMSShape(x,*(alphaFail, betaFail, peakFail, gammaFail))))
    Temp = np.array(Pass + Fail )
    return Temp


# In[ ]:


def PlotFitting(ax,
                NSig ,NBkg,
                DATA, SIG, BKG,
                eta, pt,
                color,
               ):
    TemplatePlot    = Template(NSig,NBkg, SIG, BKG)
    TemplatePlotBkg = NBkg*BKG/np.sum(BKG)
    DataPlot        = DATA
    #DataPlot        = Data[PassFail][0][IJ]/Data[PassFail][1][IJ] 

        
    ax.plot(xc,    TemplatePlot, color = color[0], linestyle='--', label=    'Fit')
    ax.plot(xc, TemplatePlotBkg, color = color[1], linestyle='--', label='Fit Bkg')
    ax.plot(xc,        DataPlot, color = color[2], linestyle= '-', label=   'Data')

    ax.legend()
    ax.grid(linestyle='--')

    if j == 0:
        ax.set_ylabel('Eta ['+str(round(eta[0],2))+','+str(round(eta[1],2))+']'  )        
    if i == 0:
        ax.set_title('Pt ['+str(pt[0])+','+str(pt[1])+']' )


# # Fitting with RooCMSShape

# In[ ]:


########## TEMPLATES ################
def TVoigt_Test(
                  NSigPass,NBkgPass, NSigFail,NBkgFail, 
                  sigPass, GammaPass, meanPass,
                  lambdaPass, xPass,
                  sigFail, GammaFail, meanFail,
                  lambdaFail, xFail,
                  MCPass, MCFail
                 ):
    
    x = np.arange(0,len(MCPass))
    
    argPass = lambdaPass, xPass
    argVoigtPass = sigPass, GammaPass, meanPass
    Pass = list(Template(NSigPass, NBkgPass, Voigt(x,*argVoigtPass)  , Exp(x,*argPass))) 
    
    
    argFail = lambdaFail, xFail
    argVoigtFail = sigFail, GammaFail, meanFail
    Fail = list(Template(NSigFail, NBkgFail, 
                         Voigt(x,*argVoigtFail) , Exp(x,*argPass)))
    
    
    #Temp = np.array(Pass + Fail )
    Temp = np.array(Pass)
    return Temp

def TVoigt_noSig(
                  NBkgPass,NBkgFail, 
                  sigPass, GammaPass, meanPass,
                  lambdaPass, xPass,
                  sigFail, GammaFail, meanFail,
                  lambdaFail, xFail,
                  MCPass, MCFail
                 ):
    x = np.arange(0,len(MCPass))
    
    argPass = lambdaPass, xPass
    argVoigtPass = sigPass, GammaPass, meanPass
    Pass = list(Template(0, NBkgPass, Voigt(x,*argVoigtPass)  , Exp(x,*argPass))) 
    
    
    argFail = lambdaFail, xFail
    argVoigtFail = sigFail, GammaFail, meanFail
    Fail = list(Template(0, NBkgFail, 
                         Voigt(x,*argVoigtFail) , Exp(x,*argPass)))
    
    
    #Temp = np.array(Pass + Fail )
    Temp = np.array(Pass)
    return Temp

def TVoigt_CMS(NSigPass, NBkgPass, NSigFail,NBkgFail, 
              sigPass, GammaPass, meanPass,
              alphaPass, betaPass, peakPass, gammaPass,
              sigFail, GammaFail, meanFail,
              alphaFail, betaFail, peakFail, gammaFail,
               MCPass, MCFail
             ):
    x = np.arange(0,len(MCPass))
    
    argPass      = alphaPass, betaPass, peakPass, gammaPass
    argVoigtPass = sigPass, GammaPass, meanPass
    Pass = list(Template(NSigPass, NBkgPass, 
                         Voigt(x,*argVoigtPass)  , RooCMSShape(x,*argPass))) 
    
    
    x = np.arange(len(MCPass),len(MCPass)*2)
    argFail      = alphaFail, betaFail, peakFail, gammaFail
    argVoigtFail = sigFail, GammaFail, meanFail
    Fail = list(Template(NSigFail, NBkgFail, 
                         Voigt(x,*argVoigtFail) , RooCMSShape(x,*argFail)))
    
    
    Temp = np.array(Pass + Fail )
    return Temp

def TVoigt_Exp(NSigPass, NBkgPass, NSigFail,NBkgFail, 
      sigPass, GammaPass, meanPass,
      lambdaPass, xPass,
      sigFail, GammaFail, meanFail,
      lambdaFail, xFail,
       MCPass, MCFail
     ):
    x = np.arange(0,len(MCPass))
    
    argPass = lambdaPass, xPass
    argVoigtPass = sigPass, GammaPass, meanPass
    Pass = list(Template(NSigPass, NBkgPass, 
                         Voigt(x,*argVoigtPass)  , Exp(x,*argPass))) 
    
    
    argFail = lambdaFail, xFail
    argVoigtFail = sigFail, GammaFail, meanFail
    Fail = list(Template(NSigFail, NBkgFail, 
                         Voigt(x,*argVoigtFail) , Exp(x,*argPass)))
    
    
    Temp = np.array(Pass + Fail )
    return Temp

def Voigt_CMS(
                xc,
                NSig, NBkg, 
                sig, Gamma, mean,
                alpha, beta, peak, gamma,
                ):
    x = xc
    arg      = alpha, beta, peak, gamma
    argVoigt = sig, Gamma, mean
    Temp = list(Template(NSig, NBkg, 
                         Voigt(x,*argVoigt) , RooCMSShape(x,*arg)))
    
    
    return np.array(Temp)

def Template(Nsig,Nbkg,Sig,Bkg):
    return Nsig * (Sig/np.sum(Sig)) + Nbkg * (Bkg/np.sum(Bkg))

########## METRIC ########
def NLL(DATA,Temp):
    return np.sum(Temp) - np.sum(DATA*np.log(Temp))

def CHI2(DATA,Temp):
    DATA[DATA==0] = 1
    SIGMA_2 = (1/DATA + 1/Temp)**(-1)
    return np.sum((Temp-DATA)**2/SIGMA_2)

def DIFFER(DATA,Temp,*arg):
    Model = Temp(*arg)
    return np.sum((Model-DATA)**2)


########## FITTING FUNCTIONS ########
def Fit(i,j,
        MC_PASS_S, MC_PASS_B,
        MC_FAIL_S, MC_FAIL_B,
        DATA_PASS, DATA_FAIL,
        Temp,
        p0, Bounded,
        Type   = '',
        Print  = False,
        TryMax = 20,
        ):

    ###############################
    
    DATA = np.array(list(DATA_PASS) + list(DATA_FAIL))

    model  = lambda x0:CHI2(DATA=DATA,Temp=Temp,*x0)

    fitSucess = False
    tries = 0
    
    while not fitSucess:
        if Print:
            print('--- Start Fitting')
        fitResult = minimize(model,
                             p0,
                             #method = 'L-BFGS-B',
                             #method = 'SLSQP',
                             bounds = Bounded,
                             #tol = 1e-6,
                             #tol = 1e-10,
                            )
        fitSucess = fitResult.success
        FIT = fitResult.x

        p0 = GoodGuess(i,j,len(etaBINS),len(ptBins),tries,p0)
        if not p0:
            p0 = np.ones(len(Bounded))
            break;
        tries += 1
        
        if tries%10 == 0 and Print:
            print('Try: ' + str(tries))
        if tries > TryMax and Print :
            print("Maximum tries reached!")
            break
    return FIT

def Fit_Curve(i,j,
        MC_PASS_S, MC_PASS_B,
        MC_FAIL_S, MC_FAIL_B,
        DATA_PASS, DATA_FAIL,
        p0, Bounded,
        ):

    ###############################
    
    DATA = np.array(list(DATA_PASS) + list(DATA_FAIL))
    x = np.arange(0,len(DATA))

    VV = lambda x,*x0 : Voigt_CMS_x(x,
                                    NSigPass  =  x0[0], NBkgPass  =  x0[1], NSigFail =  x0[2],  NBkgFail =  x0[3], 
                                    sigPass   =  x0[4], GammaPass =  x0[5], meanPass =  x0[6],
                                    alphaPass =  x0[7], betaPass  =  x0[8], peakPass =  x0[9], gammaPass = x0[10],
                                    sigFail   = x0[11], GammaFail = x0[12], meanFail = x0[13],
                                    alphaFail = x0[14], betaFail  = x0[15], peakFail = x0[16], gammaFail = x0[17],
                                    MCPass = MC_PASS_S[:len(DATA_PASS)], 
                                    MCFail = MC_FAIL_S[:len(DATA_PASS)])
    
    
    

    return FIT[0]

def Fit_Curve(
              DATA_PASS, DATA_FAIL,
              pPass,pFail,
              Bounded,
             ):
    
    VoigtCMS = lambda x,*x0 : Voigt_CMS(
                                        x,
                                        NSig  =  x0[0], NBkg  =  x0[1],
                                        sig   =  x0[2], Gamma =  x0[3], mean =  x0[4],
                                        alpha =  x0[5], beta  =  x0[6], peak =  x0[7], gamma = x0[8], 
                                        )
    
    yerr = np.sqrt(DATA_PASS)
    yerr[yerr<1] = yerr[yerr<1]*0+2
    xFit = np.arange(0,len(DATA_PASS))
    Fits = curve_fit(
                    f     = VoigtCMS,
                    xdata = xFit,
                    ydata = DATA_PASS,
                    sigma = yerr,
                    p0    = pPass,
                    method = 'trf',
                    bounds = Bounded,
                    )

    FitsPass = Fits[0]
    FitsPassSig = np.sqrt(np.diag(Fits[1]))
    ############################
    yerr = np.sqrt(DATA_FAIL)
    yerr[yerr<1] = yerr[yerr<1]*0+2
    xFit = np.arange(len(DATA_PASS),len(DATA_PASS)*2)
    Fits = curve_fit(
                    f      = VoigtCMS,
                    xdata  = xFit,
                    ydata  = DATA_FAIL,
                    sigma  = yerr,
                    p0     = pFail,
                    #method = 'lm',
                    method = 'trf',
                    #method = 'dogbox',
                    bounds = Bounded,
                    )
    FitsFail = Fits[0]
    FitsFailSig = np.sqrt(np.diag(Fits[1]))
    
    return FitsPass, FitsFail, FitsPassSig, FitsFailSig

def Fit_Curve_CHI(
              DATA_PASS, DATA_FAIL,
              pPass,pFail,
              Bounded = [
                           [0,0,
                            0,0,10,
                            0,-0.2,-1000,-1],
                           [np.inf,np.inf,
                            3,3,48,
                            70,0.2,1000,1,
                            ]
                        ]  ,
              error =  [
                        1,1,
                        0.001,0.01,1,0.01,
                        0.001,0.001,0.001
                        ],
             ):
    
    ####################
    xFit = np.arange(0,len(DATA_PASS))
    
    chi2 =lambda NSig , NBkg ,                  sig  , Gamma, mean,                  alpha, beta , peak, gamma : CHI2(  DATA_PASS,
                                                    Voigt_CMS(
                                                        xc = xFit, \
                                                        NSig=NSig , NBkg=NBkg , \
                                                        sig = sig  , Gamma  = Gamma, mean = mean, \
                                                        alpha = alpha, beta = beta , peak = peak, gamma = gamma,  
                                                        ) 
                                                    )    
    
    
    x0 = pPass
    mP = Minuit( chi2,
                NSig  =  x0[0], NBkg  =  x0[1],
                sig   =  x0[2], Gamma =  x0[3], mean =  x0[4],
                alpha =  x0[5], beta  =  x0[6], peak =  x0[7], gamma = x0[8], 
                error_NSig  =  error[0], error_NBkg  =  error[1],
                error_sig   =  error[2], error_Gamma =  error[3], error_mean =  error[4],
                error_alpha =  error[5], error_beta  =  error[6], error_peak =  error[7], error_gamma = error[8], 
                limit_NSig  =  (Bounded[0][0],Bounded[1][0]), limit_NBkg  =  (Bounded[0][1],Bounded[1][1]),
                limit_sig   =  (Bounded[0][2],Bounded[1][2]), limit_Gamma =  (Bounded[0][3],Bounded[1][3]), limit_mean =  (Bounded[0][4],Bounded[1][4]),
                limit_alpha =  (Bounded[0][5],Bounded[1][5]), limit_beta  =  (Bounded[0][6],Bounded[1][6]), limit_peak =  (Bounded[0][7],Bounded[1][7]), limit_gamma = (Bounded[0][8],Bounded[1][8]), 
                errordef = 0.5,
              )    
    
    mP.migrad()
    
    
    
    FitsPass    = mP.values.values()
    FitsPassSig = mP.errors.values()
    
    ################################################
    xFit = np.arange(len(DATA_PASS),len(DATA_PASS)*2)
    
    chi2 =lambda NSig , NBkg ,                  sig  , Gamma, mean,                  alpha, beta , peak, gamma : CHI2(  DATA_FAIL,
                                                    Voigt_CMS(
                                                        xc = xFit, \
                                                        NSig=NSig , NBkg=NBkg , \
                                                        sig = sig  , Gamma  = Gamma, mean = mean, \
                                                        alpha = alpha, beta = beta , peak = peak, gamma = gamma,  
                                                        ) 
                                                    )   
    
    x0 = pFail
    mF = Minuit( chi2,
                NSig  =  x0[0], NBkg  =  x0[1],
                sig   =  x0[2], Gamma =  x0[3], mean =  x0[4],
                alpha =  x0[5], beta  =  x0[6], peak =  x0[7], gamma = x0[8], 
                error_NSig  =  error[0], error_NBkg  =  error[1],
                error_sig   =  error[2], error_Gamma =  error[3], error_mean =  error[4],
                error_alpha =  error[5], error_beta  =  error[6], error_peak =  error[7], error_gamma = error[8], 
                limit_NSig  =  (Bounded[0][0],Bounded[1][0]), limit_NBkg  =  (Bounded[0][1],Bounded[1][1]),
                limit_sig   =  (Bounded[0][2],Bounded[1][2]), limit_Gamma =  (Bounded[0][3],Bounded[1][3]), limit_mean =  (Bounded[0][4],Bounded[1][4]),
                limit_alpha =  (Bounded[0][5],Bounded[1][5]), limit_beta  =  (Bounded[0][6],Bounded[1][6]), limit_peak =  (Bounded[0][7],Bounded[1][7]), limit_gamma = (Bounded[0][8],Bounded[1][8]), 
                errordef = 0.5,
              )    
    
    mF.migrad()
    
    
    FitsFail    = mF.values.values()
    FitsFailSig = mF.errors.values()

    #print()
    #print("\/\/\/\/\/\/\/\/\\/\/\/\/\/\/\/\/\\/\/\/\/\/\/\/\/")
    #print(mP.get_param_states())
    #print(mF.get_param_states())
    #print("\/\/\/\/\/\/\/\/\\/\/\/\/\/\/\/\/\\/\/\/\/\/\/\/\/")
          
    return FitsPass, FitsFail, FitsPassSig, FitsFailSig,mP,mF


# In[ ]:


def SkipGap(i,j,binsSelect):
    gapFlag = False
    
    if     binsSelected == "Optimized":
        if (i == 1 or i == 4) and j != 5:
            gapFlag = True
    elif   binsSelected == "Plots":
        if (i == 1 or i == 4) and j != 11:
            gapFlag = True
    elif   binsSelected == "Hien":
        if (i == 1 or i == 4) and j != 6:
            gapFlag = True
    
    return gapFlag

def InitializeParams(i,j,binsSelected):
    if   binsSelected == "Optimized":
        if isConv:
            if   j == 0:
                if i != 5:
                    pPass = [
                            5e3,   5e3, 
                            0.1, 1, 14,       # Voigt
                            1,0.1, 0.01, 0.09,  # RooCMS
                            ]

                    pFail = [
                            1.5e3,   5e4, 
                            1, 1.2, 43,       # Voigt
                            30,0.1, 0.01, 0.09,  # RooCMS
                            ]
                else:
                    pPass = [
                            6e3,   5e3, 
                            0.1, 1, 14,       # Voigt
                            1,0.1, 0.01, 0.09,  # RooCMS
                            ]

                    pFail = [
                            3e3,   3e4, 
                            1, 1.2, 43,       # Voigt
                            30,0.1, 0.01, 0.09,  # RooCMS
                            ]
            elif j == 1:
                if i == 0:
                    pPass = [
                            5e4,   7e3, 
                            0.1, 2, 15,       # Voigt
                            10,0.01, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                             3e4, 5e4,
                             2, 0.01, 42,        # Voigt
                             33, 0.1, 200, 0.09  # RooCMS
                            ]
                elif i == 2:
                    pPass = [
                            3e5,   6e4, 
                            0.1, 2, 14,       # Voigt
                            5,0.01, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                             3e4, 5e4,
                             2, 0.01, 42,        # Voigt
                             33, 0.1, 200, 0.09  # RooCMS
                            ]
                elif i == 3:
                    pPass = [
                            5e5,   4e5, 
                            0.1, 2, 14,       # Voigt
                            5,0.01, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                             3e4, 5e4,
                             2, 0.01, 42,        # Voigt
                             33, 0.1, 200, 0.09  # RooCMS
                            ]
                elif i == 5:
                    pPass = [
                            1e5,   8e4, 
                            0.1, 2, 15,       # Voigt
                            5,0.01, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                             1e4, 1e4,
                             2, 0.01, 42,        # Voigt
                             33, 0.1, 200, 0.09  # RooCMS
                            ]
            elif j == 2:
                if i == 0:
                    pPass = [
                            3e5,   5e3, 
                            0.1, 2, 15,       # Voigt
                            10,0.01, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                            1.5e5,   5e4, 
                            1, 1, 44,           # Voigt
                            20,0.01, 20, 0.09,  # RooCMS
                            ]
                if i == 2:
                    pPass = [
                            12e5,   5e3, 
                            0.1, 2, 15,       # Voigt
                            10,0.01, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                            1.5e5,   5e4, 
                            1, 1, 44,           # Voigt
                            20,0.01, 20, 0.09,  # RooCMS
                            ]
                if i == 3:
                    pPass = [
                            1e6,   5e3, 
                            0.1, 1.5, 15,       # Voigt
                            10,0.01, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                            1.5e5,   5e4, 
                            1, 1, 44,           # Voigt
                            20,0.01, 20, 0.09,  # RooCMS
                            ]
                if i == 5:
                    pPass = [
                            1e5,   5e3, 
                            0.1, 2, 15,       # Voigt
                            10,0.01, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                            1.5e5,   5e4, 
                            1, 1, 44,           # Voigt
                            20,0.01, 20, 0.09,  # RooCMS
                            ]
            elif j == 3:
                if i == 0:
                    pPass = [
                            5e4,   9e3, 
                            #0.1, 2, 15,       # Voigt
                            1, 1, 15,       # Voigt
                            13,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            9e3,   4e3, 
                            1, 1, 44,           # Voigt
                            40,0.01, 20, -0.09,  # RooCMS
                            ]
                elif i == 3:
                    pPass = [
                            1e5,   1e4, 
                            0.5, 1, 14,       # Voigt
                            15,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            3e4,   8e3, 
                            1, 1, 44,           # Voigt
                            45,0.01, 20, -0.09,  # RooCMS
                            ]                
                elif i == 5:
                    pPass = [
                            1e4,   5e3, 
                            0.5, 1, 14,       # Voigt
                            15,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            5e3,   5e3, 
                            0.5, 1, 44,           # Voigt
                            45,0.01, 20, -0.09,  # RooCMS
                            ]
                else:
                    pPass = [
                            6e4,   5e3, 
                            0.1, 2, 15,       # Voigt
                            13,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            9e3,   4e3, 
                            1, 1, 44,           # Voigt
                            45,0.01, 20, -0.09,  # RooCMS
                            ]                        
            elif j == 4:
                if i == 0:
                    pPass = [
                            1e3,  200,  
                            0.5,  1, 15,  
                            15,1, 10,-0.09,
                            ] 

                    pFail = [
                            1e2,  3e1,  
                            0.5,  1, 44,  
                            49,-0.1, 10, -0.09,  # RooCMS
                            ]  
                elif i == 2:
                    pPass = [
                            7e3,  200,  
                            0.5,  1, 15,  
                            15,1, 10,-0.09,
                            ] 

                    pFail = [
                            5e2,  5e2,  
                            0.5,  1, 44,  
                            35,-0.1, 10, -0.09,  # RooCMS
                            ] 
                elif i == 3:
                    pPass = [
                            5e3,  200,  
                            0.1,  1, 15,  
                            15,1, 10,-0.09,
                            ] 

                    pFail = [
                            5e2,  1e2,  
                            0.1,  1, 44,  
                            48,-0.1, 10, -0.09,  # RooCMS
                            ] 
                elif i == 5:
                    pPass = [1.22435554e+03, 3.20343246e+02, 9.22998413e-12,
                             1.10974344e+00, 1.50406031e+01, 1.40180622e+01,
                             6.13551539e-01, 1.00000028e+01, 5.95495234e-01]
                    pFail = [ 4.08455718e+02,  2.34193103e+02,  1.08171908e+00,
                             9.14064665e-01, 4.39415340e+01,  5.75583581e+01, 
                             -5.13886755e-01,  3.82617111e+03,-4.43517032e-02]
                else :
                    pPass = [
                            1e3,  100,  
                            0.5,  1, 15,  
                            15,0.1, 10,-0.09,
                            ] 

                    pFail = [
                            2e2,  1e2,  
                            0.1,  1, 44,  
                            45,0.01, 10, -0.09,  # RooCMS
                            ]                                        
            elif j == 5:
                if i == 0:
                    pPass = [
                            6e4,  1e2,  
                            0.1,  2, 15,  
                            1,1, 1.15814356e+02,1,
                            ] 

                    pFail = [
                            1e3,  1e2,  
                            0.1,  2, 44,  
                            35,  1, 1.15814356e+02,1,
                            ] 
                elif i == 1:
                    pPass = [
                            2e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            2e1,  1e1,  
                            0.5,  1, 44,  
                            48,  -0.1, 10,0.1,
                            ]   
                else:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            40,  3e1,  
                            1,  1, 44,  
                            35,  0.1, 1.15814356e+02,0.1,
                            ]  
        else:
            if   j == 0:
                if  i == 0:
                    pPass = [
                            1e4,   5e3, 
                            0.1, 1, 14,       # Voigt
                            1,0.1, 0.01, 0.09,  # RooCMS
                            ]

                    pFail = [
                            4e3,   2e4, 
                            1, 1.2, 43,       # Voigt
                            30,0.1, 0.01, 0.09,  # RooCMS
                            ]
                elif i != 5:

                    pPass = [
                            1e4,   5e3, 
                            0.1, 1, 14,       # Voigt
                            1,0.1, 0.01, 0.09,  # RooCMS
                            ]

                    pFail = [
                            1.5e3,   5e4, 
                            1, 1.2, 43,       # Voigt
                            30,0.1, 0.01, 0.09,  # RooCMS
                            ]
                elif i == 5:
                    pPass = [
                            5e4,   2e3, 
                            0.1, 1, 14,       # Voigt
                            1,0.1, 0.01, 0.09,  # RooCMS
                            ]

                    pFail = [
                            4e3,   2e4, 
                            1, 1.2, 43,       # Voigt
                            10,0.1, 0.01, 0.09,  # RooCMS
                            ]
            elif j == 1:
                if i == 0:
                    pPass = [
                            1e5,   7e3, 
                            0.1, 2, 15,       # Voigt
                            10,0.1, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                             3e4, 5e4,
                             2, 0.01, 43,        # Voigt
                             33, 0.1, 200, 0.09  # RooCMS
                            ]
                elif i == 2:
                    pPass = [
                            5e5,   6e4, 
                            0.1, 2, 15,       # Voigt
                            5,0.1, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                             2e4, 5e4,
                             2, 0.01, 43,        # Voigt
                             33, 0.1, 200, 0.09  # RooCMS
                            ]
                elif i == 3:
                    pPass = [
                            5e5,   1e5, 
                            0.1, 2, 14,       # Voigt
                            10,0.1, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                             3e4, 5e4,
                             2, 0.01, 43,        # Voigt
                             33, 0.1, 200, 0.09  # RooCMS
                            ]
                elif i == 5:
                    pPass = [
                            1e5,   8e4, 
                            0.1, 2, 15,       # Voigt
                            30,0.01, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                             1e4, 1e4,
                             2, 0.01, 43,        # Voigt
                             33, 0.1, 200, 0.09  # RooCMS
                            ]
            elif j == 2:
                if i == 0:
                    pPass = [
                            3e5,   5e3, 
                            0.1, 2, 15,       # Voigt
                            10,0.1, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                            1.5e5,   5e4, 
                            1, 1, 44,           # Voigt
                            20,0.1, 20, 0.09,  # RooCMS
                            ]
                if i == 2:
                    pPass = [
                            12e5,   5e3, 
                            0.1, 2, 15,       # Voigt
                            30,0.1, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                            1.5e5,   5e4, 
                            1, 1, 44,           # Voigt
                            20,0.1, 20, 0.09,  # RooCMS
                            ]
                if i == 3:
                    pPass = [
                            3e6,   5e3, 
                            0.2, 1.5, 15,       # Voigt
                            5,0.1, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                            8e4,   1e4, 
                            0.1, 1, 44,           # Voigt
                            35,0.1, 20, 0.09,  # RooCMS
                            ]
                if i == 5:
                    pPass = [
                            4e5,   1e3, 
                            1.5, 1.7, 15,       # Voigt
                            3,0.01, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                            1.5e5,   5e4, 
                            1, 1, 44,           # Voigt
                            20,0.01, 20, 0.09,  # RooCMS
                            ]
            elif j == 3:
                if i == 0:
                    pPass = [
                            5e4,   9e3, 
                            #0.1, 2, 15,       # Voigt
                            1, 1, 15,       # Voigt
                            13,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            9e3,   4e3, 
                            1, 1, 44,           # Voigt
                            40,0.01, 20, -0.09,  # RooCMS
                            ]
                elif i == 2:
                    pPass = [
                            5e4,   9e3, 
                            #0.1, 2, 15,       # Voigt
                            1, 1, 15,       # Voigt
                            13,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            9e3,   4e3, 
                            1, 1, 44,           # Voigt
                            40,0.01, 20, -0.09,  # RooCMS
                            ]
                elif i == 3:
                    pPass = [
                            5e4,   9e3, 
                            #0.1, 2, 15,       # Voigt
                            1, 1, 15,       # Voigt
                            13,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            9e3,   4e3, 
                            1, 1, 44,           # Voigt
                            40,0.01, 20, -0.09,  # RooCMS
                            ]
                elif i == 5:
                    pPass = [
                            7e4,   5e3, 
                            0.1, 2, 15,       # Voigt
                            13,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            9e3,   4e3, 
                            1, 1, 44,           # Voigt
                            40,0.01, 20, -0.09,  # RooCMS
                            ]
                else:
                    pPass = [
                            2e5,   5e3, 
                            0.1, 2, 15,       # Voigt
                            13,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            9e3,   4e3, 
                            1, 1, 44,           # Voigt
                            40,0.01, 20, -0.09,  # RooCMS
                            ]
            elif j == 4:
                if i == 0:
                    pPass = [
                            5e3,  200,  
                            0.1,  2, 15,  
                            15,-0.1, 100,1,
                            ] 

                    pFail = [
                            4e2,  1e2,  
                            0.1,  2, 44,  
                            42,-0.1, 100,1,
                            ] 
                elif i == 2:
                    pPass = [
                            5e3,  200,  
                            0.1,  2, 15,  
                            15,-0.1, 100,1,
                            ] 

                    pFail = [
                            4e2,  1e2,  
                            0.1,  2, 44,  
                            60,-0.1, 100,1,
                            ] 
                elif i == 3:
                    pPass = [
                            5e3,  200,  
                            0.1,  2, 15,  
                            15,-0.1, 100,1,
                            ] 

                    pFail = [
                            5e2,  1e2,  
                            0.1,  2, 44,  
                            60,0.1, 100,1,
                            ] 
                else :
                    pPass = [
                            5e3,  200,  
                            0.1,  2, 15,  
                            15,-0.1, 100,1,
                            ] 

                    pFail = [
                            5e2,  1e2,  
                            0.1,  2, 43,  
                            42,-0.1, 100,1,
                            ] 
            elif j == 5:
                if i == 0:
                    pPass = [
                            3e3,  1e2,  
                            0.1,  1, 15,  
                            1,0.1, 1.15814356e+02,1,
                            ] 

                    pFail = [
                            1e3,  1e2,  
                            0.1,  1, 44,  
                            70,-0.1, 1.15814356e+02,1,
                            ] 
                elif i == 1:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            200,  3e1,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
    elif binsSelected == "Plots" :
        if isConv:
            if   j == 0:
                if  i == 0:
                    pPass = [
                            1e4,   5e3, 
                            0.1, 1, 14,       # Voigt
                            1,0.1, 0.01, 0.09,  # RooCMS
                            ]

                    pFail = [
                            4e3,   2e4, 
                            1, 1.2, 43,       # Voigt
                            30,0.1, 0.01, 0.09,  # RooCMS
                            ]
                elif i != 5:

                    pPass = [
                            1e4,   5e3, 
                            0.1, 1, 14,       # Voigt
                            1,0.1, 0.01, 0.09,  # RooCMS
                            ]

                    pFail = [
                            1.5e3,   5e4, 
                            1, 1.2, 43,       # Voigt
                            30,0.1, 0.01, 0.09,  # RooCMS
                            ]
                elif i == 5:
                    pPass = [
                            5e4,   2e3, 
                            0.1, 1, 14,       # Voigt
                            1,0.1, 0.01, 0.09,  # RooCMS
                            ]

                    pFail = [
                            4e3,   2e4, 
                            1, 1.2, 43,       # Voigt
                            10,0.1, 0.01, 0.09,  # RooCMS
                            ]
            elif j == 1:
                if i == 0:
                    pPass = [
                            1e5,   7e3, 
                            0.1, 2, 15,       # Voigt
                            10,0.1, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                             3e4, 5e4,
                             2, 0.01, 43,        # Voigt
                             33, 0.1, 200, 0.09  # RooCMS
                            ]
                elif i == 2:
                    pPass = [
                            5e5,   6e4, 
                            0.1, 2, 15,       # Voigt
                            5,0.1, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                             2e4, 5e4,
                             2, 0.01, 43,        # Voigt
                             33, 0.1, 200, 0.09  # RooCMS
                            ]
                elif i == 3:
                    pPass = [
                            5e5,   1e5, 
                            0.1, 2, 14,       # Voigt
                            10,0.1, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                             3e4, 5e4,
                             2, 0.01, 43,        # Voigt
                             33, 0.1, 200, 0.09  # RooCMS
                            ]
                elif i == 5:
                    pPass = [
                            1e5,   8e4, 
                            0.1, 2, 15,       # Voigt
                            30,0.01, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                             1e4, 1e4,
                             2, 0.01, 43,        # Voigt
                             33, 0.1, 200, 0.09  # RooCMS
                            ]
            elif j == 2:
                if i == 0:
                    pPass = [
                            3e5,   5e3, 
                            0.1, 2, 15,       # Voigt
                            10,0.1, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                            1.5e5,   5e4, 
                            1, 1, 44,           # Voigt
                            20,0.1, 20, 0.09,  # RooCMS
                            ]
                if i == 2:
                    pPass = [
                            2e5,   1e3, 
                            0.1, 1, 14,       # Voigt
                            30,0.1, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            1e4,   3e3, 
                            1, 1, 44,           # Voigt
                            50,0.1, 20, -0.09,  # RooCMS
                            ]
                if i == 3:
                    pPass = [
                            3e6,   5e3, 
                            0.2, 1.5, 15,       # Voigt
                            5,0.1, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                            8e4,   1e4, 
                            0.1, 1, 44,           # Voigt
                            35,0.1, 20, 0.09,  # RooCMS
                            ]
                if i == 5:
                    pPass = [
                            4e5,   1e3, 
                            1.5, 1.7, 15,       # Voigt
                            3,0.01, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                            1.5e5,   5e4, 
                            1, 1, 44,           # Voigt
                            20,0.01, 20, 0.09,  # RooCMS
                            ]
            elif j == 3:
                if i == 0:
                    pPass = [
                            5e4,   9e3, 
                            #0.1, 2, 15,       # Voigt
                            1, 1, 15,       # Voigt
                            13,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            9e3,   4e3, 
                            1, 1, 44,           # Voigt
                            40,0.01, 20, -0.09,  # RooCMS
                            ]
                elif i == 2:
                    pPass = [
                            5e4,   9e3, 
                            #0.1, 2, 15,       # Voigt
                            1, 1, 15,       # Voigt
                            13,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            9e3,   4e3, 
                            1, 1, 44,           # Voigt
                            40,0.01, 20, -0.09,  # RooCMS
                            ]
                elif i == 3:
                    pPass = [
                            5e4,   9e3, 
                            #0.1, 2, 15,       # Voigt
                            1, 1, 15,       # Voigt
                            13,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            9e3,   4e3, 
                            1, 1, 44,           # Voigt
                            40,0.01, 20, -0.09,  # RooCMS
                            ]
                elif i == 5:
                    pPass = [
                            7e4,   5e3, 
                            0.1, 2, 15,       # Voigt
                            13,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            9e3,   4e3, 
                            1, 1, 44,           # Voigt
                            40,0.01, 20, -0.09,  # RooCMS
                            ]
                else:
                    pPass = [
                            2e5,   5e3, 
                            0.1, 2, 15,       # Voigt
                            13,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            9e3,   4e3, 
                            1, 1, 44,           # Voigt
                            40,0.01, 20, -0.09,  # RooCMS
                            ]
            elif j == 4:
                if i == 0:
                    pPass = [
                            2e5,  2e3,  
                            0.1,  2, 15,  
                            15,-0.1, 100,1,
                            ] 

                    pFail = [
                            1e4,  2e3,  
                            0.1,  2, 44,  
                            42,-0.1, 100,1,
                            ] 
                elif i == 2:
                    pPass = [
                            8e5,  5e3,
                            0.1,  1, 15,  
                            15,-0.1, 100,1,
                            ] 

                    pFail = [
                            9e4,  2e3,
                            0.1,  1, 44,  
                            60,-0.1, 100,1,
                            ] 
                elif i == 3:
                    pPass = [
                            4e5,  1e4,
                            0.1,  1, 15,  
                            15,-0.1, 100,-1,
                            ] 

                    pFail = [
                            4e4,  7e3,
                            0.1,  1, 44,  
                            60,0.1, 100,-1,
                            ] 
                elif i == 5 :
                    pPass = [
                            2e5,  4e3,
                            0.1,  2, 15,  
                            15,-0.1, 100,-1,
                            ] 

                    pFail = [
                            2e4,  3e3,  
                            0.1,  2, 44,  
                            65,-0.1, 100,-1,
                            ] 
            elif j == 5:
                if i == 0:
                    pPass = [
                            9e3,  3e2,  
                            0.2,  1, 15,  
                            10,0.1, 1.15814356e+02,1,
                            ] 

                    pFail = [
                            3e3,  3e2,  
                            0.1,  1, 44,  
                            70,-0.1, 1.15814356e+02,1,
                            ] 
                elif i == 2:
                    pPass = [
                            9e4,  3e3,
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            2e4,  3e3,
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
                elif i == 3:
                    pPass = [
                            1e5,  6e2,
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            4e3,  6e2,
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
                elif i == 5:
                    pPass = [
                            1e4,  3e3,
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            2e4,  3e3,
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
                else:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            200,  3e1,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
            elif j == 6:
                if i == 0:
                    pPass = [
                            8e3,  3e2,  
                            0.1,  1, 15,  
                            10,0.1, 1.15814356e+02,1,
                            ] 

                    pFail = [
                            1e3,  1e2,  
                            0.2,  1, 44,  
                            70,-0.1, 1.15814356e+02,1,
                            ] 
                elif i == 2:
                    pPass = [
                            3e4,  3e2,
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            8e3,  3e2,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
                elif i == 3:
                    pPass = [
                            6e4,  3e2,
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            5e3,  3e2,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
                elif i == 5:
                    pPass = [
                            3e3,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            5e3,  3e2,
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
                else:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            200,  3e1,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
            elif j == 7:
                if i == 0:
                    pPass = [
                            3e3,  5e1,
                            0.1,  1, 15,  
                            1,0.1, 1.15814356e+02,1,
                            ] 

                    pFail = [
                            1e3,  5e1,
                            0.1,  1, 44,  
                            70,-0.1, 1.15814356e+02,1,
                            ] 
                elif i == 2:
                    pPass = [
                            2e4,  2e2,
                            0.5,  1, 15,  
                            10,-0.1, 1.15814356e+02,-0.1,
                            ] 

                    pFail = [8e2, 2e2,
                             1, 1, 44, 
                             60, 0.0038985980209962634, -700, 0.015222050465143688
                            ]
                elif i == 3:
                    pPass = [
                            1e4,  3e2,
                            0.5,  1, 15,  
                            10,-0.1, 1.15814356e+02,-0.1,
                            ] 

                    pFail = [2e3, 3e2,
                             1, 1, 44, 
                             0.7044642032043633, 0.0038985980209962634, 1557.2502065025765, -0.015222050465143688
                            ]
                elif i == 5:
                    pPass = [
                            2e3,  6e1,  
                            0.5,  1, 15,  
                            10,-0.1, 1.15814356e+02,-0.1,
                            ] 

                    pFail = [2e2, 7e1,
                             1, 1, 44, 
                             70, 0.0038985980209962634, 700, -0.015222050465143688
                            ]
                else:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,-0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            200,  3e1,  
                            1,  1, 44,  
                            10,-0.1, 1.15814356e+02,0.1,
                            ]  
            elif j == 8:
                if i == 0:
                    pPass = [
                            3e3,  1e2,  
                            0.1,  1, 15,  
                            1,0.1, 1.15814356e+02,1,
                            ] 

                    pFail = [
                            5e2,  1e2,  
                            1,  1, 44,  
                            70,-0.1, 1.15814356e+02,1,
                            ] 
                elif i == 2:
                    pPass = [
                            6e3,  3e2,
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            6e2,  3e2,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
                elif i == 3:
                    pPass = [
                            1e3,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            1e3,  6e2,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,-0.1,
                            ]  
                elif i == 5:
                    pPass = [
                            9e2,  7e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            1e2,  7e1,  
                            1,  1, 44,  
                            60,  0.1, 1.15814356e+02, -0.1,
                            ]  
                else:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            200,  3e1,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
            elif j == 9:
                if i == 0:
                    pPass = [
                            5e2,  5e1,
                            0.1,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            5e1,  2e1,
                            0.1,  1, 44,  
                            50,-0.1, 1.15814356e+02,-0.1,
                            ] 
                elif i == 2:
                    pPass = [
                            6e3,  3e2,
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            6e2,  3e2,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
                elif i == 3:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            1e3,  3e1,  
                            1,  1, 44,  
                            60,  0.1, 1.15814356e+02,0.1,
                            ]  
                elif i == 5:
                    pPass = [
                            3e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            7e1,  1e1,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
                else:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            200,  3e1,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
            elif j == 10:
                if i == 0:
                    pPass = [
                            1e3,  1e2,  
                            0.1,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            1e2,  3e1,  
                            0.1,  1, 44,  
                            50,-0.1, 1.15814356e+02,0.1,
                            ] 
                elif i == 2:
                    pPass = [
                            6e3,  3e2,
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            3e2,  1e2,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
                elif i == 3:
                    pPass = [
                            3e3,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            3e2,  5e1,  
                            1,  1, 44,  
                            60,  0.1, 1.15814356e+02,0.1,
                            ]  
                elif i == 5:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            1e2,  3e1,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,-0.1,
                            ]  
                else:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            200,  3e1,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
            elif j == 11:
                if   i == 0:
                    pPass = [
                            4e3,  1e2,  
                            0.1,  1, 15,  
                            10,0.1, 1.15814356e+02,-0.05,
                            ] 

                    pFail = [
                            3e2,  5e1,  
                            0.1,  1, 44,  
                            70,-0.1, 1.15814356e+02,-0.05,
                            ] 
                elif i == 1:
                    pPass = [
                            8e2,  3e2,
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            5e1,  1e1,  
                            0.1,  1, 44,  
                            10,  0.1, 40,-0.1,
                            ]  
                elif i == 2:
                    pPass = [
                            4e3,  3e2,
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            1e2,  3e2,  
                            1,  1, 44,  
                            40,  0.1, 1.15814356e+02,0.1,
                            ]  
                elif i == 3:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            1e3,  3e1,  
                            1,  1, 44,  
                            60,  0.1, 1.15814356e+02,0.1,
                            ]  
                elif i == 5:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            200,  3e1,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
                else:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            200,  3e1,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]                      
        else:
            if   j == 0:
                if  i == 0:
                    pPass = [
                            1e4,   5e3, 
                            0.1, 1, 14,       # Voigt
                            1,0.1, 0.01, 0.09,  # RooCMS
                            ]

                    pFail = [
                            4e3,   2e4, 
                            1, 1.2, 43,       # Voigt
                            30,0.1, 0.01, 0.09,  # RooCMS
                            ]
                elif i != 5:

                    pPass = [
                            1e4,   5e3, 
                            0.1, 1, 14,       # Voigt
                            1,0.1, 0.01, 0.09,  # RooCMS
                            ]

                    pFail = [
                            1.5e3,   5e4, 
                            1, 1.2, 43,       # Voigt
                            30,0.1, 0.01, 0.09,  # RooCMS
                            ]
                elif i == 5:
                    pPass = [
                            5e4,   2e3, 
                            0.1, 1, 14,       # Voigt
                            1,0.1, 0.01, 0.09,  # RooCMS
                            ]

                    pFail = [
                            4e3,   2e4, 
                            1, 1.2, 43,       # Voigt
                            10,0.1, 0.01, 0.09,  # RooCMS
                            ]
            elif j == 1:
                if i == 0:
                    pPass = [
                            1e5,   7e3, 
                            0.1, 2, 15,       # Voigt
                            10,0.1, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                             3e4, 5e4,
                             2, 0.01, 43,        # Voigt
                             33, 0.1, 200, 0.09  # RooCMS
                            ]
                elif i == 2:
                    pPass = [
                            5e5,   6e4, 
                            0.1, 2, 15,       # Voigt
                            5,0.1, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                             2e4, 5e4,
                             2, 0.01, 43,        # Voigt
                             33, 0.1, 200, 0.09  # RooCMS
                            ]
                elif i == 3:
                    pPass = [
                            5e5,   1e5, 
                            0.1, 2, 14,       # Voigt
                            10,0.1, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                             3e4, 5e4,
                             2, 0.01, 43,        # Voigt
                             33, 0.1, 200, 0.09  # RooCMS
                            ]
                elif i == 5:
                    pPass = [
                            1e5,   8e4, 
                            0.1, 2, 15,       # Voigt
                            30,0.01, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                             1e4, 1e4,
                             2, 0.01, 43,        # Voigt
                             33, 0.1, 200, 0.09  # RooCMS
                            ]
            elif j == 2:
                if i == 0:
                    pPass = [
                            3e5,   5e3, 
                            0.1, 2, 15,       # Voigt
                            10,0.1, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                            1.5e5,   5e4, 
                            1, 1, 44,           # Voigt
                            20,0.1, 20, 0.09,  # RooCMS
                            ]
                if i == 2:
                    pPass = [
                            12e5,   5e3, 
                            0.1, 2, 15,       # Voigt
                            30,0.1, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                            1.5e5,   5e4, 
                            1, 1, 44,           # Voigt
                            20,0.1, 20, 0.09,  # RooCMS
                            ]
                if i == 3:
                    pPass = [
                            3e6,   5e3, 
                            0.2, 1.5, 15,       # Voigt
                            5,0.1, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                            8e4,   1e4, 
                            0.1, 1, 44,           # Voigt
                            35,0.1, 20, 0.09,  # RooCMS
                            ]
                if i == 5:
                    pPass = [
                            4e5,   1e3, 
                            1.5, 1.7, 15,       # Voigt
                            3,0.01, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                            1.5e5,   5e4, 
                            1, 1, 44,           # Voigt
                            20,0.01, 20, 0.09,  # RooCMS
                            ]
            elif j == 3:
                if i == 0:
                    pPass = [
                            5e4,   9e3, 
                            #0.1, 2, 15,       # Voigt
                            1, 1, 15,       # Voigt
                            13,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            9e3,   4e3, 
                            1, 1, 44,           # Voigt
                            40,0.01, 20, -0.09,  # RooCMS
                            ]
                elif i == 2:
                    pPass = [
                            5e4,   9e3, 
                            #0.1, 2, 15,       # Voigt
                            1, 1, 15,       # Voigt
                            13,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            9e3,   4e3, 
                            1, 1, 44,           # Voigt
                            40,0.01, 20, -0.09,  # RooCMS
                            ]
                elif i == 3:
                    pPass = [
                            5e4,   9e3, 
                            #0.1, 2, 15,       # Voigt
                            1, 1, 15,       # Voigt
                            13,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            9e3,   4e3, 
                            1, 1, 44,           # Voigt
                            40,0.01, 20, -0.09,  # RooCMS
                            ]
                elif i == 5:
                    pPass = [
                            7e4,   5e3, 
                            0.1, 2, 15,       # Voigt
                            13,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            9e3,   4e3, 
                            1, 1, 44,           # Voigt
                            40,0.01, 20, -0.09,  # RooCMS
                            ]
                else:
                    pPass = [
                            2e5,   5e3, 
                            0.1, 2, 15,       # Voigt
                            13,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            9e3,   4e3, 
                            1, 1, 44,           # Voigt
                            40,0.01, 20, -0.09,  # RooCMS
                            ]
            elif j == 4:
                if i == 0:
                    pPass = [
                            1e5,  4e3,  
                            0.1,  2, 15,  
                            15,-0.1, 100,1,
                            ] 

                    pFail = [
                            8e3,  4e3,  
                            0.1,  2, 44,  
                            42,-0.1, 100,1,
                            ] 
                elif i == 2:
                    pPass = [
                            5e5,  2e4,
                            0.1,  2, 15,  
                            15,-0.1, 100,1,
                            ] 

                    pFail = [
                            4e4,  1e4,
                            0.1,  2, 44,  
                            60,-0.1, 100,1,
                            ] 
                elif i == 3:
                    pPass = [
                            5e5,  2e4,
                            0.1,  2, 15,  
                            15,-0.1, 100,1,
                            ] 

                    pFail = [
                            5e4,  1e4,
                            0.1,  2, 44,  
                            60,0.1, 100,1,
                            ] 
                elif i == 5 :
                    pPass = [
                            1e5,  4e3,
                            0.1,  2, 15,  
                            15,-0.1, 100,1,
                            ] 

                    pFail = [
                            1e4,  3e3,  
                            0.1,  2, 44,  
                            65,-0.1, 100,1,
                            ] 
            elif j == 5:
                if i == 0:
                    pPass = [
                            9e3,  3e2,  
                            0.2,  1, 15,  
                            10,0.1, 1.15814356e+02,1,
                            ] 

                    pFail = [
                            3e3,  3e2,  
                            0.1,  1, 44,  
                            70,-0.1, 1.15814356e+02,1,
                            ] 
                elif i == 2:
                    pPass = [
                            9e4,  3e3,
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            2e4,  3e3,
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
                elif i == 3:
                    pPass = [
                            1e5,  6e2,
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            4e3,  6e2,
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
                elif i == 5:
                    pPass = [
                            1e4,  3e3,
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            2e4,  3e3,
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
                else:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            200,  3e1,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
            elif j == 6:
                if i == 0:
                    pPass = [
                            5e3,  1e2,  
                            0.1,  1, 15,  
                            10,0.1, 1.15814356e+02,1,
                            ] 

                    pFail = [
                            1e3,  1e2,  
                            0.2,  1, 44,  
                            70,-0.1, 1.15814356e+02,1,
                            ] 
                elif i == 2:
                    pPass = [
                            6e3,  3e2,
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            2e3,  3e2,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
                elif i == 3:
                    pPass = [
                            6e3,  3e2,
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            2e3,  3e2,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
                elif i == 5:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            2e3,  3e2,
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
                else:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            200,  3e1,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
            elif j == 7:
                if i == 0:
                    pPass = [
                            3e3,  5e1,
                            0.1,  1, 15,  
                            1,0.1, 1.15814356e+02,1,
                            ] 

                    pFail = [
                            1e3,  5e1,
                            0.1,  1, 44,  
                            70,-0.1, 1.15814356e+02,1,
                            ] 
                elif i == 2:
                    pPass = [
                            3e4,  5e2,
                            0.5,  1, 15,  
                            10,-0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [8e2, 8e2,
                             1, 1, 44, 
                             60, 0.0038985980209962634, -700, 0.015222050465143688
                            ]
                elif i == 3:
                    pPass = [
                            9e3,  3e2,
                            0.5,  1, 15,  
                            10,-0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [2e3, 7e2,
                             1, 1, 44, 
                             0.7044642032043633, 0.0038985980209962634, 1557.2502065025765, 0.015222050465143688
                            ]
                elif i == 5:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,-0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [200, 70,
                             1, 1, 44, 
                             70, 0.0038985980209962634, -700, 0.015222050465143688
                            ]
                else:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,-0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            200,  3e1,  
                            1,  1, 44,  
                            10,-0.1, 1.15814356e+02,0.1,
                            ]  
            elif j == 8:
                if i == 0:
                    pPass = [
                            3e3,  1e2,  
                            0.1,  1, 15,  
                            1,0.1, 1.15814356e+02,1,
                            ] 

                    pFail = [
                            5e2,  1e2,  
                            1,  1, 44,  
                            70,-0.1, 1.15814356e+02,1,
                            ] 
                elif i == 2:
                    pPass = [
                            6e3,  3e2,
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            6e2,  3e2,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
                elif i == 3:
                    pPass = [
                            1e3,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            1e3,  6e2,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,-0.1,
                            ]  
                elif i == 5:
                    pPass = [
                            9e2,  7e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            2e2,  2e2,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02, -0.1,
                            ]  
                else:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            200,  3e1,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
            elif j == 9:
                if i == 0:
                    pPass = [
                            3e3,  1e2,  
                            0.1,  1, 15,  
                            1,0.1, 1.15814356e+02,1,
                            ] 

                    pFail = [
                            1e3,  1e2,  
                            0.1,  1, 44,  
                            70,-0.1, 1.15814356e+02,1,
                            ] 
                elif i == 2:
                    pPass = [
                            6e3,  3e2,
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            6e2,  3e2,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
                elif i == 3:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            1e3,  3e1,  
                            1,  1, 44,  
                            60,  0.1, 1.15814356e+02,0.1,
                            ]  
                elif i == 5:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            200,  3e1,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
                else:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            200,  3e1,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
            elif j == 10:
                if i == 0:
                    pPass = [
                            3e3,  1e2,  
                            0.1,  1, 15,  
                            1,0.1, 1.15814356e+02,1,
                            ] 

                    pFail = [
                            1e3,  1e2,  
                            0.1,  1, 44,  
                            70,-0.1, 1.15814356e+02,1,
                            ] 
                elif i == 2:
                    pPass = [
                            6e3,  3e2,
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            6e2,  3e2,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
                elif i == 3:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            5e2,  3e2,  
                            1,  1, 44,  
                            60,  0.1, 1.15814356e+02,0.1,
                            ]  
                elif i == 5:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            100,  8e1,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
                else:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            200,  3e1,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
            elif j == 11:
                if   i == 0:
                    pPass = [
                            3e3,  1e2,  
                            0.1,  1, 15,  
                            1,0.1, 1.15814356e+02,1,
                            ] 

                    pFail = [
                            2e2,  5e2,  
                            0.1,  1, 44,  
                            70,-0.1, 1.15814356e+02,1,
                            ] 
                elif i == 1:
                    pPass = [
                            8e2,  3e2,
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            8e1,  1e2,  
                            0.1,  1, 44,  
                            40,  0.1, 1.15814356e+02,-0.1,
                            ]  
                elif i == 2:
                    pPass = [
                            4e3,  3e2,
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            1e2,  3e2,  
                            1,  1, 44,  
                            40,  0.1, 1.15814356e+02,0.1,
                            ]  
                elif i == 3:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            1e3,  3e1,  
                            1,  1, 44,  
                            60,  0.1, 1.15814356e+02,0.1,
                            ]  
                elif i == 5:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            200,  3e1,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
                else:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            200,  3e1,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]                      
    elif binsSelected == "Hien":
        if isConv:
            if   j == 0:
                if i != 5:
                    pPass = [
                            5e3,   5e3, 
                            0.1, 1, 14,       # Voigt
                            1,0.1, 0.01, 0.09,  # RooCMS
                            ]

                    pFail = [
                            1.5e3,   5e4, 
                            1, 1.2, 43,       # Voigt
                            30,0.1, 0.01, 0.09,  # RooCMS
                            ]
                else:
                    pPass = [
                            6e3,   5e3, 
                            0.1, 1, 14,       # Voigt
                            1,0.1, 0.01, 0.09,  # RooCMS
                            ]

                    pFail = [
                            3e3,   3e4, 
                            1, 1.2, 43,       # Voigt
                            30,0.1, 0.01, 0.09,  # RooCMS
                            ]
            elif j == 1:
                if i == 0:
                    pPass = [
                            5e4,   7e3, 
                            0.1, 2, 15,       # Voigt
                            10,0.01, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                             3e4, 5e4,
                             2, 0.01, 42,        # Voigt
                             33, 0.1, 200, 0.09  # RooCMS
                            ]
                elif i == 2:
                    pPass = [
                            3e5,   6e4, 
                            0.1, 2, 14,       # Voigt
                            5,0.01, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                             3e4, 5e4,
                             2, 0.01, 42,        # Voigt
                             33, 0.1, 200, 0.09  # RooCMS
                            ]
                elif i == 3:
                    pPass = [
                            5e5,   4e5, 
                            0.1, 2, 14,       # Voigt
                            5,0.01, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                             3e4, 5e4,
                             2, 0.01, 42,        # Voigt
                             33, 0.1, 200, 0.09  # RooCMS
                            ]
                elif i == 5:
                    pPass = [
                            1e5,   8e4, 
                            0.1, 2, 15,       # Voigt
                            5,0.01, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                             1e4, 1e4,
                             2, 0.01, 42,        # Voigt
                             33, 0.1, 200, 0.09  # RooCMS
                            ]
            elif j == 2:
                if i == 0:
                    pPass = [
                            3e5,   5e3, 
                            0.1, 2, 15,       # Voigt
                            10,0.01, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                            1.5e5,   5e4, 
                            1, 1, 44,           # Voigt
                            20,0.01, 20, 0.09,  # RooCMS
                            ]
                if i == 2:
                    pPass = [
                            12e5,   5e3, 
                            0.1, 2, 15,       # Voigt
                            10,0.01, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                            1.5e5,   5e4, 
                            1, 1, 44,           # Voigt
                            20,0.01, 20, 0.09,  # RooCMS
                            ]
                if i == 3:
                    pPass = [
                            1e6,   5e3, 
                            0.1, 1.5, 15,       # Voigt
                            10,0.01, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                            1.5e5,   5e4, 
                            1, 1, 44,           # Voigt
                            20,0.01, 20, 0.09,  # RooCMS
                            ]
                if i == 5:
                    pPass = [
                            1e5,   5e3, 
                            0.1, 2, 15,       # Voigt
                            10,0.01, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                            1.5e5,   5e4, 
                            1, 1, 44,           # Voigt
                            20,0.01, 20, 0.09,  # RooCMS
                            ]
            elif j == 3:
                if i == 0:
                    pPass = [
                            5e4,   9e3, 
                            #0.1, 2, 15,       # Voigt
                            1, 1, 15,       # Voigt
                            13,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            9e3,   4e3, 
                            1, 1, 44,           # Voigt
                            40,0.01, 20, -0.09,  # RooCMS
                            ]
                elif i == 3:
                    pPass = [
                            1e5,   1e4, 
                            0.5, 1, 14,       # Voigt
                            15,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            3e4,   8e3, 
                            1, 1, 44,           # Voigt
                            45,0.01, 20, -0.09,  # RooCMS
                            ]                
                elif i == 5:
                    pPass = [
                            1e4,   5e3, 
                            0.5, 1, 14,       # Voigt
                            15,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            5e3,   5e3, 
                            0.5, 1, 44,           # Voigt
                            45,0.01, 20, -0.09,  # RooCMS
                            ]
                else:
                    pPass = [
                            6e4,   5e3, 
                            0.1, 2, 15,       # Voigt
                            13,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            9e3,   4e3, 
                            1, 1, 44,           # Voigt
                            45,0.01, 20, -0.09,  # RooCMS
                            ]                        
            elif j == 4:
                if i == 0:
                    pPass = [
                            1e3,  200,  
                            0.5,  1, 15,  
                            15,1, 10,-0.09,
                            ] 

                    pFail = [
                            1e2,  3e1,  
                            0.5,  1, 44,  
                            49,-0.1, 10, -0.09,  # RooCMS
                            ]  
                elif i == 2:
                    pPass = [
                            7e3,  200,  
                            0.5,  1, 15,  
                            15,1, 10,-0.09,
                            ] 

                    pFail = [
                            5e2,  5e2,  
                            0.5,  1, 44,  
                            35,-0.1, 10, -0.09,  # RooCMS
                            ] 
                elif i == 3:
                    pPass = [
                            5e3,  200,  
                            0.1,  1, 15,  
                            15,1, 10,-0.09,
                            ] 

                    pFail = [
                            5e2,  1e2,  
                            0.1,  1, 44,  
                            48,-0.1, 10, -0.09,  # RooCMS
                            ] 
                elif i == 5:
                    pPass = [1.22435554e+03, 3.20343246e+02, 9.22998413e-12,
                             1.10974344e+00, 1.50406031e+01, 1.40180622e+01,
                             6.13551539e-01, 1.00000028e+01, 5.95495234e-01]
                    pFail = [ 4.08455718e+02,  2.34193103e+02,  1.08171908e+00,
                             9.14064665e-01, 4.39415340e+01,  5.75583581e+01, 
                             -5.13886755e-01,  3.82617111e+03,-4.43517032e-02]
                else :
                    pPass = [
                            1e3,  100,  
                            0.5,  1, 15,  
                            15,0.1, 10,-0.09,
                            ] 

                    pFail = [
                            2e2,  1e2,  
                            0.1,  1, 44,  
                            45,0.01, 10, -0.09,  # RooCMS
                            ]                                        
            elif j == 5:
                if i == 0:
                    pPass = [
                            6e4,  1e2,  
                            0.1,  2, 15,  
                            1,1, 1.15814356e+02,1,
                            ] 

                    pFail = [
                            1e3,  1e2,  
                            0.1,  2, 44,  
                            35,  1, 1.15814356e+02,1,
                            ] 
                elif i == 1:
                    pPass = [
                            2e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            2e1,  1e1,  
                            0.5,  1, 44,  
                            48,  -0.1, 10,0.1,
                            ]   
                else:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            40,  3e1,  
                            1,  1, 44,  
                            35,  0.1, 1.15814356e+02,0.1,
                            ]  
        else:
            if   j == 0:
                if  i == 0:
                    pPass = [
                            1e4,   5e3, 
                            0.1, 1, 14,       # Voigt
                            1,0.1, 0.01, 0.09,  # RooCMS
                            ]

                    pFail = [
                            4e3,   2e4, 
                            1, 1.2, 43,       # Voigt
                            30,0.1, 0.01, 0.09,  # RooCMS
                            ]
                elif i != 5:

                    pPass = [
                            1e4,   5e3, 
                            0.1, 1, 14,       # Voigt
                            1,0.1, 0.01, 0.09,  # RooCMS
                            ]

                    pFail = [
                            1.5e3,   5e4, 
                            1, 1.2, 43,       # Voigt
                            30,0.1, 0.01, 0.09,  # RooCMS
                            ]
                elif i == 5:
                    pPass = [
                            5e4,   2e3, 
                            0.1, 1, 14,       # Voigt
                            1,0.1, 0.01, 0.09,  # RooCMS
                            ]

                    pFail = [
                            4e3,   2e4, 
                            1, 1.2, 43,       # Voigt
                            10,0.1, 0.01, 0.09,  # RooCMS
                            ]
            elif j == 1:
                if i == 0:
                    pPass = [
                            1e5,   7e3, 
                            0.1, 2, 15,       # Voigt
                            10,0.1, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                             3e4, 5e4,
                             2, 0.01, 43,        # Voigt
                             33, 0.1, 200, 0.09  # RooCMS
                            ]
                elif i == 2:
                    pPass = [
                            5e5,   6e4, 
                            0.1, 2, 15,       # Voigt
                            5,0.1, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                             2e4, 5e4,
                             2, 0.01, 43,        # Voigt
                             33, 0.1, 200, 0.09  # RooCMS
                            ]
                elif i == 3:
                    pPass = [
                            5e5,   1e5, 
                            0.1, 2, 14,       # Voigt
                            10,0.1, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                             3e4, 5e4,
                             2, 0.01, 43,        # Voigt
                             33, 0.1, 200, 0.09  # RooCMS
                            ]
                elif i == 5:
                    pPass = [
                            1e5,   8e4, 
                            0.1, 2, 15,       # Voigt
                            30,0.01, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                             1e4, 1e4,
                             2, 0.01, 43,        # Voigt
                             33, 0.1, 200, 0.09  # RooCMS
                            ]
            elif j == 2:
                if i == 0:
                    pPass = [
                            3e5,   5e3, 
                            0.1, 2, 15,       # Voigt
                            10,0.1, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                            1.5e5,   5e4, 
                            1, 1, 44,           # Voigt
                            20,0.1, 20, 0.09,  # RooCMS
                            ]
                if i == 2:
                    pPass = [
                            12e5,   5e3, 
                            0.1, 2, 15,       # Voigt
                            30,0.1, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                            1.5e5,   5e4, 
                            1, 1, 44,           # Voigt
                            20,0.1, 20, 0.09,  # RooCMS
                            ]
                if i == 3:
                    pPass = [
                            3e6,   5e3, 
                            0.2, 1.5, 15,       # Voigt
                            5,0.1, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                            8e4,   1e4, 
                            0.1, 1, 44,           # Voigt
                            35,0.1, 20, 0.09,  # RooCMS
                            ]
                if i == 5:
                    pPass = [
                            4e5,   1e3, 
                            1.5, 1.7, 15,       # Voigt
                            3,0.01, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                            1.5e5,   5e4, 
                            1, 1, 44,           # Voigt
                            20,0.01, 20, 0.09,  # RooCMS
                            ]
            elif j == 3:
                if i == 0:
                    pPass = [
                            5e4,   9e3, 
                            #0.1, 2, 15,       # Voigt
                            1, 1, 15,       # Voigt
                            13,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            9e3,   4e3, 
                            1, 1, 44,           # Voigt
                            40,0.01, 20, -0.09,  # RooCMS
                            ]
                elif i == 2:
                    pPass = [
                            5e4,   9e3, 
                            #0.1, 2, 15,       # Voigt
                            1, 1, 15,       # Voigt
                            13,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            9e3,   4e3, 
                            1, 1, 44,           # Voigt
                            40,0.01, 20, -0.09,  # RooCMS
                            ]
                elif i == 3:
                    pPass = [
                            5e4,   9e3, 
                            #0.1, 2, 15,       # Voigt
                            1, 1, 15,       # Voigt
                            13,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            9e3,   4e3, 
                            1, 1, 44,           # Voigt
                            40,0.01, 20, -0.09,  # RooCMS
                            ]
                elif i == 5:
                    pPass = [
                            7e4,   5e3, 
                            0.1, 2, 15,       # Voigt
                            13,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            9e3,   4e3, 
                            1, 1, 44,           # Voigt
                            40,0.01, 20, -0.09,  # RooCMS
                            ]
                else:
                    pPass = [
                            2e5,   5e3, 
                            0.1, 2, 15,       # Voigt
                            13,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            9e3,   4e3, 
                            1, 1, 44,           # Voigt
                            40,0.01, 20, -0.09,  # RooCMS
                            ]
            elif j == 4:
                if i == 0:
                    pPass = [
                            5e3,  200,  
                            0.1,  2, 15,  
                            15,-0.1, 100,1,
                            ] 

                    pFail = [
                            4e2,  1e2,  
                            0.1,  2, 44,  
                            42,-0.1, 100,1,
                            ] 
                elif i == 2:
                    pPass = [
                            5e3,  200,  
                            0.1,  2, 15,  
                            15,-0.1, 100,1,
                            ] 

                    pFail = [
                            4e2,  1e2,  
                            0.1,  2, 44,  
                            60,-0.1, 100,1,
                            ] 
                elif i == 3:
                    pPass = [
                            5e3,  200,  
                            0.1,  2, 15,  
                            15,-0.1, 100,1,
                            ] 

                    pFail = [
                            5e2,  1e2,  
                            0.1,  2, 44,  
                            60,0.1, 100,1,
                            ] 
                else :
                    pPass = [
                            5e3,  200,  
                            0.1,  2, 15,  
                            15,-0.1, 100,1,
                            ] 

                    pFail = [
                            5e2,  1e2,  
                            0.1,  2, 43,  
                            42,-0.1, 100,1,
                            ] 
            elif j == 5:
                if i == 0:
                    pPass = [
                            3e3,  1e2,  
                            0.1,  1, 15,  
                            1,0.1, 1.15814356e+02,1,
                            ] 

                    pFail = [
                            1e3,  1e2,  
                            0.1,  1, 44,  
                            70,-0.1, 1.15814356e+02,1,
                            ] 
                elif i == 1:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            200,  3e1,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  

    #################################
    
    BoundedFit = [
                   [0,0,
                    0,0,10,
                    #0,-np.inf,-np.inf,-1],
                    #0,-0.9,-np.inf,-0.9],
                    0,-0.3,-np.inf,-0.9],
                   [np.inf,np.inf,
                    3,3,48,
                    #70,np.inf,np.inf,1,
                    #70, 0.9, np.inf,0.9,
                    70, 0.3, np.inf,0.9,
                   ]
                    ]
        
    return pPass, pFail, BoundedFit


# In[ ]:


pPass = [
        5e3,   5e3, 
        0.1, 1, 14,       # Voigt
        1,0.1, 0.01, 0.09,  # RooCMS
        ]
pFail = [
        1.5e3,   5e4, 
        1, 1.2, 43,       # Voigt
        30,0.1, 0.01, 0.09,  # RooCMS
        ]


fit = Fit_Curve_CHI(
                DATA_PASS = Data['Pass'][0][3][3],
                DATA_FAIL = Data['Fail'][0][3][3],
                pPass = pPass,pFail = pFail,
                )

#fit
m = fit[-1]

print("--")


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


def Voigt(x, *arg):
    alpha, gamma, mean = arg
    sigma = alpha / np.sqrt(2 * np.log(2))

    return np.real(wofz(((x-mean) + 1j*gamma)/sigma/np.sqrt(2))) / sigma                                                           /np.sqrt(2*np.pi)

def Voigt_CMS(
                xc,
                NSig, NBkg, 
                sig, Gamma, mean,
                alpha, beta, peak, gamma,
                ):
    x = xc
    arg      = alpha, beta, peak, gamma
    argVoigt = sig, Gamma, mean
    Temp = list(Template(NSig, NBkg, 
                         Voigt(x,*argVoigt) , RooCMSShape(x,*arg)))
    
    '''
    print('| NSig ',NSig, ' | NBkg ',NBkg, '\n'
          '| sig ',sig,'  | Gamma ', Gamma, ' | mean ', mean,'\n'
          '| alpha ', alpha, '  |  beta ',beta, ' | peak ' , peak, ' | gamma ',gamma, '\n'
          '| TEMP ', Temp,'\n\n'
         )
    '''
    return np.array(Temp)
##################################################################

'''
VoigtCMS = lambda x,*x0 : Voigt_CMS(
                                        x,
                                        NSig  =  x0[0], NBkg  =  x0[1],
                                        sig   =  x0[2], Gamma =  x0[3], mean =  x0[4],
                                        alpha =  x0[5], beta  =  x0[6], peak =  x0[7], gamma = x0[8], 
                                        )
xFit = np.arange(0,len(Data['Pass'][0][3][3]))
chi2 = lambda *x0 : CHI2(Data['Pass'][0][3][3],VoigtCMS(xFit,*x0))
chi2(pPass)                                        
'''         
xFit = np.arange(0,len(Data['Pass'][0][3][3]))
chi2 =lambda NSig , NBkg ,              sig  , Gamma, mean,              alpha, beta , peak, gamma : CHI2(   Data['Pass'][0][3][3],
                                                Voigt_CMS(
                                                    xc = xFit, \
                                                    NSig=NSig , NBkg=NBkg , \
                                                    sig = sig  , Gamma  = Gamma, mean = mean, \
                                                    alpha = alpha, beta = beta , peak = peak, gamma = gamma,  
                                                    ) 
                                                )
print(chi2(*pPass) )


# In[ ]:





# In[ ]:





# In[ ]:


x0 = pPass

BoundedFit = [
               [0,0,
                0,0,10,
                0,-0.2,-1000,-1],
               [np.inf,np.inf,
                3,3,48,
                70,0.2,1000,1,
                ]
            ] 

'''
errorFit = [1,1,
            0.01,0.1,1,0.1,
            0.01,0.001,0.001
           ]
'''

errorFit = [1,1,
            0.001,0.01,1,0.01,
            0.001,0.001,0.001
           ]

m = Minuit( chi2,
            NSig  =  x0[0], NBkg  =  x0[1],
            sig   =  x0[2], Gamma =  x0[3], mean =  x0[4],
            alpha =  x0[5], beta  =  x0[6], peak =  x0[7], gamma = x0[8], 
            error_NSig  =  errorFit[0], error_NBkg  =  errorFit[1],
            error_sig   =  errorFit[2], error_Gamma =  errorFit[3], error_mean =  errorFit[4],
            error_alpha =  errorFit[5], error_beta  =  errorFit[6], error_peak =  errorFit[7], error_gamma = errorFit[8], 
            limit_NSig  =  (BoundedFit[0][0],BoundedFit[1][0]), limit_NBkg  =  (BoundedFit[0][1],BoundedFit[1][1]),
            limit_sig   =  (BoundedFit[0][2],BoundedFit[1][2]), limit_Gamma =  (BoundedFit[0][3],BoundedFit[1][3]), limit_mean =  (BoundedFit[0][4],BoundedFit[1][4]),
            limit_alpha =  (BoundedFit[0][5],BoundedFit[1][5]), limit_beta  =  (BoundedFit[0][6],BoundedFit[1][6]), limit_peak =  (BoundedFit[0][7],BoundedFit[1][7]), limit_gamma = (BoundedFit[0][8],BoundedFit[1][8]), 
            errordef = 0.5,
          )
    
m.get_param_states()


# In[ ]:


'''
chi2(*x0)

chi2(NSig  =  x0[0], NBkg  =  x0[1],
    sig   =  x0[2], Gamma =  x0[3], mean =  x0[4],
    alpha =  x0[5], beta  =  x0[6], peak =  x0[7], gamma = x0[8], )
'''
m.migrad()


# In[ ]:


m.get_fmin()


# In[ ]:


pprint(m.get_fmin())


# In[ ]:


States = m.get_param_states()

pprint(m.get_param_states())


# In[ ]:


#m.hesse()


# In[ ]:


m.matrix(correlation=True)


# In[ ]:


m.matrix()


# In[ ]:


m.errors


# In[ ]:


m.values


# In[ ]:


fit


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


def assErr(k,N):
    a, b = 0.001,1
    steps = 1000
    beta = np.arange(a,b,step = (b-a)/steps)

    Beta  = spc.betainc(k+1,N-k+1,beta)
    Sols = [[100 if np.isnan(Bs-As-lamb) else np.abs(Bs-As-lamb) for Bs in Beta] for As in Beta]

    i = int(np.argmin(Sols)/steps)
    j = int(np.argmin(Sols)- i*steps)

    intLow, intHigh = beta[i],beta[j]
    print(np.argmin(Sols),np.min(Sols),Sols[i][j])
    print(i,j)


# In[ ]:


def OptYield(P0,model,index = 0,Ni=0,Nf=2e6,step=100,Plot=True):
    mod = []
    lambP = np.arange(Ni,Nf,step = step) #LAMB 0


    for p1 in lambP:
        P0[index] = p1
        mod.append(model(P0))
        
    if Plot:
        plt.figure()
        plt.plot(lambP,mod)
        ax = plt.gca()
        ax.set_yscale('log')

    return lambP[np.argmin(mod)]


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


###################################

#FitType = 'Voigt_Exp'
#FitType = 'Voigt_CMS'
FitType = 'Voigt_Curve'

###################################      
    
etaBinsEBEE    = [[0,1.4442],[1.566,2.5]]
etaBins,ptBins = BinFormat(etaBins), BinFormat(ptBins)
etaNBin,ptNBin = len(etaBins),len(ptBins)

eff, effStat  = {}, {}

fit = []
fig  =  plt.figure(1,figsize=(20,20))
fig1 =  plt.figure(2,figsize=(20,20))

for j in np.arange(ptNBin):
    if j in BinEBEE:
        etaBINS = etaBinsEBEE
    else:
        etaBINS = etaBins
    eff[j],effStat[j] = {},{}
    for i in np.arange(len(etaBINS)):
        
        #if j != 3 or i != 3:
        #    continue
            
            
        ij = ptNBin*i + (j+1)     
        IJ = i + (j*etaNBin)
        
        print(' Plotting i'+str(i)+' j'+str(j))
        

        
        if   FitType == 'MC_Exp':
            p0 = [
                    1e5,   1e3, 1e4,   1e3,
                    1, 0.2, 1,   0.2,
                    1, 0.2, 1,   0.2
                    ]

            Bounded = ((0,np.inf),(0,np.inf),(0,np.inf),(0,np.inf),
                       (-np.inf,np.inf),(-np.inf,np.inf),(-np.inf,np.inf),(-np.inf,np.inf),
                       (-np.inf,np.inf),(-np.inf,np.inf),(-np.inf,np.inf),(-np.inf,np.inf))

            Temp = lambda   NSigPass, NBkgPass, NSigFail,NBkgFail,                                      alphaPass, betaPass, peakPass, gammaPass,                                   alphaFail, betaFail, peakFail, gammaFail:                                   T(NSigPass, NBkgPass, NSigFail,NBkgFail,                                      alphaPass, betaPass, peakPass, gammaPass,                                   alphaFail, betaFail, peakFail, gammaFail,                                   MCPass = MC_PASS_S, MCFail = MC_FAIL_S)    
        elif FitType == 'Voigt_Exp':
            p0 = [
                    1e3,   1e5, 5e3,   1e5,
                    0.1, 0.1, 14,
                    0.03, 0,
                    0.1, 0.1, 14,
                    0.03, 0,
                    ]
            Bounded = (
                        (0,np.inf),(0,np.inf),(0,np.inf),(0,np.inf),
                        (0.01,4),(0.01,4),(0,40),
                        (-10,10),(0,np.inf),
                        (0.01,4),(0.01,4),(0,40),
                        (-10,10),(0,np.inf),
                      )

            Temp = lambda   NSigPass, NBkgPass, NSigFail,NBkgFail,                                         sigPass, GammaPass, meanPass, lambdaPass, xPass,                               sigFail, GammaFail, meanFail, lambdaFail, xFail:                               TVoigt_Test(NSigPass, NBkgPass, NSigFail,NBkgFail,                                         sigPass, GammaPass, meanPass,                                                  lambdaPass, xPass,                                                             sigFail, GammaFail, meanFail,                                                  lambdaFail, xFail,                                                             MCPass = MC_PASS_S, MCFail = MC_FAIL_S)    
        elif FitType == "Voigt_noSig":
            p0 = [
                    1e5,   1e5,
                    0.1, 0.1, 14,
                    0.03, 0,
                    0.1, 0.1, 14,
                    0.03, 0,
                    ]
            Bounded = (
                        (0,np.inf),(0,np.inf),
                        (0.01,4),(0.01,4),(0,40),
                        (-10,10),(0,np.inf),
                        (0.01,4),(0.01,4),(0,40),
                        (-10,10),(0,np.inf),
                      )
            Temp = lambda   NBkgPass,NBkgFail,                                                             sigPass, GammaPass, meanPass, lambdaPass, xPass,                               sigFail, GammaFail, meanFail, lambdaFail, xFail:                               TVoigt_noSig(NBkgPass,NBkgFail,                                                             sigPass, GammaPass, meanPass,                                                  lambdaPass, xPass,                                                             sigFail, GammaFail, meanFail,                                                  lambdaFail, xFail,                                                             MCPass = MC_PASS_S, MCFail = MC_FAIL_S)    
        elif FitType == 'Voigt_CMS':   
            p0 = [
                    1e2,   2e2, 1e2,   4e2,
                    0.1, 2, 14,                 # Voigt
                    1,1, 0.01, 0.05, # RooCMS
                    0.1, 2, 43,                 # Voigt
                    1, 1, 0.01, 0.05, # RooCMS
                    ]

            Bounded = (
                        (0,np.inf),(0,np.inf),(0,np.inf),(0,np.inf),
                        (0.01,20),(0.01,20),(0,30),
                        (-np.inf,np.inf),(-np.inf,np.inf),(-np.inf,np.inf),(-np.inf,np.inf),
                        (0.01,20),(0.01,20),(0,60),
                        (-np.inf,np.inf),(-np.inf,np.inf),(-np.inf,np.inf),(-np.inf,np.inf),
                      )

            Temp = lambda   NSigPass, NBkgPass, NSigFail,NBkgFail,                             sigPass, GammaPass, meanPass, alphaPass, betaPass, peakPass, gammaPass,                             sigFail, GammaFail, meanFail, alphaFail, betaFail, peakFail, gammaFail:                             TVoigt_CMS(NSigPass, NBkgPass, NSigFail,NBkgFail,                                        sigPass, GammaPass, meanPass, alphaPass, betaPass, peakPass, gammaPass,                                        sigFail, GammaFail, meanFail, alphaFail, betaFail, peakFail, gammaFail,                                        MCPass = MC_PASS_S, MCFail = MC_FAIL_S) 
        elif FitType == 'Voigt_x':
            p0 = [ 2.10010102e+04,  3.34421859e+03,  9.73858331e+03,  2.53360134e+04,
                    2.44107828e+00,  8.74878690e-01,  1.30304384e+01,  7.13139484e+00,
                   -1.30489487e+01,  1.99560639e+01,  4.61991664e-02,  2.34434414e+00,
                    9.74446121e-01,  4.20876696e+01,  3.00000000e+00,  3.00000000e+00,
                    1.97578463e+02,  7.12292034e-02]
            BoundedFit = [
                           [0,0,0,0,
                            0.01,0.01,0,
                            -np.inf,-np.inf,-np.inf,-np.inf,
                            0.01,0.01,30,
                            -np.inf,-np.inf,-np.inf,-np.inf],
                           [np.inf,np.inf,np.inf,np.inf,
                            5,5,30,
                            np.inf,np.inf,np.inf,np.inf,
                            5,5,60,
                            np.inf,np.inf,np.inf,np.inf,
                            ]
                          ]
        elif FitType == 'Voigt_Curve':
            if( SkipGap(i,j,binsSelected) ):
                eff[j][i] = 0
                effStat[j][i] = 0
                continue
    
            pPass,pFail, BoundedFit = InitializeParams(i,j,binsSelected)
            


                
        BoundedFit = [
                       [0,0,
                        0,0,10,
                        #-np.inf,-2,-np.inf,-2],
                        #0,-np.inf,-np.inf,-1],
                        0,-0.2,-np.inf,-1],
                       [np.inf,np.inf,
                        3,3,48,
                        #70,np.inf,np.inf,1,
                        70,0.2,np.inf,1,
                        ]
                    ]                

        ##################################################################

        ##################################################################
        print('--- Fitting')    
        #FitP, FitF,FitPSig, FitFSig = Fit_Curve(
        FitP, FitF,FitPSig, FitFSig,mP,mF = Fit_Curve_CHI(
                                                DATA_PASS = Data['Pass'][0][j][i],
                                                DATA_FAIL = Data['Fail'][0][j][i],
                                                pPass = pPass,pFail = pFail,
                                                Bounded = BoundedFit,
                                                )
        
        DATA = {"names" : mP.values.keys(),
                "values": mP.values.values(),
                "error" : mP.errors.values()
               }
        df = pd.DataFrame(DATA,columns=["names","values","error"])
        if isConv:
            df.to_csv(figpath+binsSelected+"/isConv/"+"FitValues_"+str(ptBins[j][0])+"_pt_"+str(ptBins[j][1])+"_"+str(etaBins[i][0])+"_eta_"+str(etaBins[i][1])+".csv")
        else:
            df.to_csv(figpath+binsSelected+"/ID/"+"FitValues_"+str(ptBins[j][0])+"_pt_"+str(ptBins[j][1])+"_"+str(etaBins[i][0])+"_eta_"+str(etaBins[i][1])+".csv")
            
        DATA = {"names" : mF.values.keys(),
                "values": mF.values.values(),
                "error" : mF.errors.values()
               }
        df = pd.DataFrame(DATA,columns=["names","values","error"])
        if isConv:
            df.to_csv(figpath+binsSelected+"/isConv/"+"FitValues_"+str(ptBins[j][0])+"_pt_"+str(ptBins[j][1])+"_"+str(etaBins[i][0])+"_eta_"+str(etaBins[i][1])+".csv")
        else:
            df.to_csv(figpath+binsSelected+"/ID/"+"FitValues_"+str(ptBins[j][0])+"_pt_"+str(ptBins[j][1])+"_"+str(etaBins[i][0])+"_eta_"+str(etaBins[i][1])+".csv")        
        ##################################################################
        
        ##################################################################
        PassFail = 'Pass'
        xs = np.arange(0,len(Data[PassFail][0][j][i]))

        if   FitType == 'MC_Exp':
            expParam = tuple(FIT[4:8])
            NSig = FIT[0]
            NBkg = FIT[1]

            SIG = MC[PassFail]['DYJets'][0][j][i]/np.sum(MC[PassFail]['DYJets'][0][j][i])
            BKG = RooCMSShape(xc,*expParam)/np.sum(RooCMSShape(xc,*expParam))
            
            eff[j][i] = FIT[0]/(FIT[0]+FIT[2])
        elif FitType == 'Voigt_Exp':
            argVoigt = FIT[4:7]
            argExp   = FIT[7:9]

            NSig = FIT[0]
            NBkg = FIT[1]

            SIG = Voigt(xs, *argVoigt)/np.sum(Voigt(xs, *argVoigt))
            BKG = Exp  (xs, *argExp)  /np.sum(Exp  (xs, *argExp))
            
            eff[j][i] = FIT[0]/(FIT[0]+FIT[2])
        elif FitType == 'Voigt_CMS':
            argVoigt = FIT[4:7]
            argExp   = FIT[7:11]

            NSig = FIT[0]
            NBkg = FIT[1]

            SIG = Voigt(xs, *argVoigt)/np.sum(Voigt(xs, *argVoigt))
            BKG = RooCMSShape(xs, *argExp)  /np.sum(RooCMSShape(xs, *argExp))
            
            eff[j][i] = FIT[0]/(FIT[0]+FIT[2])
        elif FitType == 'Voigt_x':
            argVoigt = FIT[4:7]
            argExp   = FIT[7:11]

            NSig = FIT[0]
            NBkg = FIT[1]

            SIG = Voigt(xs, *argVoigt)/np.sum(Voigt(xs, *argVoigt))
            BKG = RooCMSShape(xs, *argExp)  /np.sum(RooCMSShape(xs, *argExp))
            
            eff[j][i] = FIT[0]/(FIT[0]+FIT[2])
        elif FitType == 'Voigt_Curve':
            argVoigt = FitP[2:5]
            argExp   = FitP[5:9]

            NSig = FitP[0]
            NBkg = FitP[1]

            SIG = Voigt(xs, *argVoigt)/np.sum(Voigt(xs, *argVoigt))
            BKG = RooCMSShape(xs, *argExp)  /np.sum(RooCMSShape(xs, *argExp))
            
            Num,dNum = FitP[0], FitPSig[0]
            Dem, dDem = (FitP[0]+FitF[0]), FitPSig[0]+FitFSig[0]
            
            eff[j][i] = Num/Dem
            effStat[j][i] = Num/Dem*np.sqrt((dNum/Num)**2 + (dDem/Dem)**2)
        
            print("Nsig: ",NSig)
            print("eff: ",eff[j][i]," | deff ",effStat[j][i])
                
        if np.isnan(eff[j][i]):
            eff[j][i] = 0.0
            
        plt.figure(1)
        ax = plt.subplot(len(etaBins),len(ptBins),ij)
        color = ['b','g','r']

        print('--- Plotting Pass')    
        PlotFitting(
                    ax,
                    NSig = NSig, NBkg = NBkg,
                    DATA = Data[PassFail][0][j][i],
                    SIG  = SIG,
                    BKG  = BKG,
                    eta  = etaBINS[i], pt = ptBins[j],
                    color = color,
                   )
        '''
        ax.text(60,max(SIG)*0.5,
                 'NSig = '+str(round(NSig))+' +/- '+str(FitPSig[0]),
                 fontsize = 2)
        ax.text(60,max(SIG)*0.5,
                 'NBkg = '+str(round(NBkg))+' +/- '+str(FitPSig[1]),
                 fontsize = 2)
        '''
        
        
        ####################################################################################
        PassFail = 'Fail'
        xs = np.arange(len(Data[PassFail][0][j][i]),len(Data[PassFail][0][j][i])*2)

        if   FitType == 'MC_Exp':
            expParam = tuple(FIT[8:12])

            NSig = FIT[2]
            NBkg = FIT[3]

            SIG = MC[PassFail]['DYJets'][0][j][i]/np.sum(MC[PassFail]['DYJets'][0][j][i])
            BKG = RooCMSShape(xc,*expParam)/np.sum(RooCMSShape(xc,*expParam))   
        elif FitType == 'Voigt_Exp':
            argVoigt = FIT[9:12]
            argExp   = FIT[12:14]

            NSig = FIT[2]
            NBkg = FIT[3]

            SIG = Voigt(xs, *argVoigt)/np.sum(Voigt(xs, *argVoigt))
            BKG = Exp  (xs, *argExp)  /np.sum(Exp  (xs, *argExp))
        elif FitType == 'Voigt_CMS':
            argVoigt = FIT[11:14]
            argExp   = FIT[14:18]

            NSig = FIT[2]
            NBkg = FIT[3]

            SIG = Voigt(xs, *argVoigt)/np.sum(Voigt(xs, *argVoigt))
            BKG = RooCMSShape(xs, *argExp)/np.sum(RooCMSShape(xs, *argExp))   
        elif FitType == 'Voigt_x':
            argVoigt = FIT[11:14]
            argExp   = FIT[14:18]

            NSig = FIT[2]
            NBkg = FIT[3]

            SIG = Voigt(xs, *argVoigt)/np.sum(Voigt(xs, *argVoigt))
            BKG = RooCMSShape(xs, *argExp)/np.sum(RooCMSShape(xs, *argExp))  
        elif FitType == 'Voigt_Curve':
            argVoigt = FitF[2:5]
            argExp   = FitF[5:9]

            NSig = FitF[0]
            NBkg = FitF[1]

            SIG = Voigt(xs, *argVoigt)/np.sum(Voigt(xs, *argVoigt))
            BKG = RooCMSShape(xs, *argExp)  /np.sum(RooCMSShape(xs, *argExp))

        print('--- Plotting Fail')    
        plt.figure(2)
        ax1 = plt.subplot(len(etaBins),len(ptBins),ij)
        color = ['slateblue','olivedrab','firebrick']

        PlotFitting(
                    ax1,
                    NSig = NSig, NBkg = NBkg,
                    DATA = Data[PassFail][0][j][i],
                    SIG  = SIG,
                    BKG  = BKG,
                    eta  = etaBINS[i], pt = ptBins[j],
                    color = color,
                   )
        '''
        ax.text(60,max(SIG)*0.5,
                 'NSig = '+str(round(NSig))+' +/- '+str(FitFSig[0]),
                 fontsize = 2)
        ax.text(60,max(SIG)*0.5,
                 'NBkg = '+str(round(NBkg))+' +/- '+str(FitFSig[1]),
                 fontsize = 2)
        '''
        ####################################################################################
        print("\n")
        
fig.tight_layout()        
fig1.tight_layout()        

     
fig.suptitle("FitPass",y=1)
fig1.suptitle("FitFail",y=1) 

if isConv:
    fig .savefig(figpath+binsSelected+"/isConv/"+"FitPass.png")        
    fig1.savefig(figpath+binsSelected+"/isConv/"+"FitFail.png")     
else:
    fig .savefig(figpath+binsSelected+"/ID/"+"FitPass_Exp.png")        
    fig1.savefig(figpath+binsSelected+"/ID/"+"FitFail_Exp.png")     
plt.show()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


path = "/home/jcordero/CMS/JYCMCMS/SMP_ZG/python/Efficiency/zee/"
if isConv:
    fileOut = TFile(figpath+binsSelected+"/isConv/"+"eff_photon_data.root","recreate")
else:
    fileOut = TFile(figpath+binsSelected+"/ID/"+"eff_photon_data_VoigtCMS.root","recreate")
tree = TTree("eff_photon","eff_photon")

##################################################
ptBins, etaBins = BinFormat(ptBins,Type = 'edges'),BinFormat(etaBins,Type = 'edges')

ptNBins, etaNBins = len(ptBins)-3 , len(etaBins)-1
histDraw = TH2F("EGamma_eff_draw","Eff",
              ptNBins ,ptBins,
              etaNBins,etaBins)


ptNBins, etaNBins = len(ptBins)-1 , len(etaBins)-1
hist2d = TH2F("EGamma_eff","Eff",
              ptNBins ,ptBins,
              etaNBins,etaBins)


ptNBins, etaNBins = len(ptBins)-2 , len(etaBins)-1
statDraw = TH2F("EGamma_eff_stat_draw","Eff",
              ptNBins ,ptBins,
              etaNBins,etaBins)


ptNBins, etaNBins = len(ptBins)-1 , len(etaBins)-1
stat2d = TH2F("EGamma_eff_stat","Eff",
              ptNBins ,ptBins,
              etaNBins,etaBins)

etaBins = BinFormat(etaBins)
##################################################
tree.Branch("eff",hist2d,"TH2F")
tree.Branch("eff",hist2d,"TH2F")
for j in range(ptNBins):
    hist2d.GetZaxis().SetRangeUser(0.6,1.1)
    if j in BinEBEE:
        etaBINS = etaBinsEBEE
    else:
        etaBINS = etaBins
        
    if len(etaBINS) > 2:
        for i in np.arange(len(etaBINS)):
            hist2d.SetBinContent(int(j)+1, int(i)+1, eff[j][i])
            histDraw.SetBinContent(int(j)+1, int(i)+1, eff[j][i])
            
            stat2d.SetBinContent(int(j)+1, int(i)+1, effStat[j][i])
            statDraw.SetBinContent(int(j)+1, int(i)+1, effStat[j][i])
            tree.Fill()
    else:
        for i in range(len(etaBins)):
            if np.abs(np.average(etaBins[i])) > 1.566:
                EFF = eff[j][0]
                EFFStat =  effStat[j][0]
            elif np.abs(np.average(etaBins[i])) < 1.4442:
                EFF = eff[j][1]
                EFFStat =  effStat[j][1]
                I = 2
            else:
                EFF = 0
                EFFStat =  0
            hist2d.SetBinContent(int(j)+1, int(i)+1, EFF)
            histDraw.SetBinContent(int(j)+1, int(i)+1, EFF)
            
            stat2d.SetBinContent(int(j)+1, int(i)+1, EFFStat)
            statDraw.SetBinContent(int(j)+1, int(i)+1, EFFStat)
            tree.Fill()
    
    
fileOut.Write()
#fileOut.Close()


# In[ ]:


c = TCanvas()
if isConv:
    hist2d.GetZaxis().SetRangeUser(0.85,0.94)
else:
    hist2d.GetZaxis().SetRangeUser(0.6,0.96)
hist2d.Draw("colz text")
c.SetLogx()
c.Draw()


# In[ ]:





# 

# In[ ]:


c = TCanvas()
histDraw.SetTitle("T&P Efficiency Data")
if isConv:
    histDraw.GetZaxis().SetRangeUser(0.85,0.94)
else:
    histDraw.GetZaxis().SetRangeUser(0.6,0.96)
histDraw.GetXaxis().SetTitle('pt')
histDraw.GetYaxis().SetTitle(r'\eta')
histDraw.Draw("colz text")

#gStyle.SetPaintTextFormat("4.3f +/-")
statDraw.SetBarOffset(-0.15)
statDraw.Draw("text same")
c.SetLogx()
if isConv:
    c.SaveAs(figpath+binsSelected+"/isConv/"+"EFF_data_photonID.png")
else:
    c.SaveAs(figpath+binsSelected+"/ID/"+"EFF_data_photonID.png")
c.Draw()


# In[ ]:


c = TCanvas()
statDraw.SetTitle("T&P Uncertainties Data")
#statDraw.GetZaxis().SetRangeUser(0,0.4)
if isConv:
    statDraw.GetZaxis().SetRangeUser(0,0.023)
else:
    statDraw.GetZaxis().SetRangeUser(0,0.03)
statDraw.GetXaxis().SetTitle('pt')
statDraw.GetYaxis().SetTitle(r'\eta')
statDraw.Draw("colz text")
c.SetLogx()
if isConv:
    c.SaveAs(figpath+binsSelected+"/isConv/"+"EFF_UNC_data_photonID.png")
else:
    c.SaveAs(figpath+binsSelected+"/ID/"+"EFF_UNC_data_photonID.png")
c.Draw()


# In[ ]:


fileOut.Close()


# In[ ]:





# In[ ]:


if isConv:
    fileOut = TFile(figpath+binsSelected+"/isConv/"+"sf_photon.root","recreate")
else:
    fileOut = TFile(figpath+binsSelected+"/ID/"+"sf_photon.root","recreate")
tree = TTree("sf_photon","sf_photon")

################################################
ptBins, etaBins = BinFormat(ptBins,Type='edges'),BinFormat(etaBins,Type='edges')

ptNBins,etaNBins = len(ptBins)-2, len(etaBins)-1
histDraw = TH2F("EGamma_sf_draw","SF",
              ptNBins ,ptBins,
              etaNBins,etaBins)


ptNBins,etaNBins = len(ptBins)-1, len(etaBins)-1
hist2d = TH2F("EGamma_sf","SF",
              ptNBins ,ptBins,
              etaNBins,etaBins)

ptNBins,etaNBins = len(ptBins)-2, len(etaBins)-1
statDraw = TH2F("EGamma_sf_stat_draw","SF",
              ptNBins ,ptBins,
              etaNBins,etaBins)


ptNBins,etaNBins = len(ptBins)-1, len(etaBins)-1
stat2d = TH2F("EGamma_sf_stat","SF",
              ptNBins ,ptBins,
              etaNBins,etaBins)


etaBins = BinFormat(etaBins)
################################################

tree.Branch("sf",hist2d,"TH2F")

for j in range(ptNBins):
    #hist2d.GetXaxis().SetRangeUser(0,200)
    hist2d.GetZaxis().SetRangeUser(0.6,1.2)
    if j in BinEBEE:
        etaBINS = etaBinsEBEE
    else:
        etaBINS = etaBins
        
    if len(etaBINS) > 2:
        for i in np.arange(len(etaBINS)):
            
            if effMC[j][i] == 0:
                SF = 0
                SFStat = 0
            else:
                SF = eff[j][i]/effMC[j][i]
                SFStat = SF*np.sqrt((effStat[j][i]/eff[j][i])**2 + (effMCStat[j][i]/effMC[j][i])**2)
            
            hist2d  .SetBinContent(int(j)+1, int(i)+1, SF)
            histDraw.SetBinContent(int(j)+1, int(i)+1, SF)
            
            stat2d  .SetBinContent(int(j)+1, int(i)+1, SFStat)
            statDraw.SetBinContent(int(j)+1, int(i)+1, SFStat)
            tree.Fill()
            #print(j,i,SF)
    else:
        for i in range(len(etaBins)):
            if np.abs(np.average(etaBins[i])) > 1.566:
                SF = eff[j][0]/effMC[j][0]
                SFStat = SF*np.sqrt((effStat[j][0]/eff[j][0])**2 + (effMCStat[j][0]/effMC[j][0])**2)
            elif np.abs(np.average(etaBins[i])) < 1.4442:
                SF = eff[j][1]/effMC[j][1]
                SFStat = SF*np.sqrt((effStat[j][1]/eff[j][1])**2 + (effMCStat[j][1]/effMC[j][1])**2)
                I = 2
            else:
                SF = 0
                SFStat = 0

            hist2d  .SetBinContent(int(j)+1, int(i)+1, SF)
            histDraw.SetBinContent(int(j)+1, int(i)+1, SF)
            
            
            stat2d  .SetBinContent(int(j)+1, int(i)+1, SFStat)
            statDraw.SetBinContent(int(j)+1, int(i)+1, SFStat)
            
            tree.Fill()
            #print(j,i,SF)
hist2d.GetZaxis().SetRangeUser(0.95,1.17)
hist2d.GetXaxis().SetTitle("pt")
hist2d.GetYaxis().SetTitle(r"\eta")

fileOut.Write()
#


# In[ ]:





# In[ ]:


c = TCanvas()
histDraw.SetTitle("Scale Factors Presel PhotonID")
#histDraw.GetZaxis().SetRangeUser(0.9,1.15)
if isConv:
    histDraw.GetZaxis().SetRangeUser(0.91,1)
else:
    histDraw.GetZaxis().SetRangeUser(0.9,1.15)
histDraw.GetXaxis().SetTitle('pt')
histDraw.GetYaxis().SetTitle(r'\eta')
histDraw.Draw("colz text")
c.SetLogx()
if isConv:
    c.SaveAs(figpath+binsSelected+"/isConv/"+"SF_photonID.png")
else:
    c.SaveAs(figpath+binsSelected+"/ID/"+"SF_photonID.png")
c.Draw()


# In[ ]:


c = TCanvas()
statDraw.SetTitle("SF Uncertainties")
#statDraw.GetZaxis().SetRangeUser(0,0.03)
if isConv:
    statDraw.GetZaxis().SetRangeUser(0,0.052)
else:
    statDraw.GetZaxis().SetRangeUser(0,0.042)
statDraw.GetXaxis().SetTitle('pt')
statDraw.GetYaxis().SetTitle(r'\eta')
statDraw.Draw("colz text")
c.SetLogx()
if isConv:
    c.SaveAs(figpath+binsSelected+"/isConv/"+"SF_UNC_photonID.png")
else:
    c.SaveAs(figpath+binsSelected+"/ID/"+"SF_UNC_photonID.png")
c.Draw()


# In[ ]:


c = TCanvas()
if isConv:
    hist2d.GetZaxis().SetRangeUser(0.9,1.0)
else:
    hist2d.GetZaxis().SetRangeUser(0.9,1.15)
hist2d.Draw("colz text")
c.SetLogx()
c.Draw()


# In[ ]:


fileOut.Close()


# # -------------------------------------------------------

# # Projections

# In[ ]:


ptBins, etaBins =  BinFormat(ptBins), BinFormat(etaBins)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


projVar  = etaBins
otherVar = ptBins
for j in np.arange(len(otherVar)-1):
    fig = plt.figure(figsize=(10,8))
    ###############  Data #######################
    Proj = [eff[j][i]      for i in np.arange(len(projVar))]
    yErr = [effStat[j][i]  for i in np.arange(len(projVar))]
    xErr = np.diff(projVar[:len(Proj)])/2
    Bins = np.array(BinFormat(Bins=projVar[:len(Proj)],Type='edges'))
    Bins = (Bins[:-1]+Bins[1:])/2

    plt.errorbar(Bins,Proj,
                 xerr      = xErr,
                 yerr      = yErr,
                 linestyle = '',
                 marker    = 'o',
                 color     = 'black',
                 label     = 'data',
                )

    ###############  MC #######################
    Proj = [effMC[j][i]      for i in np.arange(len(projVar))]
    yErr = [effMCStat[j][i]  for i in np.arange(len(projVar))]
    xErr = np.diff(projVar[:len(Proj)])/2
    Bins = np.array(BinFormat(Bins=projVar[:len(Proj)],Type='edges'))
    Bins = (Bins[:-1]+Bins[1:])/2
    
    plt.errorbar(Bins,Proj,
                 xerr      = xErr,
                 yerr      = yErr,
                 linestyle = '',
                 marker    = 'o',
                 color     = 'red',
                 label     = 'MC',
                )
    ##################
    ax = plt.gca()
    xlim  = ax.get_xlim()
    ylim  = ax.get_ylim()
    ax.set_ylabel('Efficiency')
    ax.set_xlabel('eta')
    #ax.set_xlabel('pt')
    ax.set_ylim([0.4,1])

    xText = 0.4*(xlim[1]-xlim[0])+xlim[0]
    yText = 0.52

    #Text = str(round(etaBins[i][0],2))+' < '+r'$\eta$'+' < '+ str(round(etaBins[i][1],2))
    Text = str(round(ptBins[j][0],2))+' < Pt < '+ str(round(ptBins[j][1],2))

    ax.text(xText, yText,
           Text,
            fontsize = 20
           )

    xText, yText = 0.05*(xlim[1]-xlim[0])+xlim[0],0.96
    Text = 'CMS'
    ax.text(xText, yText,Text,fontsize = 20,weight='bold')
    xText, yText = 0.05*(xlim[1]-xlim[0])+xlim[0],0.93
    Text = 'Preliminary'
    ax.text(xText, yText,Text,fontsize = 15,fontstyle='italic')

    plt.grid(linestyle='--')
    plt.legend(bbox_to_anchor = (0.4,0.2),
                #loc=[xText,yText+0.1],
               fontsize = 20,
               frameon = False)

    #fig.savefig(figpath+"eff_projPt_eta"+str(round(otherVar[i][0],2))+"_"+str(round(otherVar[i][1],2))+".png")
    if isConv:
        fig.savefig(figpath+binsSelected+"/isConv/"+"eff_projEta_pt"+str(round(otherVar[j][0],2))+"_"+str(round(otherVar[j][1],2))+".png")
    else:
        fig.savefig(figpath+binsSelected+"/ID/"+"eff_projEta_pt"+str(round(otherVar[j][0],2))+"_"+str(round(otherVar[j][1],2))+".png")
    plt.show()


# In[ ]:





# In[ ]:


projVar  = ptBins
otherVar = etaBins
lastBins = False
if lastBins:
    N = 0
else:
    N = 1

for i in np.arange(len(otherVar)):
    if i == 1 or i == 4: continue
    fig = plt.figure(figsize=(10,8))
    ###############  Data #######################
    Proj = [eff[j][i]      for j in np.arange(len(projVar)-N)]
    yErr = [effStat[j][i]  for j in np.arange(len(projVar)-N)]
    xErr = np.diff(projVar[:len(Proj)])/2
    Bins = np.array(BinFormat(Bins = projVar[:len(Proj)],Type = 'edges'))
    Bins = (Bins[:-1]+Bins[1:])/2
    
    plt.errorbar(Bins,Proj,
                 xerr = xErr,
                 yerr = yErr,
                 linestyle = '',
                 marker = 'o',
                 color = 'black',
                 label = 'data',
                )

    ###############  MC #######################
    Proj = [effMC[j][i]      for j in np.arange(len(projVar)-N)]
    yErr = [effMCStat[j][i]  for j in np.arange(len(projVar)-N)]
    xErr = np.diff(projVar[:len(Proj)])/2
    Bins = np.array(BinFormat(Bins=projVar[:len(Proj)],Type = 'edges'))
    Bins = (Bins[:-1]+Bins[1:])/2
    plt.errorbar(Bins,Proj,
                 xerr = xErr,
                 yerr = yErr,
                 linestyle = '',
                 marker = 'o',
                 color = 'red',
                 label = 'MC',
                )
    ##################
    ax = plt.gca()
    xlim  = ax.get_xlim()
    ylim  = ax.get_ylim()
    ax.set_ylabel('Efficiency')
    ax.set_xlabel('eta')
    #ax.set_xlabel('pt')
    ax.set_ylim([0.4,1])

    xText = 0.4*(xlim[1]-xlim[0])+xlim[0]
    yText = 0.52

    Text = str(round(etaBins[i][0],2))+' < '+r'$\eta$'+' < '+ str(round(etaBins[i][1],2))
    #Text = str(round(ptBins[j][0],2))+' < Pt < '+ str(round(ptBins[j][1],2))

    ax.text(xText, yText,
           Text,
            fontsize = 20
           )

    xText, yText = 0.05*(xlim[1]-xlim[0])+xlim[0],0.96
    Text = 'CMS'
    ax.text(xText, yText,Text,fontsize = 20,weight='bold')
    xText, yText = 0.05*(xlim[1]-xlim[0])+xlim[0],0.93
    Text = 'Preliminary'
    ax.text(xText, yText,Text,fontsize = 15,fontstyle='italic')

    plt.grid(linestyle='--')
    plt.legend(bbox_to_anchor = (0.6,0.2),
                #loc=[xText,yText+0.1],
               fontsize = 20,
               frameon = False)

    if isConv:
        fig.savefig(figpath+binsSelected+"/isConv/"+"eff_projPt_eta"+str(round(otherVar[i][0],2))+"_"+str(round(otherVar[i][1],2))+".png")
    else:
        fig.savefig(figpath+binsSelected+"/ID/"+"eff_projPt_eta"+str(round(otherVar[i][0],2))+"_"+str(round(otherVar[i][1],2))+".png")
    #fig.savefig(figpath+"eff_projEta_pt"+str(round(otherVar[j][0],2))+"_"+str(round(otherVar[j][1],2))+".png")
    plt.show()


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


def Voigt_CMS_x(
                xc,
                NSigPass, NBkgPass, NSigFail,NBkgFail, 
                sigPass, GammaPass, meanPass,
                alphaPass, betaPass, peakPass, gammaPass,
                sigFail, GammaFail, meanFail,
                alphaFail, betaFail, peakFail, gammaFail,
                MCPass, MCFail
                ):
    #x = np.arange(0,len(MCPass))
    x = xc[:len(MCPass)]
    argPass      = alphaPass, betaPass, peakPass, gammaPass
    argVoigtPass = sigPass, GammaPass, meanPass
    Pass = list(Template(NSigPass, NBkgPass, 
                         Voigt(x,*argVoigtPass)  , RooCMSShape(x,*argPass))) 
    
    
    #x = np.arange(len(MCPass),len(MCPass)*2)
    x = xc[len(MCPass):len(MCPass)*2]
    argFail      = alphaFail, betaFail, peakFail, gammaFail
    argVoigtFail = sigFail, GammaFail, meanFail
    Fail = list(Template(NSigFail, NBkgFail, 
                         Voigt(x,*argVoigtFail) , RooCMSShape(x,*argFail)))
    
    
    Temp = np.array(Pass + Fail )
    return Temp


# In[ ]:


def Voigt_CMS(
                xc,
                NSig, NBkg, 
                sig, Gamma, mean,
                alpha, beta, peak, gamma,
                ):
    x = xc
    arg      = alpha, beta, peak, gamma
    argVoigt = sig, Gamma, mean
    Temp = list(Template(NSig, NBkg, 
                         Voigt(x,*argVoigt) , RooCMSShape(x,*arg)))
    
    
    return np.array(Temp)


# In[ ]:


PassYield = {}
FailYield = {}
FitPass = {}
FitFail = {}


# In[ ]:


def chiplot(plot,data):
    return np.sum(((plot-data)**2)/data)


# In[ ]:


plt.plot(VoigtCMS(xFit,*FitsFail))
plt.plot(DATA_FAIL)

np.sum((VoigtCMS(xFit,*FitsFail)-DATA_FAIL)**2)
#plt.plot(xFit,Mass)


# In[ ]:


def TextLegend(FitPrams,fit,sig,massFit,mass,chi):
    massFit = np.array(massFit)
    mass = np.array(mass)
    
    i , j = len(mass)-2, 0
    m = (mass[i]-mass[j])/(massFit[i]-massFit[j])
    b = massFit[i]-massFit[j]*m
    
    ndf = len(mass) - len(FitPrams)
    text = 'Chi/ndf: '+str(round(chi/ndf,2)) + '\n'
    for i in np.arange(len(FitPrams)):
        val= fit[i]
        err = sig[i]
        
        if 'mean' in FitPrams[i]:
            val = m*val+b #+ mass[0]
            err = m*err+b
        
        val = str(round(val,2))
        err = str(round(err,2))
        
        text +=  FitPrams[i] + ': ' + val +' +/- '+ err +'\n'
    return text


# In[ ]:


binsSelected = "Optimized"


# In[ ]:



PlotBefore = True
#PlotBefore = False

FailPlot = True
#FailPlot = False

FitPrams = ['NSig','NBkg','sig','Gamma','mean','alpha','beta','peak','gamma']

Mass = np.arange(60,120,step=60/len(xFit))

xTestLoc,rTestLoc = 100,0.15

for j in range(len(ptBins)):
    if j != 2: continue
    PassYield[j] = {}
    FailYield[j] = {}
    FitPass[j] = {}
    FitFail[j] = {}
    for i in range(len(etaBins)):
        print('---------------------- i: '+str(i)+' j: '+str(j)+' -------------------------')
        
        MC_PASS_S = MC['Pass']['DYJets'][0][j][i]#, MC['Pass']['WJets'][0][IJ],
        MC_FAIL_S = MC['Fail']['DYJets'][0][j][i]#, MC['Fail']['WJets'][0][IJ],
        DATA_PASS = Data['Pass'][0][j][i]
        DATA_FAIL = Data['Fail'][0][j][i]
        DATA = np.array(list(DATA_PASS) + list(DATA_FAIL))

        #####################################################
        VoigtCMS = lambda x,*x0 : Voigt_CMS(
                                            x,
                                            NSig  =  x0[0], NBkg  =  x0[1],
                                            sig   =  x0[2], Gamma =  x0[3], mean =  x0[4],
                                            alpha =  x0[5], beta  =  x0[6], peak =  x0[7], gamma = x0[8], 
                                            )
        x = np.arange(0,len(DATA_PASS))


        ##########################################################################
        ##########################################################################
        
        if( SkipGap(i,j,binsSelected) ):
            continue
    
        pPass,pFail, BoundedFit = InitializeParams(i,j,binsSelected)
        ##################################
        if PlotBefore:
            xFit = np.arange(0,len(DATA_PASS))
            BKG = pPass[1]*RooCMSShape(xFit,*pPass[5:9])/np.sum(RooCMSShape(xFit,*pPass[5:9]))
            #print(pPass,VoigtCMS(xFit,*pPass))
            
            plt.figure()
            plt.plot(Mass,VoigtCMS(xFit,*pPass),label='fit')
            plt.plot(Mass, BKG,label='Bkg',color='green',linestyle='--')
            plt.plot(Mass,       DATA_PASS,label='data',color = 'k',linewidth=0,marker = 'o',markersize=4)
            plt.title('Pass')
            plt.legend()
            plt.grid(linestyle='--')
            if FailPlot:
                xFit = np.arange(len(DATA_PASS),len(DATA_PASS)*2)
                BKG = pFail[1]*RooCMSShape(xFit,*pFail[5:9])/np.sum(RooCMSShape(xFit,*pFail[5:9]))
                
                plt.figure()
                print(pFail,VoigtCMS(xFit,*pFail))
                plt.plot(Mass,VoigtCMS(xFit,*pFail),label='fit')
                plt.plot(Mass, BKG,label='Bkg',color = 'green',linestyle='--')
                plt.plot(Mass,         DATA_FAIL,label='data',color = 'k',linewidth=0,marker = 'o',markersize=4)
                plt.title('Fail')
                plt.legend()
                plt.grid(linestyle='--')
            

        ##---------------------------------------
        print('--- Fitting')    
        
        '''
        FitP, FitF,FitPSig, FitFSig = Fit_Curve(
                                                DATA_PASS = DATA_PASS,
                                                DATA_FAIL = DATA_FAIL,
                                                pPass = pPass,pFail = pFail,
                                                Bounded = BoundedFit,
                                                )        
        '''
        FitP, FitF,FitPSig, FitFSig,mP,mF = Fit_Curve_CHI(
                                                DATA_PASS = DATA_PASS,
                                                DATA_FAIL = DATA_FAIL,                                                
                                                pPass = pPass,pFail = pFail,
                                                Bounded = BoundedFit,
                                                )
        '''
        FitP, FitF,FitPSig, FitFSig = Fit_Curve_CHI(
                                                DATA_PASS = Data['Pass'][0][j][i],
                                                DATA_FAIL = Data['Fail'][0][j][i],
                                                pPass = pPass,pFail = pFail,
                                                )
        '''
        FitsPass = FitP
        FitsPass_NBkg,FitsPass_Bkg = FitP[1], FitP[5:9]
        
        FitsFail = FitF
        FitsFail_NBkg,FitsFail_Bkg = FitF[1], FitF[5:9]

        
        print(FitsPass," | ", FitPSig)
        print(FitsFail," | ", FitFSig)
        #for i in range(len(Fits[0])):
        #    print(Fits[0][i],sigs[i])


        ###-----------------
        xFit = np.arange(0,len(DATA_PASS))
        BKG = FitsPass_NBkg*RooCMSShape(xFit,*FitsPass_Bkg)/np.sum(RooCMSShape(xFit,*FitsPass_Bkg))
        
        plt.figure()        
        plt.plot(Mass,VoigtCMS(xFit,*FitsPass),label='fit',color = 'blue')
        plt.plot(Mass, BKG,label='bkg',color = 'green',linestyle='--')
        plt.plot(Mass, DATA_PASS,label='data',color = 'k',linewidth=0,marker = 'o',markersize=4)
        ylim = plt.gca().get_ylim()
        plt.text(xTestLoc,(ylim[1]-ylim[0])*rTestLoc + ylim[0],
                 TextLegend(FitPrams,FitsPass,FitPSig,xFit,Mass,chiplot(VoigtCMS(xFit,*FitsPass),DATA_PASS)),
                 bbox={'fc':'w'})
        
        plt.title('Pass')
        plt.legend()
        plt.grid(linestyle='--')
        if FailPlot:
            xFit = np.arange(len(DATA_PASS),len(DATA_PASS)*2)
            BKG = FitsFail_NBkg*RooCMSShape(xFit,*FitsFail_Bkg)/np.sum(RooCMSShape(xFit,*FitsFail_Bkg))
            
            plt.figure()
            plt.plot(Mass, VoigtCMS(xFit,*FitsFail),label='fit',color = 'blue')
            plt.plot(Mass, BKG,label='bkg',color = 'green',linestyle='--')
            plt.plot(Mass, DATA_FAIL,label='data',color = 'k',linewidth=0,marker = 'o',markersize=4)
            ylim = plt.gca().get_ylim()
            plt.text(xTestLoc,(ylim[1]-ylim[0])*rTestLoc + ylim[0],
                 TextLegend(FitPrams,FitsFail,FitFSig,xFit,Mass,chiplot(VoigtCMS(xFit,*FitsFail),DATA_FAIL)),
                 bbox={'fc':'w'})
            plt.title('Fail')
            plt.legend()
            plt.grid(linestyle='--')

        FitPass[j][i] = FitsPass
        FitFail[j][i] = FitsFail
        PassYield[j][i] =  FitsPass[0]
        FailYield[j][i] =  FitsFail[0]
        
        #eff[j][i] = PassYield[j][i]/(FailYield[j][i] + PassYield[j][i])
        ##########################################################################
        ##########################################################################
        plt.show()
        


# In[ ]:



m.matrix()


# In[ ]:


def SkipGap(i,j,binsSelect):
    gapFlag = False
    
    if     binsSelected == "Optimized":
        if (i == 1 or i == 4) and j != 5:
            gapFlag = True
    elif   binsSelected == "Plots":
        if (i == 1 or i == 4) and j != 11:
            gapFlag = True
    elif   binsSelected == "Hien":
        if (i == 1 or i == 4) and j != 6:
            gapFlag = True
    
    return gapFlag

def InitializeParams(i,j,binsSelected):
    if   binsSelected == "Optimized":
        if isConv:
            if   j == 0:
                if i != 5:
                    pPass = [
                            5e3,   5e3, 
                            0.1, 1, 14,       # Voigt
                            1,0.1, 0.01, 0.09,  # RooCMS
                            ]

                    pFail = [
                            1.5e3,   5e4, 
                            1, 1.2, 43,       # Voigt
                            30,0.1, 0.01, 0.09,  # RooCMS
                            ]
                else:
                    pPass = [
                            6e3,   5e3, 
                            0.1, 1, 14,       # Voigt
                            1,0.1, 0.01, 0.09,  # RooCMS
                            ]

                    pFail = [
                            3e3,   3e4, 
                            1, 1.2, 43,       # Voigt
                            30,0.1, 0.01, 0.09,  # RooCMS
                            ]
            elif j == 1:
                if i == 0:
                    pPass = [
                            5e4,   7e3, 
                            0.1, 2, 15,       # Voigt
                            10,0.01, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                             3e4, 5e4,
                             2, 0.01, 42,        # Voigt
                             33, 0.1, 200, 0.09  # RooCMS
                            ]
                elif i == 2:
                    pPass = [
                            3e5,   6e4, 
                            0.1, 2, 14,       # Voigt
                            5,0.01, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                             3e4, 5e4,
                             2, 0.01, 42,        # Voigt
                             33, 0.1, 200, 0.09  # RooCMS
                            ]
                elif i == 3:
                    pPass = [
                            5e5,   4e5, 
                            0.1, 2, 14,       # Voigt
                            5,0.01, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                             3e4, 5e4,
                             2, 0.01, 42,        # Voigt
                             33, 0.1, 200, 0.09  # RooCMS
                            ]
                elif i == 5:
                    pPass = [
                            1e5,   8e4, 
                            0.1, 2, 15,       # Voigt
                            5,0.01, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                             1e4, 1e4,
                             2, 0.01, 42,        # Voigt
                             33, 0.1, 200, 0.09  # RooCMS
                            ]
            elif j == 2:
                if i == 0:
                    pPass = [
                            3e5,   5e3, 
                            0.1, 2, 15,       # Voigt
                            10,0.01, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                            1.5e5,   5e4, 
                            1, 1, 44,           # Voigt
                            20,0.01, 20, 0.09,  # RooCMS
                            ]
                if i == 2:
                    pPass = [
                            12e5,   5e3, 
                            0.1, 2, 15,       # Voigt
                            10,0.01, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                            1.5e5,   5e4, 
                            1, 1, 44,           # Voigt
                            20,0.01, 20, 0.09,  # RooCMS
                            ]
                if i == 3:
                    pPass = [
                            1e6,   5e3, 
                            0.1, 1.5, 15,       # Voigt
                            10,0.01, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                            1.5e5,   5e4, 
                            1, 1, 44,           # Voigt
                            20,0.01, 20, 0.09,  # RooCMS
                            ]
                if i == 5:
                    pPass = [
                            1e5,   5e3, 
                            0.1, 2, 15,       # Voigt
                            10,0.01, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                            1.5e5,   5e4, 
                            1, 1, 44,           # Voigt
                            20,0.01, 20, 0.09,  # RooCMS
                            ]
            elif j == 3:
                if i == 0:
                    pPass = [
                            5e4,   9e3, 
                            #0.1, 2, 15,       # Voigt
                            1, 1, 15,       # Voigt
                            13,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            9e3,   6e3, 
                            1, 1, 44,           # Voigt
                            40,0.01, 20, -0.09,  # RooCMS
                            ]
                elif i == 3:
                    pPass = [
                            1e5,   1e4, 
                            0.5, 1, 14,       # Voigt
                            15,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            3e4,   8e3, 
                            1, 1, 44,           # Voigt
                            45,0.01, 20, -0.09,  # RooCMS
                            ]                
                elif i == 5:
                    pPass = [
                            1e4,   5e3, 
                            0.5, 1, 14,       # Voigt
                            15,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            5e3,   5e3, 
                            0.5, 1, 44,           # Voigt
                            45,0.01, 20, -0.09,  # RooCMS
                            ]
                else:
                    pPass = [
                            6e4,   5e3, 
                            0.1, 2, 15,       # Voigt
                            13,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            9e3,   4e3, 
                            1, 1, 44,           # Voigt
                            45,0.01, 20, -0.09,  # RooCMS
                            ]                        
            elif j == 4:
                if i == 0:
                    pPass = [
                            1e2,  200,  
                            0.5,  1, 15,  
                            15,1, 10,-0.09,
                            ] 

                    pFail = [
                            1e2,  3e1,  
                            0.5,  1, 44,  
                            49,-0.1, 10, -0.09,  # RooCMS
                            ]  
                elif i == 2:
                    pPass = [
                            7e3,  200,  
                            0.5,  1, 15,  
                            15,1, 10,-0.09,
                            ] 

                    pFail = [
                            5e2,  5e2,  
                            0.5,  1, 44,  
                            35,-0.1, 10, -0.09,  # RooCMS
                            ] 
                elif i == 3:
                    pPass = [
                            5e3,  200,  
                            0.1,  1, 15,  
                            15,1, 10,-0.09,
                            ] 

                    pFail = [
                            5e2,  1e2,  
                            0.1,  1, 44,  
                            48,-0.1, 10, -0.09,  # RooCMS
                            ] 
                elif i == 5:
                    pPass = [1.22435554e+03, 3.20343246e+02, 9.22998413e-12,
                             1.10974344e+00, 1.50406031e+01, 1.40180622e+01,
                             6.13551539e-01, 1.00000028e+01, 5.95495234e-01]
                    pFail = [ 4.08455718e+02,  2.34193103e+02,  1.08171908e+00,
                             9.14064665e-01, 4.39415340e+01,  5.75583581e+01, 
                             -5.13886755e-01,  3.82617111e+03,-4.43517032e-02]
                else :
                    pPass = [
                            1e3,  100,  
                            0.5,  1, 15,  
                            15,0.1, 10,-0.09,
                            ] 

                    pFail = [
                            2e2,  1e2,  
                            0.1,  1, 44,  
                            45,0.01, 10, -0.09,  # RooCMS
                            ]                                        
            elif j == 5:
                if i == 0:
                    pPass = [
                            6e4,  1e2,  
                            0.1,  2, 15,  
                            1,1, 1.15814356e+02,1,
                            ] 

                    pFail = [
                            1e3,  1e2,  
                            0.1,  2, 44,  
                            35,  1, 1.15814356e+02,1,
                            ] 
                elif i == 1:
                    pPass = [
                            2e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            2e1,  1e1,  
                            0.5,  1, 44,  
                            48,  -0.1, 10,0.1,
                            ]   
                else:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            40,  3e1,  
                            1,  1, 44,  
                            35,  0.1, 1.15814356e+02,0.1,
                            ]  
        else:
            if   j == 0:
                if  i == 0:
                    pPass = [
                            1e4,   5e3, 
                            0.1, 1, 14,       # Voigt
                            1,0.1, 0.01, 0.09,  # RooCMS
                            ]

                    pFail = [
                            4e3,   2e4, 
                            1, 1.2, 43,       # Voigt
                            30,0.1, 0.01, 0.09,  # RooCMS
                            ]
                elif i != 5:

                    pPass = [
                            1e4,   5e3, 
                            0.1, 1, 14,       # Voigt
                            1,0.1, 0.01, 0.09,  # RooCMS
                            ]

                    pFail = [
                            1.5e3,   5e4, 
                            1, 1.2, 43,       # Voigt
                            30,0.1, 0.01, 0.09,  # RooCMS
                            ]
                elif i == 5:
                    pPass = [
                            5e4,   2e3, 
                            0.1, 1, 14,       # Voigt
                            1,0.1, 0.01, 0.09,  # RooCMS
                            ]

                    pFail = [
                            4e3,   2e4, 
                            1, 1.2, 43,       # Voigt
                            10,0.1, 0.01, 0.09,  # RooCMS
                            ]
            elif j == 1:
                if i == 0:
                    pPass = [
                            1e5,   7e3, 
                            0.1, 2, 15,       # Voigt
                            10,0.1, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                             3e4, 5e4,
                             2, 0.01, 43,        # Voigt
                             33, 0.1, 200, 0.09  # RooCMS
                            ]
                elif i == 2:
                    pPass = [
                            5e5,   6e4, 
                            0.1, 2, 15,       # Voigt
                            5,0.1, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                             2e4, 5e4,
                             2, 0.01, 43,        # Voigt
                             33, 0.1, 200, 0.09  # RooCMS
                            ]
                elif i == 3:
                    pPass = [
                            5e5,   1e5, 
                            0.1, 2, 14,       # Voigt
                            10,0.1, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                             3e4, 5e4,
                             2, 0.01, 43,        # Voigt
                             33, 0.1, 200, 0.09  # RooCMS
                            ]
                elif i == 5:
                    pPass = [
                            1e5,   8e4, 
                            0.1, 2, 15,       # Voigt
                            30,0.01, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                             1e4, 1e4,
                             2, 0.01, 43,        # Voigt
                             33, 0.1, 200, 0.09  # RooCMS
                            ]
            elif j == 2:
                if i == 0:
                    pPass = [
                            3e5,   5e3, 
                            0.1, 2, 15,       # Voigt
                            10,0.1, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                            1.5e5,   5e4, 
                            1, 1, 44,           # Voigt
                            20,0.1, 20, 0.09,  # RooCMS
                            ]
                if i == 2:
                    pPass = [
                            12e5,   5e3, 
                            0.1, 2, 15,       # Voigt
                            30,0.1, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                            1.5e5,   5e4, 
                            1, 1, 44,           # Voigt
                            20,0.1, 20, 0.09,  # RooCMS
                            ]
                if i == 3:
                    pPass = [
                            3e6,   5e3, 
                            0.2, 1.5, 15,       # Voigt
                            5,0.1, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                            8e4,   1e4, 
                            0.1, 1, 44,           # Voigt
                            35,0.1, 20, 0.09,  # RooCMS
                            ]
                if i == 5:
                    pPass = [
                            4e5,   1e3, 
                            1.5, 1.7, 15,       # Voigt
                            3,0.01, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                            1.5e5,   5e4, 
                            1, 1, 44,           # Voigt
                            20,0.01, 20, 0.09,  # RooCMS
                            ]
            elif j == 3:
                if i == 0:
                    pPass = [
                            5e4,   9e3, 
                            #0.1, 2, 15,       # Voigt
                            1, 1, 15,       # Voigt
                            13,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            9e3,   4e3, 
                            1, 1, 44,           # Voigt
                            40,0.01, 20, -0.09,  # RooCMS
                            ]
                elif i == 2:
                    pPass = [
                            5e4,   9e3, 
                            #0.1, 2, 15,       # Voigt
                            1, 1, 15,       # Voigt
                            13,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            9e3,   4e3, 
                            1, 1, 44,           # Voigt
                            40,0.01, 20, -0.09,  # RooCMS
                            ]
                elif i == 3:
                    pPass = [
                            5e4,   9e3, 
                            #0.1, 2, 15,       # Voigt
                            1, 1, 15,       # Voigt
                            13,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            9e3,   4e3, 
                            1, 1, 44,           # Voigt
                            40,0.01, 20, -0.09,  # RooCMS
                            ]
                elif i == 5:
                    pPass = [
                            7e4,   5e3, 
                            0.1, 2, 15,       # Voigt
                            13,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            9e3,   4e3, 
                            1, 1, 44,           # Voigt
                            40,0.01, 20, -0.09,  # RooCMS
                            ]
                else:
                    pPass = [
                            2e5,   5e3, 
                            0.1, 2, 15,       # Voigt
                            13,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            9e3,   4e3, 
                            1, 1, 44,           # Voigt
                            40,0.01, 20, -0.09,  # RooCMS
                            ]
            elif j == 4:
                if i == 0:
                    pPass = [
                            5e3,  200,  
                            0.1,  2, 15,  
                            15,-0.1, 100,1,
                            ] 

                    pFail = [
                            4e2,  1e2,  
                            0.1,  2, 44,  
                            42,-0.1, 100,1,
                            ] 
                elif i == 2:
                    pPass = [
                            5e3,  200,  
                            0.1,  2, 15,  
                            15,-0.1, 100,1,
                            ] 

                    pFail = [
                            4e2,  1e2,  
                            0.1,  2, 44,  
                            60,-0.1, 100,1,
                            ] 
                elif i == 3:
                    pPass = [
                            5e3,  200,  
                            0.1,  2, 15,  
                            15,-0.1, 100,1,
                            ] 

                    pFail = [
                            5e2,  1e2,  
                            0.1,  2, 44,  
                            60,0.1, 100,1,
                            ] 
                else :
                    pPass = [
                            5e3,  200,  
                            0.1,  2, 15,  
                            15,-0.1, 100,1,
                            ] 

                    pFail = [
                            5e2,  1e2,  
                            0.1,  2, 43,  
                            42,-0.1, 100,1,
                            ] 
            elif j == 5:
                if i == 0:
                    pPass = [
                            3e3,  1e2,  
                            0.1,  1, 15,  
                            1,0.1, 1.15814356e+02,1,
                            ] 

                    pFail = [
                            1e3,  1e2,  
                            0.1,  1, 44,  
                            70,-0.1, 1.15814356e+02,1,
                            ] 
                elif i == 1:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            200,  3e1,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
    elif binsSelected == "Plots" :
        if isConv:
            if   j == 0:
                if  i == 0:
                    pPass = [
                            1e4,   5e3, 
                            0.1, 1, 14,       # Voigt
                            1,0.1, 0.01, 0.09,  # RooCMS
                            ]

                    pFail = [
                            4e3,   2e4, 
                            1, 1.2, 43,       # Voigt
                            30,0.1, 0.01, 0.09,  # RooCMS
                            ]
                elif i != 5:

                    pPass = [
                            1e4,   5e3, 
                            0.1, 1, 14,       # Voigt
                            1,0.1, 0.01, 0.09,  # RooCMS
                            ]

                    pFail = [
                            1.5e3,   5e4, 
                            1, 1.2, 43,       # Voigt
                            30,0.1, 0.01, 0.09,  # RooCMS
                            ]
                elif i == 5:
                    pPass = [
                            5e4,   2e3, 
                            0.1, 1, 14,       # Voigt
                            1,0.1, 0.01, 0.09,  # RooCMS
                            ]

                    pFail = [
                            4e3,   2e4, 
                            1, 1.2, 43,       # Voigt
                            10,0.1, 0.01, 0.09,  # RooCMS
                            ]
            elif j == 1:
                if i == 0:
                    pPass = [
                            1e5,   7e3, 
                            0.1, 2, 15,       # Voigt
                            10,0.1, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                             3e4, 5e4,
                             2, 0.01, 43,        # Voigt
                             33, 0.1, 200, 0.09  # RooCMS
                            ]
                elif i == 2:
                    pPass = [
                            5e5,   6e4, 
                            0.1, 2, 15,       # Voigt
                            5,0.1, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                             2e4, 5e4,
                             2, 0.01, 43,        # Voigt
                             33, 0.1, 200, 0.09  # RooCMS
                            ]
                elif i == 3:
                    pPass = [
                            5e5,   1e5, 
                            0.1, 2, 14,       # Voigt
                            10,0.1, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                             3e4, 5e4,
                             2, 0.01, 43,        # Voigt
                             33, 0.1, 200, 0.09  # RooCMS
                            ]
                elif i == 5:
                    pPass = [
                            1e5,   8e4, 
                            0.1, 2, 15,       # Voigt
                            30,0.01, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                             1e4, 1e4,
                             2, 0.01, 43,        # Voigt
                             33, 0.1, 200, 0.09  # RooCMS
                            ]
            elif j == 2:
                if i == 0:
                    pPass = [
                            3e5,   5e3, 
                            0.1, 2, 15,       # Voigt
                            10,0.1, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                            1.5e5,   5e4, 
                            1, 1, 44,           # Voigt
                            20,0.1, 20, 0.09,  # RooCMS
                            ]
                if i == 2:
                    pPass = [
                            2e5,   1e3, 
                            0.1, 1, 14,       # Voigt
                            30,0.1, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            1e4,   3e3, 
                            1, 1, 44,           # Voigt
                            50,0.1, 20, -0.09,  # RooCMS
                            ]
                if i == 3:
                    pPass = [
                            3e6,   5e3, 
                            0.2, 1.5, 15,       # Voigt
                            5,0.1, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                            8e4,   1e4, 
                            0.1, 1, 44,           # Voigt
                            35,0.1, 20, 0.09,  # RooCMS
                            ]
                if i == 5:
                    pPass = [
                            4e5,   1e3, 
                            1.5, 1.7, 15,       # Voigt
                            3,0.01, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                            1.5e5,   5e4, 
                            1, 1, 44,           # Voigt
                            20,0.01, 20, 0.09,  # RooCMS
                            ]
            elif j == 3:
                if i == 0:
                    pPass = [
                            5e4,   9e3, 
                            #0.1, 2, 15,       # Voigt
                            1, 1, 15,       # Voigt
                            13,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            9e3,   4e3, 
                            1, 1, 44,           # Voigt
                            40,0.01, 20, -0.09,  # RooCMS
                            ]
                elif i == 2:
                    pPass = [
                            5e4,   9e3, 
                            #0.1, 2, 15,       # Voigt
                            1, 1, 15,       # Voigt
                            13,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            9e3,   4e3, 
                            1, 1, 44,           # Voigt
                            40,0.01, 20, -0.09,  # RooCMS
                            ]
                elif i == 3:
                    pPass = [
                            5e4,   9e3, 
                            #0.1, 2, 15,       # Voigt
                            1, 1, 15,       # Voigt
                            13,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            9e3,   4e3, 
                            1, 1, 44,           # Voigt
                            40,0.01, 20, -0.09,  # RooCMS
                            ]
                elif i == 5:
                    pPass = [
                            7e4,   5e3, 
                            0.1, 2, 15,       # Voigt
                            13,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            9e3,   4e3, 
                            1, 1, 44,           # Voigt
                            40,0.01, 20, -0.09,  # RooCMS
                            ]
                else:
                    pPass = [
                            2e5,   5e3, 
                            0.1, 2, 15,       # Voigt
                            13,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            9e3,   4e3, 
                            1, 1, 44,           # Voigt
                            40,0.01, 20, -0.09,  # RooCMS
                            ]
            elif j == 4:
                if i == 0:
                    pPass = [
                            1e5,  5e2,  
                            1,  1, 14,  
                            14,-0.01, 10,1,
                            ] 

                    pFail = [
                            1e4,  2e3,  
                            0.1,  2, 44,  
                            42,-0.1, 100,1,
                            ] 
                elif i == 2:
                    pPass = [
                            8e5,  5e3,
                            0.1,  1, 15,  
                            15,-0.1, 100,1,
                            ] 

                    pFail = [
                            9e4,  2e3,
                            0.1,  1, 44,  
                            60,-0.1, 100,1,
                            ] 
                elif i == 3:
                    pPass = [
                            4e5,  1e4,
                            0.1,  1, 15,  
                            15,-0.1, 100,-1,
                            ] 

                    pFail = [
                            4e4,  7e3,
                            0.1,  1, 44,  
                            60,0.1, 100,-1,
                            ] 
                elif i == 5 :
                    pPass = [
                            2e5,  4e3,
                            0.1,  2, 15,  
                            15,-0.1, 100,-1,
                            ] 

                    pFail = [
                            2e4,  3e3,  
                            0.1,  2, 44,  
                            65,-0.1, 100,-1,
                            ] 
            elif j == 5:
                if i == 0:
                    pPass = [
                            6e4,  9e2,  
                            0.2,  1, 15,  
                            10,0.1, 1.15814356e+02,1,
                            ] 

                    pFail = [
                            3e3,  3e2,  
                            0.1,  1, 44,  
                            70,-0.1, 1.15814356e+02,1,
                            ] 
                elif i == 2:
                    pPass = [
                            9e4,  3e3,
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            2e4,  3e3,
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
                elif i == 3:
                    pPass = [
                            1e5,  6e2,
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            4e3,  6e2,
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
                elif i == 5:
                    pPass = [
                            1e4,  3e3,
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            2e4,  3e3,
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
                else:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            200,  3e1,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
            elif j == 6:
                if i == 0:
                    pPass = [
                            8e3,  3e2,  
                            0.1,  1, 15,  
                            10,0.1, 1.15814356e+02,1,
                            ] 

                    pFail = [
                            1e3,  1e2,  
                            0.2,  1, 44,  
                            70,-0.1, 1.15814356e+02,1,
                            ] 
                elif i == 2:
                    pPass = [
                            3e4,  3e2,
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            8e3,  3e2,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
                elif i == 3:
                    pPass = [
                            6e4,  3e2,
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            5e3,  3e2,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
                elif i == 5:
                    pPass = [
                            3e3,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            5e3,  3e2,
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
                else:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            200,  3e1,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
            elif j == 7:
                if i == 0:
                    pPass = [
                            3e3,  5e1,
                            0.1,  1, 15,  
                            1,0.1, 1.15814356e+02,1,
                            ] 

                    pFail = [
                            1e3,  5e1,
                            0.1,  1, 44,  
                            70,-0.1, 1.15814356e+02,1,
                            ] 
                elif i == 2:
                    pPass = [
                            2e4,  2e2,
                            0.5,  1, 15,  
                            10,-0.1, 1.15814356e+02,-0.1,
                            ] 

                    pFail = [8e2, 2e2,
                             1, 1, 44, 
                             60, 0.0038985980209962634, -700, 0.015222050465143688
                            ]
                elif i == 3:
                    pPass = [
                            1e4,  3e2,
                            0.5,  1, 15,  
                            10,-0.1, 1.15814356e+02,-0.1,
                            ] 

                    pFail = [2e3, 3e2,
                             1, 1, 44, 
                             0.7044642032043633, 0.0038985980209962634, 1557.2502065025765, -0.015222050465143688
                            ]
                elif i == 5:
                    pPass = [
                            2e3,  6e1,  
                            0.5,  1, 15,  
                            10,-0.1, 1.15814356e+02,-0.1,
                            ] 

                    pFail = [2e2, 7e1,
                             1, 1, 44, 
                             70, 0.0038985980209962634, 700, -0.015222050465143688
                            ]
                else:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,-0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            200,  3e1,  
                            1,  1, 44,  
                            10,-0.1, 1.15814356e+02,0.1,
                            ]  
            elif j == 8:
                if i == 0:
                    pPass = [
                            3e3,  1e2,  
                            0.1,  1, 15,  
                            1,0.1, 1.15814356e+02,1,
                            ] 

                    pFail = [
                            5e2,  1e2,  
                            1,  1, 44,  
                            70,-0.1, 1.15814356e+02,1,
                            ] 
                elif i == 2:
                    pPass = [
                            6e3,  3e2,
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            6e2,  3e2,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
                elif i == 3:
                    pPass = [
                            1e3,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            1e3,  6e2,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,-0.1,
                            ]  
                elif i == 5:
                    pPass = [
                            9e2,  7e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            1e2,  7e1,  
                            1,  1, 44,  
                            60,  0.1, 1.15814356e+02, -0.1,
                            ]  
                else:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            200,  3e1,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
            elif j == 9:
                if i == 0:
                    pPass = [
                            5e2,  5e1,
                            0.1,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            5e1,  2e1,
                            0.1,  1, 44,  
                            50,-0.1, 1.15814356e+02,-0.1,
                            ] 
                elif i == 2:
                    pPass = [
                            6e3,  3e2,
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            6e2,  3e2,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
                elif i == 3:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            1e3,  3e1,  
                            1,  1, 44,  
                            60,  0.1, 1.15814356e+02,0.1,
                            ]  
                elif i == 5:
                    pPass = [
                            3e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            7e1,  1e1,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
                else:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            200,  3e1,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
            elif j == 10:
                if i == 0:
                    pPass = [
                            1e3,  1e2,  
                            0.1,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            1e2,  3e1,  
                            0.1,  1, 44,  
                            50,-0.1, 1.15814356e+02,0.1,
                            ] 
                elif i == 2:
                    pPass = [
                            6e3,  3e2,
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            3e2,  1e2,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
                elif i == 3:
                    pPass = [
                            3e3,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            3e2,  5e1,  
                            1,  1, 44,  
                            60,  0.1, 1.15814356e+02,0.1,
                            ]  
                elif i == 5:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            1e2,  3e1,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,-0.1,
                            ]  
                else:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            200,  3e1,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
            elif j == 11:
                if   i == 0:
                    pPass = [
                            4e3,  1e2,  
                            0.1,  1, 15,  
                            10,0.1, 1.15814356e+02,-0.05,
                            ] 

                    pFail = [
                            3e2,  5e1,  
                            0.1,  1, 44,  
                            70,-0.1, 1.15814356e+02,-0.05,
                            ] 
                elif i == 1:
                    pPass = [
                            8e2,  3e2,
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            5e1,  1e1,  
                            0.1,  1, 44,  
                            10,  0.1, 40,-0.1,
                            ]  
                elif i == 2:
                    pPass = [
                            4e3,  3e2,
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            1e2,  3e2,  
                            1,  1, 44,  
                            40,  0.1, 1.15814356e+02,0.1,
                            ]  
                elif i == 3:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            1e3,  3e1,  
                            1,  1, 44,  
                            60,  0.1, 1.15814356e+02,0.1,
                            ]  
                elif i == 5:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            200,  3e1,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
                else:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            200,  3e1,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]                      
        else:
            if   j == 0:
                if  i == 0:
                    pPass = [
                            1e4,   5e3, 
                            0.1, 1, 14,       # Voigt
                            1,0.1, 0.01, 0.09,  # RooCMS
                            ]

                    pFail = [
                            4e3,   2e4, 
                            1, 1.2, 43,       # Voigt
                            30,0.1, 0.01, 0.09,  # RooCMS
                            ]
                elif i != 5:

                    pPass = [
                            1e4,   5e3, 
                            0.1, 1, 14,       # Voigt
                            1,0.1, 0.01, 0.09,  # RooCMS
                            ]

                    pFail = [
                            1.5e3,   5e4, 
                            1, 1.2, 43,       # Voigt
                            30,0.1, 0.01, 0.09,  # RooCMS
                            ]
                elif i == 5:
                    pPass = [
                            5e4,   2e3, 
                            0.1, 1, 14,       # Voigt
                            1,0.1, 0.01, 0.09,  # RooCMS
                            ]

                    pFail = [
                            4e3,   2e4, 
                            1, 1.2, 43,       # Voigt
                            10,0.1, 0.01, 0.09,  # RooCMS
                            ]
            elif j == 1:
                if i == 0:
                    pPass = [
                            1e5,   7e3, 
                            0.1, 2, 15,       # Voigt
                            10,0.1, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                             3e4, 5e4,
                             2, 0.01, 43,        # Voigt
                             33, 0.1, 200, 0.09  # RooCMS
                            ]
                elif i == 2:
                    pPass = [
                            5e5,   6e4, 
                            0.1, 2, 15,       # Voigt
                            5,0.1, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                             2e4, 5e4,
                             2, 0.01, 43,        # Voigt
                             33, 0.1, 200, 0.09  # RooCMS
                            ]
                elif i == 3:
                    pPass = [
                            5e5,   1e5, 
                            0.1, 2, 14,       # Voigt
                            10,0.1, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                             3e4, 5e4,
                             2, 0.01, 43,        # Voigt
                             33, 0.1, 200, 0.09  # RooCMS
                            ]
                elif i == 5:
                    pPass = [
                            1e5,   8e4, 
                            0.1, 2, 15,       # Voigt
                            30,0.01, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                             1e4, 1e4,
                             2, 0.01, 43,        # Voigt
                             33, 0.1, 200, 0.09  # RooCMS
                            ]
            elif j == 2:
                if i == 0:
                    pPass = [
                            3e5,   5e3, 
                            0.1, 2, 15,       # Voigt
                            10,0.1, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                            1.5e5,   5e4, 
                            1, 1, 44,           # Voigt
                            20,0.1, 20, 0.09,  # RooCMS
                            ]
                if i == 2:
                    pPass = [
                            12e5,   5e3, 
                            0.1, 2, 15,       # Voigt
                            30,0.1, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                            1.5e5,   5e4, 
                            1, 1, 44,           # Voigt
                            20,0.1, 20, 0.09,  # RooCMS
                            ]
                if i == 3:
                    pPass = [
                            3e6,   5e3, 
                            0.2, 1.5, 15,       # Voigt
                            5,0.1, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                            8e4,   1e4, 
                            0.1, 1, 44,           # Voigt
                            35,0.1, 20, 0.09,  # RooCMS
                            ]
                if i == 5:
                    pPass = [
                            4e5,   1e3, 
                            1.5, 1.7, 15,       # Voigt
                            3,0.01, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                            1.5e5,   5e4, 
                            1, 1, 44,           # Voigt
                            20,0.01, 20, 0.09,  # RooCMS
                            ]
            elif j == 3:
                if i == 0:
                    pPass = [
                            5e4,   9e3, 
                            #0.1, 2, 15,       # Voigt
                            1, 1, 15,       # Voigt
                            13,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            9e3,   4e3, 
                            1, 1, 44,           # Voigt
                            40,0.01, 20, -0.09,  # RooCMS
                            ]
                elif i == 2:
                    pPass = [
                            5e4,   9e3, 
                            #0.1, 2, 15,       # Voigt
                            1, 1, 15,       # Voigt
                            13,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            9e3,   4e3, 
                            1, 1, 44,           # Voigt
                            40,0.01, 20, -0.09,  # RooCMS
                            ]
                elif i == 3:
                    pPass = [
                            5e4,   9e3, 
                            #0.1, 2, 15,       # Voigt
                            1, 1, 15,       # Voigt
                            13,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            9e3,   4e3, 
                            1, 1, 44,           # Voigt
                            40,0.01, 20, -0.09,  # RooCMS
                            ]
                elif i == 5:
                    pPass = [
                            7e4,   5e3, 
                            0.1, 2, 15,       # Voigt
                            13,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            9e3,   4e3, 
                            1, 1, 44,           # Voigt
                            40,0.01, 20, -0.09,  # RooCMS
                            ]
                else:
                    pPass = [
                            2e5,   5e3, 
                            0.1, 2, 15,       # Voigt
                            13,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            9e3,   4e3, 
                            1, 1, 44,           # Voigt
                            40,0.01, 20, -0.09,  # RooCMS
                            ]
            elif j == 4:
                if i == 0:
                    pPass = [
                            1e5,  4e3,  
                            0.1,  2, 15,  
                            15,-0.1, 100,1,
                            ] 

                    pFail = [
                            8e3,  4e3,  
                            0.1,  2, 44,  
                            42,-0.1, 100,1,
                            ] 
                elif i == 2:
                    pPass = [
                            5e5,  2e4,
                            0.1,  2, 15,  
                            15,-0.1, 100,1,
                            ] 

                    pFail = [
                            4e4,  1e4,
                            0.1,  2, 44,  
                            60,-0.1, 100,1,
                            ] 
                elif i == 3:
                    pPass = [
                            5e5,  2e4,
                            0.1,  2, 15,  
                            15,-0.1, 100,1,
                            ] 

                    pFail = [
                            5e4,  1e4,
                            0.1,  2, 44,  
                            60,0.1, 100,1,
                            ] 
                elif i == 5 :
                    pPass = [
                            1e5,  4e3,
                            0.1,  2, 15,  
                            15,-0.1, 100,1,
                            ] 

                    pFail = [
                            1e4,  3e3,  
                            0.1,  2, 44,  
                            65,-0.1, 100,1,
                            ] 
            elif j == 5:
                if i == 0:
                    pPass = [
                            9e3,  3e2,  
                            0.2,  1, 15,  
                            10,0.1, 1.15814356e+02,1,
                            ] 

                    pFail = [
                            3e3,  3e2,  
                            0.1,  1, 44,  
                            70,-0.1, 1.15814356e+02,1,
                            ] 
                elif i == 2:
                    pPass = [
                            9e4,  3e3,
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            2e4,  3e3,
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
                elif i == 3:
                    pPass = [
                            1e5,  6e2,
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            4e3,  6e2,
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
                elif i == 5:
                    pPass = [
                            1e4,  3e3,
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            2e4,  3e3,
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
                else:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            200,  3e1,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
            elif j == 6:
                if i == 0:
                    pPass = [
                            5e3,  1e2,  
                            0.1,  1, 15,  
                            10,0.1, 1.15814356e+02,1,
                            ] 

                    pFail = [
                            1e3,  1e2,  
                            0.2,  1, 44,  
                            70,-0.1, 1.15814356e+02,1,
                            ] 
                elif i == 2:
                    pPass = [
                            6e3,  3e2,
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            2e3,  3e2,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
                elif i == 3:
                    pPass = [
                            6e3,  3e2,
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            2e3,  3e2,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
                elif i == 5:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            2e3,  3e2,
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
                else:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            200,  3e1,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
            elif j == 7:
                if i == 0:
                    pPass = [
                            3e3,  5e1,
                            0.1,  1, 15,  
                            1,0.1, 1.15814356e+02,1,
                            ] 

                    pFail = [
                            1e3,  5e1,
                            0.1,  1, 44,  
                            70,-0.1, 1.15814356e+02,1,
                            ] 
                elif i == 2:
                    pPass = [
                            3e4,  5e2,
                            0.5,  1, 15,  
                            10,-0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [8e2, 8e2,
                             1, 1, 44, 
                             60, 0.0038985980209962634, -700, 0.015222050465143688
                            ]
                elif i == 3:
                    pPass = [
                            9e3,  3e2,
                            0.5,  1, 15,  
                            10,-0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [2e3, 7e2,
                             1, 1, 44, 
                             0.7044642032043633, 0.0038985980209962634, 1557.2502065025765, 0.015222050465143688
                            ]
                elif i == 5:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,-0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [200, 70,
                             1, 1, 44, 
                             70, 0.0038985980209962634, -700, 0.015222050465143688
                            ]
                else:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,-0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            200,  3e1,  
                            1,  1, 44,  
                            10,-0.1, 1.15814356e+02,0.1,
                            ]  
            elif j == 8:
                if i == 0:
                    pPass = [
                            3e3,  1e2,  
                            0.1,  1, 15,  
                            1,0.1, 1.15814356e+02,1,
                            ] 

                    pFail = [
                            5e2,  1e2,  
                            1,  1, 44,  
                            70,-0.1, 1.15814356e+02,1,
                            ] 
                elif i == 2:
                    pPass = [
                            6e3,  3e2,
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            6e2,  3e2,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
                elif i == 3:
                    pPass = [
                            1e3,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            1e3,  6e2,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,-0.1,
                            ]  
                elif i == 5:
                    pPass = [
                            9e2,  7e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            2e2,  2e2,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02, -0.1,
                            ]  
                else:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            200,  3e1,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
            elif j == 9:
                if i == 0:
                    pPass = [
                            3e3,  1e2,  
                            0.1,  1, 15,  
                            1,0.1, 1.15814356e+02,1,
                            ] 

                    pFail = [
                            1e3,  1e2,  
                            0.1,  1, 44,  
                            70,-0.1, 1.15814356e+02,1,
                            ] 
                elif i == 2:
                    pPass = [
                            6e3,  3e2,
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            6e2,  3e2,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
                elif i == 3:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            1e3,  3e1,  
                            1,  1, 44,  
                            60,  0.1, 1.15814356e+02,0.1,
                            ]  
                elif i == 5:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            200,  3e1,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
                else:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            200,  3e1,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
            elif j == 10:
                if i == 0:
                    pPass = [
                            3e3,  1e2,  
                            0.1,  1, 15,  
                            1,0.1, 1.15814356e+02,1,
                            ] 

                    pFail = [
                            1e3,  1e2,  
                            0.1,  1, 44,  
                            70,-0.1, 1.15814356e+02,1,
                            ] 
                elif i == 2:
                    pPass = [
                            6e3,  3e2,
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            6e2,  3e2,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
                elif i == 3:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            5e2,  3e2,  
                            1,  1, 44,  
                            60,  0.1, 1.15814356e+02,0.1,
                            ]  
                elif i == 5:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            100,  8e1,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
                else:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            200,  3e1,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
            elif j == 11:
                if   i == 0:
                    pPass = [
                            3e3,  1e2,  
                            0.1,  1, 15,  
                            1,0.1, 1.15814356e+02,1,
                            ] 

                    pFail = [
                            2e2,  5e2,  
                            0.1,  1, 44,  
                            70,-0.1, 1.15814356e+02,1,
                            ] 
                elif i == 1:
                    pPass = [
                            8e2,  3e2,
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            8e1,  1e2,  
                            0.1,  1, 44,  
                            40,  0.1, 1.15814356e+02,-0.1,
                            ]  
                elif i == 2:
                    pPass = [
                            4e3,  3e2,
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            1e2,  3e2,  
                            1,  1, 44,  
                            40,  0.1, 1.15814356e+02,0.1,
                            ]  
                elif i == 3:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            1e3,  3e1,  
                            1,  1, 44,  
                            60,  0.1, 1.15814356e+02,0.1,
                            ]  
                elif i == 5:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            200,  3e1,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  
                else:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            200,  3e1,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]                      
    elif binsSelected == "Hien":
        if isConv:
            if   j == 0:
                if i != 5:
                    pPass = [
                            5e3,   5e3, 
                            0.1, 1, 14,       # Voigt
                            1,0.1, 0.01, 0.09,  # RooCMS
                            ]

                    pFail = [
                            1.5e3,   5e4, 
                            1, 1.2, 43,       # Voigt
                            30,0.1, 0.01, 0.09,  # RooCMS
                            ]
                else:
                    pPass = [
                            6e3,   5e3, 
                            0.1, 1, 14,       # Voigt
                            1,0.1, 0.01, 0.09,  # RooCMS
                            ]

                    pFail = [
                            3e3,   3e4, 
                            1, 1.2, 43,       # Voigt
                            30,0.1, 0.01, 0.09,  # RooCMS
                            ]
            elif j == 1:
                if i == 0:
                    pPass = [
                            5e4,   7e3, 
                            0.1, 2, 15,       # Voigt
                            10,0.01, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                             3e4, 5e4,
                             2, 0.01, 42,        # Voigt
                             33, 0.1, 200, 0.09  # RooCMS
                            ]
                elif i == 2:
                    pPass = [
                            3e5,   6e4, 
                            0.1, 2, 14,       # Voigt
                            5,0.01, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                             3e4, 5e4,
                             2, 0.01, 42,        # Voigt
                             33, 0.1, 200, 0.09  # RooCMS
                            ]
                elif i == 3:
                    pPass = [
                            5e5,   4e5, 
                            0.1, 2, 14,       # Voigt
                            5,0.01, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                             3e4, 5e4,
                             2, 0.01, 42,        # Voigt
                             33, 0.1, 200, 0.09  # RooCMS
                            ]
                elif i == 5:
                    pPass = [
                            1e5,   8e4, 
                            0.1, 2, 15,       # Voigt
                            5,0.01, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                             1e4, 1e4,
                             2, 0.01, 42,        # Voigt
                             33, 0.1, 200, 0.09  # RooCMS
                            ]
            elif j == 2:
                if i == 0:
                    pPass = [
                            3e5,   5e3, 
                            0.1, 2, 15,       # Voigt
                            10,0.01, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                            1.5e5,   5e4, 
                            1, 1, 44,           # Voigt
                            20,0.01, 20, 0.09,  # RooCMS
                            ]
                if i == 2:
                    pPass = [
                            12e5,   5e3, 
                            0.1, 2, 15,       # Voigt
                            10,0.01, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                            1.5e5,   5e4, 
                            1, 1, 44,           # Voigt
                            20,0.01, 20, 0.09,  # RooCMS
                            ]
                if i == 3:
                    pPass = [
                            1e6,   5e3, 
                            0.1, 1.5, 15,       # Voigt
                            10,0.01, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                            1.5e5,   5e4, 
                            1, 1, 44,           # Voigt
                            20,0.01, 20, 0.09,  # RooCMS
                            ]
                if i == 5:
                    pPass = [
                            1e5,   5e3, 
                            0.1, 2, 15,       # Voigt
                            10,0.01, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                            1.5e5,   5e4, 
                            1, 1, 44,           # Voigt
                            20,0.01, 20, 0.09,  # RooCMS
                            ]
            elif j == 3:
                if i == 0:
                    pPass = [
                            5e4,   9e3, 
                            #0.1, 2, 15,       # Voigt
                            1, 1, 15,       # Voigt
                            13,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            9e3,   4e3, 
                            1, 1, 44,           # Voigt
                            40,0.01, 20, -0.09,  # RooCMS
                            ]
                elif i == 3:
                    pPass = [
                            1e5,   1e4, 
                            0.5, 1, 14,       # Voigt
                            15,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            3e4,   8e3, 
                            1, 1, 44,           # Voigt
                            45,0.01, 20, -0.09,  # RooCMS
                            ]                
                elif i == 5:
                    pPass = [
                            1e4,   5e3, 
                            0.5, 1, 14,       # Voigt
                            15,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            5e3,   5e3, 
                            0.5, 1, 44,           # Voigt
                            45,0.01, 20, -0.09,  # RooCMS
                            ]
                else:
                    pPass = [
                            6e4,   5e3, 
                            0.1, 2, 15,       # Voigt
                            13,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            9e3,   4e3, 
                            1, 1, 44,           # Voigt
                            45,0.01, 20, -0.09,  # RooCMS
                            ]                        
            elif j == 4:
                if i == 0:
                    pPass = [
                            1e3,  200,  
                            0.5,  1, 15,  
                            15,1, 10,-0.09,
                            ] 

                    pFail = [
                            1e2,  3e1,  
                            0.5,  1, 44,  
                            49,-0.1, 10, -0.09,  # RooCMS
                            ]  
                elif i == 2:
                    pPass = [
                            7e3,  200,  
                            0.5,  1, 15,  
                            15,1, 10,-0.09,
                            ] 

                    pFail = [
                            5e2,  5e2,  
                            0.5,  1, 44,  
                            35,-0.1, 10, -0.09,  # RooCMS
                            ] 
                elif i == 3:
                    pPass = [
                            5e3,  200,  
                            0.1,  1, 15,  
                            15,1, 10,-0.09,
                            ] 

                    pFail = [
                            5e2,  1e2,  
                            0.1,  1, 44,  
                            48,-0.1, 10, -0.09,  # RooCMS
                            ] 
                elif i == 5:
                    pPass = [1.22435554e+03, 3.20343246e+02, 9.22998413e-12,
                             1.10974344e+00, 1.50406031e+01, 1.40180622e+01,
                             6.13551539e-01, 1.00000028e+01, 5.95495234e-01]
                    pFail = [ 4.08455718e+02,  2.34193103e+02,  1.08171908e+00,
                             9.14064665e-01, 4.39415340e+01,  5.75583581e+01, 
                             -5.13886755e-01,  3.82617111e+03,-4.43517032e-02]
                else :
                    pPass = [
                            1e3,  100,  
                            0.5,  1, 15,  
                            15,0.1, 10,-0.09,
                            ] 

                    pFail = [
                            2e2,  1e2,  
                            0.1,  1, 44,  
                            45,0.01, 10, -0.09,  # RooCMS
                            ]                                        
            elif j == 5:
                if i == 0:
                    pPass = [
                            6e4,  1e2,  
                            0.1,  2, 15,  
                            1,1, 1.15814356e+02,1,
                            ] 

                    pFail = [
                            1e3,  1e2,  
                            0.1,  2, 44,  
                            35,  1, 1.15814356e+02,1,
                            ] 
                elif i == 1:
                    pPass = [
                            2e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            2e1,  1e1,  
                            0.5,  1, 44,  
                            48,  -0.1, 10,0.1,
                            ]   
                else:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            40,  3e1,  
                            1,  1, 44,  
                            35,  0.1, 1.15814356e+02,0.1,
                            ]  
        else:
            if   j == 0:
                if  i == 0:
                    pPass = [
                            1e4,   5e3, 
                            0.1, 1, 14,       # Voigt
                            1,0.1, 0.01, 0.09,  # RooCMS
                            ]

                    pFail = [
                            4e3,   2e4, 
                            1, 1.2, 43,       # Voigt
                            30,0.1, 0.01, 0.09,  # RooCMS
                            ]
                elif i != 5:

                    pPass = [
                            1e4,   5e3, 
                            0.1, 1, 14,       # Voigt
                            1,0.1, 0.01, 0.09,  # RooCMS
                            ]

                    pFail = [
                            1.5e3,   5e4, 
                            1, 1.2, 43,       # Voigt
                            30,0.1, 0.01, 0.09,  # RooCMS
                            ]
                elif i == 5:
                    pPass = [
                            5e4,   2e3, 
                            0.1, 1, 14,       # Voigt
                            1,0.1, 0.01, 0.09,  # RooCMS
                            ]

                    pFail = [
                            4e3,   2e4, 
                            1, 1.2, 43,       # Voigt
                            10,0.1, 0.01, 0.09,  # RooCMS
                            ]
            elif j == 1:
                if i == 0:
                    pPass = [
                            1e5,   7e3, 
                            0.1, 2, 15,       # Voigt
                            10,0.1, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                             3e4, 5e4,
                             2, 0.01, 43,        # Voigt
                             33, 0.1, 200, 0.09  # RooCMS
                            ]
                elif i == 2:
                    pPass = [
                            5e5,   6e4, 
                            0.1, 2, 15,       # Voigt
                            5,0.1, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                             2e4, 5e4,
                             2, 0.01, 43,        # Voigt
                             33, 0.1, 200, 0.09  # RooCMS
                            ]
                elif i == 3:
                    pPass = [
                            5e5,   1e5, 
                            0.1, 2, 14,       # Voigt
                            10,0.1, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                             3e4, 5e4,
                             2, 0.01, 43,        # Voigt
                             33, 0.1, 200, 0.09  # RooCMS
                            ]
                elif i == 5:
                    pPass = [
                            1e5,   8e4, 
                            0.1, 2, 15,       # Voigt
                            30,0.01, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                             1e4, 1e4,
                             2, 0.01, 43,        # Voigt
                             33, 0.1, 200, 0.09  # RooCMS
                            ]
            elif j == 2:
                if i == 0:
                    pPass = [
                            3e5,   5e3, 
                            0.1, 2, 15,       # Voigt
                            10,0.1, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                            1.5e5,   5e4, 
                            1, 1, 44,           # Voigt
                            20,0.1, 20, 0.09,  # RooCMS
                            ]
                if i == 2:
                    pPass = [
                            12e5,   5e3, 
                            0.1, 2, 15,       # Voigt
                            30,0.1, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                            1.5e5,   5e4, 
                            1, 1, 44,           # Voigt
                            20,0.1, 20, 0.09,  # RooCMS
                            ]
                if i == 3:
                    pPass = [
                            3e6,   5e3, 
                            0.2, 1.5, 15,       # Voigt
                            5,0.1, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                            8e4,   1e4, 
                            0.1, 1, 44,           # Voigt
                            35,0.1, 20, 0.09,  # RooCMS
                            ]
                if i == 5:
                    pPass = [
                            4e5,   1e3, 
                            1.5, 1.7, 15,       # Voigt
                            3,0.01, 10, 0.09,  # RooCMS
                            ]

                    pFail = [
                            1.5e5,   5e4, 
                            1, 1, 44,           # Voigt
                            20,0.01, 20, 0.09,  # RooCMS
                            ]
            elif j == 3:
                if i == 0:
                    pPass = [
                            5e4,   9e3, 
                            #0.1, 2, 15,       # Voigt
                            1, 1, 15,       # Voigt
                            13,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            9e3,   4e3, 
                            1, 1, 44,           # Voigt
                            40,0.01, 20, -0.09,  # RooCMS
                            ]
                elif i == 2:
                    pPass = [
                            5e4,   9e3, 
                            #0.1, 2, 15,       # Voigt
                            1, 1, 15,       # Voigt
                            13,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            9e3,   4e3, 
                            1, 1, 44,           # Voigt
                            40,0.01, 20, -0.09,  # RooCMS
                            ]
                elif i == 3:
                    pPass = [
                            5e4,   9e3, 
                            #0.1, 2, 15,       # Voigt
                            1, 1, 15,       # Voigt
                            13,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            9e3,   4e3, 
                            1, 1, 44,           # Voigt
                            40,0.01, 20, -0.09,  # RooCMS
                            ]
                elif i == 5:
                    pPass = [
                            7e4,   5e3, 
                            0.1, 2, 15,       # Voigt
                            13,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            9e3,   4e3, 
                            1, 1, 44,           # Voigt
                            40,0.01, 20, -0.09,  # RooCMS
                            ]
                else:
                    pPass = [
                            2e5,   5e3, 
                            0.1, 2, 15,       # Voigt
                            13,0.01, 10, -0.09,  # RooCMS
                            ]

                    pFail = [
                            9e3,   4e3, 
                            1, 1, 44,           # Voigt
                            40,0.01, 20, -0.09,  # RooCMS
                            ]
            elif j == 4:
                if i == 0:
                    pPass = [
                            5e3,  200,  
                            0.1,  2, 15,  
                            15,-0.1, 100,1,
                            ] 

                    pFail = [
                            4e2,  1e2,  
                            0.1,  2, 44,  
                            42,-0.1, 100,1,
                            ] 
                elif i == 2:
                    pPass = [
                            5e3,  200,  
                            0.1,  2, 15,  
                            15,-0.1, 100,1,
                            ] 

                    pFail = [
                            4e2,  1e2,  
                            0.1,  2, 44,  
                            60,-0.1, 100,1,
                            ] 
                elif i == 3:
                    pPass = [
                            5e3,  200,  
                            0.1,  2, 15,  
                            15,-0.1, 100,1,
                            ] 

                    pFail = [
                            5e2,  1e2,  
                            0.1,  2, 44,  
                            60,0.1, 100,1,
                            ] 
                else :
                    pPass = [
                            5e3,  200,  
                            0.1,  2, 15,  
                            15,-0.1, 100,1,
                            ] 

                    pFail = [
                            5e2,  1e2,  
                            0.1,  2, 43,  
                            42,-0.1, 100,1,
                            ] 
            elif j == 5:
                if i == 0:
                    pPass = [
                            3e3,  1e2,  
                            0.1,  1, 15,  
                            1,0.1, 1.15814356e+02,1,
                            ] 

                    pFail = [
                            1e3,  1e2,  
                            0.1,  1, 44,  
                            70,-0.1, 1.15814356e+02,1,
                            ] 
                elif i == 1:
                    pPass = [
                            6e2,  3e1,  
                            0.5,  1, 15,  
                            10,0.1, 1.15814356e+02,0.1,
                            ] 

                    pFail = [
                            200,  3e1,  
                            1,  1, 44,  
                            10,  0.1, 1.15814356e+02,0.1,
                            ]  

    #################################
    
    BoundedFit = [
                   [0,0,
                    0,0,10,
                    #0,-np.inf,-np.inf,-1],
                    #0,-0.9,-np.inf,-0.9],
                    0,-0.3,-np.inf,-0.9],
                   [np.inf,np.inf,
                    3,3,48,
                    #70,np.inf,np.inf,1,
                    #70, 0.9, np.inf,0.9,
                    70, 0.3, np.inf,0.9,
                   ]
                    ]
        
    return pPass, pFail, BoundedFit


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:



