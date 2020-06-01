#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json


# In[ ]:


def openJson(file):
    import json
    with open(file) as f:
        return json.load(f)

def openDict(file):
    import json
    with open(file) as f:
        return eval(f.read())

