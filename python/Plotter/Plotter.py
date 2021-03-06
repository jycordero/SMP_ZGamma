#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys


# In[ ]:


projectdir = "/home/jcordero/CMS/JYCMCMS/SMP_ZG/" 
sys.path.append(projectdir+"python")


# In[ ]:


import numpy as np
import pandas as pd

import array 

import matplotlib as mpl
import matplotlib.pyplot as plt

import json


# In[ ]:


from Common.CommonHelper import CommonHelper


# In[4]:


class Plotter(object):
    def __init__(self,Bkg= [],Sig=[],Data=[], Config = None):
        self.Config = Config
        self.figpath = Config.figpath + Config.date
        self.jsonProp = self.Config.projectdir + "json/plot/plot_conf.json"     
        self.__binFile = self.Config.projectdir+"json/plot/bins.csv"
        self.__rangeFile = self.Config.projectdir+"json/plot/ranges.csv"
        
        #---------------
        # Global parameters
        self.PlotSettings(Default=True)
        
        #---------------
        # Local Parameters
        self.folder = 'Stacked'
        self.histtype = 'stepfilled'
        self.density = False
        self.linewidth = 1
            
        self.Help = Helper(Config=self.Config)
        
        self.HelpPlot = Helper.Plot
    
    def __del__(self):
        del self.Config
        del self.figpath
        del self.jsonProp
        del self.Help 
        del self.folder 
        del self.histtype
        del self.density 
        del self.linewidth 

    
    def __getBins(self, part, var, ph, ranges,  Blind= True, Plotting = True):
        Bins = pd.read_csv(self.__binFile)
        bins   = Bins[var][Bins['part'] == part+ph].values[0]
        bins   = self.Help.Format.ConvertString2Float(bins)
        bins = np.array(self.Help.Plot.BinFormat(Bins=bins,ranges=ranges,Type='edges'))
        if Blind or Plotting:
            if var == 'Pt':
                if part == 'photonOne':
                    bins = bins[bins<150]
            elif var == 'Eta':
                if part == 'photonOne':
                    bins   = [[0,1.4442],[1.5666,2.5]]
                    
        if type(bins) is np.ndarray:
            bins   = list(bins)
        if not (type(bins) is list or type(bins) is np.ndarray):
            bins = int(bins) 
        return bins
        
    def __getRange(self, part, var, ph, Blind= True, Plotting = True):
        Range = pd.read_csv(self.__rangeFile)

        if part == '':
            part = ' '
        if ph == ' ':
            ph = ''
        ranges = Range[var][Range['part'] == part+ph].values[0]
        ranges = self.Help.Format.ConvertString2Float(ranges)

        if Blind or Plotting:
            if var == 'Pt':
                if part == 'photonOne':
                    bins = bins[bins<150]
            elif var == 'Eta':
                if part == 'photonOne':
                    ranges = [-2.5, 2.5]

        ranges = list(ranges)
        return ranges
        
    def getProperties(self,dataS,part,var,ph,CustomeRangeBins, weightCorrection = False, Blind = True, Plotting = True):
        
        if len(CustomeRangeBins) > 0:
            ranges,bins = CustomeRangeBins['ranges'], CustomeRangeBins['bins']
        else:
            ranges = self.__getRange(part,var,ph, Blind=False,Plotting=Plotting)
            bins = self.__getBins(part,var,ph,ranges,  Blind=False,Plotting=Plotting)
            
        weight = dataS.getWeights( weightCorrection )
        var    = dataS.getVar(part+var+ph)
        label  = dataS.getLabeledYield()
        color  = dataS.getColors()
        legend = dataS.getLegends( )
        
        return ranges, bins, color, legend, weight, var
        
    def setBinFile(self,path):
        self.__binFile = path
        
    def setRangeFile(self,path):
        self.__rangeFile = path
    #######################################        
    def Test(self):
        from Samples.DataStack import DataStackTest
        self.Plot(
                     dataS = DataStackTest( ),
                     var              = 'test',
                     part             = ' ',
                     signalInclude    = True,
                     stacked          = True,
                     density          = False,
                     log              = False,
                     weightCorrection = False,
                     Plotting         = False,
                     Blind            = False,
                     StatInclude      = False,
                     CustomeRangeBins = [],
                     CustomeSettings  = False,
                     Print            = True,
                     index            = 'test',
                    );
    
    def SaveFig(self,fig,figpath,extra,name):
        fig.savefig(self.figpath+extra+name+".png")
        
    def AddToPath(self,addFolder):
        self.folder += addFolder
            
    #######################################
    
    # Naming format to access plots, ranges, bins etc
    def NamingFormat(self, part,var):
        
        k = part.split('_')
        if len(k)>1:
            part,ph = k[0],'_'+k[1]
        else:
            part,ph = k[0],''   
            
            k1 = var.split('_')
            if len(k1) > 1:
                var,ph = k1[0],'_'+k1[1]
            else:
                var,ph = k1[0],'' 
                
        return part, var, ph

    # Take a single "data" Data format and takes the 
    # ranges and bins from the input file and generate the 
    # Histogram information,bins edges and counts in each bin
    def BinnedHist(
                    self,
                    data,
                    var,
                    part             =  '',
                    weightCorrection = True,
                    Plotting         = True,
                    Blind            = False,
                    ):

        self.PlotSettings(Single=True)
        
        part,var,ph = self.NamingFormat(part,var)
            
        ##########################
        ranges = self.__getRanges(self, part, var, ph, ranges,  Blind= Blind, Plotting = Plotting)
        bins = self.__getBins(self, part, var, ph, ranges,  Blind= Blind, Plotting = Plotting)
    
        VAR = data.GetWithCuts(part+var+ph)
        
        if data.name == "DoubleMuon_2017":
            wei = data.GetWithCuts('weight')
        elif weightCorrection:
            reWeight = data.GetWithCuts('puWeight')*data.GetWithCuts('weight')
            wei = np.array(reWeight)         
        else:
            wei = data.GetWithCuts('weight')
        
        bins = self.Help.BinFormat(Bins = bins,ranges = ranges, Type='ranges')
        bins = self.Help.BinFormat(Bins = bins,ranges = ranges, Type='edges')
        HIST = np.histogram(VAR,  weights = wei,  
                            bins  = bins, range = ranges)
                
        return HIST
    
    # Sets the matlab plotting parameters
    # Is either sigle or not, meaning a single plot 
    # or multiple subplot format            
    def SetCategorySetting(self,param,subparam,File,Print=False):
        for sparm in subparam:
                self.SetPlotSetting(param,sparm,File,Print) 
    def SetPlotSetting(self,param,subparam,File,Print=False):
        subindex = File[' '] == subparam
        try:
            value = File[param][subindex].values[0]
            mpl.rcParams[param+'.'+subparam] = value     
            if Print:
                print('Just set plot param '+param+'.'+subparam+ ' ' +str(value))
        except:
            print('Just set plot param '+param+'.'+subparam+ ' empty')
    def PlotSettings(self,Single=True,Default=False,Print=False):
        path = "/home/jcordero/CMS/JYCMCMS/SMP_ZG/python/Plotter/PlotSettings/"
        Params = {}
        Params['Default'] = pd.read_csv(path+"PlotParams_Default.csv")
        Params['Single']  = pd.read_csv(path+"PlotParams_Single.csv")
        Params['Mult']    = pd.read_csv(path+"PlotParams_Mult.csv")
        
        
        mainParams = ['axes','xtick','ytick','legend']
        subParams  = {'axes'     :['grid','titlesize','labelsize'],
                      'axes.grid':['linestyle'],
                      'xtick'    :['labelsize'],
                      'ytick'    :['labelsize'],
                      'legend'   :['loc','fontsize'],
                        }
        
        if Default:
            File = Params['Default']
            
            for param in mainParams:
                self.SetCategorySetting(param,subParams[param],File,Print=Print)

        else:
            if Single:
                File = Params['Single']
                for param in mainParams:
                    self.SetCategorySetting(param,subParams[param],File,Print=Print)
            else:
                File = Params['Mult']
                for param in mainParams:
                    self.SetCategorySetting(param,subParams[param],File,Print=Print)
                    
    def SetYLabel(self,bins,ranges):
        ylabel = '# Counts'
        try :
            if type(bins) == int:
                step = int((ranges[1]-ranges[0])/bins)
                ylabel += '/'+str(step)
            else:
                diff = np.diff(bins)
                if np.sum(np.diff(bins) - diff[0]) == 0:
                    ylabel += '/'+str(diff[0])
        except:
            ylabel = ylabel

        return ylabel 
    
    def SetFigName(self,part,var,ph,index,Single=True):
        if Single:
            FigName = var+'_'+part+"_"+str(index)
        else:
            FigName = var+"_"+str(index)
            
        return FigName
    def SetTitle(self,part,var,ph):
        if 'EE' in ph:
            ECALlabel = " ECal Endcap"
        elif 'EB' in ph:
            ECALlabel = " ECal Barrel"
        else:
            ECALlabel = ""
            
        title = part + ECALlabel
        return title
    
    #######################################

    
    def Plot_Mult(self,
                  data,
                  var,
                  part,
                  signalInclude    = False,
                  figDim           = [2,3],
                  customRange      = False,
                  stacked          = True,
                  density          = False,
                  log              = False,
                  weightCorrection = True,
                  externalData     = None,
                  Blind            = True,
                  Plotting         = True,
                  StatInclude      = False,
                  Print            = False,
                  CustomeSettings  = False,
                  index            = 0,
                 ):

        if not CustomeSettings:
            self.PlotSettings(Single=False,Print=Print)



        nx,ny = figDim[0],figDim[1]
        rowSpan,colSpan = 3,1

        ##########################
        if not signalInclude:
            N = 2
        else:
            N = 1
        ##########################
        if stacked:
            histtype = 'stepfilled'
        else:
            histtype = 'step'
        ##########################

        htemp = []
        row,col =0 , 0


        fig = plt.figure(figsize = (6*ny, 6*nx))

        for j,k in zip(range(len(part)),part): 
            
            p,v,ph = self.NamingFormat(k,var)

            ##########################

            ranges, bins, colors, legend, wei, VAR = self.getProperties(dataS,part,var,ph,CustomeRangeBins, weightCorrection, Blind = True, Plotting = True)
        
            histtype = dataS.getHistType( )[0]

            ##########################

            nx,ny = figDim[0],figDim[1]

            if j != 0:
                if j%ny == 0:
                    row += 1
                    col = 0  

            ax = plt.subplot2grid((nx*(rowSpan+1),ny),(row*(rowSpan+1),col),rowspan = rowSpan, colspan = colSpan)        

            h_bg = ax.hist(
                            VAR[:-N],                            
                            histtype  = histtype,
                            range     = ranges,
                            bins      = bins,
                            stacked   = stacked,
                            color     = colors[:-N],
                            weights   = wei[:-N],
                            label     = legend[:-N],
                            density   = density,
                            linewidth = self.linewidth,
                            )
            htemp.append(h_bg)
            ax = plt.gca()

            #----------------------------------------------------------------
            #----------------------------------------------------------------
            if stacked:
                if not signalInclude:
                    h_sig = ax.hist(
                                    VAR[-N],
                                    bins      = bins,
                                    range     = ranges,
                                    histtype  = histtype,
                                    stacked   = stacked,
                                    color     = colors[-N],
                                    weights   = wei[-N],
                                    label     = legend[-N] + "x"+str(mag),
                                    linewidth = self.linewidth+1,
                                    )
                    ax.legend(prop={'size': 10})
                else:
                    h_sig = h_bg[0][-1]

                if type(bins) is float or type(bins) is int:
                    step = (ranges[1]-ranges[0])/bins
                    bins = np.array([ranges[0]+i*step for i in np.arange(bins+1)])   


                if StatInclude:
                    x,value,statUp,statDown = self.Help.GET_StatUncertainty(data = data, hist = h_bg[0], part=p,var=v,ph=ph, bins = h_bg[1])
                    ax.fill_between(x,value-statDown,value+statUp,facecolor='lightgrey',color = 'grey',hatch='/////',alpha=0.6,label='MC stat')


                #---------------------
                #---- Ploting the Data    
                #---------------------
                # Blind the data Plot
                if len(CustomeRangeBins) > 0:
                    ranges,bins = CustomeRangeBins['ranges'], CustomeRangeBins['bins']
                else:
                    bins = self.__getBins(part, var, ph, ranges,  Blind= Blind, Plotting = Plotting)
                    ranges = self.__getRange(part, var, ph, Blind= Blind, Plotting = Plotting)

                x3,y3,x3b,xlim = self.PlotData(ax,VAR[-1],ranges,bins,log)


                #------------------------
                #---- Ploting the Data/MC    
                #-------------------------
                ax1 = plt.subplot2grid((nx*(rowSpan+1),ny),(row*(rowSpan+1)+rowSpan,col),
                                       rowspan = 1, colspan = colSpan,
                                       sharex = ax,
                                      )    

                # Data/MC  y-RANGE
                ylim = [0.5,1.5]
                try:
                    self.PlotDataMC(ax1,
                                   lims    = [xlim, ylim],
                                   Data    = [x3b, y3],
                                   Bkg     = h_bg[0][-1],
                                   Sig     = h_sig[0],
                                   ranges  = ranges,
                                   bins    = bins,
                                  )
                except:
                    self.PlotDataMC(ax1,
                                   lims    = [xlim, ylim],
                                   Data    = [x3b, y3],
                                   Bkg     = h_bg[0],
                                   Sig     = h_sig[0],
                                   ranges  = ranges,
                                   bins    = bins,
                                  )

            col+=1
            if log:
                ax.set_yscale('log')
                
            title = self.SetTitle(p,v,ph)
            ylabel = self.SetYLabel(bins,ranges)
            
            ax.set_title(title)
            ax.set_ylabel(ylabel)
            ax1.set_xlabel(None)
            ax1.set_xlabel(v)
            #########################################################

        
        fig.tight_layout()
        #fig.subplots_adjust(hspace=)
        plt.show()


        if stacked:
            Fol = 'Stacked'
        else:
            Fol = 'Unstacked'

        if log:
            stackFol = Fol+'/log'
        else:
            stackFol = Fol+'/linear'

        FigName = self.SetFigName(p,v,ph,index,Single=False)
        self.SaveFig(fig     = fig,
                     figpath = self.figpath, 
                     extra   = stackFol+'/Mult/', 
                     name    = FigName,
                    )
      
    ### Input "Data()" format ##
    # The input is the "raw" Data formats
    def Plot(self,
             dataS,
             var,
             part             =  '',
             signalInclude    = True,
             stacked          = True,
             density          = False,
             log              = False,
             weightCorrection = False,
             Plotting         = True,
             Blind            = True,
             StatInclude      = False,
             CustomeRangeBins = [],
             CustomeSettings  = False,
             Print            = False,
             index            = 0,
            ):

        ##########################
        mag = 1
        
        if not CustomeSettings:
            self.PlotSettings(Single=True,Print=Print)
        
        part,var,ph = self.NamingFormat(part,var)        
            
        ##########################

        ranges, bins, colors, legend, wei, VAR = self.getProperties(dataS,part,var,ph,CustomeRangeBins, weightCorrection, Blind = True, Plotting = True)
        
        histtype = dataS.getHistType( )[0]
        
        ##########################

        if not signalInclude:
            N = 2
        else:
            N = 1

        ###########################################################
        
        fig = plt.figure(figsize=(10,10))
        plt.subplot2grid((4,1),(0,0),rowspan = 3, colspan = 1)

        h_bg = plt.hist(
                        VAR[:-N],
                        range     = ranges,
                        bins      = bins,
                        histtype  = histtype,
                        stacked   = stacked,
                        weights   = wei[:-N],
                        label     = legend[:-N],
                        color     = colors[:-N],
                        density   = density,
                        linewidth = self.linewidth,
                        )
        
        ax = plt.gca()      
        

        ##########################
        if stacked:
            ##########################
            if not signalInclude:
                h_sig = plt.hist(
                                    VAR[-N],
                                    range     = ranges,
                                    bins      = bins,
                                    histtype  = histtype,
                                    stacked   = stacked,
                                    label     = legend[-N]+" x"+str(mag),
                                    color     = colors[-N],
                                    weights   = np.array(wei[-N])*mag,
                                    density   = density,
                                    linewidth = self.linewidth+0.5,
                                    )
            else:
                h_sig = h_bg[-N]

            if type(bins) is float or type(bins) is int:
                step = (ranges[1]-ranges[0])/bins
                bins = np.array([ranges[0]+i*step for i in np.arange(bins+1)])   

            if StatInclude:
                try:
                    x,value,statUp,statDown = self.Help.GET_StatUncertainty(data = data, hist = h_bg[0], part=part,var=var,ph=ph, bins = h_bg[1])
                except:
                    x,value,statUp,statDown = self.Help.GET_StatUncertainty(data = data, hist = [h_bg[0]], part=part,var=var,ph=ph, bins = h_bg[1])

                ax.fill_between(x,value-statDown,value+statUp,facecolor='lightgrey',color = 'grey',hatch='/////',alpha=0.5,label='MC stat')

            ##########################
            if not density:
                #---------------------
                #---- Ploting the Data    
                #---------------------
                
                # Blind the data Plot
                
                if len(CustomeRangeBins) > 0:
                    ranges,bins = CustomeRangeBins['ranges'], CustomeRangeBins['bins']
                else:
                    bins = self.__getBins(part, var, ph, ranges,  Blind= Blind, Plotting = Plotting)
                    ranges = self.__getRange(part, var, ph, Blind= Blind, Plotting = Plotting)
                
                x3,y3,x3b,xlim = self.PlotData(ax,VAR[-1],ranges = ranges,bins = bins,log = log)

                #------------------------
                #---- Ploting the Data/MC    
                #-------------------------
                plt.subplot2grid((4,1),(3,0),
                                 rowspan = 1, colspan = 1,
                                 sharex = ax
                                )
                ax1 = plt.gca()

                # Data/MC  y-RANGE
                ylim = [0.5,1.5]
                try:
                    DataMC,errDataMC = self.PlotDataMC(ax1,
                                                       lims    = [xlim, ylim],
                                                       Data    = [x3b, y3],
                                                       Bkg     = h_bg[0][-1],
                                                       Sig     = h_sig[0],
                                                       ranges  = ranges,
                                                       bins    = bins,
                                                      )
                except:
                    DataMC,errDataMC = self.PlotDataMC(ax1,
                                                       lims    = [xlim, ylim],
                                                       Data    = [x3b, y3],
                                                       Bkg     = h_bg[0],
                                                       Sig     = h_sig[0],
                                                       ranges  = ranges,
                                                       bins    = bins,
                                                      )
            
            
            
            title = self.SetTitle(part,var,ph)
            ylabel = self.SetYLabel(bins,ranges)
            
            if log:
                ax.set_yscale('log')
            ax.set_title(title)
            ax.set_ylabel(ylabel)
            ax.legend()
            ax1.set_xlabel(var)
        

        plt.tight_layout()
        fig.subplots_adjust(hspace=0)
        plt.show()

        if stacked:
            Fol = 'Stacked'
        else:
            Fol = 'Unstacked'

        if log:
            stackFol = Fol+'/log'
        else:
            stackFol = Fol+'/linear'
            
        FigName = self.SetFigName(part,var,ph,index)
        
        self.SaveFig(fig     = fig,
                     figpath = self.figpath, 
                     extra   = stackFol+'/', 
                     name    = FigName,
                    )


        try:
            return x3,y3,h_bg[0][-1],h_sig[0],DataMC,errDataMC
        except:
            return False
    
    def PlotData(self,
                 ax,
                 Data,
                 ranges,
                 bins,
                 color = 'k',
                 marker = 'o',
                 linestyle = '',
                 legend = 'data',
                 log = False,
                 ):

        y3,x3 =np.histogram(
                            Data,
                            range    = ranges,
                            bins     = bins,
                           )
        x3b = (x3[1:len(x3)] + x3[0:-1])/2
        ax.errorbar(x3b,
                    y3,
                    xerr      = np.diff(x3)/2,yerr = np.sqrt(y3),
                    color     = color,
                    marker    = marker,
                    linestyle = linestyle,
                    label     = legend,
                   )

        xlim = ax.get_xlim()

        return x3,np.array(y3),x3b,xlim   
    
    
    ## Input Binned format ###
    # This is intended to be used with "BinnedHist"
    # function to generate the binning
    def Plot_Bin(self,
                 VAR, wei,
                 label, colors,
                 ranges, bins,
                 var,
                 part             =  '',
                 signalInclude    = True,
                 stacked          = True,
                 density          = False,
                 log              = False,
                 Plotting         = True,
                 Blind            = True,
                 StatInclude      = False,
                 Print            = False,
                 CustomeSettings  = False,
                 index            = 0,
                ):

        ##########################
        if not CustomeSettings:
            self.PlotSettings(Single=True,Print=Print)
        
        part,var,ph = self.NamingFormat(part,var)        
            
        label = [label[i]+' '+str(round(np.sum(VAR[i]))) for i in range(len(label)) ]
        ##########################

        if not signalInclude:
            N = 2
        else:
            N = 1

        ###########################################################

        fig = plt.figure(figsize=(10,10))
        plt.subplot2grid((4,1),(0,0),rowspan = 3, colspan = 1)

        binsC = (bins[:-1]+bins[1:])/2
        
        h_bg = plt.hist(
                        [binsC for _ in VAR[:-N]],
                        range     = ranges,
                        bins      = bins,
                        histtype  = self.histtype,
                        stacked   = stacked,
                        weights   = list(VAR[:-N]),
                        label     = label[:-N],
                        color     = self.colors[:-N],
                        linewidth = self.linewidth,
                        )
        ax = plt.gca()  
            

        ##########################

        if stacked:
            ##########################
            if not signalInclude:
                h_sig = plt.hist(
                                    [bins for _ in VAR[-N]],
                                    range     = ranges,
                                    bins      = bins,
                                    histtype  = self.histtype,
                                    stacked   = stacked,
                                    label     = label[-N],
                                    color     = self.colors[-N],
                                    weights   = VAR[-N],
                                    linewidth = self.linewidth+0.5,
                                    )
            else:
                h_sig = h_bg[-N]

            if type(bins) is float or type(bins) is int:
                step = (ranges[1]-ranges[0])/bins
                bins = np.array([ranges[0]+i*step for i in np.arange(bins+1)])   

            if StatInclude:
                try:
                    x,value,statUp,statDown = self.Help.GET_StatUncertainty(data = data, hist = h_bg[0], part=part,var=var,ph=ph, bins = h_bg[1])
                except:
                    x,value,statUp,statDown = self.Help.GET_StatUncertainty(data = data, hist = [h_bg[0]], part=part,var=var,ph=ph, bins = h_bg[1])

                ax.fill_between(x,value-statDown,value+statUp,facecolor='lightgrey',color = 'grey',hatch='/////',alpha=0.6,label='MC stat')

            ##########################
            if not density:
                #---------------------
                #---- Ploting the Data    
                #---------------------
                                
                x3,y3,x3b,xlim = self.PlotData_Bin(ax,data=VAR[-1],ranges=ranges,bins=bins,log=log)

                #------------------------
                #---- Ploting the Data/MC    
                #-------------------------
                plt.subplot2grid((4,1),(3,0),rowspan = 1, colspan = 1)    
                ax1 = plt.gca()

                # Data/MC  y-RANGE
                ylim = [0.5,1.5]
                try:
                    DataMC, DataMCerr = self.PlotDataMC(ax1,
                                                       lims    = [xlim, ylim],
                                                       Data    = [x3b, y3],
                                                       Bkg     = h_bg[0][-1],
                                                       Sig     = h_sig[0],
                                                       ranges  = ranges,
                                                       bins    = bins,
                                                      )
                except:
                    DataMC, DataMCerr = self.PlotDataMC(ax1,
                                                       lims    = [xlim, ylim],
                                                       Data    = [x3b, y3],
                                                       Bkg     = h_bg[0],
                                                       Sig     = h_sig[0],
                                                       ranges  = ranges,
                                                       bins    = bins,
                                                      )
            title = self.SetTitle(part,var,ph)
            ylabel = self.SetYLabel(bins,ranges)
            
            if log:
                ax.set_yscale('log')
            ax.legend()
            ax.set_title(title)
            ax.set_ylabel(ylabel)
            #ax1.set_ylabel(ylabel)
            
        

        plt.tight_layout()
        plt.show()

        if stacked:
            Fol = 'Stacked'
        else:
            Fol = 'Unstacked'

        if log:
            stackFol = Fol+'/log'
        else:
            stackFol = Fol+'/linear'
            
        FigName = self.SetFigName(part,var,ph,index,Single=True)
        self.SaveFig(fig     = fig,
                     figpath = self.figpath, 
                     extra   = stackFol+'/', 
                     name    = FigName,
                    )


        try:
            return ax, x3,y3,h_bg[0][-1],h_sig[0],DataMC, DataMCerr
        except:
            return False

    def PlotData_Bin(self,
                     ax,
                     data,
                     ranges,
                     bins,
                     color = 'k',
                     marker = 'o',
                     linestyle = '',
                     legend = 'data',
                     log = False,
                     ):


        y3,x3 = data, bins
        
        x3b = (x3[1:len(x3)] + x3[0:-1])/2
        ax.errorbar(x3b,
                    y3,
                    xerr      = np.diff(x3)/2,yerr = np.sqrt(y3),
                    color     = color,
                    marker    = marker,
                    linestyle = linestyle,
                    label     = legend,
                   )
        ax.legend()

        xlim = ax.get_xlim()
        ax.set_ylabel('# Counts')
        if log:
            ax.set_yscale('log')

        return x3,np.array(y3),x3b,xlim      
    
    def PlotDataMC(self,
                ax,
                lims,
                Data,Sig,Bkg,
                ranges,bins,mag=1,
                color = 'k',
                marker = 'o',
                linestyle = '',
                signalInclude=True,
                log    = False,
                atZero = False
                ):
        Bkg = Bkg[:len(Data[0])]
        try:
            Sig = Sig[:len(Data[0])]
        except:
            Sig = Sig

        if not signalInclude:
            h = Bkg+Sig/mag
            rDataMC = Data[1]/(Bkg+Sig/mag) 
        else:
            h = np.array(Bkg)
            rDataMC = Data[1]/Bkg 

            
        if atZero:
            rDataMC    -= 1
            lims[1][0] -= 1
            lims[1][0] -= 1
            ylabel   = r'$\frac{Data}{MC} - 1$'
        else:
            ylabel = r'$\frac{Data}{MC}$'
        
        bins = self.Help.Plot.BinFormat(Bins=bins,ranges=ranges,Type='ranges')

        DataMC    = rDataMC[:len(Data[0])]
        errDataMC = Data[1]/h*np.sqrt(1/Data[1]+1/h)
        ax.errorbar(
                    Data[0], DataMC,
                    xerr      = np.diff(bins)/2,
                    yerr      = errDataMC,
                    color     = color,
                    marker    = marker,
                    linestyle = linestyle,
                    linewidth = 1.5
                   )    
        plt.grid(linestyle='--')
        
        ax.set_ylabel(ylabel)
        ax.set_xlim(lims[0])
        ax.set_ylim(lims[1])
        if log:
            ax.set_yscale('log')
        
        return DataMC, errDataMC
            
    #######################################


# In[ ]:


class Helper( CommonHelper ):
    def __init__(self,era="2017",path='',minBiasCustom = '', Config = None):
        self.Config = Config
        self.path = path
        
        self.era = era
        if self.era == "2016":
            self.xsec1 = "65"
            self.xsec2 = "69p2"
        elif self.era == "2017":
            self.xsec1 = "70"
            self.xsec2 = "69p2"
        else:
            self.xsec1 = "70"
            self.xsec2 = "69p2"
            
        if minBiasCustom != '' and minBiasCustom != ' ':
            self.xsec = "69p2"
            self.xsec = minBiasCustom
    
    ########## PU reWeight ##############       
    def IsDataName(name):
        flag = False
        if name == 'DoubleMuon_2016':
            flag = True
        if name == 'DoubleMuon_2017':
            flag = True
        if name == 'DoubleMuon_2018':
            flag = True

        if name == 'DoubleEG_2016':
            flag = True
        if name == 'DoubleEG_2017':
            flag = True
        if name == 'DoubleEG_2018':
            flag = True

        return flag
    
    def SetPath(self, path):
        self.path = path
    ########## PU reWeight ##############
    def GetDataPU(self,era = '2016',xsec='69p2'):
        pileupFile = 'pileup_sf_'+era+'_'+xsec+'mb.root'
        if era == "2016":
            DataGen = "legacy"
        elif era == "2017":
            DataGen = "rereco"
        elif era == "2018":
            DataGen = "rereco"
            
        file = TFile('/home/jcordero/CMS/data_'+era+'/'+DataGen+'/SMP_ZG/Files/'+pileupFile)
        puTree = file.Get('pileup')
        PUdata = []
        for pu in puTree:
            PUdata.append(pu)
        return PUdata    
    def GetMCPU(self,era = '2016',Flag = True):
        ########### MC Scenario ##################
        if   era == '2016':
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
        elif era == '2017':
            # Extracted from noTrig DYJets MC
            if Flag:
                PU = np.array([ 
                                 0.,  1.,  2.,  3.,  4.,  5.,  6.,  7.,  8.,  9., 10., 11., 12.,
                                13., 14., 15., 16., 17., 18., 19., 20., 21., 22., 23., 24., 25.,
                                26., 27., 28., 29., 30., 31., 32., 33., 34., 35., 36., 37., 38.,
                                39., 40., 41., 42., 43., 44., 45., 46., 47., 48., 49., 50., 51.,
                                52., 53., 54., 55., 56., 57., 58., 59., 60., 61., 62., 63., 64.,
                                65., 66., 67., 68., 69., 70., 71., 72., 73., 74., 75., 76., 77.,
                                78., 79., 80., 81., 82., 83., 84., 85., 86., 87., 88., 89., 90.,
                                91., 92., 93., 94., 95., 96., 97., 98., 99.
                                ])
                PUmc = np.array([
                                2.50071521e-02, 9.32138697e-04, 1.34349382e-03, 1.55653761e-03,
                                1.45496351e-03, 1.43526107e-03, 1.27835150e-03, 1.15729683e-03,
                                2.21869955e-03, 1.72671527e-03, 2.28850123e-03, 3.35718143e-03,
                                4.92791900e-03, 6.68134795e-03, 9.10044445e-03, 1.17060042e-02,
                                1.45309977e-02, 1.75059783e-02, 1.99916815e-02, 2.23530463e-02,
                                2.41402001e-02, 2.53499037e-02, 2.62041645e-02, 2.67175374e-02,
                                2.74284230e-02, 2.83532398e-02, 2.89839400e-02, 2.93689364e-02,
                                2.91766601e-02, 2.90470411e-02, 2.88956340e-02, 2.90606641e-02,
                                2.90281817e-02, 2.85503530e-02, 2.82879200e-02, 2.75466820e-02,
                                2.62923374e-02, 2.50091934e-02, 2.40847315e-02, 2.32438276e-02,
                                2.14996286e-02, 1.96380581e-02, 1.77144071e-02, 1.59592475e-02,
                                1.44335061e-02, 1.32091144e-02, 1.20550570e-02, 1.16780036e-02,
                                1.13855288e-02, 1.11553119e-02, 1.13355627e-02, 1.13423077e-02,
                                1.12138868e-02, 1.12709972e-02, 1.11441738e-02, 1.12494754e-02,
                                1.10476141e-02, 1.08218347e-02, 1.03416985e-02, 9.49174212e-03,
                                8.46104682e-03, 7.27566069e-03, 5.91352943e-03, 4.90768406e-03,
                                3.81464205e-03, 3.17125069e-03, 2.79472984e-03, 2.00325951e-03,
                                1.47187034e-03, 1.02776656e-03, 7.73232257e-04, 6.06693338e-04,
                                3.89700182e-04, 3.41109691e-04, 3.04988540e-04, 2.55155551e-04,
                                1.94095718e-04, 1.72041404e-04, 1.62678304e-04, 3.32811588e-04,
                                3.62454007e-04, 2.83644223e-04, 1.80738880e-04, 2.56708672e-04,
                                1.23362162e-04, 1.57264569e-04, 8.94597549e-05, 2.03769442e-04,
                                1.75902018e-04, 1.12046568e-04, 5.72879681e-05, 4.00705152e-05,
                                5.28061053e-06, 2.49386817e-05, 2.00130702e-05, 1.53980828e-04,
                                6.65623177e-06, 1.37562123e-05, 4.82798677e-05
                                ])    
            else:
                '''
                # mix_2017_25ns_UltraLegacy_PoissonOOTPU_cfi.py
                PU = np.array([
                                 0,  1,  2,  3,  4,  5,  6,  7,  8,  9,
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
                ''';
                #2017_25ns_WinterMC_PUScenarioV1_PoissonOOTPU
                PU = np.array([
                                0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 
                                15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 
                                27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 
                                39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 
                                51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 
                                63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 
                                75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 
                                87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98
                                ])
                PUmc = np.array([
                                  3.39597497605e-05,6.63688402133e-06,1.39533611284e-05,3.64963078209e-05,6.00872171664e-05,
                                  9.33932578027e-05,0.000120591524486,0.000128694546198,0.000361697233219,0.000361796847553,
                                  0.000702474896113,0.00133766053707,0.00237817050805,0.00389825605651,0.00594546732588,
                                  0.00856825906255,0.0116627396044,0.0148793350787,0.0179897368379,0.0208723871946,
                                  0.0232564170641,0.0249826433945,0.0262245860346,0.0272704617569,0.0283301107549,
                                  0.0294006137386,0.0303026836965,0.0309692426278,0.0308818046328,0.0310566806228,
                                  0.0309692426278,0.0310566806228,0.0310566806228,0.0310566806228,0.0307696426944,
                                  0.0300103336052,0.0288355370103,0.0273233309106,0.0264343533951,0.0255453758796,
                                  0.0235877272306,0.0215627588047,0.0195825559393,0.0177296309658,0.0160560731931,
                                  0.0146022004183,0.0134080690078,0.0129586991411,0.0125093292745,
                                  0.0124360740539,0.0123547104433,0.0123953922486,0.0124360740539,0.0124360740539,
                                  0.0123547104433,0.0124360740539,0.0123387597772,0.0122414455005,0.011705203844,
                                  0.0108187105305,0.00963985508986,0.00827210065136,0.00683770076341,0.00545237697118,
                                  0.00420456901556,0.00367513566191,0.00314570230825,0.0022917978982,0.00163221454973,
                                  0.00114065309494,0.000784838366118,0.000533204105387,0.000358474034915,0.000238881117601,
                                  0.0001984254989,0.000157969880198,0.00010375646169,6.77366175538e-05,4.39850477645e-05,
                                  2.84298066026e-05,1.83041729561e-05,1.17473542058e-05,7.51982735129e-06,6.16160108867e-06,
                                  4.80337482605e-06,3.06235473369e-06,1.94863396999e-06,1.23726800704e-06,7.83538083774e-07,
                                  4.94602064224e-07,3.10989480331e-07,1.94628487765e-07,1.57888581037e-07,1.2114867431e-07,
                                  7.49518929908e-08,4.6060444984e-08,2.81008884326e-08,1.70121486128e-08,1.02159894812e-08
                                ])    
        elif era == '2018':
            # mix_2018_25ns_UltraLegacy_PoissonOOTPU_cfi.py
            '''
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
            ''';
            #mix_2018_25ns_JuneProjectionFull18_PoissonOOTPU_cfi.py
            PU = np.array([
                            0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                            20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
                            40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59,
                            60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79,
                            80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99
                            ])

            PUmc = np.array([
                            4.695341e-10, 1.206213e-06, 1.162593e-06, 6.118058e-06, 1.626767e-05,
                            3.508135e-05, 7.12608e-05, 0.0001400641, 0.0002663403, 0.0004867473,
                            0.0008469, 0.001394142, 0.002169081, 0.003198514, 0.004491138,
                            0.006036423, 0.007806509, 0.00976048, 0.0118498, 0.01402411,
                            0.01623639, 0.01844593, 0.02061956, 0.02273221, 0.02476554,
                            0.02670494, 0.02853662, 0.03024538, 0.03181323, 0.03321895,
                            0.03443884, 0.035448, 0.03622242, 0.03674106, 0.0369877,
                            0.03695224, 0.03663157, 0.03602986, 0.03515857, 0.03403612,
                            0.0326868, 0.03113936, 0.02942582, 0.02757999, 0.02563551,
                            0.02362497, 0.02158003, 0.01953143, 0.01750863, 0.01553934,
                            0.01364905, 0.01186035, 0.01019246, 0.008660705, 0.007275915,
                            0.006043917, 0.004965276, 0.004035611, 0.003246373, 0.002585932,
                            0.002040746, 0.001596402, 0.001238498, 0.0009533139, 0.0007282885,
                            0.000552306, 0.0004158005, 0.0003107302, 0.0002304612, 0.0001696012,
                            0.0001238161, 8.96531e-05, 6.438087e-05, 4.585302e-05, 3.23949e-05,
                            2.271048e-05, 1.580622e-05, 1.09286e-05, 7.512748e-06, 5.140304e-06,
                            3.505254e-06, 2.386437e-06, 1.625859e-06, 1.111865e-06, 7.663272e-07,
                            5.350694e-07, 3.808318e-07, 2.781785e-07, 2.098661e-07, 1.642811e-07,
                            1.312835e-07, 1.081326e-07, 9.141993e-08, 7.890983e-08, 6.91468e-08,
                            6.119019e-08, 5.443693e-08, 4.85036e-08, 4.31486e-08, 3.822112e-08
                            ])
            
        return PU,PUmc
    
    def GetPUweight(self,era = '2016', xsec='69p2'):

        ### Get Distributions ##
        PU,PUmc = self.GetMCPU(era)
        PUdata  = self.GetDataPU(era,xsec)

        ### Normalize ###
        PUmc   = np.array(PUmc)/sum(PUmc)        
        PUdata = np.array(PUdata)/sum(PUdata)

        return PU,PUdata[:len(PUmc)]/PUmc,PUdata,PUmc,    
    
    def SF_ratio(self,
                 data,
                 era   = '2016',
                 xsec1 = '65',
                 xsec2 = '69p2',
                 Print = False,
                ):
        pu,r1,r1d,r1mc = self.GetPUweight(era = era, xsec = xsec1)
        pu,r2,r2d,r2mc = self.GetPUweight(era = era, xsec = xsec2)

        rScale = r1/r2
        rScale[np.isnan(rScale)] = np.ones(sum(np.isnan(rScale)))

        puWeight = []
        for d in data[:-1]:
            if not d.df.empty:
                puW = np.ones(len(d.df.nPU))
                if Print:
                    print('--------------',d.name)
                    print(len(d.df.nPU))
                for i in range(len(pu)-2):
                    mask = np.logical_and(np.array(d.df.nPU) > pu[i], np.array(d.df.nPU) <= pu[i+1])        
                    puW[mask] = np.ones(np.sum(mask))*rScale[i]
                puWeight.append(puW)
            else:
                puWeight.append(np.array([]))
        return puWeight
    def PU_reWeight(self,
                    data,
                    era,
                    xsec1 = "70",
                    xsec2 = "69p2", 
                    weightCorrection = False
                   ):
        if weightCorrection:
            reWeight = []
            puWeight = self.SF_ratio(data=data,era=era, xsec1=xsec1, xsec2=xsec2)
            for i in range(len(data[:-1])):
                reWeight.append(np.array(data[i].weight)*puWeight[i])
        else:
            reWeight = []
            puWeight = self.SF_ratio(data=data,era=era, xsec1=xsec1, xsec2=xsec2)
            puWeight = list(np.ones(len(puWeight)))
            for i in range(len(data[:-1])):
                reWeight.append(np.array(data[i].weight)*puWeight[i]) 
        return reWeight                    
   
    def UnStackHist(self,
                    hist):
        UnHist = []
        UnHist.append(hist[0])
        for i in np.arange(1,len(hist)):
            UnHist.append(hist[i] - hist[i-1])
        return UnHist    
    
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
        return x,count,statsUp, statsDown    
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

        return x,value,statsUp, statsDown    
    
    ##########################
    def SetDataOpt(self,data,selection="mumug",exclude = []):
        
        legend      = [          'WJets ',       'V-V ',     'TT ', 'DYJets ',  'ZG ',  'Data ']
        colors      = [ 'cornflowerblue', 'lightskyblue', 'lightcoral',   'plum',    'pink',     'k']
        dataFlag    = [            False,          False,        False,    False,     False,    True]

        ##############################
        #if selection == "ee":
        #    exclude = ['WJets', 'WWTo2L2Nu', 'TTTo2L2Nu', 'ZGToLLG']
            
        poping = []
        for i in range(len(data)):
            if data[i].name in exclude:
                poping.append(i)
                
        for i in range(len(poping)):
            data  .pop(poping[i] - i)
            legend.pop(poping[i] - i)
            colors.pop(poping[i] - i)
        
        for i in range(len(data)):
            print(i,data[i].name,colors[i])  
                
        return data,legend,colors,dataFlag
    
    ##########################
    #### Fits Section  #######
    
    # Takes "data" Data format and the name of the variable "var"
    # This name is the full name ( what traditionally might be "part+var+ph"
    # thakes the binning "binVar" that you what the distribution of "var"
    def IndicesInBin(self,data,var,binVar,absolute = False):
        binVar = self.Plot.BinFormat(Bins=binVar,Type = 'ranges')

        Ind = []
        for bins in binVar:
            if absolute:
                Ind.append(np.logical_and(np.abs(data.GetWithCuts(var)) >  bins[0],
                                          np.abs(data.GetWithCuts(var)) <= bins[1]))
            else:
                Ind.append(np.logical_and(np.array(data.GetWithCuts(var)) >  bins[0],
                                          np.array(data.GetWithCuts(var)) <= bins[1]))
        return Ind
    
    # This function extract the MVA distribution for the "data" for 
    # each pt and eta bins that are hard-coded in the function
    def FindRegionInSideband(self,
                             data,
                             part = 'photonOne',
                             var  = 'Pt',
                             ph   = '',
                             Blind         = False,
                             Plotting      = False,
                             EtaEBEERegion = True,
                            ):

        Bins,Ind = {},{}

        variable = part+var+ph

        absolute = True

        

        ##########################################################

        hist = {}

        if absolute:
            phType = ['EB','EE']
        else:
            phType = ['EE','EB','EB','EE']

        ##########################################################
        
        ranges, bins = self.GET_RangeBins(part='photonOne',var='Eta',ph='',
                                          Blind    = EtaEBEERegion, Plotting = Plotting)
        
        if type(bins) is int:
            Bins['photonOneEta'] = self.BinFormat(Bins = bins,ranges = ranges, Type='ranges')
        else:
            Bins['photonOneEta'] = self.BinFormat(Bins = bins,ranges = ranges, Type='ranges')
        Ind['photonOneEta']  = self.IndicesInBin(data,'photonOneEta',Bins['photonOneEta'],absolute = absolute)


        if (part == ' ' or part == '' ) and (var == ' ' or var == ''):
            ##########################################################

            Bins[variable] = ['']

            ##########################################################

            for eta,i in zip(Ind['photonOneEta'],range(len(Bins['photonOneEta']))):
                etai = Bins['photonOneEta'][i]
                hist[str(etai)] = {}

                MVA_HIST = data.GetWithCuts('ShowerShapeMVA_'+phType[i])
                WEI = data.GetWithCuts('weights')

                hist[str(etai)][part] = np.histogram(MVA_HIST[eta],
                                                     bins    = np.arange(-1,1.1,step=0.1),
                                                     weights = WEI[eta],
                                                    )
        else:
            ##########################################################

            ranges, bins = self.GET_RangeBins(part,var,ph,Blind    = Blind,Plotting = Plotting )

            Bins[variable] = self.BinFormat(Bins = bins,ranges = ranges, Type='ranges')
            Ind[variable]  = self.IndicesInBin(data,variable,Bins[variable])

            ##########################################################


            for eta,i in zip(Ind['photonOneEta'],range(len(Bins['photonOneEta']))):
                etai = Bins['photonOneEta'][i]
                hist[str(etai)] = {}
                MVA_HIST = data.GetWithCuts('ShowerShapeMVA_'+phType[i])
                WEI = data.GetWithCuts('weights')

                for varInd,varj in zip(Ind[variable],Bins[variable]):
                    hist[str(etai)][str(varj)] = np.histogram(MVA_HIST[np.logical_and(eta,varInd)],
                                                             bins    = np.arange(-1,1.1,step=0.1),
                                                             weights = WEI[np.logical_and(eta,varInd)],
                                                            )
        return hist,Bins
    
    
    def FindRegionInSideband_SingleEta(self,
                             data,
                             part  = 'photonOne',
                             var   = 'Pt',
                             ph    = '',
                             Blind         = False,
                             Plotting      = False,
                             EtaEBEERegion = True,
                            ):

        Bins,Ind = {},{}

        variable = part+var+ph

        absolute = True

        ##########################################################

        hist = {}

        if absolute:
            phType = ['EB','EE']
        else:
            phType = ['EE','EB','EB','EE']

        ##########################################################
        
        
        ranges, bins = self.GET_RangeBins(part='photonOne',var='Eta',ph='',
                                          Blind = EtaEBEERegion, Plotting = Plotting
                                          
                                         )
        if type(bins) is int:
            Bins['photonOneEta'] = self.BinFormat(Bins = bins,ranges = ranges, Type='ranges')
        else:
            Bins['photonOneEta'] = self.BinFormat(Bins = bins,ranges = ranges, Type='ranges')
        Ind['photonOneEta']  = self.IndicesInBin(data,'photonOneEta',Bins['photonOneEta'],absolute = absolute)


        if (part == ' ' or part == '' ) and (var == ' ' or var == ''):
            ##########################################################

            Bins[variable] = ['']

            ##########################################################

            for eta,i in zip(Ind['photonOneEta'],range(len(Bins['photonOneEta']))):
                #etai = Bins['photonOneEta'][i]
                etaS = str(Bins['photonOneEta'][i])
                if etaS == '[0, 1.4442]' and 'EE' in ph:
                    continue
                elif etaS == '[1.5666, 2.5]' and 'EB' in ph:
                    continue
                    

                MVA_HIST = data.GetWithCuts('ShowerShapeMVA_'+phType[-1])
                WEI = data.GetWithCuts('weights')

                hist[part] = np.histogram(MVA_HIST[eta],
                                                     bins    = np.arange(-1,1.1,step=0.1),
                                                     weights = WEI[eta],
                                                    )
        else:
            ##########################################################

            ranges, bins = self.GET_RangeBins(part,var,ph,Blind    = Blind,Plotting = Plotting )

            Bins[part+var] = self.BinFormat(Bins = bins,ranges = ranges, Type='ranges')
            Ind[variable]  = self.IndicesInBin(data,variable,Bins[part+var])

            ##########################################################


            for eta,i in zip(Ind['photonOneEta'],range(len(Bins['photonOneEta']))):
                etaS = str(Bins['photonOneEta'][i])
                if etaS == '[0, 1.4442]' and 'EE' in ph:
                    continue
                elif etaS == '[1.5666, 2.5]' and 'EB' in ph:
                    continue
            
        
                MVA_HIST = data.GetWithCuts('ShowerShapeMVA_'+phType[-1])
                WEI = data.GetWithCuts('weights')

                for varInd,varj in zip(Ind[variable],Bins[part+var]):
                    #print(np.sum(np.logical_and(eta,varInd)),np.sum(WEI[np.logical_and(eta,varInd)]))
                    hist[str(varj)] = np.histogram(MVA_HIST[np.logical_and(eta,varInd)],
                                                             bins    = np.arange(-1,1.1,step=0.1),
                                                             weights = WEI[np.logical_and(eta,varInd)],
                                                            )
                    #print(str(etai),str(varj),np.sum(hist[str(etai)][str(varj)][0]))
        return hist,Bins
        


# In[ ]:





# In[ ]:





# In[ ]:




