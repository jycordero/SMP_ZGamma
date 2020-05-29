
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from Plotter.ConfigMatplotlib import ConfigMatplotlib
from Common.CommonHelper import CommonHelper


# In[ ]:


class Histo( ConfigMatplotlib ):
    def __init__(self, bins=None, nbins=None, ranges=None, variable = None):
        self.variable = variable
        self.name   = variable["part"]+variable["var"]+variable["ph"]
        
        self.nbins  = nbins
        self.ranges = ranges
        self.bins   = bins #bins most be in list/array format
        
        if self.bins is None:
            if self.nbins:
                step = (self.ranges[1] - self.ranges[0])/self.nbins
                self.bins = [self.ranges[0] + step*i for i in range(self.nbins)]
                self.values = [0]*(len(self.bins)-1)
        else:
            if type(self.bins) is int:
                self.nbins = len(self.bins)
                step = (self.ranges[1] - self.ranges[0])/self.nbins
                self.bins = [self.ranges[0] + step*i for i in range(self.nbins)]
                self.values = [0]*(len(self.bins)-1)
            else:
                self.nbins = len(bins)
                self.ranges = [bins[0],bins[-1]]
                self.values = [0]*(len(self.bins)-1)
    
    def __repr__(self):              
        msg= "Histo(bins="+str(self.bins)+",\n"              "      nbins="+str(self.nbins)+",\n"              "      ranges="+str(self.ranges)+")"
        return msg    
    
       
    def __str__(self):
        msg= "Histo(bins="+str(self.bins)+",\n"              "      nbins="+str(self.nbins)+",\n"              "      ranges="+str(self.ranges)+")"
        return msg    
    
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
        self.nbins = nbins
        self.bins = bins
        self.values = [0]*(len(self.bins)-1)
    
    def TotalEntries(self):
        return np.sum(self.values)

    
    def _OutOfRangeClean(self,array, indarray=None):
        if indarray is None: indarray = np.array(array)
        arrays = np.array(array)
        return arrays[np.logical_and(indarray >= self.bins[0], indarray <= self.bins[-1])]
    
    def _getBinCount(self,i,values,weight):
        return np.sum(weight[np.logical_and(values > self.bins[i], values <= self.bins[i+1])])
        
    
    def fill(self,values,weight=None):
        if weight is None: weight = [1]*len(values)
        
        weight = self._OutOfRangeClean(weight,values) #weight must be done first
        values = self._OutOfRangeClean(values)
             
        for i in range(len(self.bins)-1):
            self.values[i] += self._getBinCount(i,values,weight)
            
    def plot(self,log=False,Type="Single"):
        
        super(Histo,self).setRC(plt.rc,Type=Type)
        
        plt.figure()
        plt.errorbar(self.bins[:-1],
                     self.values,
                     xerr = np.diff(self.bins),
                     linestyle=None,
                    )
        plt.show()
        

