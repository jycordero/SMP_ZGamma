#!/usr/bin/env python
# coding: utf-8

# In[1]:


class Cuts():
    def __init__(self,Region=[],path=''):
        self.Region = []
        self.path   = path
        
    def SetPath(path):
        self.path = path
        
    def ExtractIchRange(self,
                        path,
                        subPath  = 'Reduced/OptimalIchRange/',
                        filename = 'IchRange.csv'):
        IchRange = pd.read_csv(path+subPath+filename)
        
        IchR = {}
        for etaS in IchRange.keys():
            if etaS == '[0, 1.4442]' or etaS == '[0, 1.4666]':
                phType = 'EB'
            else:
                phType = 'EE'
            IchR[phType] = Helper().ConvertString2Float(IchRange[etaS][0]) 
        return IchR
        
    # Standard Cuts, fiducial cuts
    def STD_Cuts(self,
                data,
                phType = 'ISR',
                Charge ='oposite',
                Print  = False,
                MVA    = False,
                vetoDY = True,
                lgmDR  = True
                ):

        [d.ResetCuts() for d in data]
        #---------------------------- CUTS ------------------------------------ CUTS -----------------------

        for d in data:
            
            if Print:
                print('-----------------',d.name,'--------------')
                print('----Total----')
                print(np.sum(d.cuts))

            if not d.df.empty:
                #-------------------------------------------
                if vetoDY and  d.name == 'DYJets':
                    d.AddCuts(np.array(d.df.vetoDY)==False)


                #-------------------------------------------
                if lgmDR:
                    d.AddCuts(np.array(d.df.l1PhotonDR) > 0.7)
                    d.AddCuts(np.array(d.df.l2PhotonDR) > 0.7)
                    if Print:
                        print('----DR cuts ----')
                        print(np.sum(d.cuts))

                #-------------------------------------------
                if phType == 'ISR':
                    # 2 Body to get ISR
                    d.AddCuts(np.array(d.df.llgM)+np.array(d.df.dileptonM) > 185)
                elif phType == 'FSR' :
                    # 3 Body to get FSR
                    d.AddCuts(np.array(d.df.llgM)+np.array(d.df.dileptonM) < 185)
                if Print:
                    print('----Mass cuts ----')  
                    print(np.sum(d.cuts))

                #-------------------------------------------
                if MVA:
                    d.AddCuts(np.array(d.df.photonOneMVA > 0.2))
                if Print:
                    print('----MVA cuts ----')  
                    print(np.sum(d.cuts))


                #-------------------------------------------
                if Charge == 'oposite':
                    d.AddCuts(np.array(d.df.leptonOneCharge) != np.array(d.df.leptonTwoCharge))
                elif Charge == 'same':
                    d.AddCuts(np.array(d.df.leptonOneCharge) == np.array(d.df.leptonTwoCharge))
                if Print:
                    print('----Charge cuts ----')
                    print(sum(d.cuts))

    # Specific Cuts by region
    def PhaseSpace( self,
                    data,
                    phType   = 'ISR',
                    Charge   = 'oposite',
                    Region   = [''],
                    MVA      = False,
                    vetoDY   = True,
                    lgmDR    = True,
                    ichRange = None,
                    Print    = False,
                  ):   

        if type(Region) is not list and type(Region) is not np.ndarray:
            Region  = [Region]

        self.STD_Cuts( data, 
                      phType   = phType, 
                      Charge   = Charge,
                      vetoDY   = vetoDY,
                      MVA      = MVA,
                      lgmDR    = lgmDR,
                      Print    = Print, 
                     )
        ################################
        IchRange = self.ExtractIchRange(path     = self.path,
                                        subPath  = 'Reduced/OptimalIchRange/',
                                        filename = 'IchRange.csv'
                                       )
        

        #################################
        for d in data:            
            if Print:
                print('-------'+d.name+'-------')
                print('----- Standard Region')
                print(sum(d.cuts))
            if not d.df.empty:
                for region in Region:
                    if Print:
                        print('----'+region+'----')
                    ##########################################
                    if   region == 'Sig':
                        if Print:
                            print('-------'+d.name+'-------')
                            print('----- Total')
                            print(sum(d.cuts))
                        SigRegion = np.logical_or(
                                                  np.array(d.df.photonOneIch_EB) < 2.0,
                                                  np.array(d.df.photonOneIch_EE) < 1.5 
                                                 )
                        d.AddCuts(SigRegion)
                        #d.AddCuts()

                        if Print:
                            print('----- Signal Region')
                            print(sum(d.cuts))
                    elif region == "Inv Sig":
                        if Print:
                            print('-------'+d.name+'-------')
                            print('----- Total')
                            print(sum(d.cuts))
                        '''
                        SBRegion = np.logical_or(
                                                  np.array(d.df.photonOneIch_EB) >= ichHighEB,
                                                  np.array(d.df.photonOneIch_EE) >= ichHighEE
                                                 )
                        '''
                        SB1Region = np.logical_or(
                                                  np.array(d.df.photonOneIch_EB) >= IchRange['EB'][0],
                                                  np.array(d.df.photonOneIch_EE) >= IchRange['EE'][0]
                                                 )
                        SB2Region = np.logical_or(
                                                  np.array(d.df.photonOneIch_EB) < IchRange['EB'][1],
                                                  np.array(d.df.photonOneIch_EE) < IchRange['EE'][1]
                                                 )

                        SB_Region = np.logical_and( SB1Region, SB2Region)

                        d.AddCuts( SB_Region ) 
                        

                        if Print:
                            print('----- Signal Region')
                            print(sum(d.cuts))
                    elif region == 'Sideband':
                        if Print:
                            print('-------'+d.name+'-------')
                            print('----- Total')
                            print(sum(d.cuts))
                        SideBandRegion = np.logical_or(
                                                  np.array(d.df.photonOneIch_EB) >= 2.0,
                                                  np.array(d.df.photonOneIch_EE) >= 1.5 
                                                 )
                        d.AddCuts(SideBandRegion)
                        #d.AddCuts()

                        if Print:
                            print('----- Signal Region')
                            print(sum(d.cuts))            
                    elif region == 'Compare':
                        print(d.name)
                        if d.name == 'DYJets_Sig':
                            SigRegion = np.logical_or(
                                                      np.array(d.df.photonOneIch_EB) < 2.0,
                                                      np.array(d.df.photonOneIch_EE) < 1.5 
                                                     )
                            d.AddCuts(SigRegion)

                        elif d.name == 'DYJets_SideBand':
                            SideBandRegion = np.logical_or(
                                                  np.array(d.df.photonOneIch_EB) >= 2.0,
                                                  np.array(d.df.photonOneIch_EE) >= 1.5 
                                                 )
                            d.AddCuts(SideBandRegion)

                    ##########################################
                    ## Background Estimation ABCD Method
                    elif region == 'A' :
                        A1_Region = np.logical_or(
                                                  np.array(d.df.photonOneIch_EB) < 2,
                                                  np.array(d.df.photonOneIch_EE) < 1.5
                                                 )
                        A2_Region = np.logical_or(np.array(d.df.photonOneSieie_EB) < 0.01015,
                                                  np.array(d.df.photonOneSieie_EE) < 0.0272
                                                  )

                        d.AddCuts( np.logical_and(A1_Region, A2_Region) )
                    elif region == 'B' :
                        B1_Region = np.logical_or(
                                                  np.array(d.df.photonOneIch_EB) < 2,
                                                  np.array(d.df.photonOneIch_EE) < 1.5
                                                 )
                        B2_Region = np.logical_or(np.array(d.df.photonOneSieie_EB) >= 0.011,
                                                  np.array(d.df.photonOneSieie_EE) >= 0.03
                                                  )

                        d.AddCuts( np.logical_and(B1_Region, B2_Region) )
                    elif region == 'C' :
                        C11_Region = np.logical_or(
                                                  np.array(d.df.photonOneIch_EB) >= IchRange['EB'][0],
                                                  np.array(d.df.photonOneIch_EE) >= IchRange['EE'][0]
                                                 )
                        C12_Region = np.logical_or(
                                                  np.array(d.df.photonOneIch_EB) < IchRange['EB'][1],
                                                  np.array(d.df.photonOneIch_EE) < IchRange['EE'][1]
                                                 )
                        C1_Region = np.logical_and( C11_Region, C12_Region)

                        C2_Region = np.logical_or(np.array(d.df.photonOneSieie_EB) < 0.01015,
                                                  np.array(d.df.photonOneSieie_EE) < 0.0272
                                                  )

                        d.AddCuts( np.logical_and(C1_Region, C2_Region) )
                    elif region == 'D' :
                        D11_Region = np.logical_or(
                                                  np.array(d.df.photonOneIch_EB) >= IchRange['EB'][0],
                                                  np.array(d.df.photonOneIch_EE) >= IchRange['EE'][0]
                                                 )
                        D12_Region = np.logical_or(
                                                  np.array(d.df.photonOneIch_EB) < IchRange['EB'][1],
                                                  np.array(d.df.photonOneIch_EE) < IchRange['EE'][1]
                                                 )
                        D1_Region = np.logical_and( D11_Region, D12_Region)

                        D2_Region = np.logical_or(np.array(d.df.photonOneSieie_EB) >= 0.011,
                                                  np.array(d.df.photonOneSieie_EE) >= 0.03
                                                  )

                        d.AddCuts( np.logical_and(D1_Region, D2_Region) )
                        
                    elif region == 'Ap' or region == 'A1p' :
                        
                        #############
                        
                        Ap1_Region = np.logical_or(
                                                  np.array(d.df.photonOneIch_EB) < 2,
                                                  np.array(d.df.photonOneIch_EE) < 1.5
                                                 )
                        
                        #############
                        
                        Ap21_Region = np.logical_or(np.array(d.df.photonOneSieie_EB) >= 0.011,
                                                   np.array(d.df.photonOneSieie_EE) >= 0.03
                                                  )
                        
                        Ap22_Region = np.logical_or(np.array(d.df.photonOneSieie_EB) < 0.0122,
                                                   np.array(d.df.photonOneSieie_EE) < 0.036
                                                  )
                        Ap2_Region = np.logical_and(Ap21_Region,Ap22_Region)
                        
                        #############
                        
                        d.AddCuts( np.logical_and(Ap1_Region, Ap2_Region) )
                    elif region == 'Bp' or region == 'B1p':
                        #############
                        
                        Bp1_Region = np.logical_or(
                                                  np.array(d.df.photonOneIch_EB) < 2,
                                                  np.array(d.df.photonOneIch_EE) < 1.5
                                                 )
                        
                        #############
                        
                        Bp2_Region = np.logical_or(np.array(d.df.photonOneSieie_EB) > 0.0122,
                                                  np.array(d.df.photonOneSieie_EE) > 0.036
                                                  )

                        #############
                        
                        d.AddCuts( np.logical_and(Bp1_Region, Bp2_Region) )
                    elif region == 'Cp' or region == 'C1p':
                        #############
                        
                        Cp11_Region = np.logical_or(
                                                  np.array(d.df.photonOneIch_EB) >= IchRange['EB'][0],
                                                  np.array(d.df.photonOneIch_EE) >= IchRange['EE'][0]
                                                 )
                        Cp12_Region = np.logical_or(
                                                  np.array(d.df.photonOneIch_EB) < IchRange['EB'][1],
                                                  np.array(d.df.photonOneIch_EE) < IchRange['EE'][1]
                                                 )
                        Cp1_Region = np.logical_and( Cp11_Region, Cp12_Region)
                            
                        #############
                        
                        Cp21_Region = np.logical_or(np.array(d.df.photonOneSieie_EB) >= 0.011,
                                                    np.array(d.df.photonOneSieie_EE) >= 0.03
                                                  )
                        
                        Cp22_Region = np.logical_or(np.array(d.df.photonOneSieie_EB) < 0.0122,
                                                    np.array(d.df.photonOneSieie_EE) < 0.036
                                                  )
                        Cp2_Region = np.logical_and(Cp21_Region,Cp22_Region)
                        
                        #############
                        
                        d.AddCuts( np.logical_and(Cp1_Region, Cp2_Region) )
                    elif region == 'Dp' or region == 'D1p':
                        
                        #############
                        
                        Dp11_Region = np.logical_or(
                                                  np.array(d.df.photonOneIch_EB) >= IchRange['EB'][0],
                                                  np.array(d.df.photonOneIch_EE) >= IchRange['EE'][0]
                                                 )

                        Dp12_Region = np.logical_or(
                                                  np.array(d.df.photonOneIch_EB) < IchRange['EB'][1],
                                                  np.array(d.df.photonOneIch_EE) < IchRange['EE'][1]
                                                 )
                        Dp1_Region = np.logical_and( Dp11_Region, Dp12_Region)
                        
                        #############
                        
                        Dp2_Region = np.logical_or(np.array(d.df.photonOneSieie_EB) > 0.0122,
                                                   np.array(d.df.photonOneSieie_EE) > 0.036
                                                  )

                        #############
                        
                        d.AddCuts( np.logical_and(Dp1_Region, Dp2_Region) )
                        
                    elif region == 'AB' :
                        AB_Region = np.logical_or(
                                                  np.array(d.df.photonOneIch_EB) < 2,
                                                  np.array(d.df.photonOneIch_EE) < 1.5
                                                 )

                        d.AddCuts( AB_Region )
                    elif region == 'CD' :
                        CD1_Region = np.logical_or(
                                                  np.array(d.df.photonOneIch_EB) >= IchRange['EB'][0],
                                                  np.array(d.df.photonOneIch_EE) >= IchRange['EE'][0]
                                                 )
                        CD2_Region = np.logical_or(
                                                  np.array(d.df.photonOneIch_EB) < IchRange['EB'][1],
                                                  np.array(d.df.photonOneIch_EE) < IchRange['EE'][1]
                                                 )
                        CD_Region = np.logical_and( CD1_Region, CD2_Region)

                        d.AddCuts( CD_Region )                   

                    ##########################################
                    elif region == "EB":
                        d.AddCuts(np.abs(d.df.photonOneEta) < 1.4442)
                    elif region == "EE":
                        d.AddCuts(np.logical_and(np.abs(d.df.photonOneEta) > 1.5666,
                                                 np.abs(d.df.photonOneEta) <= 2.5,
                                                )
                                )

                    ##########################################
                    elif region == "IPFS":
                        d.AddCuts(np.array(d.df.genPhotonIPFS) == True)
                    elif region == "noIPFS":
                        d.AddCuts(np.array(d.df.genPhotonIPFS) == False)        
                    elif region == "Ich":
                        R11_Region = np.logical_or(
                                                  np.array(d.df.photonOneIch_EB) >= ichRange[0][0],
                                                  np.array(d.df.photonOneIch_EE) >= ichRange[0][1]
                                                 )
                        R12_Region = np.logical_or(
                                                  np.array(d.df.photonOneIch_EB) < ichRange[1][0],
                                                  np.array(d.df.photonOneIch_EE) < ichRange[1][1]
                                                 )
                        R1_Region = np.logical_and( R11_Region, R12_Region)
                        d.AddCuts(R1_Region)


# In[5]:


import numpy as np
import pandas as pd


# In[7]:


from Plotter.Helper import Helper


# In[ ]:




