#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from Common.StackList import StackList


# In[ ]:


class DataSample( StackList ):
    def __init__(self,stack = None):
        StackList.__init__(self, stack )
                   
    def getSamples(self):
        return [stk.name for stk in self.stack]


# In[ ]:




