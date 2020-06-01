#!/usr/bin/env python
# coding: utf-8

# In[ ]:


class Event:
    def __init__(self,event):
        self.event = event

    def __len__(self):
        return len(self.event)
    
    def __getitem__(self,key):
        return self.event[key]
        
    def value(self,key):
        return getattr(self.event,key).values

