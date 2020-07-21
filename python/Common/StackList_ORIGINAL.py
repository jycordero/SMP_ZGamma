#!/usr/bin/env python
# coding: utf-8

# In[1]:


class StackList:
    def __init__(self,stack = None):
        self.stack = stack
        
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
        try :
            key = int(key)
            return self.stack[key]
        except:
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
    
    def append(self,istack):
        if self.stack:
            self.stack.append(istack)
        else:
            self.stack = [istack]
            

