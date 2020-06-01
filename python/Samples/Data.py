
# coding: utf-8

# In[1]:


from ROOT import TFile, TMVA
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from root_pandas import read_root 
import sys

class Data(object):
    def __init__(self, 
                 folderFile = '',
                 nameFile   = '',
                 trigger    = '',
                 era        = '',
                 data       = False,
                 flag       = False,
                 var        = [],
                 df         = pd.DataFrame(),
                 Print      = True,
                ):
        self.folder  = folderFile
        self.name    = nameFile
        self.trigger = trigger
        self.data    = data
        self.era     = era
        self.flag    = flag
        self.file    = None
        self.df      = df
        self.var     = var
        
        self.sampLength = 0
        self.Topo = Topology(self.era)
                     
        if not df.empty:
            self.df = df
            self.sampLength = len(self.df)
            self.cuts       = [True for _ in range(self.sampLength)] 
            #self.weight  = self.df.weights
            #self.weights = self.weight
            
            self.weight  = np.array(self.df.weights)
            self.weights = np.array(self.weight)
            
            self.puWeight = self.df.puWeight
            
            self.TotalEventBin = 31       
            self.TotalEvent    = [0 for _ in range(self.TotalEventBin)]
        else:
            ### Reading the Data/MC
            if data:
                if Print:
                    print('----------------- DATA --------------------------')
                    print('Opening    File::' + folderFile + "output_" + self.name + self.trigger + "_v.root")
                    print('Opening    tree::'   +"   tree_" + self.name + self.trigger)
                    print('-------------------------------------------------')
                try:
                    if len(self.var) > 0:
                        self.df   = read_root(folderFile + "output_" + self.name + self.trigger +"_v.root",columns = self.var)
                    else:
                        self.df   = read_root(folderFile + "output_" + self.name + self.trigger +"_v.root")
                    self.file = TFile    (folderFile + "output_" + self.name + self.trigger +"_v.root",'read')
                    self.sampLength = len(self.df.nPV)
                except:
                    self.file = None
                    self.df = pd.DataFrame()
                    self.sampLength = 0
            else :
                if flag:
                    if Print:
                        print('-------------------- MC -----------------------')
                        print('Opening    File::' + folderFile + "output_" + self.name + self.trigger + "_0.root")
                        print('Opening    tree::' + "   tree_" + self.name + self.trigger)           
                        print('-----------------------------------------------')   

                    try:
                        if len(self.var) > 0:
                            self.df = read_root(folderFile + "output_" + self.name + self.trigger + "_0.root",columns = self.var)
                        else:
                            self.df = read_root(folderFile + "output_" + self.name + self.trigger + "_0.root")
                        self.file = TFile(folderFile + "output_" + self.name + self.trigger + "_0.root")
                        self.sampLength = len(self.df.nPV)
                    except:
                        self.file = None
                        self.df = pd.DataFrame()
                        self.sampLength = 0
                else :
                    if Print:
                        print('-------------------- MC -----------------------')
                        print('Opening    File::' + folderFile + "output_" + self.name + self.trigger + "_0.root")
                        print('Opening    tree::' + "   tree_" + self.name.lower())# + self.trigger)
                        print('-----------------------------------------------')            
                    try:
                        if len(self.var) > 0:
                            self.df = read_root(folderFile + "output_" + self.name + self.trigger + "_0.root",columns = self.var)
                        else:
                            self.df = read_root(folderFile + "output_" + self.name + self.trigger + "_0.root")
                        self.file = TFile(folderFile + "output_" + self.name + self.trigger + "_0.root")
                        self.sampLength = len(self.df.nPV)
                    except:
                        self.file = None
                        self.df   = pd.DataFrame()
                        self.sampLength = 0

            self.cuts = [True for _ in range(self.sampLength)] 

            self.TotalEventBin = 31       
            self.TotalEvent    = [0 for _ in range(self.TotalEventBin)]

            if self.file != None:
                for i in range(self.TotalEventBin):
                    self.TotalEvent[i]    = self.TotalEvents(i)            
                #self.weights  = self.Weights(self.era)
                #self.weight   = self.Weights(self.era)   
                
                self.weights  = np.array(self.Weights(self.era))
                self.weight   = np.array(self.Weights(self.era) )  
                
                self.puWeight = np.ones(len(self.weight))

                try:
                    for attr in self.df.columns:
                        self.df[attr+'_EE'] = self.df[attr][np.abs(self.df.photonOneEta) > 1.48 ]
                        self.df[attr+'_EE'] = [None]*len(self.df[attr][np.abs(self.df.photonOneEta) <= 1.48 ])

                    for attr in self.df.columns:
                        self.df[attr+'_EB'] = self.df[attr][np.abs(self.df.photonOneEta) <= 1.48 ]
                        self.df[attr+'_EB'] = [None]*len(self.df[attr][np.abs(self.df.photonOneEta) > 1.48 ])
                except:
                    err = sys.exc_info()[0]
                    print( "<p>Error: %s</p>" % err )
            else:
                for i in range(self.TotalEventBin):
                    self.TotalEvent[i]    = 0
                #self.weights  = self.Weights(self.era)
                #self.weight   = self.Weights(self.era)
                
                self.weights  = np.array(self.Weights(self.era))
                self.weight   = np.array(self.Weights(self.era))
                
                self.puWeight = np.ones(len(self.weight))
                   
    def __add__(self,other):
        Other = Data()
        
        Other.folder     = self.folder
        Other.name       = self.name
        Other.trigger    = other.trigger
        Other.data       = other.data 
        Other.flag       = other.flag
        Other.era        = self.era
        
        Other.cuts       = self.cuts  + other.cuts
        Other.sampLength = self.sampLength + other.sampLength
        
        
        
        Other.file    = other.file
        Other.weights = np.array(list(self.weights) + list(other.weights))
        Other.weight  = Other.weights
        
        Other.puWeight = list(self.puWeight) + list(other.puWeight)
        
        Other.TotalEventBin = other.TotalEventBin
        try:
            Other.df = self.df.append(other.df)
            for i in range(other.TotalEventBin):
                Other.TotalEvent[i] = self.TotalEvent[i] + other.TotalEvent[i]
        except:
            Other.df = pd.DataFrame()
            for i in range(other.TotalEventBin):
                Other.TotalEvent[i] = self.TotalEvent[i]
            print('-/!\- Could not sum!')
        
        return Other
                
    # ---------------
    # Num of events and SF/weights   
    def TotalEvents(self,n):
        if n == '':
            return self.file.Get("TotalEvents_"+self.name.lower())
        elif self.data:
            return self.file.Get("TotalEvents_"+self.name+self.trigger).GetBinContent(n)
        else: 
            if self.flag:
                return self.file.Get("TotalEvents_" + self.name + self.trigger).GetBinContent(n)
            else:
                return self.file.Get("TotalEvents_" + self.name.lower()).GetBinContent(n)
    def ScaleFactor(self,era):
        return self.Topo.GetSF( self.N(), era,self.name,self.data) 
    def XSec():
        return sefl.Topo._GetXsec(self.name)
    def N(self,Type=''):
        if Type == '':
            return self.TotalEvent[1] - 2*self.TotalEvent[30] 
        elif Type == 'selection':
            return np.sum(self.cuts)         
    def Weights(self,era):
        if self.data:
            return [    1              for _ in range(self.sampLength)]   
        else :
            try:
                #return list(np.array(self.df.genWeight)*np.array(self.df.eventWeight)*self.df.photonIDWeight*np.array([self.ScaleFactor(era) for _ in range(self.sampLength)]))
                return list(np.array(self.df.genWeight)*np.array(self.df.eventWeight)*np.array([self.ScaleFactor(era) for _ in range(self.sampLength)]))
            except:
                return [    1              for _ in range(self.sampLength)]   
    # ---------------
    # CUTS functions
    def AddCuts(self,cuts):
        self.cuts = np.logical_and(self.cuts,cuts)
    def RemoveCuts(self,cuts):
        self.cuts = np.logical_or(self.cuts,np.logical_not(cuts))
    def ResetCuts(self,cuts = []):
        if len(cuts) != 0:
            self.cuts = cuts
        else:
            self.cuts = np.ones(len(self.cuts),dtype=np.bool)
    def GetWithCuts(self,var):
        if self.df.empty:
            return np.array([])
        else:
            if var == 'weight' or var == 'weights':
                return np.array(getattr(self,var))[self.cuts]
            elif var == 'puWeight' or var == 'puWeight':
                return np.array(getattr(self,var))[self.cuts]
            else:
                return np.array(getattr(self.df,var))[self.cuts]

    # ---------------
    # GET BDT
    def FillBDTscore(self):
        phVals = ["EE","EB"]
        path = "/home/jcordero/CMS/JYCMCMS/SMP_ZG/python/Corrections/"
        file = {}
        for ph in phVals:
            file[ph] = "TMVAnalysis_BDT_"+ph+".weights.xml"
            reader[ph] = TMVA.Reader()
        
        ###########################################
        ##
        ## Adding the variables to the MVA object
        ## &
        ## Fill in the variables from the Data
        ##
        phVar = {}
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
        var = {}
        for ph in ["EE","EB"]:
            var[ph] = {}
            for vn in varName.keys():
                var[ph][vn] = array.array('f',[0])
                reader[ph].AddVariable(vn, var[ph][vn])
                
                if ph == "EE": # this is just to fill in once
                    if len(varName[vn]) > 1:
                        phVar[vn] = ZG.GetWithCuts(varName[vn][0])/ZG.GetWithCuts(varName[vn][1])
                    else:
                        phVar[vn] = ZG.GetWithCuts(varName[vn][0])
                
                
            reader[ph].BookMVA("BDT",path+file[ph])
            
        #######################
        ##
        ## Fill the BDT
        ##
        ShowerShapeBDT = []
        
        for i in range(len(self.GetWithCuts('cuts'))):
            if np.abs(phVar["recoSCEta"][i]) > 1.48:
                ph = "EE"
            else:
                ph = "EB"
            
            for vn in varName:
                var[ph][vn] = phVar[vn]
                
            ShowerShapeBDT.append(reader[ph].EvaluateMVA("BDT"))
            
        #######################################
        ##
        ## Add the BDT score to the DataFrame
        ##
        sefl.df["ShowerShapeBDT"] = ShowerShapeBDT


# In[15]:


class Topology(object):
    def __init__(self,era):
        self.era = era
        self.__xsec = {}
        self.__BR = {}
        self.__lumi = {}
        #--------------------------------------
        # Luminosity --- units = fb^-1
        self.__lumi = {}
        #self.__lumi['2016'] = 37.80 
        self.__lumi['2016'] = 35.922 # After Lumi Mask | Ming's Lumi = 35867.1
        self.__lumi['2017'] = 41.529
        self.__lumi['2017_50ns'] = 135.27
        self.__lumi['2017_RunA'] = 0
        self.__lumi['2017_RunB'] =  4.823 # 4.792
        self.__lumi['2017_RunC'] =  9.664 # 9.755
        self.__lumi['2017_RunD'] =  4.252 # 4.319
        self.__lumi['2017_RunE'] =  9.278 # 9.424
        self.__lumi['2017_RunF'] = 13.540 #13.500
        self.__lumi['2018']      = 58.83
        self.__lumi['2018_RunA'] = 13.48
        self.__lumi['2018_RunB'] = 6.785
        self.__lumi['2018_RunC'] = 6.612
        self.__lumi['2018_RunD'] = 31.95
        #--------------------------------------
        # Branchin Ratio
        self.__BR["All"] = 1
        #self.__BR["H2ZGm"] = 1.54e-3
        self.__BR["H2ZGm"] = 1

        ### W Branching
        self.__BR["W2e"]   = 0.108
        self.__BR["W2mu"]  = 0.106
        self.__BR["W2tau"] = 0.112
        #self.__BR["W2ud"] = 0.676/3
        #self.__BR["W2sc"] = 0.676/3

        ### Z Branching
        self.__BR["Z2ee"]     = 0.0363
        self.__BR["Z2mumu"]   = 0.0366
        self.__BR["Z2tautau"] = 0.0367
        self.__BR["Z2jj"]     = 0.692
        self.__BR["Z2bbbar"]  = 0.156
        self.__BR["Z2ddbar"]  = 0.156
        self.__BR["Z2ssbar"]  = 0.156
        self.__BR["Z2uubar"]  = 0.116
        self.__BR["Z2ccbar"]  = 0.116

        # Top to Wb
        self.__BR["t2Wb"] = 0.91
        
        #--------------------------------------
        self.__xsec["Test"]     = 1
        
        self.__xsec["Muon"]     = 1
        self.__xsec["DoubleMuon"]     = 1
        
        # Crossection of H = 125.5 GeV @ 13 TeV --- units = pb        
        self.__xsec["TT"]             = 831.76
        self.__xsec["TTTo2L2Nu"]      = 87.31
        self.__xsec['VBFHToZG_ZToJJ'] = 3.766*self.__BR['H2ZGm']*self.__BR['Z2jj']  
        self.__xsec["WplusH"]         = 0.831*self.__BR['H2ZGm']*self.__BR['Z2jj']
        self.__xsec["WminusH"]        = 0.527*self.__BR['H2ZGm']*self.__BR['Z2jj']
        self.__xsec["WH"]             = 1.380*self.__BR['H2ZGm']*self.__BR['Z2jj']  
        # Note
        # --xsecFrac[W+] = 0.831
        # --xsecFrac[W-] = 0.527
        # -----Br[H->Z+gm] = 0.002
        # -----Br[Z->j+j]  = 0.72
        
        
        if era == "2016":
            self.__xsec['ZGToLLG']  = 47.34 
            self.__xsec['ZG_ZToLL'] = 47.34 
        elif era == "2017":
            self.__xsec['ZGToLLG']  = 117.864 
            #self.__xsec['ZGToLLG']  = 147.5
        else:
            self.__xsec['ZGToLLG']  = 117.864 
            #self.__xsec['ZGToLLG']  = 147.5
        
        #self.__xsec['DYJets']      = 5943.2 #DYJetsToLL_M-50_amcatnlo 5765.4 #3503.7#
        self.__xsec['DYJets']      = 6077.22
        #self.__xsec['DYJets']      = 6225.42
        #self.__xsec['DYJets']      = 7500
        
        self.__xsec['ZZTo2L2Q']    = 3.22
        self.__xsec['ZZTo2L2Nu']   = 0.564
        self.__xsec['ZZTo4L']      = 1.212        
        
        self.__xsec["WWTo2L2Nu"]   = 12.178
        self.__xsec["WWToLNuQQ"]   = 49.997
        
        self.__xsec["WZ"]          = 0.8594 
        self.__xsec['WZTo2L2Q']    = 5.595
        self.__xsec['WZTo1L1Nu2Q'] = 10.71
        self.__xsec["WZTo3LNu"]    = 4.42965
        self.__xsec["WZTo1L3Nu"]   = 3.033
        
        self.__xsec['ggF']         = 43.62  
        self.__xsec['VBF']         = 3.727  
        
        self.__xsec['WJets']       = 61526.7
        self.__xsec['W1Jets']      = 9493.0
        self.__xsec['W2Jets']      = 3120.0 
        self.__xsec['W3Jets']      = 942.3
        self.__xsec['W4Jets']      = 524.1
        
        self.__xsec['W1JetsToLNu'] = 9493.0
        self.__xsec['W2JetsToLNu'] = 3120.0 
        self.__xsec['W3JetsToLNu'] = 942.3
        self.__xsec['W4JetsToLNu'] = 524.1
        
    def _GetXsec(self, process):
        if type(process) == str:
            return(self.__xsec[process])
        else :
            return(np.prod([self.__xsec[p] for p in process]))

    def _GetBR(self, process):
        if type(process) == str:
            return(self.__BR[process])
        else: 
            return(np.prod([self.__BR[p] for p in process]))

    def _GetLumi(self, process):
        return(self.__lumi[process])

    def GetSF(self, N,lumName,xsecName,data=False):
        if(N != 0 and not data):
            return(1e3*self._GetXsec(xsecName)*self._GetLumi(lumName)/N)
        else: 
            return(1)
        

