
# coding: utf-8

# In[ ]:


from Common.CommonHelper import CommonHelper


# In[ ]:


class ConfigHist:
    confpath="/home/jcordero/CMS/SMP_ZGamma/json/plot/"
    
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

