#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import scipy.stats   as stat
import scipy.special as spc
import matplotlib.pyplot as plt


# In[2]:


from ROOT import TCanvas, TFile
from Common.CommonHelper import CommonHelper


# In[ ]:


class Efficiency():
    def __init__(self,
                 Config,
                 Data = None,
                 Signal = None,
                 Bkg = None,
                ):
        self.Config = Config
        self.projectdir = Config.projectdir
        self.effPlotPath = self.projectdir + "json/plot/eff_bins.json"
        self.effFitIni = self.projectdir + "json/plot/eff_fit_ini.json"
        self.effConfPath = self.projectdir + "json/plot/eff_conf.json"
        self.PlotPath = self.projectdir + "json/plot/bins_efficiency.csv"
        
        
        self.Data   = Data
        self.Signal = Signal
        self.Bkg    = Bkg
        
        # These variables are set through member functions
        self.binsFile = None
        self.bins = {}
        self.var  = []
        self.Type = None
    
        self.binsAlternative = {}
        self.Help = EffHelp
        
    def __repr__(self):
        space = len(Efiiciency.__name__)
        spacer = " "*space
        msg = "{}(Config={})\n".format(Efficiency.__name__,self.Config)
        msg += spacer+"--> projectdir: {}\n".format(self.projectdir)
        msg += spacer+"--> effPlotPath: {}\n".format(self.effPlotPath)
        msg += spacer+"--> effFitIni: {}\n".format(self.effFitIni)
        msg += spacer+"--> effConfPath: {}\n".format(self.effConfPath)
        msg += spacer+"--> PlotPath: {}\n".format(self.PlotPath)
        return msg
        
    def __str__(self):
        msg =   "--Json source: {}\n"                 "--Bins type: {}\n"                 "--Bin variables: {}\n".format(self.effPlotPath,self.Type, self.vars)
        for v in self.bins:
            msg += "--{}: {}\n".format(v,self.bins[v])
                
        return msg 
    
    def __getPlotConf(self):
        import json
        with open(self.effConfPath) as f:
            JS = f.read()
        return json.loads(JS)
    
    def __getEffConf(self):
        import json
        with open(self.effConfPath) as f:
            JS = f.read()
        return json.loads(JS)
    
    def __getEffConf(self):
        import json
        with open(self.effFitIni) as f:
            JS = f.read()
        return json.loads(JS)
        
    def __getLinewidth(self,Type):
        return self.__getPlotConf()[Type.lower()]["linewidth"]

    def __getColor(self,Type):
        return self.__getPlotConf()[Type.lower()]["color"]
    
    ##################       
    ## Binning
    @staticmethod
    def __validateType(bins,Type):
        return True if Type in list(bins.keys()) else False
    
    @staticmethod
    def __validateVar(bins,Type,var):
        return True if var in list(bins[Type].keys()) else False
    
    @staticmethod
    def __useAlternative(index,BinIndexAlt):
        return True if index in BinIndexAlt else False

    def __validationForYield(self,bins1,bins2):
        var1, var2 = next(iter(bins1)), next(iter(bins2))
        if not self.__validateVar(self.binsFile,self.Type,var1):
            bins1 = {}
        if not self.__validateVar(self.binsFile,self.Type,var2):
            bins2 = {}
        
        if bins1 == {}:
            bins1 = {self.vars[0]:self.bins[self.vars[0]]}
            print("From: {}".format(self.effPlotPath))
            print("Bins1 set to  {} form json file".format(self.vars[0]) )
            
        if bins2 == {}:
            bins2 = {self.vars[1]:self.bins[self.vars[1]]}
            print("From: {}".format(self.effPlotPath))
            print("Bins2 set to  {} form json file".format(self.vars[1]) )
            
        return bins1,bins2

    
    def readFile(self):
        import json
        with open(self.effPlotPath) as f:
            JS = f.read()
        return json.loads(JS)

    def loadBins(self, Type = "BinSet1"):
        bins = self.readFile()
        
        if self.__validateType(bins, Type):
            self.binsFile = bins
            self.Type = Type
            self.vars = [ v for v in bins[Type] ]
            self.bins = { var:bins[Type][var] for var in self.vars }
            self.binsAlternative = { var:[] for var in self.vars }
            
        else:
            print("Bin Type is not valid")
            for typ in bins:
                print('---'+typ)
        
    def setBinRegion(self,var,alt):
        if alt == []:
            if self.__validateVar(self.binsFile, self.Type, var):
                self.binsAlternative[var] = alt
            else:
                print("Variable is not on the binning json or incorrect.")
        else:
            print("Region variable empty")
                
    @staticmethod
    def getIndex(sample,filters, flag ):
        Indices = np.ones(len(sample))
        for filt in filters:
            Indices = np.logical_and(Indices, sample.df[filt] == flag)
        return Indices
    
    @staticmethod
    def getEff(Pass,Fail):
        Pass, Fail = float(Pass), float(Fail)
        return 0 if (Pass + Fail) == 0 else Pass/(Pass + Fail)
        
    @staticmethod
    def getEffStat(eff, Pass,Fail):
        Pass, Fail = float(Pass), float(Fail)
        return 0 if (Pass + Fail) == 0 or Pass == 0 else eff*np.sqrt( 1/Pass + 1/(Pass + Fail))
        
    def eff(self,Pass,Fail):
        eff,effStat = {},{}
        for j in  Pass:
            eff[j], effStat[j] = {},{}
            for i in  Pass[j]:
                eff[j][i] = self.getEff(Pass[j][i], Fail[j][i])
                effStat[j][i] = self.getEffStat(eff[j][i], Pass[j][i], Fail[j][i])
        return eff, effStat

    def GetYields(self,
                  dist1, dist2,
                  bins1 = {}, bins2 = {},
                  Alternative = {},
                  Abs1 = False, Abs2 = False,
                ):
        """Gets the yields on the samples distribution, binned in 2d"""
        """ Dist1 and Dist2 corresponding distributions for variables of bins1 and bins2"""
        
        ### Input validation
        bins1, bin2 = self.__validationForYield(bins1,bins2)
        var1, var2 = next(iter(bins1)), next(iter(bins2))
        
        ### Bin formating
        bins1[var1],bins2[var2] = CommonHelper.Plot.BinFormat(bins1[var1]), CommonHelper.Plot.BinFormat(bins2[var2])
        N1Bin,N2Bin = len(bins1[var1]),len(bins2[var2])

        Yield = {}
        bin1 = bins1[var1]
        for j in np.arange(N1Bin):
            Yield[j] = {}
            if self.__useAlternative(j,Alternative):
                Bin2 = self.binsAlternative[var2]
            else:
                Bin2 = bins2[var2]

            for i in np.arange(len(Bin2)): 
                Ind1 = CommonHelper.Plot.BinIndex( dist1, bin1[j][0], bin1[j][1], Abs=Abs1)
                Ind2 = CommonHelper.Plot.BinIndex( dist2, Bin2[i][0], Bin2[i][1], Abs=Abs2)
                
                Ind    = np.logical_and(Ind1,Ind2)
                
                Yield[j][i] = np.sum(Ind)
                
        return Yield
    
    
    def EffGrid(
                self,
                sample,
                dist1,dist2,
                bins1, bins2,
                Alternative = {},
                Abs1 = True, Abs2 = True,
                ranges       = [60,120],
                bins         =  60, # Should be ranges[1]-ranges[0]
                ProbeType     = "Pass",
                tempType     = 'KDE',
               ):
        #### Array Outputs
        template,ratios = {},{}
        
        ### Input validation
        bins1, bin2 = self.__validationForYield(bins1,bins2)
        var1, var2 = next(iter(bins1)), next(iter(bins2))
        
        ### Bin formating
        bins1[var1],bins2[var2] = CommonHelper.Plot.BinFormat(bins1[var1]), CommonHelper.Plot.BinFormat(bins2[var2])
        N1Bin,N2Bin = len(bins1[var1]),len(bins2[var2])
        

        figx, figy = N2Bin, N1Bin

        fig = plt.figure(figsize=(figy*3,figx*4))
        bin1 = bins1[var1]
        for j in np.arange(N1Bin):
            if self.__useAlternative(j,Alternative):
                Bin2 = self.binsAlternative[var2]
            else:
                Bin2 = bins2[var2]

            template[j],ratios[j] = {},{}
            for i in np.arange(len(Bin2)):                
                Ind1 = CommonHelper.Plot.BinIndex( dist1, bin1[j][0], bin1[j][1], Abs=Abs1)
                Ind2 = CommonHelper.Plot.BinIndex( dist2, Bin2[i][0], Bin2[i][1], Abs=Abs2)
                
                Ind    = np.logical_and(Ind1,Ind2)
                Var = np.array(sample[Ind])


                ij = N1Bin*i + (j+1)     
                plt.subplot(N2Bin, N1Bin, ij)
                ax = plt.gca()

                TEMP, RATIO = self.Plot(
                                    ax       = ax,
                                    Var      = Var,
                                    ranges   = ranges,
                                    bins     = bins,
                                    color    = self.__getColor(ProbeType),
                                    tempType = tempType,
                                    )

                template[j][i] = TEMP
                ratios[j][i]   = RATIO


                if j == 0:
                    ax.set_ylabel(var2+' ['+str(round(Bin2[i][0],2))+','+str(round(Bin2[i][1],2))+']'  )        
                if i == 0:
                    ax.set_title(var1+' ['+str(bin1[j][0])+','+str(bin1[j][1])+']' )




        plt.tight_layout()
        plt.show()
        
        '''
        if isConv:
            fig.savefig(figpath+DataMC+samples+'_'+ProbeType+'_PeakMap_isConv.png')
        else:
            fig.savefig(figpath+DataMC+samples+'_'+ProbeType+'_PeakMap.png')
        '''

        return template,ratios
    def Plot(
             self,
             ax,
             Var,
             ranges, bins, color,
             tempType='KDE'
            ):


            if type(bins) is np.ndarray or type(bins) is list:
                hist = np.histogram(
                                    Var,
                                    range    = ranges,
                                    bins     = bins,
                                    )
                hist = ax.hist(
                                bins[:-1],
                                histtype = 'step',
                                range    = ranges,
                                weights  = hist[0]/np.diff(bins),
                                bins     = bins,
                                color    = color,
                                label    = 'HIST', 
                                )
            else:
                hist = ax.hist(
                                Var,
                                histtype = 'step',
                                range    = ranges,
                                bins     = bins,
                                color    = color,
                                label    = 'HIST', 
                                #density  = True,
                                )

            xc = (hist[1][:-1]+hist[1][1:])/2
            hist[0][np.isnan(hist[0])] = 0

            #######
            if   tempType == 'KDE':
                try:
                    kde       = stat.gaussian_kde(dataset = Var)    
                    template  = kde(xc)
                    ratio     = np.sum(template)/np.sum(hist[0])
                except:
                    template = xc*0
                    ratio    = 1
            elif tempType == 'HIST':
                    template = hist[0]
                    ratio    = 1


            ax.plot(xc,template/ratio,'k--',label = 'KDE')
            ax.grid(linestyle = '--')
            ax.legend()

            return template, ratio
        
    def getBounds(self):
        return [self.__getEffConf()["bounds"]["min"],self.__getEffConf()["bounds"]["max"]]
        
    def getFitIni(self,Type,isConv):
        conv = "convVeto" if isConv else "noconvVeto"
        return self.__getEffConf()[self.Type][conv]
    
    def getFit(self,isConv,bin1Index,bin2Index,ProbeType):        
        return self.getFitIni(self.Type,isConv)["bins"+str(bin1Index)]["bins"+str(bin2Index)][ProbeType]

    def Fit(self,
            i,j,
            MC_PASS_S, MC_PASS_B,
            MC_FAIL_S, MC_FAIL_B,
            DATA_PASS, DATA_FAIL,
            Temp,
            p0, Bounded,
            Type   = '',
            Print  = False,
            TryMax = 20,
            ):

        ###############################

        DATA = np.array(list(DATA_PASS) + list(DATA_FAIL))

        model  = lambda x0:self.Help.Stat.CHI2(DATA=DATA,Temp=Temp,*x0)

        fitSucess = False
        tries = 0

        while not fitSucess:
            if Print:
                print('--- Start Fitting')
            fitResult = minimize(model,
                                 p0,
                                 #method = 'L-BFGS-B',
                                 #method = 'SLSQP',
                                 bounds = Bounded,
                                 #tol = 1e-6,
                                 #tol = 1e-10,
                                )
            fitSucess = fitResult.success
            FIT = fitResult.x

            p0 = GoodGuess(i,j,len(etaBINS),len(ptBins),tries,p0)
            if not p0:
                p0 = np.ones(len(Bounded))
                break;
            tries += 1

            if tries%10 == 0 and Print:
                print('Try: ' + str(tries))
            if tries > TryMax and Print :
                print("Maximum tries reached!")
                break
        return FIT

    
    def Fit_Curve(self,
                  i,j,
                    MC_PASS_S, MC_PASS_B,
                    MC_FAIL_S, MC_FAIL_B,
                    DATA_PASS, DATA_FAIL,
                    p0, Bounded,
                    ):

        ###############################

        DATA = np.array(list(DATA_PASS) + list(DATA_FAIL))
        x = np.arange(0,len(DATA))

        VV = lambda x,*x0 : Voigt_CMS_x(x,
                                        NSigPass  =  x0[0], NBkgPass  =  x0[1], NSigFail =  x0[2],  NBkgFail =  x0[3], 
                                        sigPass   =  x0[4], GammaPass =  x0[5], meanPass =  x0[6],
                                        alphaPass =  x0[7], betaPass  =  x0[8], peakPass =  x0[9], gammaPass = x0[10],
                                        sigFail   = x0[11], GammaFail = x0[12], meanFail = x0[13],
                                        alphaFail = x0[14], betaFail  = x0[15], peakFail = x0[16], gammaFail = x0[17],
                                        MCPass = MC_PASS_S[:len(DATA_PASS)], 
                                        MCFail = MC_FAIL_S[:len(DATA_PASS)])




        return FIT[0]
    
    
    def Fit_Curve(
                  DATA_PASS, DATA_FAIL,
                  pPass,pFail,
                  Bounded,
                 ):

        VoigtCMS = lambda x,*x0 : self.Help.Voigt_CMS(
                                            x,
                                            NSig  =  x0[0], NBkg  =  x0[1],
                                            sig   =  x0[2], Gamma =  x0[3], mean =  x0[4],
                                            alpha =  x0[5], beta  =  x0[6], peak =  x0[7], gamma = x0[8], 
                                            )

        yerr = np.sqrt(DATA_PASS)
        yerr[yerr<1] = yerr[yerr<1]*0+2
        xFit = np.arange(0,len(DATA_PASS))
        Fits = curve_fit(
                        f     = self.Help.VoigtCMS,
                        xdata = xFit,
                        ydata = DATA_PASS,
                        sigma = yerr,
                        p0    = pPass,
                        method = 'trf',
                        bounds = Bounded,
                        )

        FitsPass = Fits[0]
        FitsPassSig = np.sqrt(np.diag(Fits[1]))
        ############################
        yerr = np.sqrt(DATA_FAIL)
        yerr[yerr<1] = yerr[yerr<1]*0+2
        xFit = np.arange(len(DATA_PASS),len(DATA_PASS)*2)
        Fits = curve_fit(
                        f      = self.Help.VoigtCMS,
                        xdata  = xFit,
                        ydata  = DATA_FAIL,
                        sigma  = yerr,
                        p0     = pFail,
                        #method = 'lm',
                        method = 'trf',
                        #method = 'dogbox',
                        bounds = Bounded,
                        )
        FitsFail = Fits[0]
        FitsFailSig = np.sqrt(np.diag(Fits[1]))

        return FitsPass, FitsFail, FitsPassSig, FitsFailSig


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
        from iminuit import Minuit
        from pprint import pprint
        
        ####################
        xFit = np.arange(0,len(DATA_PASS))

        chi2 =lambda NSig , NBkg ,                      sig  , Gamma, mean,                      alpha, beta , peak, gamma : self.Help.Stat.CHI2(  DATA_PASS,
                                                        self.Help.Voigt_CMS(
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

        chi2 =lambda NSig , NBkg ,                      sig  , Gamma, mean,                      alpha, beta , peak, gamma : self.Help.Stat.CHI2(  DATA_FAIL,
                                                        self.Help.Voigt_CMS(
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

        


# In[ ]:


class EffHelp( CommonHelper ):
    @staticmethod
    def RooCMSShape(x,*arg):        
        alpha, beta, peak, gamma = arg

        erf = spc.erfc((alpha - x)*beta)
        u = (x-peak)*gamma

        u = np.exp(-u)   
        #u[u <- 70] = u[u <- 70]*0 + 1e20
        #u[u > 70]  = u[u > 70]*0
        #ind  =  np.logical_and(u>=-70, u<=70)
        #u[ind]     = np.exp(-u[ind])

        return erf*u
    @staticmethod
    ########## TEMPLATES ################
    def TVoigt_Test(
                      NSigPass,NBkgPass, NSigFail,NBkgFail, 
                      sigPass, GammaPass, meanPass,
                      lambdaPass, xPass,
                      sigFail, GammaFail, meanFail,
                      lambdaFail, xFail,
                      MCPass, MCFail
                     ):

        x = np.arange(0,len(MCPass))

        argPass = lambdaPass, xPass
        argVoigtPass = sigPass, GammaPass, meanPass
        Pass = list(EffHelp.Stat.Template(NSigPass, NBkgPass, 
                                          EffHelp.Voigt(x,*argVoigtPass)  , Exp(x,*argPass))) 


        argFail = lambdaFail, xFail
        argVoigtFail = sigFail, GammaFail, meanFail
        Fail = list(EffHelp.Stat.Template(NSigFail, NBkgFail, 
                                         EffHelp.Voigt(x,*argVoigtFail) , Exp(x,*argPass)))


        #Temp = np.array(Pass + Fail )
        Temp = np.array(Pass)
        return Temp

    @staticmethod
    def TVoigt_noSig(
                      NBkgPass,NBkgFail, 
                      sigPass, GammaPass, meanPass,
                      lambdaPass, xPass,
                      sigFail, GammaFail, meanFail,
                      lambdaFail, xFail,
                      MCPass, MCFail
                     ):
        x = np.arange(0,len(MCPass))

        argPass = lambdaPass, xPass
        argVoigtPass = sigPass, GammaPass, meanPass
        Pass = list(Template(0, NBkgPass, EffHelp.Voigt(x,*argVoigtPass)  , Exp(x,*argPass))) 


        argFail = lambdaFail, xFail
        argVoigtFail = sigFail, GammaFail, meanFail
        Fail = list(Template(0, NBkgFail, 
                             Voigt(x,*argVoigtFail) , Exp(x,*argPass)))


        #Temp = np.array(Pass + Fail )
        Temp = np.array(Pass)
        return Temp

    @staticmethod
    def TVoigt_CMS(NSigPass, NBkgPass, NSigFail,NBkgFail, 
                  sigPass, GammaPass, meanPass,
                  alphaPass, betaPass, peakPass, gammaPass,
                  sigFail, GammaFail, meanFail,
                  alphaFail, betaFail, peakFail, gammaFail,
                   MCPass, MCFail
                 ):
        x = np.arange(0,len(MCPass))

        argPass      = alphaPass, betaPass, peakPass, gammaPass
        argVoigtPass = sigPass, GammaPass, meanPass
        Pass = list(EffHelp.Stat.Template(NSigPass, NBkgPass, 
                                         EffHelp.Voigt(x,*argVoigtPass)  , EffHelp.RooCMSShape(x,*argPass))) 


        x = np.arange(len(MCPass),len(MCPass)*2)
        argFail      = alphaFail, betaFail, peakFail, gammaFail
        argVoigtFail = sigFail, GammaFail, meanFail
        Fail = list(EffHelp.Stat.Template(NSigFail, NBkgFail, 
                                         EffHelp.Voigt(x,*argVoigtFail) , EffHelp.RooCMSShape(x,*argFail)))


        Temp = np.array(Pass + Fail )
        return Temp

    @staticmethod
    def TVoigt_Exp(NSigPass, NBkgPass, NSigFail,NBkgFail, 
          sigPass, GammaPass, meanPass,
          lambdaPass, xPass,
          sigFail, GammaFail, meanFail,
          lambdaFail, xFail,
           MCPass, MCFail
         ):
        x = np.arange(0,len(MCPass))

        argPass = lambdaPass, xPass
        argVoigtPass = sigPass, GammaPass, meanPass
        Pass = list(EffHelp.Stat.Template(NSigPass, NBkgPass, 
                                         EffHelp.Voigt(x,*argVoigtPass)  , Exp(x,*argPass))) 


        argFail = lambdaFail, xFail
        argVoigtFail = sigFail, GammaFail, meanFail
        Fail = list(EffHelp.Stat.Template(NSigFail, NBkgFail, 
                                         EffHelp.Voigt(x,*argVoigtFail) , Exp(x,*argPass)))


        Temp = np.array(Pass + Fail )
        return Temp

    @staticmethod
    def Voigt(x, *arg):
        from scipy.special import wofz
        
        alpha, gamma, mean = arg
        sigma = alpha / np.sqrt(2 * np.log(2))

        return np.real(wofz(((x-mean) + 1j*gamma)/sigma/np.sqrt(2))) / sigma                                                               /np.sqrt(2*np.pi)

    
    @staticmethod
    def Voigt_CMS(
                    xc,
                    NSig, NBkg, 
                    sig, Gamma, mean,
                    alpha, beta, peak, gamma,
                    ):
        x = xc
        arg      = alpha, beta, peak, gamma
        argVoigt = sig, Gamma, mean
        Temp = list(EffHelp.Stat.Template(NSig, NBkg, 
                                         EffHelp.Voigt(x,*argVoigt) , 
                                         EffHelp.RooCMSShape(x,*arg)))


        return np.array(Temp)


    ########## METRIC ########
    @staticmethod
    def NLL(DATA,Temp):
        return np.sum(Temp) - np.sum(DATA*np.log(Temp))

    @staticmethod
    def CHI2(DATA,Temp):
        DATA[DATA==0] = 1
        SIGMA_2 = (1/DATA + 1/Temp)**(-1)
        return np.sum((Temp-DATA)**2/SIGMA_2)

    @staticmethod
    def DIFFER(DATA,Temp,*arg):
        Model = Temp(*arg)
        return np.sum((Model-DATA)**2)


# In[ ]:


class EffConf:
    '''
    self.projectdir = Config.projectdir
    self.effPlotPath = self.projectdir + "json/plot/eff_bins.json"
    self.effConfPath = self.projectdir + "json/plot/eff_conf.json"
    self.PlotPath = self.projectdir + "json/plot/bins_efficiency.csv"
    '''
    pass
    


# In[ ]:


CommonHelper


# In[ ]:




