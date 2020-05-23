#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import json


# In[1]:


from Common.CommonHelper import CommonHelper
from Common.Stack import Stack
from Samples.Data import Data


# In[1]:


class DataStack( Stack ):
    def __init__(self, data):
        Stack.__init__(self,data)
        self.projectdir = self.__getProjectDir()
        self.jsonProp = self.projectdir+"json/plot/plot_conf.json"
        
        self.colors = self.getColors()
        self.legend = self.getLegends()
            
    def __del__(self):
        del self.stack
        del self.colors
        del self.legend
        del self.jsonProp
    
    def __getProjectDir(self):
        with open("../conf/config") as f:
            projectdir = f.read()
        return projectdir.split('\n')[0]
    
    def __getDataProp(self):
        with open(self.jsonProp) as f:
            JS = f.read()
        return json.loads(JS)
    
    def getMC(self):
        stack = []
        for st in self:
            if not st.data:
                stack.append(st)
        return DataStack(stack)
              
    def getData(self):
        stack = []
        for st in self:
            if st.data:
                stack.append(st)
        return DataStack(stack)
    
    def getDataFlag(self):
        return [ d.data for d in self]
        
    def getLabels(self, dataType = "all"):
        if dataType == "all":
            return [d.name for d in self]
        elif dataType == "mc":
            tmp = []
            for d in self:
                if not d.data:
                    tmp.append(d.name)
            return tmp
        elif dataType == "mcNoSignal":
            tmp = []
            for d in self:
                if not d.data and not d.signal:
                    tmp.append(d.name)
            return tmp
        elif dataType == "data":
            tmp = []
            for d in self:
                if d.data:
                    tmp.append(d.name)
            return tmp
        else:
            print("Invalid type")
    
    def getWeights(self, weightCorrection = False):
        return [ d.getWeight(weightCorrection) for d in self ] 
    
    def getVar(self,variable):
        return [d.GetWithCuts(variable) for d in self]

    def getWeightedYields(self):
        return [np.sum(w) for w in self.getWeights()]
    
    def getColors(self, labels = []):
        if labels == []: labels = self.getLabels()
        return [ self.__getDataProp()[label]["color"] for label in labels]

    def getMarker(self, labels = []):
        if labels == []: labels = self.getLabels()
        return [ self.__getDataProp()[label]["plot"]["marker"] for label in labels]
    
    def getLegends(self, labels = []):
        if labels == []: labels = self.getLabels()
        return [ self.__getDataProp()[label]["label"] for label in labels]
    
    def getHistType(self, labels = []):
        if labels == []: labels = self.getLabels()
        return [ self.__getDataProp()[label]["hist"]["histtype"] for label in labels]
    
    def getLabeledYield(self):
        return [ name +" "+ str(round(Yield)) for name, Yield in zip(self.getLabels(), self.getWeightedYields() ) ] 

    ######## Uncertainty #########
    def GetStatUncertainty(self,
                           bins, 
                           counts, 
                           scale):
        x = []
        x.append(bins[0])
        for i in np.arange(1,len(bins)-1):
            x.append(bins[i])
            x.append(bins[i])
        x.append(bins[-1])

        statUn = np.sqrt(counts)
        statsUp, statsDown = [],[]
        count = []
        for i in np.arange(len(counts)):
            count.append(counts[i])
            count.append(counts[i])

            statsUp.append(statUn[i]*scale[i])
            statsUp.append(statUn[i]*scale[i])

            statsDown.append(statUn[i]*scale[i])
            statsDown.append(statUn[i]*scale[i])

        count     =     np.array(count)
        statsUp   =   np.array(statsUp)
        statsDown = np.array(statsDown)
        return x,count,statsUp, statsDown     # To modify
    def GET_StatUncertainty(self,
                            data,
                            hist,
                            part,var,ph,
                            bins):

        variable = part+var+ph
        ########################################

        VAL  = hist[-1]
        hist = self.UnStackHist(hist)
        bins = np.array(bins)

        xc = (bins[:-1]+bins[1:])/1
        for i in np.arange(len(hist)-1):
            scale = []
            for j in np.arange(len(bins)-1):
                Ind = np.logical_and(data[i].GetWithCuts(variable) > bins[j], data[i].GetWithCuts(variable) <= bins[j+1])
                #weightPerBin.append(np.sum(d.GetWithCuts('weights')[Ind]))
                if np.sum(Ind) == 0:
                    scale.append(1)
                else:
                    weightOverYield = np.sum(data[i].GetWithCuts('weights')[Ind])/np.sum(Ind)
                    scale.append(weightOverYield)

            if i == 0:
                x,value, Up, Down = self.GetStatUncertainty(xc,hist[i],scale)
                statsUp   = Up
                statsDown = Down
            else:
                x,value, Up, Down = self.GetStatUncertainty(xc,hist[i],scale)
                statsUp   += Up
                statsDown += Down              
        x,value, Up, Down = self.GetStatUncertainty(bins,VAL,scale)

        return x,value,statsUp, statsDown     # To modify


# In[ ]:


class DataStackTest( DataStack ):
    def __init__(self):
        DataStack.__init__(self, self.__makeTestStack() )
        
    def __makeTestStack(self):
        names = ["test1","test2","test3"]
        dataF = [False, False, True]
        data = [ Data() for _ in names]
        for d,name,isData in zip(data,names,dataF):
            N = 400 if isData else 200
            d.name = name
            d.weight = np.ones(N)
            d.cuts = np.ones(N,dtype=np.bool )
            d.data = isData
            d.df["test"] = np.random.random(N) 
            d.df[" test"] = np.random.random(N) 

        return data

