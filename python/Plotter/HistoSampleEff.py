#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import array

from ROOT import TFile,TTree,TH2F,gROOT,gStyle,TCanvas

from iminuit import Minuit

from Common.CommonHelper import CommonHelper
from Plotter.HistoSample import HistoSample


# In[1]:


class HistoSampleEff( HistoSample ):
    def __init__(self,stack = None,name=None,Print=False):
        HistoSample.__init__(self,name=name,stack=stack,Print=Print)    
        
        self.effConfPath = "/home/jcordero/CMS/SMP_ZGamma/json/plot/eff_fit_ini.json"

        self.FitRes = {}
        
        self.Yield = {}
        
        self.effMC = {}
        self.effMCStat = {}
        
        self.eff = {}
        self.effStat = {}
        
        self.nBin1 = 0
        self.nBin2 = 0
        
    def __getEffConf(self):
        import json
        with open(self.effConfPath) as f:
            JS = f.read()
        return json.loads(JS)        
        
    def InitializeParams(self,i,j,BinType, Type):
        bounds = self.getBounds()
        pPass = self.getFit(BinType,Type,j,i,"pass")
        pFail = self.getFit(BinType,Type,j,i,"fail")
        return pPass, pFail, bounds   
        
    def getBounds(self):
        return [self.__getEffConf()["bounds"]["min"],self.__getEffConf()["bounds"]["max"]]
        
    def getFitIni(self,BinType,Type):
        #conv = "convVeto" if Type else "noconvVeto"
        if Type == "ProbeIsConv":
            Type = "convVeto"
        return self.__getEffConf()[BinType][Type]
    
    def getFit(self,BinType,Type,bin1Index,bin2Index,ProbeType):        
        return self.getFitIni(BinType,Type)["bins"+str(bin1Index)]["bins"+str(bin2Index)][ProbeType]        
        
    def getEff(self,Pass,Fail):
        Pass, Fail = float(Pass), float(Fail)
        return 0 if (Pass + Fail) == 0 else Pass/(Pass + Fail)
        
    def getEffStat(self,eff, Pass,Fail):
        Pass, Fail = float(Pass), float(Fail)
        return 0 if (Pass + Fail) == 0 or Pass == 0 else eff*np.sqrt( 1/Pass + 1/(Pass + Fail))
        
    def effCalc(self,Pass,Fail):
        eff= self.getEff(Pass, Fail)
        return eff, self.getEffStat(eff, Pass, Fail)
    
    def GetYieldMC(self):
        Histo = self.getMC()
        
        for histo in Histo:
            PassList, FailList = histo.getPass(),histo.getFail()
            self.nBin1, self.nBin2 = len(PassList.bins1), len(PassList.bins2)
            
            self.eff[histo.name] ,self.eff[histo.name] = {},{}
            self.effStat[histo.name] ,self.effStat[histo.name] = {},{}
            self.Yield[histo.name] ,self.Yield[histo.name] = {},{}
            self.Yield[histo.name]['Pass'],self.Yield[histo.name]['Fail'] = {},{}

            for n,PassH,FailH in zip(range(len(PassList)),PassList,FailList):
                Pass, Fail = PassH.values, FailH.values
                i,j = n%self.nBin2, int(np.floor(n/self.nBin2))
                xc = CommonHelper.Plot.BinFormat(Bins=FailH.bins,Type="center")

                var = 'pt'
                binj = PassH.variable['extra'].split("_")
                binj = '['+binj[binj.index(var)+1]+', '+ binj[binj.index(var)+2]+']'

                var = 'eta'
                bini = PassH.variable['extra'].split("_")
                bini = '['+bini[bini.index(var)+1]+', '+ bini[bini.index(var)+2]+']'


                try:
                    self.Yield[histo.name]['Fail'][binj]
                except:
                    self.Yield[histo.name]['Fail'][binj] = {}

                try:
                    self.Yield[histo.name]['Pass'][binj]
                except:
                    self.Yield[histo.name]['Pass'][binj] = {}

                try: 
                    self.eff[histo.name][binj]
                except: 
                    self.eff[histo.name][binj] = {}

                try:
                    self.effStat[histo.name][binj]
                except: 
                    self.effStat[histo.name][binj] = {}

                self.Yield[histo.name]['Pass'][binj][bini] = np.sum(Pass)
                self.Yield[histo.name]['Fail'][binj][bini] = np.sum(Fail)

                self.eff[histo.name][binj][bini], self.effStat[histo.name][binj][bini] = self.effCalc(np.sum(Pass),np.sum(Fail))

    def GetYieldOneData(self,n,ax1,ax2,EffType,Plot=True):
        h = self.getData()
        
        PassList, FailList = h.getPass(),h.getFail()
        self.nBin1, self.nBin2 = len(PassList.bins1), len(PassList.bins2)
        
        
        self.FitRes[h.name] = {}
        '''
        self.eff[h.name] = {}
        self.effStat[h.name] = {}
        '''
        
        ##################################
        PassH, FailH = PassList[n], FailList[n]
        
        Pass, Fail = PassH.values, FailH.values
        i,j = n%self.nBin2, int(np.floor(n/self.nBin2))
        xc = CommonHelper.Plot.BinFormat(Bins=FailH.bins,Type="center")

        pPass, pFail, BoundedFit = self.InitializeParams(i,j,"Optimized",Type=EffType)

        FitP, FitF, FitPSig, FitFSig,mP,mF = self.Fit_Curve_CHI(
                                                    DATA_PASS = Pass, DATA_FAIL = Fail,
                                                    pPass = pPass,pFail = pFail,
                                                    Bounded = BoundedFit,
                                                    )
        fitRes = {  "names" : mP.values.keys(),
                    "values": mP.values.values(),
                    "error" : mP.errors.values()
                   }
        df = pd.DataFrame(fitRes,columns=fitRes.keys())
        self.FitRes[h.name][PassH.name] = df
        
        fitRes = {  "names" : mF.values.keys(),
                    "values": mF.values.values(),
                    "error" : mF.errors.values()
                   }
        df = pd.DataFrame(fitRes,columns=fitRes.keys())
        
        self.FitRes[h.name][FailH.name] = df


        ####################################

        if Plot:
            xs = np.arange(0,len(Pass))

            argVoigt = FitP[2:5]
            argExp   = FitP[5:9]

            NSig = FitP[0]
            NBkg = FitP[1]

            SIG = CommonHelper.Math.Voigt(xs, *argVoigt)/np.sum(CommonHelper.Math.Voigt(xs, *argVoigt))
            BKG = CommonHelper.Math.RooCMSShape(xs, *argExp)  /np.sum(CommonHelper.Math.RooCMSShape(xs, *argExp))


            color = ['b','g','r']

            print('--- Plotting Pass')    
            self.PlotFitting(
                        ax1,
                        xc,
                        NSig = NSig, NBkg = NBkg,
                        DATA = Pass, SIG  = SIG, BKG  = BKG,
                        #eta  = etaBINS[i], pt = ptBins[j],
                        color = color,
                       )

            #######################################
            xs = np.arange(len(Fail),len(Fail)*2)

            argVoigt = FitF[2:5]
            argExp   = FitF[5:9]

            NSig = FitF[0]
            NBkg = FitF[1]

            SIG = CommonHelper.Math.Voigt(xs, *argVoigt)/np.sum(CommonHelper.Math.Voigt(xs, *argVoigt))
            BKG = CommonHelper.Math.RooCMSShape(xs, *argExp)  /np.sum(CommonHelper.Math.RooCMSShape(xs, *argExp))


            color = ['slateblue','olivedrab','firebrick']

            print('--- Plotting Fail')
            self.PlotFitting(
                        ax2,
                        xc,
                        NSig = NSig, NBkg = NBkg,
                        DATA = Fail, SIG  = SIG, BKG  = BKG,
                        #eta  = etaBINS[i], pt = ptBins[j],
                        color = color,
                       )


            ############################################

        Num,dNum = FitP[0], FitPSig[0]
        Dem, dDem = (FitP[0]+FitF[0]), FitPSig[0]+FitFSig[0]

        '''
        self.eff[h.name][PassH.variable['extra']] = Num/Dem
        self.effStat[h.name][PassH.variable['extra']] = Num/Dem*np.sqrt((dNum/Num)**2 + (dDem/Dem)**2)
        if np.isnan(self.eff[h.name][PassH.variable['extra']]):
            self.eff[h.name][PassH.variable['extra']] = 0.0
        ''' 
        return pPass, pFail, FitP, FitF




    def GetYieldData(self, EffType, Plot=True, figsize = (20,20)):
        Yield = {}
        h = self.getData()
        
        self.eff[h.name] ,self.eff[h.name] = {},{}
        self.effStat[h.name] ,self.effStat[h.name] = {},{}
                
        self.FitRes[h.name],self.FitRes[h.name] = {},{}
        self.Yield[h.name],self.Yield[h.name] = {},{}
        
        self.FitRes[h.name]['Pass'],self.FitRes[h.name]['Fail'] = {},{}
        self.Yield[h.name]['Pass'],self.Yield[h.name]['Fail'] = {},{}
        PassList, FailList = h.getPass(),h.getFail()
        self.nBin1, self.nBin2 = len(PassList.bins1), len(PassList.bins2)
        
        if Plot:
            fig1 = plt.figure(1,figsize=figsize)
            fig2 = plt.figure(2,figsize=figsize)
        
        for n,PassH,FailH in zip(range(len(PassList)),PassList,FailList):
            Pass, Fail = PassH.values, FailH.values
            i,j = n%self.nBin2, int(np.floor(n/self.nBin2))
            xc = CommonHelper.Plot.BinFormat(Bins=FailH.bins,Type="center")
            
            var = 'pt'
            binj = PassH.variable['extra'].split("_")
            binj = '['+binj[binj.index(var)+1]+', '+ binj[binj.index(var)+2]+']'

            var = 'eta'
            bini = PassH.variable['extra'].split("_")
            bini = '['+bini[bini.index(var)+1]+', '+ bini[bini.index(var)+2]+']'

            try:
                self.FitRes[h.name]['Fail'][binj]
            except:
                self.FitRes[h.name]['Fail'][binj] = {}
                
            try:
                self.FitRes[h.name]['Pass'][binj]
            except:
                self.FitRes[h.name]['Pass'][binj] = {}
                
            try:
                self.Yield[h.name]['Fail'][binj]
            except:
                self.Yield[h.name]['Fail'][binj] = {}
                
            try:
                self.Yield[h.name]['Pass'][binj]
            except:
                self.Yield[h.name]['Pass'][binj] = {}
                        
            try: 
                self.eff[h.name][binj]
            except: 
                self.eff[h.name][binj] = {}
                
            try:
                self.effStat[h.name][binj]
            except: 
                self.effStat[h.name][binj] = {}

            pPass, pFail, BoundedFit = self.InitializeParams(i,j,"Optimized",Type=EffType)

            FitP, FitF, FitPSig, FitFSig,mP,mF = self.Fit_Curve_CHI(
                                                        DATA_PASS = Pass, DATA_FAIL = Fail,
                                                        pPass = pPass,pFail = pFail,
                                                        Bounded = BoundedFit,
                                                        )
            fitRes = {  "names" : mP.values.keys(),
                        "values": mP.values.values(),
                        "error" : mP.errors.values()
                       }
            df = pd.DataFrame(fitRes,columns=fitRes.keys())

            self.FitRes[h.name]['Pass'][binj][bini] = mP.values.values()
            self.FitRes[h.name]['Fail'][binj][bini] = mF.values.values()

            self.Yield[h.name]['Pass'][binj][bini] = FitP[0]
            self.Yield[h.name]['Fail'][binj][bini] = FitF[0]

            
            ####################################
            
            if Plot:
                xs = np.arange(0,len(Pass))

                argVoigt = FitP[2:5]
                argExp   = FitP[5:9]

                NSig = FitP[0]
                NBkg = FitP[1]

                SIG = CommonHelper.Math.Voigt(xs, *argVoigt)/np.sum(CommonHelper.Math.Voigt(xs, *argVoigt))
                BKG = CommonHelper.Math.RooCMSShape(xs, *argExp)  /np.sum(CommonHelper.Math.RooCMSShape(xs, *argExp))


                plt.figure(1)
                ax = plt.subplot(self.nBin2, self.nBin1, n+1)
                color = ['b','g','r']

                print('--- Plotting Pass')    
                self.PlotFitting(
                            ax,
                            xc,
                            NSig = NSig, NBkg = NBkg,
                            DATA = Pass, SIG  = SIG, BKG  = BKG,
                            #eta  = etaBINS[i], pt = ptBins[j],
                            color = color,
                           )

                #######################################
                xs = np.arange(len(Fail),len(Fail)*2)

                argVoigt = FitF[2:5]
                argExp   = FitF[5:9]

                NSig = FitF[0]
                NBkg = FitF[1]

                SIG = CommonHelper.Math.Voigt(xs, *argVoigt)/np.sum(CommonHelper.Math.Voigt(xs, *argVoigt))
                BKG = CommonHelper.Math.RooCMSShape(xs, *argExp)  /np.sum(CommonHelper.Math.RooCMSShape(xs, *argExp))


                plt.figure(2)
                ax1 = plt.subplot(self.nBin2, self.nBin1, n+1)
                color = ['slateblue','olivedrab','firebrick']

                print('--- Plotting Fail')
                self.PlotFitting(
                            ax1,
                            xc,
                            NSig = NSig, NBkg = NBkg,
                            DATA = Fail, SIG  = SIG, BKG  = BKG,
                            #eta  = etaBINS[i], pt = ptBins[j],
                            color = color,
                           )


                ############################################

            Num,dNum = FitP[0], FitPSig[0]
            Dem, dDem = (FitP[0]+FitF[0]), FitPSig[0]+FitFSig[0]

            self.eff[h.name][binj][bini] = Num/Dem
            self.effStat[h.name][binj][bini] = Num/Dem*np.sqrt((dNum/Num)**2 + (dDem/Dem)**2)

            if np.isnan(self.eff[h.name][binj][bini]):
                self.eff[h.name][binj][bini] = 0.0
        
        if Plot:
            fig1.tight_layout()        
            fig2.tight_layout() 
            fig1.savefig('/home/jcordero/CMS/SMP_ZGamma/fig/2018/ee/20200706/sf_eff/eff_pass.png')
            fig2.savefig('/home/jcordero/CMS/SMP_ZGamma/fig/2018/ee/20200706/sf_eff/eff_fail.png')

        return Yield, fig1,fig2
    
        
    def Fit_Curve_CHI(self,
                      DATA_PASS, DATA_FAIL,
                      pPass,pFail,
                      Bounded,
                      error =  [
                                1,1,
                                0.001,0.01,1,0.01,
                                0.001,0.001,0.001
                                ],
                     ):
        
        ####################
        xFit = np.arange(0,len(DATA_PASS))

        chi2 =lambda NSig , NBkg ,                      sig  , Gamma, mean,                      alpha, beta , peak, gamma : CommonHelper.Stat.CHI2(  DATA_PASS,
                                                        CommonHelper.Math.Voigt_CMS(
                                                            xc = xFit, \
                                                            NSig=NSig , NBkg=NBkg , \
                                                            sig = sig  , Gamma  = Gamma, mean = mean, \
                                                            alpha = alpha, beta = beta , peak = peak, gamma = gamma,  
                                                            ) 
                                                        )    


        x0 = pPass
        mP = Minuit( chi2,
                    NSig  =  x0[0], NBkg  =  x0[1],
                    sig   =  x0[2], Gamma =  x0[3], mean =  x0[4],
                    alpha =  x0[5], beta  =  x0[6], peak =  x0[7], gamma = x0[8], 
                    error_NSig  =  error[0], error_NBkg  =  error[1],
                    error_sig   =  error[2], error_Gamma =  error[3], error_mean =  error[4],
                    error_alpha =  error[5], error_beta  =  error[6], error_peak =  error[7], error_gamma = error[8], 
                    limit_NSig  =  (Bounded[0][0],Bounded[1][0]), limit_NBkg  =  (Bounded[0][1],Bounded[1][1]),
                    limit_sig   =  (Bounded[0][2],Bounded[1][2]), limit_Gamma =  (Bounded[0][3],Bounded[1][3]), limit_mean =  (Bounded[0][4],Bounded[1][4]),
                    limit_alpha =  (Bounded[0][5],Bounded[1][5]), limit_beta  =  (Bounded[0][6],Bounded[1][6]), limit_peak =  (Bounded[0][7],Bounded[1][7]), limit_gamma = (Bounded[0][8],Bounded[1][8]), 
                    errordef = 0.5,
                  )    

        mP.migrad()



        FitsPass    = mP.values.values()
        FitsPassSig = mP.errors.values()

        ################################################
        xFit = np.arange(len(DATA_PASS),len(DATA_PASS)*2)

        chi2 =lambda NSig , NBkg ,                      sig  , Gamma, mean,                      alpha, beta , peak, gamma : CommonHelper.Stat.CHI2(  DATA_FAIL,
                                                        CommonHelper.Math.Voigt_CMS(
                                                            xc = xFit, \
                                                            NSig=NSig , NBkg=NBkg , \
                                                            sig = sig  , Gamma  = Gamma, mean = mean, \
                                                            alpha = alpha, beta = beta , peak = peak, gamma = gamma,  
                                                            ) 
                                                        )   

        x0 = pFail
        mF = Minuit( chi2,
                    NSig  =  x0[0], NBkg  =  x0[1],
                    sig   =  x0[2], Gamma =  x0[3], mean =  x0[4],
                    alpha =  x0[5], beta  =  x0[6], peak =  x0[7], gamma = x0[8], 
                    error_NSig  =  error[0], error_NBkg  =  error[1],
                    error_sig   =  error[2], error_Gamma =  error[3], error_mean =  error[4],
                    error_alpha =  error[5], error_beta  =  error[6], error_peak =  error[7], error_gamma = error[8], 
                    limit_NSig  =  (Bounded[0][0],Bounded[1][0]), limit_NBkg  =  (Bounded[0][1],Bounded[1][1]),
                    limit_sig   =  (Bounded[0][2],Bounded[1][2]), limit_Gamma =  (Bounded[0][3],Bounded[1][3]), limit_mean =  (Bounded[0][4],Bounded[1][4]),
                    limit_alpha =  (Bounded[0][5],Bounded[1][5]), limit_beta  =  (Bounded[0][6],Bounded[1][6]), limit_peak =  (Bounded[0][7],Bounded[1][7]), limit_gamma = (Bounded[0][8],Bounded[1][8]), 
                    errordef = 0.5,
                  )    

        mF.migrad()


        FitsFail    = mF.values.values()
        FitsFailSig = mF.errors.values()

        return FitsPass, FitsFail, FitsPassSig, FitsFailSig,mP,mF


    def PlotFitting(self,
                    ax,
                    xc,
                    NSig ,NBkg,
                    DATA, SIG, BKG,
                    #eta, pt,
                    color,
                   ):
        TemplatePlot    = CommonHelper.Math.Template(NSig,NBkg, SIG, BKG)
        TemplatePlotBkg = NBkg*BKG/np.sum(BKG)
        DataPlot        = DATA

        ax.plot(xc,    TemplatePlot, color = color[0], linestyle='--', label=    'Fit')
        ax.plot(xc, TemplatePlotBkg, color = color[1], linestyle='--', label='Fit Bkg')
        ax.plot(xc,        DataPlot, color = color[2], linestyle= '-', label=   'Data')

        ax.legend()
        ax.grid(linestyle='--')

        '''
        if j == 0:
            ax.set_ylabel('Eta ['+str(round(eta[0],2))+','+str(round(eta[1],2))+']'  )        
        if i == 0:
            ax.set_title('Pt ['+str(pt[0])+','+str(pt[1])+']' )
        '''
    
    def EffPlot(self,figpath,bins1,bins2):
        
        fileOut = TFile(figpath,"recreate")
        tree = TTree("eff_photon","eff_photon")

        gStyle.SetOptStat(0)
        #################################################

        Bin1 = array.array("f",CommonHelper.Plot.BinFormat(bins1,Type='edges'))
        Bin2 = array.array("f",CommonHelper.Plot.BinFormat(bins2,Type='edges'))


        nBin1,nBin2 = self.nBin1-2, self.nBin2-1
        histDraw = TH2F("EGamma_eff","Eff",
                      nBin1, Bin1,
                      nBin2, Bin2)


        nBin1,nBin2 = self.nBin1-1, self.nBin2-1
        hist2d = TH2F("EGamma_eff","Eff",
                      nBin1, Bin1,
                      nBin2, Bin2)

        nBin1,nBin2 = self.nBin1-2, self.nBin2-1
        statDraw = TH2F("EGamma_eff_draw_stat","Eff",
                      nBin1, Bin1,
                      nBin2, Bin2)
        
        nBin1,nBin2 = self.nBin1-1, self.nBin2-1
        stat2d = TH2F("EGamma_eff_stat","Eff",
                      nBin1, Bin1,
                      nBin2, Bin2)


        #################################################
        tree.Branch("eff",hist2d,"TH2F")


        for j,binj in zip(range(nBin1),bins1):
            hist2d.GetZaxis().SetRangeUser(0.6,1.1)

            for i,bini in zip(range(nBin2),bins2):
                EFF = self.eff[str(binj)][str(bini)]
                EFFStat = self.effStat[str(binj)][str(bini)]

                hist2d.SetBinContent(int(j)+1, int(i)+1, EFF)
                histDraw.SetBinContent(int(j)+1, int(i)+1, EFF)

                stat2d.SetBinContent(int(j)+1, int(i)+1, EFFStat)
                statDraw.SetBinContent(int(j)+1, int(i)+1, EFFStat)
                tree.Fill()
                
        hist2d.GetZaxis().SetRangeUser(0.6,0.95)
        hist2d.Draw("COLZ text")
        
        fileOut.Write()

        return hist2d
        
    def EffMCPlot(self,figpath,bins1,bins2):
        
        fileOut = TFile(figpath,"recreate")
        tree = TTree("eff_photon","eff_photon")

        gStyle.SetOptStat(0)
        #################################################

        Bin1 = array.array("f",CommonHelper.Plot.BinFormat(bins1,Type='edges'))
        Bin2 = array.array("f",CommonHelper.Plot.BinFormat(bins2,Type='edges'))


        nBin1,nBin2 = self.nBin1-2, self.nBin2-1
        histDraw = TH2F("EGamma_eff","Eff",
                      nBin1, Bin1,
                      nBin2, Bin2)


        nBin1,nBin2 = self.nBin1-1, self.nBin2-1
        hist2d = TH2F("EGamma_eff","Eff",
                      nBin1, Bin1,
                      nBin2, Bin2)

        nBin1,nBin2 = self.nBin1-2, self.nBin2-1
        statDraw = TH2F("EGamma_eff_draw_stat","Eff",
                      nBin1, Bin1,
                      nBin2, Bin2)
        
        nBin1,nBin2 = self.nBin1-1, self.nBin2-1
        stat2d = TH2F("EGamma_eff_stat","Eff",
                      nBin1, Bin1,
                      nBin2, Bin2)


        #################################################
        tree.Branch("eff",hist2d,"TH2F")


        for j,binj in zip(range(nBin1),bins1):
            hist2d.GetZaxis().SetRangeUser(0.6,1.1)

            for i,bini in zip(range(nBin2),bins2):
                EFF = self.effMC[str(binj)][str(bini)]
                EFFStat = self.effMCStat[str(binj)][str(bini)]

                hist2d.SetBinContent(int(j)+1, int(i)+1, EFF)
                histDraw.SetBinContent(int(j)+1, int(i)+1, EFF)

                stat2d.SetBinContent(int(j)+1, int(i)+1, EFFStat)
                statDraw.SetBinContent(int(j)+1, int(i)+1, EFFStat)
                tree.Fill()
                
        hist2d.GetZaxis().SetRangeUser(0.6,0.95)
        hist2d.Draw("COLZ text")
        
        fileOut.Write()

        return hist2d
        
        


# In[9]:


if __name__ == "__main__":
    HS = HistoSampleEff()
    #print(HS._HistoSampleEff__getEffConf())
    print(HS.InitializeParams(i=1,j=1,BinType="Optimized", isConv=True))
    HS.EffPlot("",
               [0,1,2,4],
               [0,1,2,4])


# In[ ]:





# In[ ]:




