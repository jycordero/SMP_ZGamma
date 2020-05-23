#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import sys


# In[ ]:


from Common.CommonHelper import CommonHelper


# In[ ]:


class Config:
    def __init__(self, path, era, DataGen, selection, run, LoadVars = []):
        self.confdir = "/home/jcordero/CMS/SMP_ZGamma/conf/config"
        #self.confdir = "../conf/config"
        self.projectdir = self.__getProjectDir()
        self.path = path 
        self.era  = era
        self.run  = run
        self.selection = selection
        self.LoadVars  = LoadVars
        self.DataGen   = DataGen

        self.date = self.__setDate()
        self.figpath = self.projectdir+"figs/"+era+"/"+DataGen+"/"+selection+"/"
        self.jsondir = self.projectdir+"json/"
        
        self.dirStructure()
        
    def __repr__(self):
        space = len(Config.__name__)
        spacer = " "*space
        msg = "{}(path={},\n".format(Config.__name__,self.path)
        msg += spacer+"era={},\n".format(self.era)
        msg += spacer+"DataGen={},\n".format(self.era) 
        msg += spacer+"selection={},\n".format(self.selection) 
        msg += spacer+"run={},\n".format(self.run) 
        msg += spacer+"LoadVars={}\n".format(self.LoadVars) 
        msg += spacer+")\n"
        msg += spacer+"--> projectdir: {} (extracted from {})\n".format(self.projectdir, self.confdir)
        msg += spacer+"--> date: {}\n".format(self.date)
        msg += spacer+"--> figpath: {}\n".format(self.figpath)
        msg += spacer+"--> jsondir: {}\n".format(self.jsondir)
        
        return msg
    
    def __del__(self):
        del self.projectdir
        del self.path 
        del self.era  
        del self.run  
        del self.selection
        del self.LoadVars 
        del self.DataGen  
        del self.date
        del self.figpath 
        del self.jsondir 
    
    def __getProjectDir(self):
        with open(self.confdir) as f:
            projectdir = f.read()
        return projectdir.split('\n')[0]
    
    def __setDate(self):
        import datetime
        date = datetime.datetime.now()
        return str(date.year) + str(date.month) + str(date.day) + "/"
    
    def _setProjectDir(self, projectdir):
        self.projectdir = projectdir
    
    def _setPath(self, path):
        self.path = path
        
    def _setEra(self, era):
        self.era = era
        
    def _setDataGen(self, DataGen):
        self.DataGen = DataGen
        
    def _setSelection(self, selection):
        self.selection = selection
        
    def _setRun(self, sun):
        self.run = run
    
    def _setLoadVars(self, LoadVars):
        self.LoadVars = LoadVars
    
    def _set(self,var,value):
        setattr(self,var,value)    
        
    def CreateDir(self,figpath,fileName='',sufix='', Print = False):
        try:
            os.mkdir(figpath+fileName+sufix) 
        except:
            if Print:
                print("Directory "+fileName+sufix+ " already exist")
    
    def dirStructure(self,Print = False):
        path = self.figpath + self.date
        
        self.CreateDir(path)
        self.CreateDir(path,sufix = 'ShowerShapeMVA/')
        

        self.dirSubStructure(path +   "Stacked/", Print=Print)
        self.dirSubStructure(path + "Unstacked/", Print=Print)
        self.dirSubStructure(path +     "nJets/", Print=Print)
        for i in range(5):
            self.dirSubStructure(path + "nJets/Stacked_nJets"+str(i)+"/", Print=Print)
            self.dirSubStructure(path + "nJets/Unstacked_nJets"+str(i)+"/", Print=Print)


    def dirSubStructure(self, path,Print = False):
        self.CreateDir(path, Print=Print)
        self.CreateDir(path+"log",Print=Print)
        self.CreateDir(path+"log/Mult", Print=Print)
        self.CreateDir(path+"linear", Print=Print)
        self.CreateDir(path+"linear/Mult", Print=Print)

