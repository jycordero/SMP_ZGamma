#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from Common.StackList import StackList


# In[ ]:


class DataEras( StackList ):
    def __init__(self,stack=None,name=None):
        StackList.__init__(self,name=name,stack=stack)
        
    def append(self,stack,name=None):
        if name is None and stack.name is None:
            raise "Name is not specified, provide argument \"name\" or set is in Histo"
            
        if name is None:
            name = stack.name
        else:
            stack.name = name

        super().append(stack,stack.name)

