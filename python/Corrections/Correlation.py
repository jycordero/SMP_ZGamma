#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import matplotlib.pyplot as plt
import matplotlib.colors as col
import numpy as np

import sys
sys.path.append('/home/jcordero/CMS/JYCMCMS/SMP_ZG/python')

from Plotter.Helper import Helper


# In[ ]:


class Correlation():
    def __init__(self, Config, data):
        self.d = data
        
        self.phVars = {'':[],
                  'EE':[],
                  'EB':[],
                 }

        self.heatlabel = { '':[],
                      'EE':[],
                      'EB':[],
                     }
        
        self.iniVars()
        self.Help = Helper()
        
        self.era = Config.era
        self.figpath = Config.figpath
        
        self.coef = {}
        self.corr = {}
        
    def iniVars(self):
        for variable in self.d.df.keys():
            if 'Eta' in variable and 'Sc' not in variable:
                continue
            if 'Phi' in variable and 'Sc' not in variable:
                continue
            if 'EE_EB' in variable:
                continue 
            if 'Pt' in variable:
                continue
            if 'ERes' in variable:
                continue
            if 'MVA' in variable:
                continue


            if 'photonOne' in variable:

                if 'EE' in variable:
                    phType = 'EE'
                elif 'EB' in variable:
                    if 'Srr' in variable or 'PreShower' in variable:
                        continue
                    phType = 'EB'
                else:
                    phType = ''

                self.phVars[phType].append(variable)
                self.heatlabel[phType].append(variable.split('photonOne')[1])
        
    def CorrCalc(self,Print=False):
        
        for phType in ['EE','EB']:
            
            self.coef[phType] = {}
            self.corr[phType] = []


            for i in np.arange(len(self.phVars[phType])):
                var1 = self.phVars[phType][i]
                self.coef[phType][i] = {}
                self.corr[phType].append([])
                for j in np.arange(len(self.phVars[phType])):
                    var2 = self.phVars[phType][j]

                    var1Vals = np.array(self.d.GetWithCuts(var1))
                    var2Vals = np.array(self.d.GetWithCuts(var2))

                    var1Vals = var1Vals[np.logical_not(np.isnan(var1Vals))]
                    var2Vals = var2Vals[np.logical_not(np.isnan(var2Vals))]


                    #print(var1,':',var2,np.correlate(var1Vals,var2Vals))
                    mult = 10
                    try:
                        self.coef[phType][i][j] = np.corrcoef(var1Vals,var2Vals)[0][1]
                        self.corr[phType][i].append(round(self.coef[phType][i][j]*mult,2))
                    except:
                        self.coef[phType][i][j] = mult
                        self.corr[phType][i].append(self.coef[phType][i][j])
                    if Print:
                        print(var1,':',var2,self.coef[phType][i][j])
                
    def Corr(self,phType):
        label = self.heatlabel[phType]

        fig = plt.figure()
        fig,ax = plt.subplots(figsize=(20,20))
        ax = plt.gca()

        ax.set_xticks(np.arange(len(label)))
        ax.set_yticks(np.arange(len(label)))

        for i in np.arange(len(self.phVars[phType])):
            for j in np.arange(len(self.phVars[phType])):
                ax.text(i,j,self.corr[phType][i][j],ha='center',va='center',color = 'w',fontsize=15)

        #im = ax.imshow(corr,cmap='jet')
        thersh = 1
        filterCorr = np.array(self.corr[phType])
        filterCorr[np.abs(filterCorr)<thersh] = np.array(filterCorr)[np.abs(filterCorr)<thersh]
        filterCorr[np.abs(filterCorr)>=thersh] = thersh

        im = ax.imshow(filterCorr,cmap='jet')
        cbar = ax.figure.colorbar(im,ax=ax)

        plt.xticks(rotation=90)
        ax.set_xticklabels(label)
        ax.set_yticklabels(label)
        #ax.set_xtickslabel()
        ax.tick_params(axis='both',labelsize=20)
        ax.grid(False)

        plt.show()

        fig.savefig(self.figpath+"Photon_Correlation_"+phType+".png")
        
    def getMinCorr(self,phType):
        Min = np.argmin(np.abs(self.corr[phType]))
        Dim = len(self.heatlabel[phType])
        xi  = int(Min/Dim)
        yi  = Min - xi*Dim

        var1 = self.phVars[''][xi].split('photonOne')[1]
        var2 = self.phVars[''][yi].split('photonOne')[1]
        

        Min = np.logical_and(np.abs(self.corr[phType])< 0.015, np.abs(self.corr[phType]) >  0.000 )
        
        print(var1,var2)
        print(np.sum(Min))
        
        return var1,var2,np.sum(Min)
        
        
    def Hist2d(d,
               part1,var1,ph1,
               part2,var2,ph2,
               log   = True,
               d2    = None,
               label = None,
              ):

        ranges,bins = {},{}
        wei = {}

        if log:
            logScale = col.LogNorm()
        else:
            logScale = None

        if not d2:
            d2 = d
        x = d.GetWithCuts(part1+var1+'')
        y = d2.GetWithCuts(part2+var2+'')


        ranges[var1],bins[var1] = self.Help.GET_RangeBins(part=part1,var=var1,ph='')
        ranges[var2],bins[var2] = self.Help.GET_RangeBins(part=part2,var=var2,ph='',Blind=False,Plotting=True,File =True)

        wei[var1] = d.GetWithCuts('weight')
        wei[var2] = d2.GetWithCuts('weight')

        ##############################

        if len(x) >len(y) :
            x = x[:len(y)]
        else:
            y = y[:len(x)]

        print('Corr:\n',np.corrcoef(x,y))
        fig = plt.figure(figsize=(10,8))

        plt.hist2d(x,y,
                   bins    = [  bins[var1],  bins[var2]],
                   range   = [ranges[var1],ranges[var2]],
                   #weights = [   wei[var1],   wei[var2]],
                   norm = logScale,
                    );
        plt.title(label)
        plt.colorbar()
        plt.xlabel(var1)
        plt.ylabel(var2)
        plt.show()

        return fig,x,y

    def Hist1d(d,part,var,ph):

        Val = d.GetWithCuts(part+var)

        plt.figure(figsize=(8,8))
        plt.hist(Val,
                 histtype = 'step',

                 )
        plt.xlabel(var)
        
    


# In[ ]:


'''
import matplotlib.colors as col
log = True
#log = False

##########################

part1 = 'photonOne'
#var1 = 'Ich'
#ph1 = ''
ph1 = 'EB'
#ph1 = 'EE'

##########################
#part2 = 'dilepton'
#var2 = 'M'

part2 = 'photonOne'
#var2 = 'Sieip'
#ph2 = ''
ph2 = 'EB'
#ph2 = 'EE'
##########################

Hist1d(d=DY,part = part1,var = var1,ph = ph1)
Hist1d(d=DY,part = part2,var = var2,ph = ph2)

fig,x,y = Hist2d(d=DY,
                part1 = part1,var1 = var1,ph1 = ph1,
                part2 = part2,var2 = var2,ph2 = ph2,
                log   = log,
                label = DY.name,
                )
ZG = data[-2]
fig,x,y = Hist2d(d=ZG,
                part1 = part1,var1 = var1,ph1 = ph1,
                part2 = part2,var2 = var2,ph2 = ph2,
                log   = log,
                label = ZG.name,
                )
################

fig,x,y = Hist2d(d=DY,d2=ZG,
                part1 = part1,var1 = var1,ph1 = ph1,
                part2 = part1,var2 = var1,ph2 = ph1,
                log   = log,
                label = ZG.name + ' '+ DY.name,
                )

fig,x,y = Hist2d(d=DY,d2=ZG,
                part1 = part2,var1 = var2,ph1 = ph2,
                part2 = part2,var2 = var2,ph2 = ph2,
                log   = log,
                label = ZG.name + ' '+ DY.name,
                )
''';

