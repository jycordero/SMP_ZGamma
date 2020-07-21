#!/usr/bin/env python
# coding: utf-8

# In[43]:


from Common.CommonHelper import CommonHelper


# In[81]:


class ConfigHist:
    confpath="/home/jcordero/CMS/SMP_ZGamma/json/plot/"
    
    '''
    Depricated Parent class should implement this function if needed
    def getProperties(self,name=""):
        prop = {}
        prop['color']    = self.getColor(name) 
        prop['label']    = self.getLabel(name)
        prop['histtype'] = self.getHisttpe(name)
        return prop    
    '''
    
    def getMarket(self,name):
        return CommonHelper.Read.openJson(self.confpath+"plot_conf.json")[name]['plot']['marker']
    
    def getHisttpe(self,name):
        return CommonHelper.Read.openJson(self.confpath+"plot_conf.json")[name]['hist']['histtype']
    
    def getLabel(self,name):
        return CommonHelper.Read.openJson(self.confpath+"plot_conf.json")[name]['label']
        
    def getLinewidth(self,name):
        return CommonHelper.Read.openJson(self.confpath+"plot_conf.json")[name]['plot']["linewidth"]
    
    def getColor(self,name):
        return CommonHelper.Read.openJson(self.confpath+"plot_conf.json")[name]["color"]
    
    def Var2PlotDict(self,part,var,ph,extra=None):
        VarDict = []
        dirstruc = {}
        if extra is None:
            extra = [""]
            
        for p in part:
            for v in var:
                for gm in ph:
                    for ext in extra:
                        VarDict.append({
                                        "part":p,
                                        "var":v,
                                        "ph":gm,
                                        "extra":ext,
                                        })

        return VarDict
    
    def Var2Plot(self,BinType=None):
        PartVar = []
        VarDict = []

        '''
        parts = [" "]
        var = ["eventWeight","nPV"]
        ph = [""]
        #ph = ["","_EE","_EB"]
        PartVar += [p+v+gm for p in parts for v in var for gm in ph]
        VarDict += self.Var2PlotDict(parts,var,ph)    
        '''
        if BinType == 'ee':
            parts = ["photonOne","leptonOne","leptonTwo","dilepton"]
        else:
            parts = ["photonOne","leptonOne","leptonTwo","dilepton","llg"]
        var = ["Pt"]
        #ph = [""]
        ph = ["","_EE","_EB"]
        PartVar += [p+v+gm for p in parts for v in var for gm in ph]
        VarDict += self.Var2PlotDict(parts,var,ph)    

        if BinType == 'ee':
            parts = ["dilepton"]
        else:
            parts = ["dilepton","llg"]
        var = ["M"]
        #ph = [""]
        ph = ["","_EE","_EB"]
        PartVar += [p+v+gm for p in parts for v in var for gm in ph]
        VarDict += self.Var2PlotDict(parts,var,ph)    

        parts = ["photonOne","leptonOne","leptonTwo"]
        var = ["Eta","Phi"]
        #ph = [""]
        ph = ["","_EE","_EB"]
        PartVar += [p+v+gm for p in parts for v in var for gm in ph]
        VarDict += self.Var2PlotDict(parts,var,ph)    

        if BinType == 'ee':
            parts = ["dilepton"]
        else:
            parts = ["dilepton","dileptonPhoton","l1Photon","l2Photon"]
        var = ["DR","DEta","DPhi"]
        #ph = [""]
        ph = ["","_EE","_EB"]
        PartVar += [p+v+gm for p in parts for v in var for gm in ph]
        VarDict += self.Var2PlotDict(parts,var,ph)

        return PartVar,VarDict
    
    
    def Var2Plot_Eff(self,BinType='Optimized'):
        PartVar = []
        VarDict = []
        
        parts = ["dilepton"]
        var = ["M"]
        ph = [""]
        
        pt,eta = self.getGridBinning(BinType)
        extra = []
        
        for eff in ["_Pass","_Fail"]:
            for ipt in pt:
                for ieta in eta:
                    extra.append(eff+"_pt_"+str(ipt[0])+'_'+str(ipt[1])+"_eta_"+str(ieta[0])+"_"+str(ieta[1]))
                
        PartVar += [p+v+gm for p in parts for v in var for gm in ph]
        VarDict += self.Var2PlotDict(parts,var,ph,extra) 

        return PartVar,VarDict
    
    def getGridBinning(self,BinType):
        pt = CommonHelper.Read.openJson(self.confpath+'eff_bins.json')[BinType]['pt']
        eta = CommonHelper.Read.openJson(self.confpath+'eff_bins.json')[BinType]['etaAbs']
        
        pt = CommonHelper.Plot.BinFormat(pt,Type='ranges')
        eta = CommonHelper.Plot.BinFormat(eta,Type='ranges')
        
        gap = [[1.4442, 1.566],[-1.566, -1.4442]]
        
        if gap[0] in eta:
            eta.remove(gap[0])
        if gap[1] in eta:
            eta.remove(gap[1])
        
        return pt, eta
        


# In[82]:


if __name__ == "__main__":
    C = ConfigHist()
    confpath="/home/jcordero/CMS/SMP_ZGamma/json/plot/"
    BinType="Optimized"
    #print(CommonHelper.Read.openJson(confpath+'eff_bins.json')[BinType]['pt'])
    pt,eta = C.getGridBinning(BinType="Optimized")
    
    
    print(pt,eta)

