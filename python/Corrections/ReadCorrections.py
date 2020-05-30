#!/usr/bin/env python
# coding: utf-8

# In[11]:


from ROOT import TFile
import ROOT
import numpy as np
import matplotlib.pyplot as plt


# In[3]:


path = "/home/jcordero/CMS/JYCMCMS/SMP_ZG/python/Corrections/"
inputFile = "transformation_pho_presel_BDTUpto6000.root"
file = TFile(path+inputFile)


# In[4]:


var = [
        "EtaWidth",
        "PhiWidth",
        "full5x5sieie",
        "full5x5sieip",
        "full5x5R9",
        "S4",
        "rho",
        ]
phType = ["EE","EB"]

hist = {}
for v in var:
    for ph in phType:
        hist["transf"+v+ph] = file.Get("transf"+v+ph)


# In[5]:


x = ROOT.Double(0)
y = ROOT.Double(0)

func = {}
for k in hist.keys():
    xarr,yarr = [],[]
    for i in range(hist[k].GetN()):
        hist[k].GetPoint(i,x,y)
        #print(x,y)
        xarr.append(float(x))
        yarr.append(float(y))
        
    func[k] = [xarr,yarr]
    


# In[32]:


def transf(x0,f):
    x,y = np.array(f[0]), np.array(f[1])
    n = np.sum(x<x0) 
    m = (y[n]-y[n-1])/(x[n] - x[n-1])
    b = y[n]-m*x[n]

    return m*x0+b


# In[33]:


x = np.array(func[list(hist.keys())[-1]][0])
y = np.array(func[list(hist.keys())[-1]][1])


# In[34]:


k = "transffull5x5R9EE"

x1,y1 = [],[]
xrange = np.arange(func[k][0][0],func[k][0][-1],step=(func[k][0][-1] -func[k][0][0])/4000)
for xr in xrange:
    x1.append(xr)
    y1.append(transf(xr,func[k]))


# In[31]:



if min(func[k][0]) < min(func[k][1]):
    xmin = min(func[k][0])
else:
    xmin = min(func[k][1])

if max(func[k][0]) < max(func[k][1]):
    xmax = max(func[k][1])
else:
    xmax = max(func[k][0])
    
x = np.arange(xmin,xmax,step = 0.1)
    
plt.figure()
plt.plot(func[k][0],func[k][1],'xr')
plt.plot(x,x,'-b')
plt.plot(x1,y1,'-g')
plt.show()


# In[13]:


hist.keys()


# In[ ]:





# In[ ]:





# In[19]:


#hist["full5x5R9"]


# In[ ]:




