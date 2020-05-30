#!/usr/bin/env python
# coding: utf-8

# In[3]:


import numpy as np
import matplotlib.pyplot as plt

from Plotter.ConfigHist import ConfigHist
from Plotter.ConfigMatplotlib import ConfigMatplotlib
from Common.CommonHelper import CommonHelper
from Common.StackList import StackList


# In[4]:


class HistoSample( StackList, ConfigMatplotlib, ConfigHist ):
    def __init__(self,name=None,stack = None,Print=False):
        StackList.__init__(self, stack)
        self.Print = Print
        if name is None:            
            self.name     = None
        else:
            if type(variable) is list:
                self.name     = self.name
            else:
                self.name     = [ self.name ]
    
    def size(self,sample=None,variable=None,weighted=True):
        if sample is None:
            return len(self)
        else:
            try:
                return self[sample].size(variable,weighted)
            except:
                return self[sample].size(weighted)
            
    def sizes(self,variable = None, weighted=True): 
        return [ ist.size(variable,weighted) for ist in self ]
    
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
                
    def getEntries(self):
        return self.sizes(weighted=False)
    
    def _setOrder(self,ind):
        self.name = list(np.array(self.name)[ind])
        self.stack = self[ind]
    
    def _order(self,order="l2m",weighted=True,ind=None):
        if ind is None:
            entries = self.sizes()
            ind = np.argsort(entries)
            if order == "l2m":
                self._setOrder(ind)
            elif order == "m2l":
                self._setOrder(ind[::-1])
            else:
                print("Type of ordering is not supported")
        else:
            self._setOrder(ind)
    
    def Name2Index(self,sample):
        index = np.arange(len(self))
        return int(index[np.array(self.name) == sample])
    
    def getProperties(self):
        prop = {}
        prop['color']    = [ super(HistoSample,self).getColor(name) for name in self.name]
        prop['label']    = [ super(HistoSample,self).getLabel(name) for name in self.name]
        prop['histtype'] = super(HistoSample,self).getHisttpe(self.name[0])

        return prop
    
    def pop(self,i):
        self.name.pop(i)
        return super().pop(i)
        
    def merge(self,samples,name=None):
        if name is None:
            raise BaseException("Provide a name for the merged sample")
        
        self.append(sum([self.pop(self.Name2Index(smp)) for smp in samples]),name)
        

    
    def plot(self,variable,log=False,Type = "Single",Debug=False,order="l2m",ind=None):
        super(HistoSample,self).setRC(plt.rc,Type=Type)
        
        fig = plt.figure()       
        
        self._order(order,ind)
        
        value = [histo[variable].values for histo in self.stack]
        bins = self.stack[0][variable].bins
        binc = CommonHelper.Plot.BinFormat(Bins=bins, Type="center")
        binc = [binc]*len(value)
        
        prop = self.getProperties()
        plt.hist(binc,
                 weights  = value,
                 **prop,
                 )
        
        ax = plt.gca()
        ax.legend()
        ax.set_ylabel('Counts')
        ax.set_xlabel(variable)
        
        if log:
            ax.set_yscale('log')
        if Debug:
            return fig,ax,binc,value,prop,
        else:
            return fig,ax


# In[ ]:




