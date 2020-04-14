#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys


# In[ ]:


projectdir = "/home/jcordero/CMS/JYCMCMS/SMP_ZG/"
sys.path.append(projectdir + "python")


# In[4]:


import numpy as np
from scipy.special import wofz

import json


# In[ ]:


from ROOT import TCanvas, TFile
from Common.CommonHelper import CommonHelper


# In[14]:


class Efficiency():
    def __init__(self,
                 Config,
                 Data = None,
                 Signal = None,
                 Bkg = None,
                ):
        self.projectdir = Config.projectdir
        self.jsonSRC = self.projectdir + "json/plot/eff_bins.json"
        
        self.Data   = Data
        self.Signal = Signal
        self.Bkg    = Bkg
        
        # This variables are set through member functions
        self.binsFile = None
        self.bins = {}
        self.var  = []
        self.Type = None
    
        self.binsAlternative = {}
        
    def __str__(self):
        msg =   "--Json source: {}\n"                 "--Bins type: {}\n"                 "--Bin variables: {}\n".format(self.jsonSRC,self.Type, self.vars)
        for v in self.bins:
            msg += "--{}: {}\n".format(v,self.bins[v])
                
        return msg 
            
    def __validateType(self,bins,Type):
        return True if Type in list(bins.keys()) else False
    
    def __validateVar(self,bins,Type,var):
        return True if var in list(bins[Type].keys()) else False
    
    def __useAlternative(self,index,BinIndexAlt):
        return True if index in BinIndexAlt else False

    def __validationForYield(self,bins1,bins2):
        var1, var2 = next(iter(bins1)), next(iter(bins2))
        if not self.__validateVar(self.binsFile,self.Type,var1):
            bins1 = {}
        if not self.__validateVar(self.binsFile,self.Type,var2):
            bins2 = {}
        
        if bins1 == {}:
            bins1 = {self.vars[0]:self.bins[self.vars[0]]}
            print("From: {}".format(self.jsonSRC))
            print("Bins1 set to  {} form json file".format(self.vars[0]) )
            
        if bins2 == {}:
            bins2 = {self.vars[1]:self.bins[self.vars[1]]}
            print("From: {}".format(self.jsonSRC))
            print("Bins2 set to  {} form json file".format(self.vars[1]) )
            
        return bins1,bins2

    
    def readFile(self):
        with open(self.jsonSRC) as f:
            JS = f.read()
        return json.loads(JS)

    def loadBins(self, Type = "BinSet1"):
        bins = self.readFile()
        
        if self.__validateType(bins, Type):
            self.binsFile = bins
            self.Type = Type
            self.vars = [ v for v in bins[Type] ]
            self.bins = { var:bins[Type][var] for var in self.vars }
            self.binsAlternative = { var:[] for var in self.vars }
            
        else:
            print("Bin Type is not valid")
            for typ in bins:
                print('---'+typ)
        
    def setBinRegion(self,var,alt):
        if alt == []:
            if self.__validateVar(self.binsFile, self.Type, var):
                self.binsAlternative[var] = alt
            else:
                print("Variable is not on the binning json or incorrect.")
        else:
            print("Region variable empty")
            
            
    
    def GetYields(self,
                  dist1, dist2,
                  bins1 = {}, bins2 = {},
                  Alternative = {},
                  Abs1 = False, Abs2 = False,
                ):
        """Gets the yields on the samples distribution, binned in 2d"""
        """ Dist1 and Dist2 corresponding distributions for variables of bins1 and bins2"""
        
        ### Input validation
        bins1, bin2 = self.__validationForYield(bins1,bins2)
        var1, var2 = next(iter(bins1)), next(iter(bins2))
        
        ### Bin formating
        bins1[var1],bins2[var2] = CommonHelper.Plot.BinFormat(bins1[var1]), CommonHelper.Plot.BinFormat(bins2[var2])
        N1Bin,N2Bin = len(bins1[var1]),len(bins2[var2])

        Yield = {}
        bin1 = bins1[var1]
        for j in np.arange(N1Bin):
            Yield[j] = {}
            if self.__useAlternative(j,Alternative):
                Bin2 = self.binsAlternative[var2]
            else:
                Bin2 = bins2[var2]

            for i in np.arange(len(Bin2)): 
                Ind1 = CommonHelper.Plot.BinIndex( dist1, bin1[j][0], bin1[j][1], Abs=Abs1)
                Ind2 = CommonHelper.Plot.BinIndex( dist2, Bin2[i][0], Bin2[i][1], Abs=Abs2)
                
                Ind    = np.logical_and(Ind1,Ind2)
                
                Yield[j][i] = np.sum(Ind)
                
        return Yield
        
    def getIndex(self,sample,filters, flag ):
        Indices = np.ones(len(sample))
        for filt in filters:
            Indices = np.logical_and(Indices, sample.df[filt] == flag)
        return Indices
    
    def getEff(self,Pass,Fail):
        Pass, Fail = float(Pass), float(Fail)
        return 0 if (Pass + Fail) == 0 else Pass/(Pass + Fail)
        
    def getEffStat(self,Pass,Fail):
        Pass, Fail = float(Pass), float(Fail)
        return 0 if (Pass + Fail) == 0 else eff*np.sqrt( 1/Pass + 1/(Pass + Fail))
        
    def eff(self,Pass,Fail):
        eff,effStat = {},{}
        for j in  Pass:
            eff[j], effStat[j] = {},{}
            for i in  Pass[j]:
                eff[j][i] = self.getEff(Pass[j][i], Fail[j][i])
                effStat[j][i] = self.getEffStat(eff[j][i], Pass[j][i], Fail[j][i])
        return eff, effStat
                


# In[ ]:




