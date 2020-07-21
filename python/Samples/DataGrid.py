#!/usr/bin/env python
# coding: utf-8

# In[1]:


from Common.StackList import StackList


# In[ ]:


class DataGrid( StackList ):
    def __init__(self,stack = None,name = None):
        StackList.__init__(self, name = name, stack= stack )                   
        
    def getGrid(self):
        return [stk.name for stk in self.stack]
    
    

