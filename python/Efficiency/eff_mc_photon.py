#!/usr/bin/env python
# coding: utf-8

# In[39]:


import sys
import datetime
import os


# In[40]:


projectdir = "/home/jcordero/CMS/JYCMCMS/SMP_ZG/"
sys.path.append(projectdir + "python")


# In[41]:


import array
import matplotlib.pyplot as plt
import numpy as np

import scipy.special as spc
from scipy.optimize import curve_fit


# In[42]:


from ROOT import TFile,TTree,TH2F, TCanvas,gROOT,gStyle
from root_pandas import read_root 


# In[43]:


from Config import Config
from Plotter.Plotter import Helper


# In[44]:


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


# In[45]:


def BinIndex(Data,Low,Max):
    return np.logical_and(np.array(Data) >= Low, np.array(Data) <  Max)


# In[50]:


def setConfiguration(selection,era):
    
    if   era == "2016":
        run = ['B','C','D','E','F','G','H']    
        DataGen = 'legacy'
        #path = "/home/jcordero/CMS/data/data_"+era+"/"+DataGen+"/SMP_ZG/Files/ee/"+SampleSet+"/DYJets/"
        if selection == "mumug":
            SampleSet = "MatchZGpaper"
        elif selection == "elelg":
            SampleSet = "MatchZGpaper"
        elif selection == "ee":
            SampleSet = "/EfficiencyCorrection/files_zee/TagProbe"
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
            SampleSet  = "V6_Accept"  
        elif selection == "elelg":
            #SampleSet = 'V1'
            #SampleSet = 'V2_puWeight'
            #SampleSet = 'V2_puWeight_phID'
            #SampleSet = "V4_phID_isConv"
            #SampleSet = "V4_phID_isConv_MINUIT"
            #SampleSet  = "V5_mediumID"
            #SampleSet  = "V6_lPhoton"
            SampleSet  = "V6_Accept"   
        elif selection == "mumu":
            #SampleSet = 'V1'
            #SampleSet = 'V2_puWeight'
            SampleSet = 'V2_puWeight_phID'
        elif selection == "ee":
            SampleSet = 'EfficiencyCorrection/files_zee/TagProbe'
    elif era == "2018":
        run = ['A','B','C','D']
        DataGen = 'rereco'
        if selection == "mumug":
            #SampleSet = 'V1_trigBits'
            SampleSet = 'V2_trigBits_pu'
        elif selection == "elelg":
            SampleSet = 'V2_trigBits'
        elif selection == "mumu":
            SampleSet = 'V2_trigBits'
        elif selection == "ee":
            SampleSet = 'EfficiencyCorrection/files_zee/V2_trigBits_pu'

    print(era,selection)
    print(SampleSet)
    path = "/home/jcordero/CMS/data/data_"+era+"/"+DataGen+"/SMP_ZG/Files/"+selection+"/"+SampleSet
    
    pathMVA = "/home/jcordero/CMS/data/data_"+era+"/"+DataGen+"/SMP_ZG/Files/ShowerShapeMVA/"
    #path    = "/home/jcordero/CMS/data/data_"+era+"/"+DataGen+"/SMP_ZG/Files/"+selection+"/"+SampleSet+"/"
    figpath = "/home/jcordero/CMS/JYCMCMS/SMP_ZG/figs/"+era+"/"+DataGen+"/"+selection+"/"
    pathSelection = "/home/jcordero/CMS/data/data_"+era+"/"+DataGen+"/SMP_ZG/Files/"+selection+"/"+SampleSet+"/Reduced"

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


# In[51]:


era = "2016"
#era = "2017"
#era = "2018"

selection = "ee"
#selection = "mumug"
#selection = "elelg"

config, pathMVA, path, figpath, pathSelections = setConfiguration(selection,era)

figpath = dirStructure(figpath, Print = True)


# In[8]:


fileName = "output_DYJets_v_0.root"
file = TFile(path+fileName,"read")


# # Create Eff for MC

# In[4]:


var = ["dileptonM",
       "leptonOnePt","leptonOneEta",
       "leptonTwoPt","leptonTwoEta",
       "vetoDY","genIsoPass",
       "ProbeIDPass","ProbeISOPass","ProbeWorstPass","ProbeSigPass",
       #"ProbePass",
       #"TagFromZ","ProbeFromZ",
      ]


# In[ ]:





# In[5]:


#samples = ["DYJets","WJets"]
samples = ["DYJets"]
s = samples[0]

#path = "/home/jcordero/CMS/data_2016/legacy/SMP_ZG/Files/ee/files_zee/"+NewOld+s+"/"
fileName = "output_"+s+"_v_0.root"
dfMC = read_root(path+fileName,columns = var)


# In[7]:


ptBins  = array.array('f',[15, 20,  35,  50,  90,  150,  1500])
#ptBins = BinFormat(ptBins)
#################
etaBins = array.array("f",[-2.5,-1.566,-1.4442,0,1.4442,1.566,2.5])


# In[8]:


ProbeType = "Pass"
part      = 'dilepton'
variable  = 'M'
sample    = dfMC

ptBins, etaBins = BinFormat(ptBins,Type='ranges'),BinFormat(etaBins,Type='ranges')
ptNBins , etaNBins= len(ptBins), len(etaBins)

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
        VAL = sample[part+variable]
        #Ind = sample.vetoDY == False
        if ProbeType == "Pass":
            Ind = sample["ProbeIDPass"] == True
            Ind = np.logical_and(Ind,sample["ProbeISOPass"]   == True)
            Ind = np.logical_and(Ind,sample["ProbeWorstPass"] == True)
            Ind = np.logical_and(Ind,sample["ProbeSigPass"]   == True)
        else:
            Ind = sample["ProbeIDPass"] == False
            Ind = np.logical_or(Ind,sample["ProbeISOPass"]   == False)
            Ind = np.logical_or(Ind,sample["ProbeWorstPass"] == False)
            Ind = np.logical_or(Ind,sample["ProbeSigPass"]   == False)
            
        if samples == "DYJets":
            Ind = np.logical_and(Ind,sample.ProbeFromZ == True)

        Var = np.array(VAL[Ind])
        Pt  = sample['leptonTwoPt'][Ind]
        Eta = sample['leptonTwoEta'][Ind]


        ptInd  = BinIndex(Pt , ptBins [j][0], ptBins [j][1])
        #etaInd = BinIndex(Eta, etaBINS[i][0], etaBINS[i][1])
        etaInd = BinIndex(Eta, etaBins[i][0], etaBins[i][1])
        Ind    = np.logical_and(ptInd,etaInd)
        
        #print(i,j,np.sum(ptInd),np.sum(etaInd))
        Yields[ProbeType][j][i] = np.sum(Ind)
#dfMC.leptonProbeFailPt


# In[ ]:





# In[9]:


ProbeType = "Fail"
part      = 'dilepton'
variable  = 'M'

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
        VAL = sample[part+variable]

        if ProbeType == "Pass":
            Ind = sample["ProbeIDPass"] == True
            Ind = np.logical_and(Ind,sample["ProbeISOPass"]   == True)
            Ind = np.logical_and(Ind,sample["ProbeWorstPass"] == True)
            Ind = np.logical_and(Ind,sample["ProbeSigPass"]   == True)
        else:
            Ind = sample["ProbeIDPass"] == False
            Ind = np.logical_or(Ind,sample["ProbeISOPass"]   == False)
            Ind = np.logical_or(Ind,sample["ProbeWorstPass"] == False)
            Ind = np.logical_or(Ind,sample["ProbeSigPass"]   == False)
            
        if samples == "DYJets":
            Ind = np.logical_and(Ind,sample.ProbeFromZ == True)
        
        Var = np.array(VAL[Ind])
        Pt  = sample['leptonTwoPt'][Ind]
        Eta = sample['leptonTwoEta'][Ind]
        

        ptInd  = BinIndex(Pt , ptBins [j][0], ptBins [j][1])
        #etaInd = BinIndex(Eta, etaBINS[i][0], etaBINS[i][1])
        etaInd = BinIndex(Eta, etaBins[i][0], etaBins[i][1])
        Ind    = np.logical_and(ptInd,etaInd)
        
        print(i,j,ptBins[j], etaBins[i],np.sum(Ind))
        
        Yields[ProbeType][j][i] = np.sum(Ind)


# In[10]:


eff = {}
for j in np.arange(ptNBins):    
    eff[j] = {}
    for i in np.arange(etaNBins):        
        if Yields['Pass'][j][i] + Yields['Fail'][j][i] != 0:
            eff[j][i] = float(Yields['Pass'][j][i])/(Yields['Pass'][j][i] + Yields['Fail'][j][i])
        else:
            eff[j][i] = 0
        print(j,i,Yields['Pass'][j][i],Yields['Fail'][j][i],eff[j][i])


# In[11]:


figpath


# In[81]:


fileOut = TFile(figpath + "eff_mc_photon.root","recreate")
tree = TTree("eff_photon","eff_photon")

ptBins, etaBins = BinFormat(ptBins,Type='edges'),BinFormat(etaBins,Type='edges')
#ptNBins,etaNBins = len(ptBins),len(etaBins)
ptNBins,etaNBins = len(ptBins)-1,len(etaBins)-1


gStyle.SetOptStat(0)

hist2d = TH2F("EGamma_eff","Eff",
              ptNBins ,ptBins,
              etaNBins,etaBins)
histText = TH2F("EGamma_eff","Eff",
              ptNBins ,ptBins,
              etaNBins,etaBins)

tree.Branch("eff",hist2d,"TH2F")


#for i in range(ptNBins):
#    for j in range(etaNBins):
for i in range(ptNBins):
    for j in range(etaNBins):        
        hist2d.SetBinContent(i+1,j+1,eff[i][j])
        histText.SetBinContent(i+1,j+1,eff[i][j])
        tree.Fill()

hist2d.GetXaxis().SetRangeUser(0,-250)
hist2d.GetZaxis().SetRangeUser(0.5,0.95)
fileOut.Write()
fileOut.Close()


# In[82]:


fileOut = TFile(figpath + "eff_draw_photon.root","recreate")
tree = TTree("eff_photon","eff_photon")

ptBins, etaBins = BinFormat(ptBins,Type='edges'),BinFormat(etaBins,Type='edges')
#ptNBins,etaNBins = len(ptBins),len(etaBins)
ptNBins,etaNBins = len(ptBins)-2,len(etaBins)-1


gStyle.SetOptStat(0)

hist2d = TH2F("EGamma_eff","Eff",
              ptNBins ,ptBins,
              etaNBins,etaBins)
histText = TH2F("EGamma_eff","Eff",
              ptNBins ,ptBins,
              etaNBins,etaBins)

tree.Branch("eff",hist2d,"TH2F")


#for i in range(ptNBins):
#    for j in range(etaNBins):
for i in range(ptNBins):
    for j in range(etaNBins):        
        hist2d.SetBinContent(i+1,j+1,eff[i][j])
        histText.SetBinContent(i+1,j+1,eff[i][j])
        tree.Fill()

hist2d.GetXaxis().SetRangeUser(0,-250)
hist2d.GetZaxis().SetRangeUser(0.5,0.95)
fileOut.Write()
#fileOut.Close()


# In[83]:


#c = TCanvas('c','c',200,100,10)
c = TCanvas()
#hist2d.GetXaxis().SetRange(0,200)
#histText.GetXaxis().SetRange(0,200)
hist2d.Draw("COLZ")
histText.Draw("TEXT SAME")
c.Draw()


# In[ ]:





# In[ ]:




