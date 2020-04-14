#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np 
from scipy.special import wofz
import scipy.special as spc
import array


# In[ ]:


class CommonHelper:
    class Format:
        def ConvertString2Float(varS):
            if varS == '' or varS == ' ':
                convert = False
            elif type(varS) is int or type(varS) is float or type(varS) is np.float64 or type(varS) is np.int64:
                convert = varS
            else:
                if '[' in varS:
                    convert = [float(v) for v in varS.replace('[ ','').replace('[','').replace(']','').replace(' ]','').replace(',','').replace('  ',' ').split(' ')]
                elif type(varS) is list:
                    convert = varS

                else:
                    convert = float(varS)
            return convert        

    class Plot:
        def BinFormat(Bins,ranges = None,Type='ranges', Print=False):
            bins = []
            if Bins == []:
                return Bins

            if type(Bins) is int or type(Bins) is float or type(Bins) is np.int64 or type(Bins) is np.float64:
                if Print:
                    print('Enter the Int bins category')

                try:
                    step = (ranges[1]-ranges[0])/Bins
                    if step*Bins+ranges[0] != ranges[1] and Print:
                        print('Last bin will be omited')
                except:
                    if Print:
                        print('Please provide a range')

                Bins = int(Bins)
                if Type=='ranges':    
                    for i in np.arange(Bins):
                        bins.append([i*step+ranges[0],(i+1)*step+ranges[0]])
                elif Type == 'edges':
                    for i in range(Bins+1):
                        bins.append(i*step+ranges[0])

                elif Type == 'center':
                    bins = np.array(self.BinFormat(Bins = Bins,Type='edges'))
                    bins = (bins[:-1]+bins[1:])/2
            else:
                if Print:
                    print('Enter the List bins category')
                if Type == 'ranges':
                    if type(Bins[0]) is np.ndarray or type(Bins[0]) is list:
                        bins = Bins
                    else:
                        for i in np.arange(len(Bins)-1):
                            bins.append([Bins[i],Bins[i+1]])
                elif Type == 'edges':
                    if type(Bins[0]) is int or type(Bins[0]) is float or type(Bins[0]) is np.int64:
                        bins = Bins
                    else:
                        for b in Bins:
                            bins.append(b[0])
                        bins.append(Bins[-1][1])
                    bins = array.array("f",bins)
                elif Type == 'center':
                    bins = np.array(self.BinFormat(Bins = Bins,Type='edges'))
                    bins = (bins[:-1]+bins[1:])/2

            return bins
        
        def BinIndex(Data,Low,Max,Abs = False):
            if Abs:
                return np.logical_and(np.abs(Data) >= Low, np.abs(Data) <  Max)
            else:
                return np.logical_and(np.array(Data) >= Low, np.array(Data) <  Max)   
        
    class Math:
        ###########
        ### Math
        def Exp(x,*arg):
            lamb,x0 = arg
            return np.exp(-lamb*(x-x0))
        def RooCMSShape(x,*arg):
            alpha, beta, peak, gamma = arg

            erf = spc.erfc((alpha - x)*beta)
            u = (x-peak)*gamma

            u = np.exp(-u)   
            #u[u <- 70] = u[u <- 70]*0 + 1e20
            #u[u > 70]  = u[u > 70]*0
            #ind  =  np.logical_and(u>=-70, u<=70)
            #u[ind]     = np.exp(-u[ind])

            return erf*u
        def G(x, *arg):
            """ Return Gaussian line shape at x with HWHM alpha """
            alpha, mean = arg
            return np.sqrt(np.log(2) / np.pi) / alpha* np.exp(-((x-mean) / alpha)**2 * np.log(2))

        def L(x, *arg):
            """ Return Lorentzian line shape at x with HWHM gamma """
            gamma, mean = arg
            return gamma / np.pi / ((x-mean)**2 + gamma**2)

        def Voigt(x, *arg):
            """ Return Voigt-Weigner line shape at x"""
            alpha, gamma, mean = arg
            sigma = alpha / np.sqrt(2 * np.log(2))
            return np.real(wofz(((x-mean) + 1j*gamma)/sigma/np.sqrt(2))) / sigma                                                                   /np.sqrt(2*np.pi)

        def NLL(DATA,Temp,*arg):
            Model = Temp(*arg)
            return np.sum(Model) - np.sum(DATA*np.log(Model))

        def CHI2(DATA,Temp,*arg):
            Model = Temp(*arg)
            DATA[DATA==0] = 1
            SIGMA_2 = (1/DATA + 1/Model)**(-1)
            return np.sum((Model-DATA)**2/SIGMA_2)

        def gauss(self,x,*a):
            return a[0]*np.exp(-(x-a[1])**2/(2*a[2]**2)) + a[3]
        
        def crystal_ball(self,x,*params):
            x = x+0j 
            N, a, n, xb, sig = params
            if a < 0:
                a = -a
            if n < 0:
                n = -n
            aa = abs(a)
            A = (n/aa)**n * np.exp(- aa**2 / 2)
            B = n/aa - aa
            total = 0.*x
            total += ((x-xb)/sig  > -a) * N * np.exp(- (x-xb)**2/(2.*sig**2))
            total += ((x-xb)/sig <= -a) * N * A * (B - (x-xb)/sig)**(-n)
            try:
                return total.real
            except:
                return totat
            return total

        def Template(Nsig,Nbkg,Sig,Bkg):
            return Nsig * (Sig/np.sum(Sig)) + Nbkg * (Bkg/np.sum(Bkg))
        
    class Stat:
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

