#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from Samples.Data      import Data
import pandas as pd 
import dask.dataframe as dd
from root_pandas import read_root


# In[ ]:


class Reader():
    def __init__(self, Config, Print = False):
        self.Config = Config
        self.projectdir = Config.projectdir
        self.path = Config.path 
        self.era  = Config.era
        self.selection = Config.selection
        self.LoadVars  = Config.LoadVars
        self.DataGen   = Config.DataGen
        
        if  self.era == "2016":
            self.run = ['B','C','D','E','F','G','H']
        elif self.era == "2017":
            self.run = ['B','C','D','E','F']
        elif self.era == "2018":
            self.run = ['A','B','C','D']
            
        self.Print     = Print
        
    def __repr__(self):
        space = len(Reader.__name__)
        spacer = space*" "
        msg  = "{}(Config={},Print={})".format(Reader.__name__,self.Config,self.Print) 
        msg += spacer+"--> projectdir: {}".format(self.projectdir)
        msg += spacer+"--> path: {}".format(self.path)
        msg += spacer+"--> era: {}".format(self.era)
        msg += spacer+"--> selection: {}".format(self.selection)
        msg += spacer+"--> run: {}".format(self.run)
        return msg
    
    def read(self, Region = "AB", Type = "analysis", run  = []):
        if run == []:
            run = self.run
        
        if Type == "reduce":
            data = self.readReduce( Region = Region )
        elif Type == "analysis":
            data = self.rootReadAllMC()
            data.append( self.rootReadAllData(run ) )
        elif Type == "efficiency":
            self.readEff()
        else:
            print("Property Type most be reduce, analysis or efficiency")
            
        
        return data
    
        
    def rootReadAllData(self, run):
        if self.selection   == 'mumug':
            Lepton = [Data(self.projectdir, self.path + "DoubleMuon/", "DoubleMuon_" + self.era,trigger = r,era = self.era, data = True, var = self.LoadVars, Print= self.Print) for r in run]
        elif self.selection == 'elelg':
            Lepton = [Data(self.projectdir, self.path + "DoubleEG/", "DoubleEG_" + self.era,trigger = r,era = self.era, data = True, var = self.LoadVars, Print= self.Print) for r in run]
        elif self.selection == 'ee':
            Lepton = [Data(self.projectdir, self.path+"SingleElectron/","Electron_"+self.era,trigger = r, era = self.era, data = True, var = self.LoadVars, Print= self.Print) for r in run]
            #SingleLepton = [Data(self.projectdir, self.path + "SingleElectron/","Electron_"+era,trigger = r,era = '2017_RunD', data=True, var = LoadVars) for r in run]
            #SingleLepton = [Data(self.projectdir, self.path + "SingleElectron/","Electron_"+era,trigger = r,era = '2017_Run'+r, data=True) for r in run]
            #Lepton = [Data(self.projectdir, self.path+"SingleElectron/","Electron_"+self.era,trigger = 'D',era = '2017_RunD', data=True, var = self.LoadVars, Print= self.Print)]


        Leptons = self.sampleJoin(Lepton) 
                
        return Leptons 

    def rootReadMC(self,sample):
        postName = "_v"
        
        # sample can be a list and this is intrepreted as several sample
        # merged insto one. Ex. WWTo2L2Nu, ZZTo4L -> VV (Diboson samples)
        if type(sample) == list:
            if len(sample) > 1:
                datas = []
                for smp in sample:
                    datas.append(Data(self.projectdir, self.path + smp+"/", smp, postName, era = self.era, var = self.LoadVars, Print= self.Print))

                data = self.sampleJoin(datas)
            elif len(sample) == 1:
                data = Data(self.projectdir, self.path + sample[0]+"/", sample[0], postName, era = self.era, var = self.LoadVars, Print= self.Print) 
            else:
                print("Sample not read")
        elif type(sample) == str:
            data = Data(self.projectdir, self.path + sample+"/", sample, postName, era = self.era, var = self.LoadVars, Print= self.Print) 
        else:
            print("Sample not read")
            
        return data
    
    def rootReadAllMC(self):
        samples = []
        if self.selection == "mumug" or self.selection == "elelg":
            samples.append(["DYJets"])

            if self.DataGen == "legacy" or self.era == '2017' or self.era == '2018':
                samples.append(["ZGToLLG"])
                samples.append(["WJets"])
                samples.append(["TTTo2L2Nu"])
            elif self.DataGen == "rereco":                
                samples.append(["ZG_ZToLL"])
                samples.append(["TT"])
                samples.append(["W1JetsToLNu","W2JetsToLNu","W3JetsToLNu","W4JetsToLNu"])
                
            samples.append(["WWTo2L2Nu","ZZTo2L2Nu","ZZTo2L2Q","ZZTo4L","WZTo2L2Q","WZTo3LNu"])

        elif self.selection == "ee":
            samples.append(["DYJets"])
            
            '''
            if self.DataGen == "legacy" or self.era == '2017':
                samples.append(["ZGToLLG"])
            elif self.DataGen == "rereco":
                samples.append(["ZG_ZToLL"])
            ''' 
            samples.append(["WJets"])
            samples.append(["TTTo2L2Nu"])         
            samples.append(["WWTo2L2Nu","ZZTo2L2Nu","ZZTo2L2Q","ZZTo4L","WZTo2L2Q","WZTo3LNu"])
        ###############
        
        data = []
        for smp in samples:
            data.append(self.rootReadMC(smp))
            
        return data 
            
    def sampleJoin(self,Sample):
        Samples = Sample[0]
        for i in range(len(Sample[1:])):
            Samples =   Samples + Sample[1]
            del Sample[1]   
            
        return Samples
    
    def readReduce(self, Region, Print = False):
        Names =['WJets','WWTo2L2Nu','TTTo2L2Nu','DYJets','ZGToLLG', 'DoubleMuon_'+self.era]
        reduced = []
        
        for name in Names:
            filename = self.path+'Reduced/'+name+'_'+Region.replace(" ","")+'.csv'
            if Print:
                print('----- Reading '+name+' in Region ' +Region+ '--------')
                print('-- '+filename)

            reduced.append(pd.read_csv(filename))
            
            
        isData = [True if name == 'DoubleMuon_'+self.era else False for name in Names]
        data = [Data(projectdir = self.projectdir, df = reduced[i],nameFile = Names[i],data = isData[i], Print=False)  for i in range(len(Names))]

        
        return data

    ##################################################
    
    
    # Reader functions meant for efficiency Efficiency 
    def readRoot(self,files,Type="join"):
        
        for i,file in enumerate(files):
            print('-----------')
            print("Reading " + file.split("/")[-1] )
            
            if Type == "join":
                if i == 0:
                    data = read_root(file,columns= self.LoadVars)
                else:
                    data = data.append(read_root(file, columns = self.LoadVars))
            elif Type == "array":
                if i == 0:
                    data = []                
                data.append(read_root(file,columns = self.LoadVars))
            else:
                print("Property \"Type\" is needs to be \"join\" or \"array\".")

        return data


# In[ ]:




