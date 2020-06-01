#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def assErr(k,N):
    a, b = 0.001,1
    steps = 1000
    beta = np.arange(a,b,step = (b-a)/steps)

    Beta  = spc.betainc(k+1,N-k+1,beta)
    Sols = [[100 if np.isnan(Bs-As-lamb) else np.abs(Bs-As-lamb) for Bs in Beta] for As in Beta]

    i = int(np.argmin(Sols)/steps)
    j = int(np.argmin(Sols)- i*steps)

    intLow, intHigh = beta[i],beta[j]
    print(np.argmin(Sols),np.min(Sols),Sols[i][j])
    print(i,j)


def Template(Nsig,Nbkg,Sig,Bkg):
    return Nsig * (Sig/np.sum(Sig)) + Nbkg * (Bkg/np.sum(Bkg))


def GetCDF(dist):
    return np.cumsum(dist/np.sum(dist))      


def CHI2(Exp,Obs):
    if np.sum(Exp) == 0:
        return np.sum((Exp-Obs)**2/np.sqrt(Exp))
    else:
        return np.sum((Exp-Obs)**2)


def Sampling(dist,N):
    indices = []

    CDF = self.GetCDF(dist[0])

    for samp in np.random.rand(N):
        indices.append(np.sum(CDF < samp))
    hist = np.histogram(dist[1][indices],bins=np.arange(-1,1.1,step=0.1))
    return np.array(hist[0])

