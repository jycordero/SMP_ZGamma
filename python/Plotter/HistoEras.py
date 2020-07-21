#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os 
import matplotlib.pyplot as plt
from Common.StackList import StackList


# In[4]:


class HistoEras( StackList ):
    def __init__(self,stack=None, name=None,Print=False):
        StackList.__init__(self,name=name,stack=stack,Print=Print)    
    
    def append(self,stack,name=None):
        if name is None and stack.name is None:
            raise "Name is not specified, provide argument \"name\" or set is in Histo"
            
        if name is None:
            name = stack.name
        else:
            stack.name = name

        super().append(stack,stack.name)
          
    
    def savefig(self,fig,fullpath):
        fig.savefig(fullpath)

    def _savefigjoin(self,fullpath,ind):    
        pass
    def _savefigind(self,fullpath,ind):
        for era in self.names:
            self[era].savefigs(fullpath, ind=ind)
    def _savefigmult(self,fullpath,ind,WithYield):
        for var in self[0][0].names:
            for log in [True,False]:
                LOG = "log" if log else "linear"
                fig = plt.figure()
                self.plotmult(variable=var,ind=ind,WithYield=WithYield,log=log)
                self.savefig(fig,os.path.join(fullpath,LOG,"single",var) )

    
    def savefigs(self,fullpath,Type,WithYield=False,ind=None):
        if   Type == "ind":
            self._savefigind(fullpath=fullpath,ind=ind)
        elif Type == "mult":
            self._savefigmult(fullpath=fullpath,ind=ind,WithYield=WithYield)
        elif Type == "join":
            self._savefigjoin(fullpath=fullpath,ind=ind)
    
        
    def plotind(self,variable,era,ind,WithYield,log):
        self[era].plot(variable=variable,ind=ind,log=log,WithYield=WithYield)
    
    def plotmult(self,variable,ind,WithYield,log):
        Runs = self.names
        FIG = plt.figure(figsize=(11*len(Runs),10))
        for i, era in enumerate(Runs):
            fig, ax = self[era].plot( variable=variable,log=log,
                                      ind = ind,
                                      shape=(4,len(Runs)),loc = i,
                                      WithYield = WithYield,
                                      Create = False,
                                    )
        return FIG
    
    def plotjoin(self,variable):
        pass
    
    def plot(self,variable,log=True,era=None,ind=None,WithYield=False,Type='ind'):
        if   Type == 'ind':
            self.plotind(variable=variable,era=era,ind=ind,WithYield=WithYield,log=log)
        elif Type == 'mult':
            self.plotmult(variable=variable,ind=ind,WithYield=WithYield,log=log)
        elif Type == 'join':
            self.plotjoin(variable=variable,log=log)
        
        
    def plots(self,variables,log=True,era=None,ind=None,WithYield=False,Type='ind'):
        if Type == 'mult':
            fig = self.plotmult(variable=variable,ind=ind,WithYield=WithYield,log=log)
        elif Type == 'join':
            self.plotjoin(variable=variable,log=log)


# In[ ]:




