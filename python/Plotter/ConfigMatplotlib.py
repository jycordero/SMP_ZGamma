
# coding: utf-8

# In[1]:


from Common.CommonHelper import CommonHelper


# In[2]:


class ConfigMatplotlib:
    confpath = "/home/jcordero/CMS/SMP_ZGamma/json/plot/"
    file = "plot_params.json"
    
    def setRC(self,rc,rcDict = None,Type = "Single"):
        if rcDict is None:
            rcDict = self.getRC(Type=Type)
        
        for key in rcDict:
            rc(key, **rcDict[key])

    def getRC(self,Type = "Single"):
        return CommonHelper.Read.openJson(self.confpath+self.file)[Type]
            
    def getAxesLabelSize(self,Type="Single"):
        return CommonHelper.Read.openJson(self.confpath+self.file)[Type]['axes']['labelsize']
    
    def getAxesTitleSize(self,Type="Single"):
        return CommonHelper.Read.openJson(self.confpath+self.file)[Type]['axes']['titlesize'] 
    
    def getAxesGrid(self,Type="Single"):
        return CommonHelper.Read.openJson(self.confpath+self.file)[Type]['axes']['grid.linestyle']
    
    def getYtickLabelSize(self,Type="Single"):
        return CommonHelper.Read.openJson(self.confpath+self.file)[Type]['ytick']['labelsize']  
                    
    def getXtickLabelSize(self,Type="Single"):
        return CommonHelper.Read.openJson(self.confpath+self.file)[Type]['xtick']['labelsize']  
                    
    def getLegendFontSize(self,Type="Single"):
        return CommonHelper.Read.openJson(self.confpath+self.file)[Type]['legend']['fontsize']
        


# In[32]:


if __name__ == "__main__":
    Config = ConfigMatplotlib()
    Config.confpath+Config.file
    Config.getRC()

