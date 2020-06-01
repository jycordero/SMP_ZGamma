
# coding: utf-8

# In[1]:


class Helper():
    def __init__(self,DataEra='legacy',selection='mumug',SampleSet='Correction'):
        self.selection = selection
        self.DataEra = DataEra
        self.SampleSet = SampleSet
        
        self.PU = {
                    'path':'/home/jcordero/CMS/data_2016/'+self.DataEra+'/SMP_ZG/Files/',
                  }
        
    def GET_WeiVAR(data,var,part,ph,reWeight,weightCorrection = True,Filter = ''):
        if weightCorrection:        
            wei = [np.array(reWeight[i][data[i].cuts])/(np.array(data[i].df.photonIDWeight)[data[i].cuts]) for i in range(len(data[:-1]))]
            wei.append(data[-1].GetWithCuts('weight')//(np.array(data[-1].df.photonIDWeight)[data[-1].cuts]))
        else:
            wei = [d.GetWithCuts('weight') for d in data]

        VAR = [d.GetWithCuts(part+var+ph) for d in data]        
        
        '''
        if Filter == 'photonOnePt':
            bins = Helper.bins['Pt']['photonOne'] 
            Ind  = BinIndex(VAR,)
        else:
            Ind = np.ones(len(VAR), dtype=np.bool)
        '''
        for i in range(len(data)):
            Ind = np.ones(len(VAR[i]), dtype=np.bool)
            VAR[i] = VAR[i][Ind]
            wei[i] = wei[i][Ind]
            
        return wei,VAR
        
    # ReWeight
    def GetMCPU(self):
        ########### MC Scenario ##################
        PU = np.array([
                        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 
                        11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 
                        21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 
                        31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 
                        41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 
                        51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 
                        61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 
                        71, 72, 73, 74]
                        )
        PUmc = np.array([
                        1.78653e-05 ,2.56602e-05 ,5.27857e-05 ,8.88954e-05 ,
                        0.000109362 ,0.000140973 ,0.000240998  ,0.00071209  ,
                        0.00130121  ,0.00245255  ,0.00502589   ,0.00919534  ,
                        0.0146697   ,0.0204126   ,0.0267586    ,0.0337697   ,
                        0.0401478   ,0.0450159   ,0.0490577    ,0.0524855   ,
                        0.0548159   ,0.0559937   ,0.0554468    ,0.0537687   ,
                        0.0512055   ,0.0476713   ,0.0435312    ,0.0393107   ,
                        0.0349812   ,0.0307413   ,0.0272425    ,0.0237115   ,
                        0.0208329   ,0.0182459   ,0.0160712    ,0.0142498   ,
                        0.012804    ,0.011571    ,0.010547     ,0.00959489  ,
                        0.00891718  ,0.00829292  ,0.0076195    ,0.0069806   ,
                        0.0062025   ,0.00546581  ,0.00484127   ,0.00407168  ,
                        0.00337681  ,0.00269893  ,0.00212473   ,0.00160208  ,
                        0.00117884  ,0.000859662 ,0.000569085  ,0.000365431 ,
                        0.000243565 ,0.00015688  ,9.88128e-05  ,6.53783e-05 ,
                        3.73924e-05 ,2.61382e-05 ,2.0307e-05   ,1.73032e-05 ,
                        1.435e-05   ,1.36486e-05 ,1.35555e-05  ,1.37491e-05 ,
                        1.34255e-05 ,1.33987e-05 ,1.34061e-05  ,1.34211e-05 ,
                        1.34177e-05 ,1.32959e-05 ,1.33287e-05]
                        )

        return PU,PUmc
    
    def GetDataPU(self,xsec='69p2'):
        pileupFile = 'pileup_sf_2016_'+xsec+'mb.root'
        file = TFile(self.PU['path']+pileupFile)
        puTree = file.Get('pileup')
        PUdata = []
        for pu in puTree:
            PUdata.append(pu)
        return PUdata
    def GetPUweight(self,xsec='69p2'):
    
        ### Get Distributions ##
        PU,PUmc= self.GetMCPU()
        PUdata = self.GetDataPU(xsec)

        ### Normalize ###
        PUmc   = np.array(PUmc)/sum(PUmc)        
        PUdata = np.array(PUdata)/sum(PUdata)

        return PU,PUdata/PUmc,PUdata,PUmc,
    def PUSF_ratio(
                    self,
                    data,
                    xsec1='65',
                    xsec2='69p2',
                    Print = False,
                    ):
        pu,r1,r1d,r1m = self.GetPUweight(xsec = xsec1)
        pu,r2,r2d,r2m = self.GetPUweight(xsec = xsec2)
        
        rScale = r1/r2
        rScale[np.isnan(rScale)] = np.ones(sum(np.isnan(rScale)))

        puWeight = []
        for d in data[:-1]:
            puW = np.ones(len(d.df.nPU))
            if Print:
                print('--------------',d.name)
                print(len(d.df.nPU))
            for i in range(len(pu)-2):
                mask = np.logical_and(np.array(d.df.nPU) > pu[i], np.array(d.df.nPU) <= pu[i+1])        
                puW[mask] = np.ones(np.sum(mask))*rScale[i]
            puWeight.append(puW)
        return puWeight


# In[2]:


import numpy as np
from ROOT import TFile

