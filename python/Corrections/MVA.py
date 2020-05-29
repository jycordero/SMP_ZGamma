
# coding: utf-8

# In[ ]:


from ROOT import TMVA
import array


# In[1]:


class MVA():
    def __init__(self, Config,variables):
        self.projectdir = Config.projectdir
        self.era = Config.era
        self.DataGen = Config.DataGen
        self.variables = variables
        
        self.pathMVA = "/home/jcordero/CMS/data_" + self.era + "/" + self.DataGen + "/SMP_ZG/Files/ShowerShapeMVA/"
        
        
        self.file = {}
        self.reader = {}
        
        self.phVals = ["EE","EB"]
        
        self.var = {}
        self.BDT = {}
        
        self.iniFiles()
        
        
    def iniFiles(self):
        for ph in self.phVals:
            if self.era == "2016":
                preName = "spring16_80x_"+ph
            elif self.era == "2017":
                preName = "fall17_94X_"+ph
            elif self.era == "2018":
                preName = "autumn18_"+ph
                
            self.file[ph] = self.pathMVA + preName + "_TMVAnalysis_BDT.weights.xml"
            self.reader[ph] = TMVA.Reader()
        
    def loadMVA(self):
        for ph in self.phVals:
            self.var[ph] = {}
            for mvaVar in self.variables[ph]:
                    self.var[ph][mvaVar] = array.array('f',[0])
                    self.reader[ph].AddVariable(mvaVar, 
                                                self.var[ph][mvaVar]
                                               )
            self.reader[ph].BookMVA("BDT",self.file[ph])        
            
    def readMVA(self, data, inMVA):
        self.BDT = {}
        for ph in self.phVals:
            print('============='+ph+"============")
            self.BDT[ph] = {}
            for d in data:
                print('--------',d.name,'-------',len(inMVA[ph][d.name]["recoPhi"]))
                self.BDT[ph][d.name] = []
                for i in range(len(inMVA[ph][d.name]["recoPhi"])):
                    for v in inMVA[ph][d.name]:
                        self.var[ph][v][0] = inMVA[ph][d.name][v][i]

                    self.BDT[ph][d.name].append(self.reader[ph].EvaluateMVA("BDT"))
        

