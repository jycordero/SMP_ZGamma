
# coding: utf-8

# In[2]:


import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from Plotter.ConfigHist import ConfigHist
from Plotter.ConfigMatplotlib import ConfigMatplotlib
from Common.CommonHelper import CommonHelper


# In[1]:


class Histo( ConfigMatplotlib, ConfigHist ):
    def __init__(self, bins=None, nbins=None, ranges=None, variable = None):
        self.variable = variable
        self.name   = variable["part"]+variable["var"]+variable["ph"]
        
        self.nbins   = nbins
        self.ranges  = ranges
        self.bins    = bins #bins most be in list/array format
        self.weights = None
        self.values  = None
        self.entries = 0
        
        if self.bins is None:
            if self.nbins:
                step = (self.ranges[1] - self.ranges[0])/self.nbins
                self.bins = [self.ranges[0] + step*i for i in range(self.nbins)]
                self.values = [0]*(len(self.bins)-1)
                self.weights = [0]*(len(self.bins)-1)
        else:
            if type(self.bins) is int:
                self.nbins = len(self.bins)
                step = (self.ranges[1] - self.ranges[0])/self.nbins
                self.bins = [self.ranges[0] + step*i for i in range(self.nbins)]
                self.values = [0]*(len(self.bins)-1)
                self.weights = [0]*(len(self.bins)-1)
            else:
                self.nbins = len(bins)
                self.ranges = [bins[0],bins[-1]]
                self.values = [0]*(len(self.bins)-1)
                self.weights = [0]*(len(self.bins)-1)
        
        #weights initiated but not implemented
    
    def __repr__(self):              
        msg= "Histo(bins="+str(self.bins)+",\n"              "      nbins="+str(self.nbins)+",\n"              "      ranges="+str(self.ranges)+")"
        return msg    
    
       
    def __str__(self):
        msg= "Histo(bins="+str(self.bins)+",\n"              "      nbins="+str(self.nbins)+",\n"              "      ranges="+str(self.ranges)+")"
        return msg  

    def __len__(self):
        return int(np.sum(self.values))
    
    def __add__(self,other):
        #if other.bins != self.bins:
        #    raise BaseException("bins must match")
        histo = Histo(self.bins, self.nbins,self.ranges, self.variable)
        histo.entries = self.entries + other.entries
        histo.values = list(np.array(self.values) + np.array(other.values))
        
        return histo
    
    def __radd__(self,other):
        if other == 0:
            return self
        else:
            return self.__add__(other)
    
    def _getRanges(self,part,var,ph):
        rangefile = self.confpath + "ranges.csv"
        Range = pd.read_csv(rangefile)
        ranges = Range.loc[Range['part'] == part+ph][var].values[0]
        ranges = CommonHelper.Format.ConvertString2Float(ranges)    
        return ranges
    
    def _getBins(self,part,var,ph):       
        binfile = self.confpath + "bins.csv"
        Bins = pd.read_csv(binfile)
        bins = Bins.loc[Bins['part'] == part][var].values[0]
        bins = CommonHelper.Format.ConvertString2Float(bins)
        #bins = np.array(CommonHelper.Plot.BinFormat(Bins=bins,ranges=ranges,Type='edges'))
        return bins
    
    def setup(self,bins=None,ranges=None,nbins=None):
        self.ranges = ranges
        self.nbins  = nbins
        self.bins   = bins
        if self.values is None:
            self.values = [0]*(len(self.bins)-1)
    
    def size(self,weighted=True):
        if weighted:
            return len(self)
        else:
            return self.entries
    
    def getEntries(self):
        return self.size(weighted=False)
    
    def _OutOfRangeClean(self,array, indarray=None):
        if indarray is None: indarray = np.array(array)
        arrays = np.array(array)
        return arrays[np.logical_and(indarray >= self.bins[0], indarray <= self.bins[-1])]
    
    def _getBinCount(self,i,dfvalues,weight):
        return np.sum(weight[np.logical_and(dfvalues > self.bins[i], dfvalues <= self.bins[i+1])])
        
    
    def fill(self,dfvalues,weight=None):
        if weight is None: weight = [1]*len(dfvalues)
        self.entries += len(dfvalues)
        weight = self._OutOfRangeClean(weight,dfvalues) #weight must be done first
        dfvalues = self._OutOfRangeClean(dfvalues)
             
        for i in range(len(self.bins)-1):
            self.values[i] += self._getBinCount(i,dfvalues,weight)
    
    def save(self,path,prefix=""):
        binc = CommonHelper.Plot.BinFormat(Bins=self.bins, Type="center")
        df = pd.DataFrame.from_dict({'binc':binc,'values':self.values})
        df.to_csv(path+prefix+self.name+".csv")
    
    def plot(self,log=False,Type="single"):
        
        super(Histo,self).setRC(plt.rc,Type=Type)
        binc = CommonHelper.Plot.BinFormat(Bins=self.bins, Type="center")
        
        plt.figure()
        prop = super(Histo,self).getProperties()
        plt.hist(binc,
                 weights = self.values,
                 **prop,
                )
        plt.legend()
        #plt.show()
        

