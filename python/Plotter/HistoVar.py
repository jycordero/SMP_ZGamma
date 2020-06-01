#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from Plotter.ConfigHist import ConfigHist
from Plotter.ConfigMatplotlib import ConfigMatplotlib
from Plotter.Histo        import Histo
from Common.CommonHelper import CommonHelper
from Common.StackList import StackList


# In[4]:


class HistoVar(  StackList, ConfigMatplotlib, ConfigHist ):
    def __init__(self,variable=None,stack = None,Print=False):
        StackList.__init__(self, stack )
        self.Print = Print
        
        self.defaultvar = {
                            "part":"",
                            "var" :"",
                            "ph"  :""
                            }
        if variable is None:
            self.vardict  = None
            self.variable = None
            self.name     = None
        else:
            if type(variable) is list:
                self.vardict  = variable
                self.variable = [ v["part"]+v["var"]+v["ph"] for v in variable ]
                self.name     = self.variable
            else:
                self.vardict  = [ variable ]
                self.variable = [ variable["part"]+variable["var"]+variable["ph"] ]
                self.name     = self.variable

        self.confpath="/home/jcordero/CMS/SMP_ZGamma/json/plot/"

        if variable is not None and variable != "":
            self.__addVariable(variable)
        else:
            self.variable = variable
            
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
        
    def _getRanges(self,variable,part=None,var=None,ph=None):
        if variable is not None:
            part,var,ph = variable["part"],variable["var"],variable["ph"]

        rangefile = self.confpath + "ranges.csv"
        Range = pd.read_csv(rangefile)
        ranges = Range.loc[Range['part'] == part+ph][var].values[0]
        ranges = CommonHelper.Format.ConvertString2Float(ranges)    
        return ranges
    
    def _getBins(self,variable,part=None,var=None,ph=None):
        if variable is not None:
            part,var,ph = variable["part"],variable["var"],variable["ph"]
        
        binfile = self.confpath + "bins.csv"
        Bins = pd.read_csv(binfile)
        bins = Bins.loc[Bins['part'] == part][var].values[0]
        bins = CommonHelper.Format.ConvertString2Float(bins)
        #bins = np.array(CommonHelper.Plot.BinFormat(Bins=bins,ranges=ranges,Type='edges'))
        return bins  
    
    def __addVariable(self,variable):
        if self.variable is None:
            self.vardict  = []
            self.variable = []
            self.name     = []
        
        if variable is not None:
            if type(variable) is list:
                self.vardict  += variable
                self.variable += [ v["part"]+v["var"]+v["ph"] for v in variable ]
                self.name     = self.variable
            else:
                self.vardict  += [ variable ]
                self.variable += [ variable["part"]+variable["var"]+variable["ph"] ]
                self.name     = self.variable
    
    def initialize(self):
        HVarStack = HistoVar()
        _,vardict = self.Var2Plot()
    
        for var in vardict:
            HVarStack.append(Histo(variable = var))
        return HVarStack
    
    def size(self,variable=None,weighted=True):
        if variable is None:
            return self[0].size(weighted)
        else:
            return self[variable].size(weighted)
            
    #Overwritting append from StackList
    def append(self,stack,variable=None):
        if variable is None and stack.variable is None:
            raise "Variable is not specified, provide argument \"variable\" or set is in Histo"
        
        if variable is None:
            variable = stack.variable
        else:
            stack.variable = variable
            
        ranges = self._getRanges(stack.variable)
        bins = self._getBins(stack.variable)
        if CommonHelper.Type.isNumeric(bins):
            bins = np.array(CommonHelper.Plot.BinFormat(Bins=bins,ranges=ranges,Type='edges'))
        elif np.isnan(bins).any():
                raise BaseException("NaN bin")

        stack.setup(bins=bins,ranges=ranges)
        
        self.vappend(stack)
        
    def vappend(self,stack):
        super().append(stack)
        self.__addVariable(stack.variable)
        
    def save(self,path,prefix=""):
        for histo in self:
            histo.save(path,prefix)
    
    def plot(self,variable,log=False,Type = "Single"):
        
        super(HistoVar,self).setRC(plt.rc,Type=Type)
        
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




