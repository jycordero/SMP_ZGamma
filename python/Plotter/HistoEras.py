
# coding: utf-8

# In[1]:


from Common.StackList import StackList


# In[2]:


class HistoEras( StackList ):
    def __init__(self,stack=None, name=None):
        StackList.__init__(self,stack)
        if name is None:            
            self.name     = None
        else:
            if type(name) is list:
                self.name     = name
            else:
                self.name     = [ name ]
    
    def append(self,stack,name=None):
        if name is None and stack.name is None:
            raise "Name is not specified, provide argument \"name\" or set is in Histo"
            
        self.__addVariable(name)
        self.vappend(stack)
        
    def vappend(self,stack):
        super().append(stack)
        #self.__addVariable(stack.name)
        
    def __addVariable(self,name):
        if self.name is None:
            self.name = []
        
        if name is not None:
            if type(name) is list:
                self.name  += name
            else:
                self.name  += [ name ]    
    
    
    def savefig(self,fig,fullpath):  
        fig.savefig(fullpath)
    
    '''
    def savefigs(self)
        fig.savefig(fullpath)
    '''
    
    def plot():
        pass

