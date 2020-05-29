
# coding: utf-8

# In[3]:


import pandas as pd
import numpy as np
from Plotter.ConfigHist import ConfigHist
from Common.CommonHelper import CommonHelper
from Common.StackList import StackList


# In[4]:


class HistoVar( StackList ):
    def __init__(self,variable=None,stack = None):
        StackList.__init__(self, stack )
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

    def __addVariable(self,variable):
        if self.variable is None:
            self.vardict = []
            self.variable = []
            self.name = []
        
        if variable is not None:
            if type(variable) is list:
                self.vardict  += variable
                self.variable += [ v["part"]+v["var"]+v["ph"] for v in variable ]
                self.name     = self.variable
            else:
                self.vardict  += [ variable ]
                self.variable += [ variable["part"]+variable["var"]+variable["ph"] ]
                self.name     = self.variable
        

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
        
        stack.setup(bins=bins,ranges=ranges)
        
        self.vappend(stack)
        
    def vappend(self,stack):
        super().append(stack)
        self.__addVariable(stack.variable)
        
            
    def getPartVarPh(self,variable):
        part,var,ph = "photonOne","Pt","_EE"
        return part,var,ph
    

    
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
    
    

