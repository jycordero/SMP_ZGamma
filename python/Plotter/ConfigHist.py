#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from Common.CommonHelper import CommonHelper


# In[ ]:


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

