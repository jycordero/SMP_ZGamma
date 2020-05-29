
# coding: utf-8

# In[ ]:


import json


# In[ ]:


class ConfigPlot():
    def __init__(self, projectdir, name):
        self.projectdir = projectdir
        self.name = name
        
        self.setConfigVars( self.getConfigFile() )

    def getConfigFile(self):
        #self.projectdir + "conf/confPlot.txt"
        file = self.projectdir + "json/plot/plot_conf.json"
        with open(file, 'r') as f:
            JS = f.read()
        
        config = json.loads(JS)
        
        return config
        
    def setConfigVars(self,config):
        conf = config[self.name]
        
        for var in conf.keys():
            setattr(self,var, conf[var])

