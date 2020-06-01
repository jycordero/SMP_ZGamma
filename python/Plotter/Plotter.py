
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
        for i in np.arange(len(VAR)):
            VAR[i] = VAR[i][np.logical_not(np.isnan(VAR[i]))]
        
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
        path = "/home/jcordero/CMS/SMP_ZGamma/python/Plotter/"
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
             CustomeRangeBins = None,
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

        if CustomeRangeBins is not None:
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

        print(ranges,bins)
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
                if CustomeRangeBins is not None:
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


class Helper():
    def __init__(self,era="2017",path='',minBiasCustom = ''):
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
        
        __ranges = {
                    'mlep2'     : {'':[80,100]},
                    'M'         : {
                                    'dilepton'   : [50,200],
                                    'dilepton_EE': [50,200],
                                    'dilepton_EB': [50,200],
                                    'llg'        : [50,250],
                                    'llg_EE'     : [50,250],
                                    'llg_EB'     : [50,250],
                                    'dijet'      : [50,125],
                                    'dijetgm'    : [100,140],
                                  },
                    'E'         : { 
                            'photonOne'     :[0,100],
                            'photonOne_EE'     :[0,100],
                            'photonOne_EB'     :[0,100],
                            'leptonOne'   :[0,300],
                            'leptonTwo'   :[0,300],
                            'leptonOne_EE'   :[0,300],
                            'leptonTwo_EE'   :[0,300],
                            'leptonOne_EB'   :[0,300],
                            'leptonTwo_EB'   :[0,300],
                            'jet1'   :[0,500],
                            'jet2'   :[0,300],
                            'dilepton'  :[0,800],
                            'dilepton_EE'  :[0,800],
                            'dilepton_EB'  :[0,800],
                            'llg':[0,800],
                            'llg_EE':[0,800],
                            'llg_EB':[0,800],
                            'dijet'  :[0,800],
                            'dijetgm':[0,800],
                           },
                    'Pt'        : { 
                                    'photonOne'     :[15,140],
                                    'photonOne_EE'  :[15,140],
                                    'photonOne_EB'  :[15,140],
                                    #'photonOne'     :[15,80],
                                    #'photonOne_EE'  :[15,80],
                                    #'photonOne_EB'  :[15,80],
                                    'leptonOne'     :[25,140],
                                    'leptonOne_EE'  :[25,140],
                                    'leptonOne_EB'  :[25,140],
                                    'leptonTwo'     :[20,140],
                                    'leptonTwo_EE'  :[20,140],
                                    'leptonTwo_EB'  :[20,140],
                                    'jet1'          :[0,150],
                                    'jet2'          :[0,100],
                                    'dilepton'      :[0,150],
                                    'dilepton_EE'   :[0,150],
                                    'dilepton_EB'   :[0,150],
                                    'llg'           :[0,150],
                                    'llg_EE'        :[0,150],
                                    'llg_EB'        :[0,150],
                                    'dijet'         :[0,150],
                                    'dijetgm'       :[0,150],
                                   },
                    'Eta'       : { 
                                    'photonOne'    :[-np.pi,np.pi],
                                    'photonOne_EE' :[-np.pi,np.pi],
                                    'photonOne_EB' :[-np.pi,np.pi],
                                    'leptonOne'    :[-np.pi,np.pi],
                                    'leptonOne_EE' :[-np.pi,np.pi],
                                    'leptonOne_EB' :[-np.pi,np.pi],
                                    'leptonTwo'    :[-np.pi,np.pi],
                                    'leptonTwo_EE' :[-np.pi,np.pi],
                                    'leptonTwo_EB' :[-np.pi,np.pi],
                                    'jet1'         :[-5,5],
                                    'jet2'         :[-5,5],
                                    'dilepton'     :[-5,5],
                                    'dilepton_EE'  :[-5,5],
                                    'dilepton_EB'  :[-5,5],
                                    'llg'          :[-5,5],
                                    'llg_EE'       :[-5,5],
                                    'llg_EB'       :[-5,5],
                                    'dijet'        :[-5,5],
                                    'dijetgm'      :[-5,5],
                                   },
                    'Phi'       : {
                        'photonOne'     :[-np.pi,np.pi],
                        'photonOne_EE'     :[-np.pi,np.pi],
                        'photonOne_EB'     :[-np.pi,np.pi],
                        'leptonOne'   :[-np.pi,np.pi],
                        'leptonOne_EE'   :[-np.pi,np.pi],
                        'leptonOne_EB'   :[-np.pi,np.pi],
                        'leptonTwo'   :[-np.pi,np.pi],
                        'leptonTwo_EE'   :[-np.pi,np.pi],
                        'leptonTwo_EB'   :[-np.pi,np.pi],
                        'jet1'   :[-np.pi,np.pi],
                        'jet2'   :[-np.pi,np.pi],
                        'dilepton'  :[-np.pi,np.pi],
                        'dilepton_EE'  :[-np.pi,np.pi],
                        'dilepton_EB'  :[-np.pi,np.pi],
                        'llg':[-np.pi,np.pi],
                        'llg_EE':[-np.pi,np.pi],
                        'llg_EB':[-np.pi,np.pi],
                        'dijet'  :[-np.pi,np.pi],
                        'dijetgm':[-np.pi,np.pi],
                       },
                    'DEta'      : {
                            'l1Photon'    :[0,np.pi],
                            'l2Photon'    :[0,np.pi],
                            'l1Photon_EE'    :[0,np.pi],
                            'l2Photon_EE'    :[0,np.pi],
                            'l1Photon_EB'    :[0,np.pi],
                            'l2Photon_EB'    :[0,np.pi],
                            'dilepton'     :[0,np.pi], 
                            'dilepton_EE'     :[0,np.pi], 
                            'dilepton_EB'     :[0,np.pi], 
                            'dijet'     :[0,np.pi], 
                            'j1Photon'    :[0,np.pi],
                            'j2Photon'    :[0,np.pi],
                            'Jet1Lep1'  :[0,np.pi],
                            'Jet2Lep1'  :[0,np.pi],
                            'Jet1Lep2'  :[0,np.pi],
                            'Jet2Lep2'  :[0,np.pi],
                            'dileptonPhoton'  :[0,np.pi], 
                            'dileptonPhoton_EE'  :[0,np.pi], 
                            'dileptonPhoton_EB'  :[0,np.pi], 
                            'dijet_gm'  :[0,np.pi], 
                            'dijet_lep' :[0,np.pi],
                         },
                    'DPhi'      : {
                            'l1Photon'    :[0,np.pi],
                            'l2Photon'    :[0,np.pi],
                            'l1Photon_EE'    :[0,np.pi],
                            'l2Photon_EE'    :[0,np.pi],
                            'l1Photon_EB'    :[0,np.pi],
                            'l2Photon_EB'    :[0,np.pi],
                            'dilepton'     :[0,np.pi], 
                            'dilepton_EE'     :[0,np.pi], 
                            'dilepton_EB'     :[0,np.pi], 
                            'dijet'     :[0,np.pi], 
                            'j1Photon'    :[0,np.pi],
                            'j2Photon'    :[0,np.pi],
                            'Jet1Lep1'  :[0,np.pi],
                            'Jet2Lep1'  :[0,np.pi],
                            'Jet1Lep2'  :[0,np.pi],
                            'Jet2Lep2'  :[0,np.pi],
                            'dileptonPhoton'  :[0,np.pi], 
                            'dileptonPhoton_EE'  :[0,np.pi], 
                            'dileptonPhoton_EB'  :[0,np.pi], 
                            'dijet_gm'  :[0,np.pi], 
                            'dijet_lep' :[0,np.pi],
                         },
                    'DR'        : {
                            'l1Photon'      :[0.7,4.5],
                            'l2Photon'      :[0.7,4.5],
                            'l1Photon_EE'   :[0.7,4.5],
                            'l2Photon_EE'   :[0.7,4.5],
                            'l1Photon_EB'   :[0.7,4.5],
                            'l2Photon_EB'   :[0.7,4.5],
                            'dijet'         :[0,4.5], 
                            'dilepton'      :[0,4.5], 
                            'dilepton_EE'   :[0,4.5], 
                            'dilepton_EB'   :[0,4.5], 
                            'j1Photon'    :[0,4.5],
                            'j2Photon'    :[0,4.5],
                            'Jet1Lep1'    :[0,5.5],
                            'Jet2Lep1'    :[0,6],
                            'Jet1Lep2'    :[0,5.5],
                            'Jet2Lep2'    :[0,6],
                            'dileptonPhoton'  :[0,4.5],
                            'dileptonPhoton_EE'  :[0,4.5],
                            'dileptonPhoton_EB'  :[0,4.5],
                            'dijet_gm'  :[0,4.5], 
                            'dijet_lep' :[0,4.5],
                         },
                    'nMuons'    : {'':[0,5]},
                    'nElectrons': {'':[0,5]},
                    'nPhotons'  : {'':[0,5]},
                    'nBJets'    : {'':[0,5]},
                    'nPV'       : {'':[0,100]},
                    'nPU'       : {'':[0,100]},
                    'met'       : {'':[0,100]},
                    'Sieie'     : {
                                    'photonOne':[0,0.045],
                                    'photonOne_EE':[0,0.04],
                                    'photonOne_EB':[0,0.02],
                                  },
                    'Sieip'     : {
                                    'photonOne'   :[-0.0004,0.0004],
                                    'photonOne_EE':[-0.0004,0.0004],
                                    'photonOne_EB':[-0.0001,0.0001],

                                    },
                    'Sipip'     : {
                                    'photonOne'   :[0.001,0.04],
                                    'photonOne_EE':[0.015,0.07],
                                    'photonOne_EB':[0.001,0.03],
                                    },
                    'Srr'       : {
                                    'photonOne'   :[0.01,15],
                                    'photonOne_EE':[0.01,15],
                                    'photonOne_EB':[0.01,15],
                                    },
                    'E2x2'      : {
                                    'photonOne'   :[0,200],
                                    'photonOne_EE':[0,200],
                                    'photonOne_EB':[0,200],
                                    },
                    'E5x5'      : {
                                    'photonOne'   :[0,200],
                                    'photonOne_EE':[0,200],
                                    'photonOne_EB':[0,200],
                                    },
                    'ScEtaWidth': {
                                    'photonOne'   :[0.0,0.04],
                                    'photonOne_EE':[0.0,0.04],
                                    'photonOne_EB':[0.0,0.04],
                                    },
                    'ScPhiWidth': {
                                    'photonOne'   :[0.0,0.1],
                                    'photonOne_EE':[0.0,0.1],
                                    'photonOne_EB':[0.0,0.1],
                                    },
                    'ScRawE'    : {
                                    'photonOne'   :[0.0,200],
                                    'photonOne_EE':[0.0,200],
                                    'photonOne_EB':[0.0,200],
                                    },
                    'ScBrem'    : {
                                    'photonOne'   :[0,12],
                                    'photonOne_EE':[0,12],
                                    'photonOne_EB':[0,12],
                                    },
                    'PreShowerE': {
                                    'photonOne'   :[0.01,25],
                                    'photonOne_EE':[0.01,25],
                                    'photonOne_EB':[0.01,25],
                                    },
                    'HoverE'    : {
                                    'photonOne'   :[0.001,0.1],
                                    'photonOne_EE':[0.001,0.1],
                                    'photonOne_EB':[0.001,0.1],
                                    },
                    'Ich'       : {
                                    'photonOne'   :[0.001,3],
                                    'photonOne_EE':[0.001,3],
                                    'photonOne_EB':[0.001,3],
                                    },
                    'Ineu'      : {
                                    'photonOne':[0.001,4],
                                    'photonOne_EE':[0.001,4],
                                    'photonOne_EB':[0.001,4],
                                    },
                    'Iph'       : {
                                    'photonOne'   :[0.001,5],
                                    'photonOne_EE':[0.001,5],
                                    'photonOne_EB':[0.001,5],

                                    },
                    'R9'        : {
                                    'photonOne':[0,1.1],
                                    'photonOne_EE':[0,1.1],
                                    'photonOne_EB':[0,1.1],
                                    },
                    'MVA'       : {
                                    'photonOne':[-1,1],
                                    'photonOne_EE':[-1,1],
                                    'photonOne_EB':[-1,1],
                                    },
                    'ShowerShapeMVA': {
                                    '':[-1,1],
                                    '_EE':[-1,1],
                                    '_EB':[-1,1],
                                    },
                    'eres'      : {
                                    'photonOne':[0,0.2],
                                    'photonOne_EE':[0,0.2],
                                    'photonOne_EB':[0,0.2],
                                    },            
                 }

        __bins   = {
                    'mlep2'     : {'':20},
                    'M'         : {
                                    'dilepton'    : 40,
                                    'dilepton_EE' : 40,
                                    'dilepton_EB' : 40,
                                    'llg'         : np.arange(50,250,step=2),
                                    'llg_EE'      : np.arange(50,250,step=2),
                                    'llg_EB'      : np.arange(50,250,step=2),
                                    'dijet'       : {'':15},
                                    'dijetgm'     : {'':15},
                                    },
                    'm2'        : {'':30},
                    'm3'        : {'':40},
                    'E'         : {
                                    'photonOne'     :40,
                                    'photonOne_EE'     :40,
                                    'photonOne_EB'     :40,
                                    'leptonOne'   :40,
                                    'leptonOne_EE'   :40,
                                    'leptonOne_EB'   :40,
                                    'leptonTwo'   :40,
                                    'leptonTwo_EE'   :40,
                                    'leptonTwo_EB'   :40,
                                    'jet1'   :40,
                                    'jet2'   :40,
                                    'dilepton'  :40,
                                    'dilepton_EE'  :40,
                                    'dilepton_EB'  :40,
                                    'llg':40,
                                    'llg_EE':40,
                                    'llg_EB':40,
                                    'dijet'  :40,
                                    'dijetgm':40,
                                   },                        
                    'Pt'        : {                      
                                    'photonOne'     :[15,20,25,30,35,45,55, 65,  75,  85,  95,  120,  1000],
                                    'photonOne_EE'  :[15,20,25,30,35,45,55, 65,  75,  85,  95,  120,  1000],
                                    'photonOne_EB'  :[15,20,25,30,35,45,55, 65,  75,  85,  95,  120,  1000],
                                    #'photonOne'     :[15,20,25,30,35,45,55],
                                    #'photonOne_EE'  :[15,20,25,30,35,45,55],
                                    #'photonOne_EB'  :[15,20,25,30,35,45,55],                        
                                    'leptonOne'     :40,
                                    'leptonOne_EE'  :40,
                                    'leptonOne_EB'  :40,
                                    'leptonTwo'     :40,
                                    'leptonTwo_EE'  :40,
                                    'leptonTwo_EB'  :40,
                                    'jet1'          :40,
                                    'jet2'          :40,
                                    'dilepton'      :40,
                                    'dilepton_EE'   :40,
                                    'dilepton_EB'   :40,
                                    'llg'           :40,
                                    'llg_EE'        :40,
                                    'llg_EB'        :40,
                                    'dijet'         :40,
                                    'dijetgm'       :40,
                                   },
                    'Eta'       : {
                                 'photonOne'    :30,
                                 'photonOne_EE' :30,
                                 'photonOne_EB' :30,
                                 'leptonOne'    :30,
                                 'leptonOne_EE' :30,
                                 'leptonOne_EB' :30,
                                 'leptonTwo'    :30,
                                 'leptonTwo_EE' :30,
                                 'leptonTwo_EB' :30,
                                 'jet1'         :15,
                                 'jet2'         :15,
                                 'dilepton'     :40,
                                 'dilepton_EE'  :40,
                                 'dilepton_EB'  :40,
                                 'llg'          :40,
                                 'llg_EE'       :40,
                                 'llg_EB'       :40,
                                 'dijet'        :15,
                                 'dijetgm'      :15,
                               },
                    'Phi'       : {
                                     'photonOne'    :30,
                                     'photonOne_EE' :30,
                                     'photonOne_EB' :30,
                                     'leptonOne'    :30,
                                     'leptonOne_EE' :30,
                                     'leptonOne_EB' :30,
                                     'leptonTwo'    :30,
                                     'leptonTwo_EE' :30,
                                     'leptonTwo_EB' :30,
                                     'jet1'         :30,
                                     'jet2'         :30,
                                     'dilepton'     :40,
                                     'dilepton_EE'  :40,
                                     'dilepton_EB'  :40,
                                     'llg'          :40,
                                     'llg_EE'       :40,
                                     'llg_EB'       :40,
                                     'dijet'        :15,
                                     'dijetgm'      :15,                       
                                    },
                    'DEta'      : {
                                'l1Photon'    :30,
                                'l2Photon'    :30,
                                'l1Photon_EE'    :30,
                                'l2Photon_EE'    :30,
                                'l1Photon_EB'    :30,
                                'l2Photon_EB'    :30,
                                'dijet'     :30, 
                                'dilepton'     :30, 
                                'dilepton_EE'     :30, 
                                'dilepton_EB'     :30, 
                                'j1Photon'    :30,
                                'j2Photon'    :30,
                                'j1Photon_EE'    :30,
                                'j2Photon_EE'    :30,
                                'j1Photon_EB'    :30,
                                'j2Photon_EB'    :30,
                                'Jet1Lep1'  :30,
                                'Jet2Lep1'  :30,
                                'Jet1Lep2'  :30,
                                'Jet2Lep2'  :30,
                                'dileptonPhoton'  :30, 
                                'dileptonPhoton_EE'  :30, 
                                'dileptonPhoton_EB'  :30, 
                                'dijet_gm'  :30, 
                                'dijet_lep' :30,
                           },
                    'DPhi'      : {
                                'l1Photon'    :30,
                                'l2Photon'    :30,
                                'l1Photon_EE'    :30,
                                'l2Photon_EE'    :30,
                                'l1Photon_EB'    :30,
                                'l2Photon_EB'    :30,
                                'dijet'     :30, 
                                'dilepton'     :30, 
                                'dilepton_EE'     :30, 
                                'dilepton_EB'     :30, 
                                'j1Photon'    :30,
                                'j2Photon'    :30,
                                'j1Photon_EE'    :30,
                                'j2Photon_EE'    :30,
                                'j1Photon_EB'    :30,
                                'j2Photon_EB'    :30,
                                'Jet1Lep1'  :30,
                                'Jet2Lep1'  :30,
                                'Jet1Lep2'  :30,
                                'Jet2Lep2'  :30,
                                'dileptonPhoton'  :30, 
                                'dileptonPhoton_EE'  :30, 
                                'dileptonPhoton_EB'  :30, 
                                'dijet_gm'  :30, 
                                'dijet_lep' :30,
                             },
                    'DR'        : {
                                'l1Photon'    :30,
                                'l2Photon'    :30,
                                'l1Photon_EE'    :30,
                                'l2Photon_EE'    :30,
                                'l1Photon_EB'    :30,
                                'l2Photon_EB'    :30,
                                'dijet'     :30, 
                                'dilepton'     :30, 
                                'dilepton_EE'     :30, 
                                'dilepton_EB'     :30, 
                                'j1Photon'    :30,
                                'j2Photon'    :30,
                                'j1Photon_EE'    :30,
                                'j2Photon_EE'    :30,
                                'j1Photon_EB'    :30,
                                'j2Photon_EB'    :30,
                                'Jet1Lep1'  :30,
                                'Jet2Lep1'  :30,
                                'Jet1Lep2'  :30,
                                'Jet2Lep2'  :30,
                                'dileptonPhoton'  :30, 
                                'dileptonPhoton_EE'  :30, 
                                'dileptonPhoton_EB'  :30, 
                                'dijet_gm'  :30, 
                                'dijet_lep' :30,
                             },
                    'nMuons'    : {'': 5},
                    'nElectrons': {'': 5},
                    'nPhotons'  : {'': 5},
                    'nBJets'    : {'': 5},
                    'nPV'       : {'':100},
                    'nPU'       : {'':100},
                    'met'       : {'':40},
                    'Sieie'     : {
                                'photonOne'   :50,
                                'photonOne_EE':50,
                                'photonOne_EB':50,
                                },
                    'Sieip'     : {
                                    'photonOne'   :40,
                                    'photonOne_EE':40,
                                    'photonOne_EB':40,

                                    },
                    'Sipip'     : {
                                    'photonOne'   :40,
                                    'photonOne_EE':40,
                                    'photonOne_EB':40,
                                    },
                    'Srr'       : {
                                    'photonOne'   :40,
                                    'photonOne_EE':40,
                                    'photonOne_EB':40,
                                    },
                    'E2x2'      : {
                                    'photonOne'   :40,
                                    'photonOne_EE':40,
                                    'photonOne_EB':40,
                                    },
                    'E5x5'      : {
                                    'photonOne'   :60,
                                    'photonOne_EE':60,
                                    'photonOne_EB':60,
                                    },
                    'ScEtaWidth': {
                                    'photonOne'   :40,
                                    'photonOne_EE':40,
                                    'photonOne_EB':40,
                                    },
                    'ScPhiWidth': {
                                    'photonOne'   :30,
                                    'photonOne_EE':30,
                                    'photonOne_EB':30,
                                    },
                    'ScRawE'    : {
                                    'photonOne'   :40,
                                    'photonOne_EE':40,
                                    'photonOne_EB':40,
                                    },
                    'ScBrem'    : {
                                    'photonOne'   :40,
                                    'photonOne_EE':40,
                                    'photonOne_EB':40,
                                    },
                    'PreShowerE': {
                                    'photonOne'   :40,
                                    'photonOne_EE':40,
                                    'photonOne_EB':40,
                                    },            
                    'HoverE'    : {
                                'photonOne'   :40,
                                'photonOne_EE':40,
                                'photonOne_EB':40,
                                },
                    'Ich'       : {
                                'photonOne':30,
                                'photonOne_EE':30,
                                'photonOne_EB':30,
                                },
                    'Ineu'      : {
                                'photonOne':30,
                                'photonOne_EE':30,
                                'photonOne_EB':30,
                                },
                    'Iph'       : {
                                'photonOne':30,
                                'photonOne_EE':30,
                                'photonOne_EB':30,
                                },
                    'R9'        : {
                                'photonOne'   :40,
                                'photonOne_EE':40,
                                'photonOne_EB':40,
                                },
                    'MVA'       : {
                                'photonOne'   :40,
                                'photonOne_EE':40,
                                'photonOne_EB':40,
                                },
                    'ShowerShapeMVA': {
                                    ''  :np.arange(-1,1,step=0.1),
                                    '_EE':np.arange(-1,1,step=0.1),
                                    '_EB':np.arange(-1,1,step=0.1),
                                    },            
                    'eres'      : {
                                'photonOne':30,
                                'photonOne_EE':30,
                                'photonOne_EB':30,
                                },            
                 }
        
        self.ranges  = __ranges
        self.bins    = __bins
        
        self.options = [
                    'color',
                    'linewidth',
                    'linestyle',
                    'histtype' ,
                    'bins'     ,
                    'range'    ,
                    'label'    ,
                    'normed'   ,
                    'stacked'  ,
                    ]

        self.plotOps= {}
        self.plotOps['muon_2016']       = {
                            'color'    : 'k',
                            'linewidth': 1.2,
                            'linestyle': 'o',
                            'histtype' : 'step',
                            'bins'     : self.bins,
                            'range'    : self.ranges,
                            'label'    : 'SingleMuon',
                            'normed'   : False,
                            'stacked'  : True,
                            }
        self.plotOps['DoubleMuon_2016'] = {
                            'color'    : 'k',
                            'linewidth': 1.2,
                            'linestyle': 'o',
                            'histtype' : 'step',
                            'bins'     : self.bins,
                            'range'    : self.ranges,
                            'label'    : 'DoubleMuon',
                            'normed'   : False,
                            'stacked'  : True,
                            }        
        self.plotOps['ZG_ZToLL']        = {
                            'color'    : 'magenta',
                            'linewidth': 1.2,
                            'linestyle': '-',
                            'histtype' : 'step',
                            'bins'     : self.bins,
                            'range'    : self.ranges,
                            'label'    : 'ZG_ZToLL',
                            'normed'   : False,
                            'stacked'  : False,        
                            } 
        self.plotOps['VBFHToZG_ZToJJ']  = {
                                            'color'    : 'b',
                                            'linewidth': 1.8,
                                            'linestyle': '-',
                                            'histtype' : 'step',
                                            'bins'     : self.bins,
                                            'range'    : self.ranges,
                                            'label'    : 'VBFH',
                                            'normed'   : False,
                                            'stacked'  : False,    
                                            }        
        self.plotOps['WplusH']          = {
                            'color'    : 'b',
                            'linewidth': 1.8,
                            'linestyle': '-',
                            'histtype' : 'step',
                            'bins'     : self.bins,
                            'range'    : self.ranges,
                            'label'    : 'WH',
                            'normed'   : False,
                            'stacked'  : False,    
                            }
        self.plotOps['WminusH']         = {
                            'color'    : 'b',
                            'linewidth': 1.8,
                            'linestyle': '-',
                            'histtype' : 'step',
                            'bins'     : self.bins,
                            'range'    : self.ranges,
                            'label'    : 'WH',
                            'normed'   : False,
                            'stacked'  : False,    
                            }
        self.plotOps['WH']              = {
                            'color'    : 'b',
                            'linewidth': 1.8,
                            'linestyle': '-',
                            'histtype' : 'step',
                            'bins'     : self.bins,
                            'range'    : self.ranges,
                            'label'    : 'WH',
                            'normed'   : False,
                            'stacked'  : False,    
                            }
        
        self.plotOps['TT'] = {
                            'color'    : 'magenta',
                            'linewidth': 1.2,
                            'linestyle': '-',
                            'histtype' : 'stepfilled',
                            'bins'     : self.bins,
                            'range'    : self.ranges,
                            'label'    : 'TT',
                            'normed'   : False,
                            'stacked'  : True,        
                            }
        
        self.plotOps['DYJets'] = {
                                    'color'    : 'cyan',
                                    'linewidth': 1.2,
                                    'linestyle': '-',
                                    'histtype' : 'stepfilled',
                                    'bins'     : self.bins,
                                    'range'    : self.ranges,
                                    'label'    : 'DYJets',
                                    'normed'   : False,
                                    'stacked'  : False,        
                                    }

        self.plotOps['WWTo2L2Nu']   = {
                                        'color'    : 'grey',
                                        'linewidth': 1.2,
                                        'linestyle': '-',
                                        'histtype' : 'stepfilled',
                                        'bins'     : self.bins,
                                        'range'    : self.ranges,
                                        'label'    : 'WWTo2L2Nu',
                                        'normed'   : False,
                                        'stacked'  : False,        
                                        }   
        self.plotOps['ZZTo2L2Q']    = {
                            'color'    : 'grey',
                            'linewidth': 1.2,
                            'linestyle': '-',
                            'histtype' : 'stepfilled',
                            'bins'     : self.bins,
                            'range'    : self.ranges,
                            'label'    : 'ZZTo2L2Q',
                            'normed'   : False,
                            'stacked'  : False,        
                            }    
        self.plotOps['ZZTo2L2Nu']   = {
                            'color'    : 'grey',
                            'linewidth': 1.2,
                            'linestyle': '-',
                            'histtype' : 'stepfilled',
                            'bins'     : self.bins,
                            'range'    : self.ranges,
                            'label'    : 'ZZTo2L2Nu',
                            'normed'   : False,
                            'stacked'  : False,        
                            }   
        self.plotOps['ZZTo4L']      = {
                            'color'    : 'grey',
                            'linewidth': 1.2,
                            'linestyle': '-',
                            'histtype' : 'stepfilled',
                            'bins'     : self.bins,
                            'range'    : self.ranges,
                            'label'    : 'ZZTo4L',
                            'normed'   : False,
                            'stacked'  : False,        
                            }              
        self.plotOps['WZTo1L1Nu2Q'] = {
                            'color'    : 'teal',
                            'linewidth': 1.2,
                            'linestyle': '-',
                            'histtype' : 'stepfilled',
                            'bins'     : self.bins,
                            'range'    : self.ranges,
                            'label'    : 'WZTo1L1Nu2Q',
                            'normed'   : False,
                            'stacked'  : False,        
                            }    
        self.plotOps['WZTo2L2Q']    = {
                            'color'    : 'purple',
                            'linewidth': 1.2,
                            'linestyle': '-',
                            'histtype' : 'stepfilled',
                            'bins'     : self.bins,
                            'range'    : self.ranges,
                            'label'    : 'WZTo2L2Q',
                            'normed'   : False,
                            'stacked'  : False,        
                            }  
        self.plotOps['WZTo3LNu']    = {
                            'color'    : 'purple',
                            'linewidth': 1.2,
                            'linestyle': '-',
                            'histtype' : 'stepfilled',
                            'bins'     : self.bins,
                            'range'    : self.ranges,
                            'label'    : 'WZTo3LNu',
                            'normed'   : False,
                            'stacked'  : False,        
                            }            
        self.plotOps['V V']         = {
                            'color'    : 'r',
                            'linewidth': 1.2,
                            'linestyle': '-',
                            'histtype' : 'stepfilled',
                            'bins'     : self.bins,
                            'range'    : self.ranges,
                            'label'    : 'WZTo2L2Q',
                            'normed'   : False,
                            'stacked'  : True,        
                            }         
        
        self.plotOps['W1Jets']      = {
                            'color'    : 'r',
                            'linewidth': 1.2,
                            'linestyle': '-',
                            'histtype' : 'stepfilled',
                            'bins'     : self.bins,
                            'range'    : self.ranges,
                            'label'    : 'W1Jets',
                            'normed'   : False,
                            'stacked'  : False,        
                            }
        self.plotOps['W2Jets']      = {
                            'color'    : 'g',
                            'linewidth': 1.2,
                            'linestyle': '-',
                            'histtype' : 'stepfilled',
                            'bins'     : self.bins,
                            'range'    : self.ranges,
                            'label'    : 'W2Jets',
                            'normed'   : False,
                            'stacked'  : False,        
                            }
        self.plotOps['W3Jets']      = {
                            'color'    : 'orange',
                            'linewidth': 1.2,
                            'linestyle': '-',
                            'histtype' : 'stepfilled',
                            'bins'     : self.bins,
                            'range'    : self.ranges,
                            'label'    : 'W3Jets',
                            'normed'   : False,
                            'stacked'  : False,        
                            }
        self.plotOps['W4Jets']      = {
                            'color'    : 'magenta',
                            'linewidth': 1.2,
                            'linestyle': '-',
                            'histtype' : 'stepfilled',
                            'bins'     : self.bins,
                            'range'    : self.ranges,
                            'label'    : 'W4Jets',
                            'normed'   : False,
                            'stacked'  : False,        
                            }    
        self.plotOps['W1JetsToLNu'] = {
                            'color'    : 'r',
                            'linewidth': 1.2,
                            'linestyle': '-',
                            'histtype' : 'stepfilled',
                            'bins'     : self.bins,
                            'range'    : self.ranges,
                            'label'    : 'W1JetsToLNu',
                            'normed'   : False,
                            'stacked'  : False,        
                            }
        self.plotOps['W2JetsToLNu'] = {
                            'color'    : 'g',
                            'linewidth': 1.2,
                            'linestyle': '-',
                            'histtype' : 'stepfilled',
                            'bins'     : self.bins,
                            'range'    : self.ranges,
                            'label'    : 'W2JetsToLNu',
                            'normed'   : False,
                            'stacked'  : False,        
                            }
        self.plotOps['W3JetsToLNu'] = {
                            'color'    : 'orange',
                            'linewidth': 1.2,
                            'linestyle': '-',
                            'histtype' : 'stepfilled',
                            'bins'     : self.bins,
                            'range'    : self.ranges,
                            'label'    : 'W3JetsToLNu',
                            'normed'   : False,
                            'stacked'  : False,        
                            }       
        self.plotOps['W4JetsToLNu'] = {
                            'color'    : 'magenta',
                            'linewidth': 1.2,
                            'linestyle': '-',
                            'histtype' : 'stepfilled',
                            'bins'     : self.bins,
                            'range'    : self.ranges,
                            'label'    : 'W4JetsToLNu',
                            'normed'   : False,
                            'stacked'  : False,        
                            }    
        self.plotOps['WJets']       = {
                                        #'color'    : 'teal',
                                        'color'    : 'limegreen',
                                        'linewidth': 1.2,
                                        'linestyle': '-',
                                        'histtype' : 'stepfilled',
                                        'bins'     : self.bins,
                                        'range'    : self.ranges,
                                        'label'    : 'W+Jets',
                                        'normed'   : False,
                                        'stacked'  : True,        
                                        }    
  
        self.plotOps['W3JetsToLNu'] = {
                                    'color'    : 'orange',
                                    'linewidth': 1.2,
                                    'linestyle': '-',
                                    'histtype' : 'stepfilled',
                                    'bins'     : self.bins,
                                    'range'    : self.ranges,
                                    'label'    : 'W3JetsToLNu',
                                    'normed'   : False,
                                    'stacked'  : False,        
                                    } 

        self.plotOpsAll = [
                            self.plotOps['TT'], 
                            self.plotOps['DYJets'],
                            self.plotOps['WWTo2L2Nu'],
                            self.plotOps['ZZTo2L2Nu'],
                            self.plotOps['ZZTo2L2Q'],
                            self.plotOps['ZZTo4L'],
                            self.plotOps['WZTo2L2Q'],
                            self.plotOps['WZTo3LNu'],
                            self.plotOps['ZG_ZToLL'],
                            self.plotOps['DoubleMuon_2016'],
                          ]    
    
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
            
        file = TFile('/home/jcordero/CMS/data/data_'+era+'/'+DataGen+'/SMP_ZG/Files/'+pileupFile)
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

    ######################
    def ConvertString2Float(self,
                           varS):
        if varS == '' or varS == ' ':
            convert = False
        elif type(varS) is int or type(varS) is float or type(varS) is np.float64 or type(varS) is np.int64:
            convert = varS
        else:
            if '[' in varS:
                convert = [float(v) for v in varS.replace('[ ','').replace('[','').replace(']','').replace(' ]','').replace(',','').replace('  ',' ').split(' ')]
            elif type(varS) is list:
                convert = varS
                
            else:
                convert = float(varS)
        return convert        
    
    def BinFormat(self,Bins,ranges = None,Type='ranges', Print=False):
        bins = []
        if Bins == []:
            return Bins
        
        if type(Bins) is int or type(Bins) is float or type(Bins) is np.int64 or type(Bins) is np.float64:
            if Print:
                print('Enter the Int bins category')
            
            try:
                step = (ranges[1]-ranges[0])/Bins
                if step*Bins+ranges[0] != ranges[1] and Print:
                    print('Last bin will be omited')
            except:
                if Print:
                    print('Please provide a range')

            Bins = int(Bins)
            if Type=='ranges':    
                for i in np.arange(Bins):
                    bins.append([i*step+ranges[0],(i+1)*step+ranges[0]])
            elif Type == 'edges':
                for i in range(Bins+1):
                    bins.append(i*step+ranges[0])
        
            elif Type == 'center':
                bins = np.array(self.BinFormat(Bins = Bins,Type='edges'))
                bins = (bins[:-1]+bins[1:])/2
        else:
            if Print:
                print('Enter the List bins category')
            if Type == 'ranges':
                if type(Bins[0]) is np.ndarray or type(Bins[0]) is list:
                    bins = Bins
                else:
                    for i in np.arange(len(Bins)-1):
                        bins.append([Bins[i],Bins[i+1]])
            elif Type == 'edges':
                if type(Bins[0]) is int or type(Bins[0]) is float or type(Bins[0]) is np.int64:
                    bins = Bins
                else:
                    for b in Bins:
                        bins.append(b[0])
                    bins.append(Bins[-1][1])
                bins = array.array("f",bins)
            elif Type == 'center':
                bins = np.array(self.BinFormat(Bins = Bins,Type='edges'))
                bins = (bins[:-1]+bins[1:])/2

        return bins

    def GET_WeiVAR(self,
                   data,
                   part,
                   var,
                   ph,
                   weightCorrection = False,
                   Print            = False
                  ):    
        
        ###################################
        
        if weightCorrection:
            if Print:
                print('Enter Weight Correction')
            reWeight = [d.GetWithCuts('puWeight')*d.GetWithCuts('weight') for d in data]
            # MODIFICATIONS

            #wei = [np.array(reWeight[i][data[i].cuts])/(np.array(data[i].df.photonIDWeight)[data[i].cuts]) for i in range(len(data[:-1]))]
            #wei.append(data[-1].GetWithCuts('weight')//(np.array(data[-1].df.photonIDWeight)[data[-1].cuts]))

            #wei = [np.array(reWeight[i][data[i].cuts])*(np.array(data[i].df.photonIDWeight)[data[i].cuts]) for i in range(len(data[:-1]))]
            #wei.append(data[-1].GetWithCuts('weight'))

            #wei = [np.array(reWeight[i][data[i].cuts]) for i in range(len(data[:-1]))]
            #wei.append(data[-1].GetWithCuts('weight'))

            ######################
            ### Eliminate IDWeight and isConv
            #wei = [np.array(reWeight[i][data[i].cuts])/(np.array(data[i].df.photonIDWeight)[data[i].cuts]) for i in range(len(data[:-1]))]
            #wei.append(data[-1].GetWithCuts('weight')//(np.array(data[-1].df.photonIDWeight)[data[-1].cuts]))

            ######################
            ### Eliminate IDWeight and isConv
            #wei = [np.array(reWeight[i][data[i].cuts])/(np.array(data[i].df.photonIDWeight)[data[i].cuts]*np.array(data[i].df.photonIsConvWeight)[data[i].cuts]) for i in range(len(data[:-1]))]
            #wei.append(data[-1].GetWithCuts('weight')//((np.array(data[-1].df.photonIDWeight)*np.array(data[-1].df.photonIsConvWeight))[data[-1].cuts]))

            ######################
            ### ONLY isConv Added 
            #wei = [np.array(reWeight[i][data[i].cuts])*np.array(data[i].df.photonIsConvWeight)[data[i].cuts] for i in range(len(data[:-1]))]
            #wei.append(data[-1].GetWithCuts('weight'))
            
            ######################
            ### Nothing Added
            #wei = [np.array(reWeight[i][data[i].cuts]) for i in range(len(data[:-1]))]
            wei = [np.array(reWeight[i]) for i in range(len(data[:-1]))]
            wei.append(data[-1].GetWithCuts('weight'))
        else:
            if Print:
                print('Weights are not corrected')
            # ORIGINAL
            wei = [d.GetWithCuts('weight') for d in data]

        ###################################
        
        VAR = [d.GetWithCuts(part+var+ph) for d in data]        

        ###################################
        
        return wei,VAR
    
    def GET_RangeBins(self,
                      part,
                      var,
                      ph,
                      Blind    = True,
                      Plotting = True, 
                      File     = True,
                      ):
        #####################################
        if not File:
            if   var == 'nJets':
                ranges = [0,7]
                bins   = 7
            elif var == 'Pt':
                if not Blind:
                    if part == 'photonOne' and Plotting:
                        ranges = self.plotOpsAll[0]['range'][var][part+ph]
                        bins   = self.plotOpsAll[0]['bins'][var][part+ph][:-1]
                    else:
                        ranges = self.plotOpsAll[0]['range'][var][part+ph]
                        bins   = self.plotOpsAll[0]['bins'][var][part+ph]
                elif part == 'photonOne':       
                    ranges = [20,1000]
                    bins = [20,22,25,27,29,32,35,40,45,50,55,60,65,70,75,80,85,90,95,105,120,200,1000]
                else:
                    ranges = self.plotOpsAll[0]['range'][var][part+ph]
                    bins   = self.plotOpsAll[0]['bins'][var][part+ph]
            elif var == 'Eta':
                ranges = [-2.5, 2.5]
                #bins   = [-2.5,-1.5666,1.4442,0,1.4442,1.5666,2.5]     
                bins   = [0,1.4442,1.5666,2.5]     
            elif var == 'M':
                if not Blind:
                    if part == 'llg' and Plotting:
                        ranges = self.plotOpsAll[0]['range'][var][part+ph]
                        bins   = self.plotOpsAll[0]['bins'][var][part+ph][:-1]
                    else:
                        ranges = self.plotOpsAll[0]['range'][var][part+ph]
                        bins   = self.plotOpsAll[0]['bins'][var][part+ph]
                elif part == 'llg' :
                    ranges = [50,135]
                    bins   = [50,  85,  95,  110,  135,  170,  210,  270]            
                else:
                    ranges = self.plotOpsAll[0]['range'][var][part+ph]
                    bins   = self.plotOpsAll[0]['bins'][var][part+ph]
            else:
                ranges = self.plotOpsAll[0]['range'][var][part+ph]
                bins   = self.plotOpsAll[0]['bins'][var][part+ph]
        else:
            path = "/home/jcordero/CMS/SMP_ZGamma/python/Plotter/"
            Range = pd.read_csv(path+"ranges.csv")
            Bins  = pd.read_csv(path+"bins.csv")
            
            if part == '':
                part = ' '
            if ph == ' ':
                ph = ''
            ranges = Range[var][Range['part'] == part+ph].values[0]
            bins   = Bins[var][Bins['part'] == part+ph].values[0]
            
            ranges = self.ConvertString2Float(ranges)
            bins   = self.ConvertString2Float(bins)
            
            bins = np.array(self.BinFormat(Bins=bins,ranges=ranges,Type='edges'))
            
            if Blind or Plotting:
                if var == 'Pt':
                    if part == 'photonOne':
                        
                        bins = bins[bins<150]
                        '''
                        if type(bins) is list or type(bins) is np.ndarray:
                            bins = np.array(bins)
                            bins = bins[bins<150]
                        else:
                            ranges = [ranges[0],150]
                        '''
                elif var == 'Eta':
                    if part == 'photonOne':
                        ranges = [-2.5, 2.5]
                        #bins   = [-2.5,-1.5666,1.4442,0,1.4442,1.5666,2.5]     
                        #bins   = [0,1.4442,1.5666,2.5]     
                        bins   = [[0,1.4442],[1.5666,2.5]]
                
            ranges = list(ranges)
            if type(bins) is np.ndarray:
                bins   = list(bins)
                
            if not (type(bins) is list or type(bins) is np.ndarray):
                bins = int(bins)
                
                        
        ##########################

        return ranges,bins

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
        binVar = self.BinFormat(Bins=binVar,Type = 'ranges')

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
        
    
    #############################
    ### Math and Stats ###########
    
    def gauss(self,x,*a):
        return a[0]*np.exp(-(x-a[1])**2/(2*a[2]**2)) + a[3]
    def crystal_ball(self,x,*params):
        x = x+0j 
        N, a, n, xb, sig = params
        if a < 0:
            a = -a
        if n < 0:
            n = -n
        aa = abs(a)
        A = (n/aa)**n * np.exp(- aa**2 / 2)
        B = n/aa - aa
        total = 0.*x
        total += ((x-xb)/sig  > -a) * N * np.exp(- (x-xb)**2/(2.*sig**2))
        total += ((x-xb)/sig <= -a) * N * A * (B - (x-xb)/sig)**(-n)
        try:
            return total.real
        except:
            return totat
        return total
    def CHI2(self,Exp,Obs):
        if np.sum(Exp) == 0:
            return np.sum((Exp-Obs)**2/np.sqrt(Exp))
        else:
            return np.sum((Exp-Obs)**2)
    def GetCDF(self,dist):
        return np.cumsum(dist/np.sum(dist))
    def Sampling(self,dist,N):
        indices = []

        CDF = self.GetCDF(dist[0])

        for samp in np.random.rand(N):
            indices.append(np.sum(CDF < samp))
        hist = np.histogram(dist[1][indices],bins=np.arange(-1,1.1,step=0.1))
        return np.array(hist[0])


# In[ ]:


import numpy as np
import pandas as pd

import matplotlib as mpl
import matplotlib.pyplot as plt

from Plotter.Helper import Helper
import Samples

