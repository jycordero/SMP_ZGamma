
# coding: utf-8

# In[ ]:


class Event:
    def __init__(self,event):
        self.event = event

    def value(self,key):
        return getattr(self.event,key).values

