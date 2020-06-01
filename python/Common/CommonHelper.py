#!/usr/bin/env python
# coding: utf-8

# In[9]:


import numpy as np 
import array
import scipy.special as spc

from functools import wraps


# In[4]:


class CommonHelper:
    class Log:       
        @staticmethod
        def logger(obj):
            import logging
            logging.basicConfig(filename="log/{}.log".format(obj.__name__), level=logging.INFO)
            
            @wraps(obj)
            def wrapper(*args,**kwargs):
                logging.info(
                            "Input args: {}, kwargs:{}".format(args,kwargs)
                            )
                return obj(*args **kwargs)
            return wrapper
        
        @staticmethod
        def timer(obj):
            import time
            @wraps(obj)
            def wrapper(*arg, **kwargs):
                t1 = time.time()
                result =  obj(*arg, **kwargs)
                t2 = time.time() -t1
                return result
            return wrapper
        
    class Type:
        @staticmethod
        def isNumeric(num):
            try: float(num)
            except: return False
            else: return True
        
        @staticmethod
        def isIterable(ite):
            try: iter(num)
            except:return False
            else: return True
    
    
        @staticmethod
        def isListOrArray(larr):
            if larr is list or larr is np.ndarray:
                return True
            else:
                return False
            
    class Read:
        @staticmethod
        def openJson(file):
            import json
            with open(file) as f:
                return json.load(f)
                #JSON = f.read()
            #return json.loads(JSON)
                            
    class Format:
        @staticmethod
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
        @staticmethod
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
                    for i in range(Bins+1):
                        bins.append(i*step+ranges[0])
                    bins = np.array(bins)
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
                    #if type(Bins[0]) is int or type(Bins[0]) is float or type(Bins[0]) is np.int64:
                    if CommonHelper.Type.isNumeric(Bins[0]):
                        bins = Bins
                    else:
                        for b in Bins:
                            bins.append(b[0])
                        bins.append(Bins[-1][1])
                    bins = np.array(bins)
                    bins = (bins[:-1]+bins[1:])/2

            return bins
        
        @staticmethod
        def BinIndex(Data,Low,Max,Abs = False):
            if Abs:
                return np.logical_and(np.abs(Data) >= Low, np.abs(Data) <  Max)
            else:
                return np.logical_and(np.array(Data) >= Low, np.array(Data) <  Max)   
    class Logic:
        @staticmethod
        def ABS(a):
            return np.abs(a)
        @staticmethod
        def NOT(a):
            return np.logical_not(a)
        @staticmethod
        def AND(a,b):
            return np.logical_and(a,b)
        @staticmethod
        def OR(a,b):
            return np.logical_or(a,b)
    
    class Math:
        import numpy as np         
        
        ###########
        ### Math
        @staticmethod
        def Exp(x,*arg):
            lamb,x0 = arg
            return np.exp(-lamb*(x-x0))
        
        @staticmethod
        def G(x, *arg):
            """ Return Gaussian line shape at x with HWHM alpha """
            alpha, mean = arg
            return np.sqrt(np.log(2) / np.pi) / alpha* np.exp(-((x-mean) / alpha)**2 * np.log(2))

        @staticmethod
        def L(x, *arg):
            """ Return Lorentzian line shape at x with HWHM gamma """
            gamma, mean = arg
            return gamma / np.pi / ((x-mean)**2 + gamma**2)

        @staticmethod
        def Voigt(x, *arg):
            from scipy.special import wofz
            """ Return Voigt-Weigner line shape at x"""
            alpha, gamma, mean = arg
            sigma = alpha / np.sqrt(2 * np.log(2))
            return np.real(wofz(((x-mean) + 1j*gamma)/sigma/np.sqrt(2))) / sigma                                                                   /np.sqrt(2*np.pi)
        @staticmethod
        def NLL(DATA,Temp,*arg):
            Model = Temp(*arg)
            return np.sum(Model) - np.sum(DATA*np.log(Model))

        @staticmethod
        def CHI2(DATA,Temp,*arg):
            Model = Temp(*arg)
            DATA[DATA==0] = 1
            SIGMA_2 = (1/DATA + 1/Model)**(-1)
            return np.sum((Model-DATA)**2/SIGMA_2)

        @staticmethod
        def gauss(x,*a):
            return a[0]*np.exp(-(x-a[1])**2/(2*a[2]**2)) + a[3]
        
        @staticmethod
        def crystal_ball(x,*params):
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
        
        @staticmethod
        def Template(Nsig,Nbkg,Sig,Bkg):
            return Nsig * (Sig/np.sum(Sig)) + Nbkg * (Bkg/np.sum(Bkg))
        
    class Stat:
        @staticmethod
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
            
        @staticmethod
        def Template(Nsig,Nbkg,Sig,Bkg):
            return Nsig * (Sig/np.sum(Sig)) + Nbkg * (Bkg/np.sum(Bkg))
        
        @staticmethod
        def GetCDF(dist):
            return np.cumsum(dist/np.sum(dist))      
        
        @staticmethod
        def CHI2(Exp,Obs):
            if np.sum(Exp) == 0:
                return np.sum((Exp-Obs)**2/np.sqrt(Exp))
            else:
                return np.sum((Exp-Obs)**2)
            
        @staticmethod
        def Sampling(dist,N):
            indices = []

            CDF = self.GetCDF(dist[0])

            for samp in np.random.rand(N):
                indices.append(np.sum(CDF < samp))
            hist = np.histogram(dist[1][indices],bins=np.arange(-1,1.1,step=0.1))
            return np.array(hist[0])


# In[ ]:





# In[ ]:




