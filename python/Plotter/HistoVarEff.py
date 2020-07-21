#!/usr/bin/env python
# coding: utf-8

# In[4]:


from Plotter.Histo import Histo
from Plotter.HistoVar import HistoVar


# In[26]:


class HistoVarEff(  HistoVar ):
    def __init__(self,variable=None,stack = None,Print=False):
        HistoVar.__init__(self, variable=variable, stack=stack , Print=Print)

        self.bins1 = None
        self.bins2 = None
        
    def __add__(self,other):
        if self.variable != other.variable:
            raise BaseException("Variable stack must have the same variables (in the same order)")
            
        histoVar = HistoVarEff(Print=self.Print)
        histoVar.bins1, histoVar.bins2 = other.bins1, other.bins2
        for ise, iot in zip(self,other):
            histoVar.append(ise+iot)
            
        return histoVar        
        
    def initialize(self,Type=None,BinType="Optimized",rangefile="ranges.csv",binfile="bins.csv"):
        HVarStack = HistoVarEff()
        if Type is None or Type == "Normal":
            _,vardict = self.Var2Plot()
        elif Type == "Eff":
            _,vardict = self.Var2Plot_Eff(BinType)
            HVarStack.bins1, HVarStack.bins2  = HVarStack.getGridBinning(BinType)
    
        for var in vardict:
            HVarStack.append(Histo(variable = var), rangefile=rangefile, binfile=binfile)
        return HVarStack
        
    def getPass(self):
        #Pass = []
        Pass = HistoVarEff()
        for h in self:
            if "Pass" in h.name:
                Pass.append(h)
                
        Pass.bins1, Pass.bins2 = self.bins1, self.bins2
        return Pass
    
    def getFail(self):
        #Fail = []
        Fail = HistoVarEff()
        for h in self:
            if "Fail" in h.name:
                Fail.append(h)
        Fail.bins1, Fail.bins2 = self.bins1, self.bins2
        return Fail      
    


# In[27]:


if __name__ == "__main__":
    HV = HistoVarEff()
    variable = {"part":"dilepton",
                "var":"M",
                "ph":"",
                }
    
    binfile= "bins_efficiency.csv"
    
    #print(HV._getRanges(**variable))    
    #print(HV._getBins(**variable,sourcefile=binfile))
    HV = HV.initialize(Type = "Eff",BinType="Optimized",binfile=binfile)
    #for h in HV.initialize(Type = "Eff",BinType="Optimized",binfile=binfile):
    #    print(h.bins)
    print(HV.getGridBinning("Optimized"),HV.bins1)


# In[ ]:




