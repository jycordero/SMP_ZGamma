#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from Common.CommonHelper import CommonHelper


# In[1]:


class ConfigHist:
    confpath="/home/jcordero/CMS/SMP_ZGamma/json/plot/"
    
    def getProperties(self,name=""):
        prop = {}
        prop['color']    = self.getColor(name) 
        prop['label']    = self.getLabel(name)
        prop['histtype'] = self.getHisttpe(name)
        return prop    
    
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
    
    def Var2PlotDict(self,part,var,ph):
        VarDict = []
        dirstruc = {}
        for p in part:
            for v in var:
                for gm in ph:
                    VarDict.append({
                                    "part":p,
                                    "var":v,
                                    "ph":gm
                                    })

        return VarDict
    
    def Var2Plot(self):
        PartVar = []
        VarDict = []

        parts = ["photonOne","leptonOne","leptonTwo","dilepton","llg"]
        var = ["Pt"]
        ph = [""]
        #ph = ["","_EE","_EB"]
        PartVar += [p+v+gm for p in parts for v in var for gm in ph]
        VarDict += self.Var2PlotDict(parts,var,ph)    

        parts = ["dilepton","llg"]
        var = ["M"]
        ph = [""]
        #ph = ["","_EE","_EB"]
        PartVar += [p+v+gm for p in parts for v in var for gm in ph]
        VarDict += self.Var2PlotDict(parts,var,ph)    

        parts = ["photonOne","leptonOne","leptonTwo"]
        var = ["Eta","Phi"]
        ph = [""]
        #ph = ["","_EE","_EB"]
        PartVar += [p+v+gm for p in parts for v in var for gm in ph]
        VarDict += self.Var2PlotDict(parts,var,ph)    

        parts = ["dilepton","dileptonPhoton","l1Photon","l2Photon"]
        var = ["DR","DEta","DPhi"]
        ph = [""]
        PartVar += [p+v+gm for p in parts for v in var for gm in ph]
        VarDict += self.Var2PlotDict(parts,var,ph)

        return PartVar,VarDict


# In[ ]:




