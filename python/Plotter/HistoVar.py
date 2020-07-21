#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from Plotter.ConfigHist import ConfigHist
from Plotter.ConfigMatplotlib import ConfigMatplotlib
from Plotter.Histo        import Histo
from Common.CommonHelper import CommonHelper
from Common.StackList import StackList


# In[2]:


class HistoVar(  StackList, ConfigMatplotlib, ConfigHist ):
    
    confpath="/home/jcordero/CMS/SMP_ZGamma/json/plot/"
    
    def __init__(self,variable=None,stack = None,Print=False):
        StackList.__init__(self, stack=stack )
        self.Print = Print
        
        self.name     = None
        self.vardict  = None
        self.variable = None
        
        if variable is not None:
            if type(variable) is list:
                self.vardict  = variable
                self.variable = [ v["part"]+v["var"]+v["ph"] for v in variable ]
            else:
                self.vardict  = [ variable ]
                self.variable = [ variable["part"]+variable["var"]+variable["ph"] ]

        if variable is not None and variable != "":
            self.__addVariable(variable)
        else:
            self.variable = variable
            
    def initialize(self,Type=None,BinType="Optimized",rangefile="ranges.csv",binfile="bins.csv"):
        HVarStack = HistoVar()
        if Type is None or Type == "Normal":
            _,vardict = self.Var2Plot(BinType)
        elif Type == "Eff":
            _,vardict = self.Var2Plot_Eff(BinType)
    
        for var in vardict:
            #print(var,rangefile,binfile)
            HVarStack.append(Histo(variable = var), rangefile=rangefile, binfile=binfile)
        return HVarStack
    
    def size(self,variable=None,weighted=True):
        if variable is None:
            return self[0].size(weighted)
        else:
            return self[variable].size(weighted)
            
    def __add__(self,other):
        if self.variable != other.variable:
            raise BaseException("Variable stack must have the same variables (in the same order)")
            
        histoVar = HistoVar(Print=self.Print)
        for ise, iot in zip(self,other):
            histoVar.append(ise+iot)
            
        return histoVar
    
    def __radd__(self,other):
        if other == 0:
            return self
        else:
            return self.__add__(other)  
           
    def __addVariable(self,variable):
        if self.variable is None:
            self.vardict  = []
            self.variable = []
        
        if variable is not None:
            if type(variable) is list:
                self.vardict  += variable
                self.variable += [ v["part"]+v["var"]+v["ph"] for v in variable ]
            else:
                self.vardict  += [ variable ]
                self.variable += [ variable["part"]+variable["var"]+variable["ph"] ]
    
    def _getCSV(self,part,var,ph,sourcefile):
        CSV = pd.read_csv(self.confpath + sourcefile)
        cell = CSV.loc[CSV['part'] == part+ph][var].values[0]
        return CommonHelper.Format.ConvertString2Float(cell)
    
    def _getRanges(self,part,var,ph,sourcefile = "ranges.csv"):
        return self._getCSV(part,var,ph,sourcefile = sourcefile)
    
    def _getBins(self,part,var,ph,sourcefile = "bins.csv"):       
        return self._getCSV(part,var,ph,sourcefile = sourcefile)
    
    
    #Overwritting append from StackList
    def append(self,stack,variable=None, rangefile="ranges.csv",binfile="bins.csv"):
        if variable is None and stack.variable is None:
            raise "Variable is not specified, provide argument \"variable\" or set is in Histo"
        
        if variable is None:
            variable = stack.variable
        else:
            stack.variable = variable
            
        #ranges = self._getRanges(**stack.variable,sourcefile)
        #bins = self._getBins(**stack.variable)
        if stack.bins is None:
            ranges = self._getRanges(part = stack.variable['part'], 
                                     var = stack.variable['var'],
                                     ph = stack.variable['ph'],
                                     sourcefile = rangefile)
            bins = self._getBins(part = stack.variable['part'], 
                                 var = stack.variable['var'],
                                 ph = stack.variable['ph'],
                                 sourcefile = binfile)
        else:
            ranges = stack.ranges
            bins = stack.bins
                
        if CommonHelper.Type.isNumeric(bins):
            bins = np.array(CommonHelper.Plot.BinFormat(Bins=bins,ranges=ranges,Type='edges'))
        elif np.isnan(bins).any():
                raise BaseException("NaN bin")

        #print(ranges,bins,CommonHelper.Type.isNumeric(bins))
        stack.setup(bins=bins,ranges=ranges)
        
        self.vappend(stack)
        
    def vappend(self,stack):
        super().append(stack,stack.name)
        self.__addVariable(stack.variable)
        
    def save(self,path,prefix=""):
        
        try:
            if self.name not in path:                
                path = os.path.join(path,self.name)
                os.mkdir(path)
        except:
            if self.name not in path:                
                path = os.path.join(path,self.name)
            
        print('HistoVar',path)
        for i, histo in enumerate(self):
            histo.save(path,prefix)
    
    def plot(self,variable,log=False,Type = "single"):
        
        super().setRC(plt.rc,Type=Type)
        
        fig = plt.figure()       
        
        value = self[variable].values 
        bins = self[variable].bins
        binc = CommonHelper.Plot.BinFormat(Bins=bins, Type="center")
        
        prop = self.getProperties()
        plt.hist(binc,
                 weights  = value,
                 **prop,
                 )
        
        plt.legend()
        
        ax = plt.gca()
        if log:
            ax.set_yscale('log')
        return fig,ax
    
    


# In[ ]:


if __name__ == "__main__":
    HV = HistoVar()
    variable = {"part":"dilepton",
                "var":"M",
                "ph":"",
                }
    
    binfile= "bins_efficiency.csv"
    
    print(HV._getRanges(**variable))    
    print(HV._getBins(**variable,sourcefile=binfile))
    for h in HV.initialize(Type = "Eff",BinType="Optimized",binfile=binfile):
        print(h.bins)

