
# coding: utf-8

# In[3]:


from ROOT import TFile
import numpy as np


# In[4]:


class ShowerShape():
    def __init__(self, Config):
        self.projectdir = Config.projectdir
        self.era = Config.era
        self.selection = Config.selection
        self.DataGen = Config.DataGen
        self.corrFilePrefix = "trans_ShowerShape_"
        self.corrGraphPrefix = "trans_"
        
        self.corrPath = self.projectdir + 'figs/' + self.era + '/'+ self.DataGen +'/ee/ShowerShapeCorrections/'
        
        self.graph = {}
        
        self.phType = ['EE','EB']
        self.mva_to_ntuple   = {"EE":{
                                    "recoPhi"                :["photonOnePhi"],
                                    "r9"                     :["photonOneR9"],
                                    "sieieFull5x5"           :["photonOneSieie"],
                                    "sieipFull5x5"           :["photonOneSieip"],
                                    "e2x2Full5x5/e5x5Full5x5":["photonOneE2x2","photonOneE5x5"],
                                    "recoSCEta"              :["photonOneEta"],
                                    "rawE"                   :["photonOneScRawE"],
                                    "scEtaWidth"             :["photonOneScEtaWidth"],
                                    "scPhiWidth"             :["photonOneScPhiWidth"],
                                    "esEn/rawE"              :["photonOnePreShowerE","photonOneScRawE"],
                                    "esRR"                   :["photonOneSrr"],
                                    "rho"                    :["Rho"],
                                },
                                "EB":{
                                    "recoPhi"                :["photonOnePhi"],
                                    "r9"                     :["photonOneR9"],
                                    "sieieFull5x5"           :["photonOneSieie"],
                                    "sieipFull5x5"           :["photonOneSieip"],
                                    "e2x2Full5x5/e5x5Full5x5":["photonOneE2x2","photonOneE5x5"],
                                    "recoSCEta"              :["photonOneEta"],
                                    "rawE"                   :["photonOneScRawE"],
                                    "scEtaWidth"             :["photonOneScEtaWidth"],
                                    "scPhiWidth"             :["photonOneScPhiWidth"],
                                    "rho"                    :["Rho"],  
                                    }
                               }

    def checkPh(self,ph):
        checkFlag = False
        for phTarget in self.phType:
            if ph in phTarget:
                checkFlag = True
                
        return checkFlag
    def checkVar(self, var):
        checkFlag = False
        for varTarget in self.mva_to_ntuple['EE']:
            if var in varTarget:
                checkFlag = True
                
        for varTarget in self.fileNameFormat("EE"):
            if var in varTarget:
                checkFlag = True
        
        return checkFlag
    def checkInput(self,ph, var):
        return (self.checkPh(ph) and self.checkVar(var))
    
    def getNameFromNtuple(self,name):
        if 'photonOne' in name:
            fileName = name.split('photonOne')[1]
        else:
            fileName = name
            
        return fileName  
    def fileNameFormat(self, phType,Type = "SingleArray"):
        fileNameArray = []
        if Type == "SingleArray":
            for myvar in self.mva_to_ntuple[phType]:
                for mv in self.mva_to_ntuple[phType][myvar]:
                    fileName = self.getNameFromNtuple(mv)
                    fileNameArray.append(fileName)
        else:
            for myvar in self.mva_to_ntuple[phType]:
                fileNameSubArray = []
                for mv in self.mva_to_ntuple[phType][myvar]:
                    fileName = self.getNameFromNtuple(mv)
                    fileNameSubArray.append(fileName)
                fileNameArray.append(fileNameSubArray)
            
        return fileNameArray
    
    def loadToGraph(self):
        for ph in self.phType:
            self.graph[ph] = {}
            for ssV in self.fileNameFormat(ph):
                file = TFile(self.corrPath + self.corrFilePrefix + ssV + '_' + ph + '.root')
                self.graph[ph][ssV] = file.Get(self.corrGraphPrefix + ssV + '_' + ph)    
    
    def ShowerShapeCorrection(self,ph,ssVar,valueArray):
        if not self.checkInput(ph,ssVar):
            print("Input of phType and variable is not valid")
        else:
            for i in range(len(valueArray)):
                valueArray[i] = self.graph[ph][ssVar].Eval(valueArray[i])
            return valueArray
        
    def SSCorrected(self, data):
        toMVA = {}
        for ph in self.phType:
            toMVA[ph] = {}
            for d in data:
                toMVA[ph][d.name] = {}
                for mvaName in self.mva_to_ntuple[ph]:
                    #print(mvaName)
                    VALUES = []
                    for ntupleName in self.mva_to_ntuple[ph][mvaName]:
                        #print('-----', ntupleName)
                        VALUES.append(self.ShowerShapeCorrection(ph = ph, 
                                                                 ssVar = self.getNameFromNtuple(ntupleName ), 
                                                                 valueArray =  d.GetWithCuts(ntupleName ),
                                                                )
                                     )

                    if len(VALUES) > 1 :
                        toMVA[ph][d.name][mvaName] = np.array(VALUES[0]) / np.array(VALUES[1])
                    else:
                        toMVA[ph][d.name][mvaName] = VALUES[0]
                
        return toMVA

