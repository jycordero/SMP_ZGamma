
# coding: utf-8

# In[ ]:


import numpy as np


# In[1]:


class StackDict():
    def __init__(self, data = []):
        self.stack = {}
        
        self.__begin = 0
        self.__end = 0
        
        if data != []:
            self.stack = self.initiate(data)
    
        
    def __iter__(self):
        self.__begin = 0
        return self

    def __next__(self):
            if self.__begin >= self.__end:
                self.__begin = 0
                raise StopIteration
            else:
                self.__begin += 1
                return self[self.__begin - 1]
        
    def __getitem__(self,key):
        try:
            if   type(key) == int:
                return self.stack[self.__getIndexToKey(key)]
            elif type(key) == str:
                return self.stack[key]
            elif type(key) == list or type(key) == np.ndarray:
                return self.__listItemizeHandle(key)
            else:
                print("Invalid key")
        except:
            print("Invalid key")
            
    def __len__(self):
        return len(self.stack)
        
    def __listItemizeHandle(self,key):
        if len(key) == self.size():
            if isinstance(key[-1], np.bool_) or isinstance(key[-1], bool):
                tmp = []
                for i,k in enumerate(key):
                    if k:
                        tmp.append(self.stack[self.__getIndexToKey(i)])
                return tmp
            elif type(key[-1]) == int:
                return [ self.stack[self.__getIndexToKey(k)] for k in key ]
            elif type(key[-1]) == str:
                return [ self.stack[k] for k in key ]
            else:
                print("Invalid key in array")
        else:
            print("Indexing lenght must match Stack size")
    
    def __getIndexToKey(self,key):
        for i,k in enumerate(self.stack.keys()):
            if key == i:
                break
        return k
        
    def initiate(self,data):
        stack = {}
        for d in data:
            if not d.df.empty:
                stack[d.name] = d 
            else:
                print("{} is empty and excluded from stack".format(d.name))
            del d
        self.__end = len(stack)
        return stack

    def __inStackKey(self,key):
        return True if key in self.stack.keys() else False
    
    def __inStack(self,data):
        return self.__inStackKey(data.name)
        
    def append(self,data):
        if self.__inStack(data):
            print("Already in Stack")
        else:
            self.__end += 1
            self.stack[data.name] = data
    
    def remove(self,key):
        try:
            if type(key) == int:
                del self.stack[self.__getIndexToKey(key)]
            elif type(key) == str:
                del self.stack[key]
            else:
                print("Invalid key")    
        except:
            print("Invalid key")
    
    def size(self):
        return len(self)

