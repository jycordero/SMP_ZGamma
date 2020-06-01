#!/usr/bin/env python
# coding: utf-8

# In[3]:


import os
import numpy as np
import matplotlib.pyplot as plt

from Plotter.ConfigMatplotlib import ConfigMatplotlib
from Plotter.ConfigHist  import ConfigHist
from Common.CommonHelper import CommonHelper
from Common.StackList    import StackList
from Samples.ConfigData  import ConfigData


# In[ ]:


class HistoSample( StackList, ConfigMatplotlib, ConfigHist, ConfigData):
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
        try:
            return int(index[np.array(self.name) == sample])
        except:
            return None
        
    def getData(self):
        return self[self.getDataName()]
    
    def getDataName(self):
        names = []
        for nm in self.name:
            if super().isData(nm):
                return str(nm)
            
        return None
        
    def getMC(self):
        return self[self.getMCName()]
        
    def getMCName(self):
        names = []
        for nm in self.name:
            if not super().isData(nm):
                names.append(str(nm))
        return names
    
    def getProperties(self,names=None):
        if names is None:
            names = self.name
        prop = {}
        prop['color']    = [ super(HistoSample,self).getColor(name) for name in names]
        prop['label']    = [ super(HistoSample,self).getLabel(name) for name in names]
        prop['histtype'] = super(HistoSample,self).getHisttpe(names[0])

        return prop
    
    def getMCCounts(self,hist):
        return hist[-1]
    
    def pop(self,i):
        self.name.pop(i)
        return super().pop(i)
        
    def merge(self,samples,name=None):
        if name is None:
            raise BaseException("Provide a name for the merged sample")

        Merge = sum([self.pop(self.Name2Index(smp)) for smp in samples if self.Name2Index(smp)])

        self.append(Merge,name)
        
    def savehists(self,path,prefix=""):
        for i, histo in enumerate(self):
            histo.save(path,prefix+self.name[i])

    def savefig(self,fig,fullpath):
        fig.savefig(fullpath)
        
    def savefigs(self,path):
        for var in self[0].variable:
            for log in [True,False]:
                fig, _ = self.plot(var,log=log)
                self.savefig(fig, path+var)
        
            
    def plotDataMC(self,bins,Data,MC,ax=None):
        if ax is None:
            fig = plt.figure()
            ax = plt.gca()
        Data,MC = np.array(Data), np.array(MC)
            
        Ratio = Data/MC
        binc = CommonHelper.Plot.BinFormat(Bins=bins, Type="center")
        err = Data/MC*(np.sqrt(1/Data + 1/MC))
        
        prop = {'marker':'o',
                'color':'k',
                'linestyle':'',
                'linewidth':1.5,
               }
        
        plt.errorbar(binc, Ratio,
                     xerr = np.diff(bins)/2,
                     yerr = err,
                     **prop,
                    )
        ax = plt.gca()
        ax.set_ylim([0.5,1.5])
        
        return ax
    
    def plot(self,variable,log=False,Type = "Single",Debug=False,order="l2m",ind=None):
        super(HistoSample,self).setRC(plt.rc,Type=Type)
        
        fig = plt.figure()
        plt.subplot2grid((4,1),(0,0),rowspan = 3, colspan = 1)
        
        self._order(order,ind)
        
        mc = [ self[name][variable].values  for name in self.getMCName() ]
        bins = self.stack[0][variable].bins
        binc = CommonHelper.Plot.BinFormat(Bins=bins, Type="center")
        binc = [binc]*len(mc)
        
        prop = self.getProperties(names = self.getMCName() )
        hist = plt.hist(binc,
                         bins = bins,
                         weights  = mc,
                         **prop,
                         )
        ax = plt.gca()

        ### Plot Data
        if self.getDataName() is not None:
            prop = {'marker':'o',
                'color':'k',    
                'linestyle':'',
                'label':'Data',
               }
            data = self[self.getDataName()][variable].values
            err = np.sqrt(data)

            plt.errorbar(binc[0],
                         data,
                         xerr = np.diff(bins)/2,
                         yerr = err,
                         **prop
                        )

            ax = plt.gca()          

            ### Plot Data/MC
            plt.subplot2grid((4,1),(3,0), rowspan = 1, colspan = 1, sharex = ax)
            ax1 = plt.gca()            

            self.plotDataMC(bins,data,mc[-1],ax1)
            ax1.set_xlabel(variable)

            plt.tight_layout()
            fig.subplots_adjust(hspace=0)
        else:
            ax.set_xlabel(variable)
            
        ax.set_ylabel('Counts')
        ax.legend()
        if log:
            ax.set_yscale('log')
            
        if Debug:
            return fig,ax,binc,mc,data,prop,
        else:
            return fig,ax


# In[ ]:





# In[ ]:




