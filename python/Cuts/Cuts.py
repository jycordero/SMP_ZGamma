#!/usr/bin/env python
# coding: utf-8

# In[10]:


import numpy as np
from Common.Logic import AND, OR, NOT, ABS


# In[13]:


class Cuts:
    def __init__(self,
                 PhotonRadiation = None,
                 OppositeCharge = None, 
                 VetoDY = None,
                 MVA = None
                ):
        
        self.PhotonRadiation = PhotonRadiation
        self.OppositeCharge = OppositeCharge
        self.VetoDY = VetoDY
        self.MVA = MVA
        
    
    def Pass(self,event,Region = None):
        flag = np.ones(len(event), dtype= np.bool)
        flag *= self._STD(event)
        if Region is not None:
            flag *= self._Region(event, Region)
        return flag
    
    def _STD(self,event):    
        flag = self._DR_l1gm(event)
        flag *= self._DR_l2gm(event)
        
        if self.PhotonRadiation is not None:
            if self.PhotonRadiation == 'ISR': 
                flag *= self._ISR(event)
            elif self.PhotonRadiation == 'FSR': 
                flag *= self._ISR(event)
                
        if self.MVA is not None and self.MVA: 
            flag *= self._MVA(event)
            
        if self.OppositeCharge is not None: 
            if self.OppositeCharge:
                flag *= self._oppositeCharge(event)
            else: 
                flag *= self._sameCharge(event)
            
        return flag
    
    
    def _Region(self,event,region):
        return getattr(self,"_"+region)
    
    
    
        
    def _vetoDY(self,event):
        return event.value('vetoDY') == False
    
    def _oppositeCharge(self,event):
        return event.value('leptonOneCharge') != event.value('leptonTwoCharge')
    
    def _MVA(self,event):
        return event.value('photonOneMVA') > 2
    
    def _ISR(self,event):                
        return event.value('dileptonM') + event.value('llgM') >= 185
    
    def _FSR(self,event):                
        return event.value('dileptonM') + event.value('llgM') < 185
    
    def _DR_l1gm(self,event):
        return event.value('l1PhotonDR') > 0.7
    
    def _DR_l2gm(self,event):
        return event.value('l1PhotonDR') > 0.7
    


    
    def EB(self,event):
        return ABS(event.value('photonOneEta')) < 1.442
    def EE(self, event):
        return AND(ABS(event.value('photonOneEta')) > 1.5666,ABS(event.value('photonOneEta')) <=2.5)

    def _H1_Ich(self, event):
        return OR(event.value('photonOneIch_EB') < 2.0, event.value('photonOneIch_EE') < 1.5)
    def _H2_Ich(self, event):
        return OR(event.value('photonOneIch_EB') >= 2.0, event.value('photonOneIch_EE') >= 1.5)

    def _H1_Sieie(self,event):
        return OR(event.value('photonOneSieie_EB') < 0.01015, event.value('photonOneSieie_EE') < 0.0272)
    def _H2_Sieie(self,event):
        return OR(event.value('photonOneSieie_EB') >= 0.011, event.value('photonOneSieie_EE') >= 0.03)
    
    def _A(self,event):
        return AND(self._H1_Ich(event), self._H1_Sieie(event))
    def _B(self,event):
        return AND(self._H1_Ich(event), self._H2_Sieie(event))
    def _C(self,event):
        return AND(self._H2_Ich(event), self._H1_Sieie(event))
    def _D(self,event):
        return AND(self._H2_Ich(event), self._H2_Sieie(event))
        
    def _AB(self,event):
        return self._A(event) + self._B(event)
    def _CD(self,event):
        return self._C(event) + self._D(event)
        
    def _SIG(self,event):
        return self._H1_Ich(event)
    def _invSIG(self,event):
        return NOT(self._H1_Ich(event))
    
    def _IPFS(self,event):
        return event.value('genPhotonIPFS')

    def _invIPFS(self,event):
        return NOT(event.value('genPhotonIPFS'))
    
    def _H1p_Sieie(self,event):
        P = OR(event.value('photonOneSieie_EB') < 0.0122, event.value('photonOneSieie_EE') < 0.036)
        return AND(self._B(event),P)
    def _H2p_Sieie(self,event):
        P = OR(event.value('photonOneSieie_EB') >= 0.0122, event.value('photonOneSieie_EE') >= 0.036)
        return AND(self._B(event), P)
    def _H1p_Ich(self, event):
        P = OR(event.value('photonOneIch_EB') < 2.0, event.value('photonOneIch_EE') < 1.5)
        return AND(self._B(event), P)
    def _H2p_Ich(self, event):
        P = OR(event.value('photonOneIch_EB') >= 2.0, event.value('photonOneIch_EE') >= 1.5)
        return AND(self._B(event), P)
    
    
    def _Ap(self,event):
        return AND(self._H1p_Ich(event), self._H1p_Sieie(event))
    def _Bp(self,event):
        return AND(self._H1p_Ich(event), self._H2p_Sieie(event))
    def _Cp(self,event):
        return AND(self._H2p_Ich(event), self._H1p_Sieie(event) )     
    def _Dp(self,event):
        return AND(self._H2p_Ich(event), self._H2p_Sieie(event))
    
    def _A1p(self,event):
        return self._Ap(event)
    def _B1p(self,event):
        return self._Bp(event)
    def _C1p(self,event):
        return self._Cp(event)
    def _D1p(self,event):
        return self._Dp(event)
    
    def ExtractIchRange(self,
                        path,
                        subPath  = 'Reduced/OptimalIchRange/',
                        filename = 'IchRange.csv'):
        '''
        IchRange = self.ExtractIchRange(path     = self.path,
                                        subPath  = 'Reduced/OptimalIchRange/',
                                        filename = 'IchRange.csv'
                                       )
        '''
        
        IchRange = pd.read_csv(path+subPath+filename)
        
        IchR = {}
        for etaS in IchRange.keys():
            if etaS == '[0, 1.4442]' or etaS == '[0, 1.4666]':
                phType = 'EB'
            else:
                phType = 'EE'
            IchR[phType] = Helper().ConvertString2Float(IchRange[etaS][0]) 
        return IchR
        


                        


# In[ ]:





# In[ ]:




