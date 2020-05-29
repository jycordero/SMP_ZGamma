
# coding: utf-8

# In[3]:


import numpy as np
import matplotlib.pyplot as plt
from Plotter.ConfigHist import ConfigHist
from Plotter.ConfigMatplotlib import ConfigMatplotlib
from Common.CommonHelper import CommonHelper
from Common.StackList import StackList


# In[4]:


class HistoSample( StackList, ConfigHist, ConfigMatplotlib ):
    def __init__(self,name=None,stack = None):
        StackList.__init__(self, stack)
        if name is None:            
            self.name     = None
        else:
            if type(variable) is list:
                self.name     = self.name
            else:
                self.name     = [ self.name ]

        
    
    def append(self,stack,name=None):
        if name is None and stack.name is None:
            raise "Name is not specified, provide argument \"name\" or set is in Histo"
        
        if name is None:
            name = stack.name
        else:
            stack.name = name
        
        self.vappend(stack)
        
    def vappend(self,stack):
        super().append(stack)
        self.__addVariable(stack.name)
    
    
    def __addVariable(self,name):
        if self.name is None:
            self.name = []
        
        if name is not None:
            if type(name) is list:
                self.name  += name
            else:
                self.name  += [ name ]
    
    def getProperties(self):
        prop = {}
        prop['color']    = [ super(HistoSample,self).getColor(name) for name in self.name]
        prop['label']    = [ super(HistoSample,self).getLabel(name) for name in self.name]
        prop['histtype'] = super(HistoSample,self).getHisttpe(self.name[0])
        return prop
    
    def plot(self,variable="photonOnePt",log=False,Type = "Single"):
        
        super(HistoSample,self).setRC(plt.rc,Type=Type)
        
        fig = plt.figure()       
        
        value = [histo[variable].values for histo in self.stack]
        bins = self.stack[0][variable].bins
        binc = CommonHelper.Plot.BinFormat(Bins=bins, Type="center")
        binc = [binc]*len(value)
        
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

