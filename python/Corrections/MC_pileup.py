#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
from ROOT import TFile,TTree, TGraph, TCanvas
import array 
import matplotlib.pyplot as plt
# My Dependencies
from Samples.Data      import Data
from Plotter.Helper    import Helper

import Samples
import Plotter


# In[ ]:





# In[11]:


selection = 'mumug'
#selection = 'elelg'

era = "2017"

if era == "2016":
    run = ['B','C','D','E','F','G','H']
    #DataGen = 'rereco'
    DataGen = 'legacy'
    if DataGen == 'legacy':
        #SampleSet = 'MatchZGpaper'
        #SampleSet = 'Rerun'
        SampleSet = 'Correction'
    else:
        SampleSet = 'MatchZGpaper_newAna'
elif era == "2017":
    run = ['B','C','D','E','F']
    DataGen = 'rereco'
    #SampleSet = 'V1'
    SampleSet = 'V2_puWeight'

path    = "/home/jcordero/CMS/data_"+era+"/"+DataGen+"/SMP_ZG/Files/"+selection+"/"+SampleSet+"/"
figpath = "/home/jcordero/CMS/JYCMCMS/SMP_ZG/figs/"+era+"/"+DataGen+"/"+selection+"/puReweight/"


#Help    = Plotter.Helper.Helper()
Help    = Helper()

LoadVars = [
            'nPV','nPU', 
            'genWeight','eventWeight','puWeight',
            #'photonIDWeight',
            #'triggerWeight',
            'photonOnePt','photonOneEta','photonOnePhi',
            'vetoDY','genIsoPass',
            ]


# In[12]:


def GetMCPU(era = '2016',Flag = True):
    ########### MC Scenario ##################
    
    if era == '2016':
        if Flag:
            # mix_2016_25ns_Moriond17MC_PoissonOOTPU_cfi.py
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
        else :
            #mix_2016_25ns_SpringMC_PUScenarioV1_PoissonOOTPU_cfi.py
            PU = np.array([
                            0,1,2,3,4,5,6,7,8,9,10,
                            11,12,13,14,15,16,17,18,19,20,
                            21,22,23,24,25,26,27,28,29,30,
                            31,32,33,34,35,36,37,38,39,40,
                            41,42,43,44,45,46,47,48,49
                            ])                        
            PUmc = np.array([
                            0.000829312873542, 0.00124276120498, 0.00339329181587, 
                            0.00408224735376, 0.00383036590008, 0.00659159288946,
                            0.00816022734493, 0.00943640833116,0.0137777376066,
                            0.017059392038, 0.0213193035468, 0.0247343174676,
                            0.0280848773878, 0.0323308476564, 0.0370394341409,
                            0.0456917721191, 0.0558762890594,0.0576956187107,
                            0.0625325287017, 0.0591603758776, 0.0656650815128, 
                            0.0678329011676, 0.0625142146389, 0.0548068448797,
                            0.0503893295063, 0.040209818868, 0.0374446988111,
                            0.0299661572042, 0.0272024759921, 0.0219328403791,
                            0.0179586571619, 0.0142926728247, 0.00839941654725,
                            0.00522366397213, 0.00224457976761, 0.000779274977993,
                            0.000197066585944, 7.16031761328e-05, 0.0,
                            0.0, 0.0, 0.0,
                            0.0, 0.0, 0.0,
                            0.0, 0.0, 0.0,
                            0.0, 0.0 ]
                            )
    # mix_2017_25ns_UltraLegacy_PoissonOOTPU_cfi.py
    elif era == '2017':
        PU = np.array([
                        0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                        10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                        20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
                        30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
                        40, 41, 42, 43, 44, 45, 46, 47, 48, 49,
                        50, 51, 52, 53, 54, 55, 56, 57, 58, 59,
                        60, 61, 62, 63, 64, 65, 66, 67, 68, 69,
                        70, 71, 72, 73, 74, 75, 76, 77, 78, 79,
                        80, 81, 82, 83, 84, 85, 86, 87, 88, 89,
                        90, 91, 92, 93, 94, 95, 96, 97, 98
                        ])
        PUmc = np.array([
                        1.1840841518e-05, 3.46661037703e-05, 8.98772521472e-05, 7.47400487733e-05, 0.000123005176624,
                        0.000156501700614, 0.000154660478659, 0.000177496185603, 0.000324149805611, 0.000737524009713,
                        0.00140432980253, 0.00244424508696, 0.00380027898037, 0.00541093042612, 0.00768803501793,
                        0.010828224552, 0.0146608623707, 0.01887739113, 0.0228418813823, 0.0264817796874,
                        0.0294637401336, 0.0317960986171, 0.0336645950831, 0.0352638818387, 0.036869429333,
                        0.0382797316998, 0.039386705577, 0.0398389681346, 0.039646211131, 0.0388392805703,
                        0.0374195678161, 0.0355377892706, 0.0333383902828, 0.0308286549265, 0.0282914440969,
                        0.0257860718304, 0.02341635055, 0.0213126338243, 0.0195035612803, 0.0181079838989,
                        0.0171991315458, 0.0166377598339, 0.0166445341361, 0.0171943735369, 0.0181980997278,
                        0.0191339792146, 0.0198518804356, 0.0199714909193, 0.0194616474094, 0.0178626975229,
                        0.0153296785464, 0.0126789254325, 0.0100766041988, 0.00773867100481, 0.00592386091874,
                        0.00434706240169, 0.00310217013427, 0.00213213401899, 0.0013996000761, 0.000879148859271,
                        0.000540866009427, 0.000326115560156, 0.000193965828516, 0.000114607606623, 6.74262828734e-05,
                        3.97805301078e-05, 2.19948704638e-05, 9.72007976207e-06, 4.26179259146e-06, 2.80015581327e-06,
                        1.14675436465e-06, 2.52452411995e-07, 9.08394910044e-08, 1.14291987912e-08, 0.0,
                        0.0, 0.0, 0.0, 0.0, 0.0,
                        0.0, 0.0, 0.0, 0.0, 0.0,
                        0.0, 0.0, 0.0, 0.0, 0.0,
                        0.0, 0.0, 0.0, 0.0, 0.0,
                        0.0, 0.0, 0.0, 0.0
                        ])
    # mix_2018_25ns_UltraLegacy_PoissonOOTPU_cfi.py
    elif era == '2018':
        PU = np.array([
                        0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                        10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                        20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
                        30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
                        40, 41, 42, 43, 44, 45, 46, 47, 48, 49,
                        50, 51, 52, 53, 54, 55, 56, 57, 58, 59,
                        60, 61, 62, 63, 64, 65, 66, 67, 68, 69,
                        70, 71, 72, 73, 74, 75, 76, 77, 78, 79,
                        80, 81, 82, 83, 84, 85, 86, 87, 88, 89,
                        90, 91, 92, 93, 94, 95, 96, 97, 98
                        ])
        PUmc = np.array([
                        8.89374611122e-07, 1.1777062868e-05, 3.99725585118e-05, 0.000129888015252, 0.000265224848687,
                        0.000313088635109, 0.000353781668514, 0.000508787237162, 0.000873670065767, 0.00147166880932,
                        0.00228230649018, 0.00330375581273, 0.00466047608406, 0.00624959203029, 0.00810375867901,
                        0.010306521821, 0.0129512453978, 0.0160303925502, 0.0192913204592, 0.0223108613632,
                        0.0249798930986, 0.0273973789867, 0.0294402350483, 0.031029854302, 0.0324583524255,
                        0.0338264469857, 0.0351267479019, 0.0360320204259, 0.0367489568401, 0.0374133183052,
                        0.0380352633799, 0.0386200967002, 0.039124376968, 0.0394201612616, 0.0394673457109,
                        0.0391705388069, 0.0384758587461, 0.0372984548399, 0.0356497876549, 0.0334655175178,
                        0.030823567063, 0.0278340752408, 0.0246009685048, 0.0212676009273, 0.0180250593982,
                        0.0149129830776, 0.0120582333486, 0.00953400069415, 0.00738546929512, 0.00563442079939,
                        0.00422052915668, 0.00312446316347, 0.00228717533955, 0.00164064894334, 0.00118425084792,
                        0.000847785826565, 0.000603466454784, 0.000419347268964, 0.000291768785963, 0.000199761337863,
                        0.000136624574661, 9.46855200945e-05, 6.80243180179e-05, 4.94806013765e-05, 3.53122628249e-05,
                        2.556765786e-05, 1.75845711623e-05, 1.23828210848e-05, 9.31669724108e-06, 6.0713272037e-06,
                        3.95387384933e-06, 2.02760874107e-06, 1.22535149516e-06, 9.79612472109e-07, 7.61730246474e-07,
                        4.2748847738e-07, 2.41170461205e-07, 1.38701083552e-07, 3.37678010922e-08, 0.0,
                        0.0, 0.0, 0.0, 0.0, 0.0,
                        0.0, 0.0, 0.0, 0.0, 0.0,
                        0.0, 0.0, 0.0, 0.0, 0.0,
                        0.0, 0.0, 0.0, 0.0
                        ])

    return PU,PUmc

def GetDataPU(era = '2016',xsec='69p2'):
    pileupFile = 'pileup_sf_'+era+'_'+xsec+'mb.root'
    file = TFile('/home/jcordero/CMS/data_'+era+'/'+DataGen+'/SMP_ZG/Files/'+pileupFile)
    puTree = file.Get('pileup')
    PUdata = []
    for pu in puTree:
        PUdata.append(pu)
    return PUdata

def GetPUweight(era = '2016', xsec='69p2'):
    
    ### Get Distributions ##
    PU,PUmc= GetMCPU(era,Flag=Flag)
    PUdata = GetDataPU(era,xsec)
    
    ### Normalize ###
    PUmc   = np.array(PUmc)/sum(PUmc)        
    PUdata = np.array(PUdata)/sum(PUdata)
    
    return PU,PUdata[:len(PUmc)]/PUmc,PUdata,PUmc,

def SF_ratio(
             era = '2016',
             xsec1='65',
             xsec2='69p2',
            ):
    pu,r1,r1d,r1m = GetPUweight(era = era, xsec = xsec1)
    pu,r2,r2d,r2m = GetPUweight(era = era, xsec = xsec2)
    rScale = r1/r2
    rScale[np.isnan(rScale)] = np.ones(sum(np.isnan(rScale)))

    puWeight = []
    for d in data[:-1]:
        puW = np.ones(len(d.df.nPU))
        print('--------------',d.name)
        print(len(d.df.nPU))
        for i in range(len(pu)-2):
            mask = np.logical_and(np.array(d.df.nPU) > pu[i], np.array(d.df.nPU) <= pu[i+1])        
            puW[mask] = np.ones(np.sum(mask))*rScale[i]
        puWeight.append(puW)
    return puWeight


# In[ ]:





# In[13]:


trigger    = "_v"
#DYJets = Data(path +    "DYJets/",    "DYJets", trigger, era = era, var = LoadVars)
if era == "2017":
    DYJets = Data("/home/jcordero/CMS/data_2017/rereco/SMP_ZG/Files/ee/TagProbe_noTrig/DYJets/",    "DYJets", trigger, era = era, var = LoadVars)
    ZG     = Data(path +   "ZGToLLG/",   "ZGToLLG", trigger, era = era, var = LoadVars)
    #WJets  = Data(path +     "WJets/",     "WJets", trigger, era = era, var = LoadVars)
    #TT     = Data(path + "TTTo2L2Nu/", "TTTo2L2Nu", trigger, era = era, var = LoadVars)
elif era == '2016':
    DYJets = Data("/home/jcordero/CMS/data_2016/legacy/SMP_ZG/Files/ee/TagProbe_noTrig/DYJets/",    "DYJets", trigger, era = era, var = LoadVars)


# In[ ]:


DYJets.df


# In[14]:


'''
data        = [  DYJets,        ZG]
listSamples = [ 'DYJets',      'ZG']
legend      = [ 'DYJets',      'ZG']
colors      = [ 'purple', 'magenta']
dataFlag    = [    False,     False]
combFlag    = [    False,     False]
'''


data        = [  DYJets]
listSamples = [ 'DYJets']
legend      = [ 'DYJets']
colors      = [ 'purple']
dataFlag    = [    False]
combFlag    = [    False]


# In[15]:


Flag = True
xsec1, xsec2 = '69p2', '69p2'

### Get Distributions ##
PU,PUmc= GetMCPU(era=era,Flag=Flag)
PUdata = GetDataPU(era=era,xsec=xsec1)

PUmc   = np.array(PUmc)/sum(PUmc)        
PUdata = np.array(PUdata)/sum(PUdata)


# In[16]:


MC = {}
M = {}
for d in data:
    h = plt.hist(
                d.df.nPU,
                histtype = 'step',
                range = [0,99],
                bins = 99,
                normed = True,
                label = d.name,
                )
    
    MC[d.name] = h[0] 
    M[d.name] = h
plt.legend()


# In[ ]:





# In[20]:


Flag = True
PUdata = {}

### Get Distributions ##
PU,PUmc= GetMCPU(era=era,Flag=Flag)
PUmc   = np.array(PUmc)/sum(PUmc)        

#XSecs = ['65','67','69p2','70','71p5','72p4']
XSecs = ['65','69p2','67','70','72p4']
#XSecs = ['67','69p2','70','71p5','72p4']

#XSecs = ['67','69p2']
#XSecs = ['69p2','70']
#XSecs = ['69p2','72p4']

#XSecs = ['67']
#XSecs = ['69p2']
#XSecs = ['70']
#XSecs = ['71p5']
#XSecs = ['72p4']

if len(XSecs) > 2:
    linewidth = 0.7
else:
    linewidth = 1.2

for xsec in XSecs:
    PUdata[xsec] = GetDataPU(era=era,xsec=xsec)
    PUdata[xsec] = np.array(PUdata[xsec])/sum(PUdata[xsec])

puLim = [0,85] 

############################################
figsize = (6,5)
fig = plt.figure(figsize=figsize)
for d in data:
    plt.plot(PU,MC[d.name],
             label='mc '+d.name,
             linewidth = linewidth,
            )

for xsec in XSecs:
    plt.plot(PU,PUdata[xsec][:len(PU)],
             label = 'data '+xsec+' mb',
             linewidth = linewidth,
            )
    
#plt.plot(PU,ratioDataMC[xsec]*MC,label = 'mc '+xsec)
ax = plt.gca()
ax.set_xlim(puLim)
plt.grid(linestyle='--')
plt.title('PileUp '+era)
plt.xlabel('PU')
plt.ylabel('a.u.')
plt.legend()

############################################
ratioDataMC = {}
figsize = (6,3)
fig1 = plt.figure(figsize=figsize)
for xsec in XSecs:
    ratioDataMC[xsec] = PUdata[xsec][:len(PU)]/MC['DYJets']
    plt.plot(PU,ratioDataMC[xsec],
             label     = 'mc DYJets '+xsec,
             linewidth = linewidth,
            )
    
ax = plt.gca()
ax.set_xlim(puLim)

ylim = [0,2]

ax.set_ylim(ylim)
plt.grid(linestyle='--')

plt.title('Ratio PileUp '+era)
plt.xlabel('PU')
plt.ylabel('Data/MC')
plt.legend()

XSName = ''
for XS in XSecs:
    XSName += '_'+XS 
fig.savefig(figpath+'DataMC_pileup'+XSName+'.png')
fig1.savefig(figpath+'DataMC_ratioPileup'+XSName+'.png')


# In[21]:


path = '/home/jcordero/CMS/data_'+era+'/'+DataGen+'/SMP_ZG/Files/'
file = TFile(path+'pileup_sf_'+era+'_full.root','recreate')
file.cd();


# In[22]:


#graph = TGraph(len(pu), array.array('f',pu), array.array('f',r1))
c1 = TCanvas('c1','Canva',200,20,700,500)
c1.SetFillColor(0)
c1.SetGrid()


N, x, y  = int(len(PU)), array.array('d'), array.array('d')
for i in range(N):
    x.append(PU[i])
    #y.append(r1[i])
    y.append(ratioDataMC['69p2'][i])
    #print(' i %i %f %f ' % (i,x[i],y[i]))
    
graph = TGraph(N, x, y)

graph.SetLineColor( 2 )
graph.SetLineWidth( 4 )
graph.SetMarkerColor( 4 )
graph.SetMarkerStyle( 21 )
graph.GetXaxis().SetTitle( 'X title' )
graph.GetYaxis().SetTitle( 'Y title' )
graph.Draw("AP")
c1.Update()

graph.Write('pileup_sf')
file.Write()


# In[23]:


plt.figure()
for xsec in XSecs:
    plt.plot(PU,ratioDataMC[xsec]/ratioDataMC['69p2'], label = xsec+'/69p2')
plt.legend()
plt.grid(linestyle='--')


# In[32]:


graph.Draw()


# In[33]:


graph.Eval(50)


# In[ ]:





# In[ ]:




