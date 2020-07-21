#!/usr/bin/env python
# coding: utf-8

# In[1]:


from Common.CommonHelper import CommonHelper


# In[2]:


class StackList:
    def __init__(self,name=None, stack = None,Print=False):
        self.stack = stack
        self.name = name
        self.names = None
        self.Print=Print
        
    def __repr__(self):
        msg = "Stack("+str(self.stack)+")"
        return msg
    
    def __str__(self):
        msg = ""
        if self.stack:
            msg += "Samples:\n"
            for samp in self.stack:
                msg += "---"+samp.name+"\n"
        else:
            msg += "Stack is empty"
        return msg
    
    def __getitem__(self,key):
        if CommonHelper.Type.isNumeric(key):
            return self.stack[key]
        else:
            if type(key) is str:
                try:
                    for istack in self.stack:
                        if istack.name.lower() == key.lower():
                            return istack
                    return None
                except:
                    raise BaseException("Stack elements does not have \"name\" member. Use int index")
            else:
                try:
                    return [ self[k] for k in key ]
                except:
                    raise BaseException("Type of key is not supported")
        
    def __len__(self):
        return len(self.stack)
    
    def __iter__(self):
        return iter(self.stack)
    
    def remove(self,i):
        self.stack.remove(i)
    
    def pop(self,i):
        return self.stack.pop(i)
    
    def append(self,stack,name = None):
        try:
            name = stack.name
        except:
            name = ""
        
        
        if self.stack:
            self.stack.append(stack)
            self.names.append(name)
        else:
            self.stack = [ stack ]
            self.names = [ name ]
            


# In[ ]:




