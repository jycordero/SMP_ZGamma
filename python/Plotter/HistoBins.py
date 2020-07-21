#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from Common.StackList import StackList


# In[ ]:


class HistoBins( StackList ):
    def __init__(self,stack=None, name=None,Print=False):
        StackList.__init__(self,name=name,stack=stack,Print=Print)    
    
    def append(self,stack,name=None):
        if name is None and stack.name is None:
            raise "Name is not specified, provide argument \"name\" or setit in Histo"
        
        if name is None:
            name = stack.name
        else:
            stack.name = name
        
        super().append(stack,stack.name)

