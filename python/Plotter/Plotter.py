#!/usr/bin/env python
# coding: utf-8

# In[4]:


class Plotter(object):
    def __init__(self,Help,stacked=True,Bkg= [],Sig=[],Data=[]):
        
        self.Test = Samples.Data.Data()
        self.Test.df['test']   = np.random.random(200)
        self.Test.weight = np.ones(200)
        self.Test.cuts   = np.ones(200,dtype=np.bool)
        self.SetPlotOpt(colors = ['r','b','k'],legend = ['signal','bkg','data'])
        
        #---------------
        # Global parameters
        self.PlotSettings(Default=True)
        
        #---------------
        # Local Parameters
        if stacked:
            self.folder = 'Stacked'
            self.histtype = 'stepfilled'
            self.density = False
            self.linewidth = 1
        else:
            self.folder = 'Unstaked'
            self.histtype = 'step'
            self.density = False
            self.linewidth = 1.7
            
        self.Help = Help
        self.figpath = ''

    #######################################
    def SetPlotOpt(self,
                   colors,
                   legend,
                  ):
        self.legend = legend
        self.colors = colors
        
    def SetPath(self,stacked = True):
        self.folder   = folder        
    def SetFig(self,figpath):
        self.figpath = figpath
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
        
        ranges,bins = self.Help.GET_RangeBins(part,var,ph, Blind=Blind,Plotting=Plotting)
    
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
        path = "/home/jcordero/CMS/JYCMCMS/SMP_ZG/python/Plotter/"
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
                

    def LabeledYields(self,data,part,var,ph,wei,ranges,bins):
        
        # Note that the yield using the "GetWithCuts" inat this point will give 
        # you the Yield, without considering the puWeights. On the otherhand if you sum 
        # the "wei" variable you  will get the correction, regardless one thing to keep 
        # in mind is that it doesn't account for the events excluded when chossing a range to graph
        Yield = []
        for i in range(len(data)):
            if type(bins) is int or type(bins) is float or type(bins) is np.int64 or type(bins) is np.float64:
                Yield.append(np.sum(wei[i][np.array(data[i].GetWithCuts(part+var+ph)) < ranges[-1] ]))
            else:
                Yield.append(np.sum(wei[i][np.array(data[i].GetWithCuts(part+var+ph)) < bins[-1] ]))
        label = [self.legend[i] + ' Yield '+ str(int(Yield[i])) for i in np.arange(len(data))]
        
        return label
    
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

            ranges,bins = self.Help.GET_RangeBins(p,v,ph, Blind=False,Plotting=Plotting)
            wei, VAR    = self.Help.GET_WeiVAR(data, p,v,ph, 
                                               weightCorrection = weightCorrection,
                                              )
            label = self.LabeledYields(data,part=p,var=v,ph=ph,wei=wei,ranges=ranges,bins=bins)

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
                            color     = self.colors[:-N],
                            weights   = wei[:-N],
                            label     = label,
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
                                    histtype  = Help.plotOpsAll[-N]['histtype'],
                                    stacked   = Help.plotOpsAll[-N]['stacked'],
                                    color     = self.colors[-N],
                                    weights   = wei[-N],
                                    label     = label[-N] + "x"+str(mag),
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
                ranges,bins = self.Help.GET_RangeBins(p,v,ph,Blind=Blind,Plotting=Plotting)

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
             data,
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

        if len(CustomeRangeBins) > 0:
            ranges,bins = CustomeRangeBins['ranges'], CustomeRangeBins['bins']
        else:
            ranges,bins = self.Help.GET_RangeBins(part,var,ph, Blind=False,Plotting=Plotting)
            
        wei , VAR  = self.Help.GET_WeiVAR   (data,part,var,ph, 
                                              weightCorrection = weightCorrection ,
                                             )
        label = self.LabeledYields(data,part=part,var=var,ph=ph,wei=wei,ranges=ranges,bins=bins)
        
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
                        histtype  = self.histtype,
                        stacked   = stacked,
                        weights   = wei[:-N],
                        label     = label[:-N],
                        color     = self.colors[:-N],
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
                                    histtype  = self.histtype,
                                    stacked   = stacked,
                                    label     = label[-N]+" x"+str(mag),
                                    color     = self.colors[-N],
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
                    ranges,bins = self.Help.GET_RangeBins(part,var,ph,Blind=Blind,Plotting=Plotting)
                
                x3,y3,x3b,xlim = self.PlotData(ax,VAR[-1],ranges,bins,log)

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
                    color     = self.colors[-1],
                    marker    ='o',
                    linestyle ='',
                    label     = self.legend[-1]
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
                
                # Blind the data Plot
                #ranges,bins = self.Help.GET_RangeBins(part,var,ph,Blind=Blind,Plotting=Plotting)
                
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
                 log = False,
                 ):


        y3,x3 = data, bins
        
        x3b = (x3[1:len(x3)] + x3[0:-1])/2
        ax.errorbar(x3b,
                    y3,
                    xerr      = np.diff(x3)/2,yerr = np.sqrt(y3),
                    color     = self.colors[-1],
                    marker    ='o',
                    linestyle ='',
                    label     = self.legend[-1]
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
        
        bins = self.Help.BinFormat(Bins=bins,ranges=ranges,Type='ranges')

        DataMC    = rDataMC[:len(Data[0])]
        errDataMC = Data[1]/h*np.sqrt(1/Data[1]+1/h)
        ax.errorbar(
                    Data[0], DataMC,
                    xerr      = np.diff(bins)/2,
                    yerr      = errDataMC,
                    color     = self.colors[-1],
                    marker    = 'o',
                    linestyle = '',
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





# In[ ]:





# In[ ]:


import numpy as np
import pandas as pd

import matplotlib as mpl
import matplotlib.pyplot as plt

from Plotter.Helper import Helper
import Samples


# In[ ]:





# In[ ]:




