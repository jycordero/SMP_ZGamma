#!/usr/bin/env python
# coding: utf-8

# In[1]:


from ROOT import TMVA,TH2F, TCanvas
import array


# In[2]:


#path = "/eos/uscms/store/user/corderom/Corrections2016Rereco/"
#phVals = ["EE","EB"]
phVals = ["EE"]
path = ""
file = {}
reader = {}
for ph in phVals:
    file[ph] = "TMVAnalysis_BDT_"+ph+".weights.xml"
    reader[ph] = TMVA.Reader()


varName= [
                "recoPhi",
                "r9",
                "sieieFull5x5",
                "sieipFull5x5",
                "e2x2Full5x5/e5x5Full5x5",
                "recoSCEta",
                "rawE",
                "scEtaWidth",
                "scPhiWidth",
                "esEn/rawE",
                "esRR",
                "rho",
            ]


# In[3]:


var = {}
for phType in phVals:
    var[ph] = {}
    for vn in varName:
            var[ph][vn] = (array.array('f',[0]))
            reader[ph].AddVariable(vn, var[ph][vn])
    reader[ph].BookMVA("BDT",path+file[ph])        


# In[4]:


# create a new 2D histogram with fine binning
histo2 = TH2F("histo2","",200,0,1,200,-5,5)

# loop over the bins of a 2D histogram
for b1 in range(1,histo2.GetNbinsX() + 1):
    for b2 in range(1,histo2.GetNbinsY() + 1):
        #for k 
        # find the bin center coordinates
        var[0][0] = histo2.GetXaxis().GetBinCenter(b1)
        var[1][0] = histo2.GetYaxis().GetBinCenter(b2)

        # calculate the value of the classifier
        # function at the given coordinate
        bdtOutput = reader.EvaluateMVA("BDT")

        # set the bin content equal to the classifier output
        histo2.SetBinContent(i,j,bdtOutput)


# In[ ]:


#gcSaver.append(TCanvas())
histo2.Draw("colz")


# In[ ]:


var


# In[ ]:


bdtOutput


# In[ ]:


varName= {
        "recoPhi"                :["photonOnePhi"],
        "r9"                     :["photonOneR9"],
        "sieieFull5x5"           :["photonOneSieie"],
        "sieipFull5x5"           :["photonOneSieip"],
        "e2x2Full5x5/e5x5Full5x5":["photonOneE2x2","photonOneE5x5"],
        "recoSCEta"              :["photonOneEta"],
        "rawE"                   :["photonOneScRawE"],
        "scEtaWidth"             :["photonOneScEtaWidth"],
        "scPhiWidth"             :["photonOneScPhiWidth"],
        "esEn/rawE"              :["photonOnePreShowerE","photonOneScRawE"],
        "esRR"                   :["photonOneSrr"],
        "rho"                    :["Rho"],
        }


# In[ ]:





# In[ ]:


# create a new 2D histogram with fine binning
histo2 = TH2F("histo2","",200,0,1,200,-5,5)

# loop over the bins of a 2D histogram
for b1 in range(1,histo2.GetNbinsX() + 1):
    for b2 in range(1,histo2.GetNbinsY() + 1):
        #for k 
        # find the bin center coordinates
        var[0][0] = histo2.GetXaxis().GetBinCenter(b1)
        var[1][0] = histo2.GetYaxis().GetBinCenter(b2)

        # calculate the value of the classifier
        # function at the given coordinate
        bdtOutput = reader.EvaluateMVA("BDT")

        # set the bin content equal to the classifier output
        histo2.SetBinContent(i,j,bdtOutput)

