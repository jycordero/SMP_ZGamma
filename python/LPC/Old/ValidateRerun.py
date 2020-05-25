import numpy as np
import pandas as pd

import os
#################################
def Merge(indexOverlap,indexNonOverlap, MergePath, ResubmitPath, Print = False):
	path = {}
	path["Resubmit"] = ResubmitPath
	path["Merge"]    = MergePath

	File = {}
	for ind,i in zip(indexOverlap,np.arange(1,len(indexOverlap)+1)):
		File["Resubmit"] = "Output_"+  str(i)+".root"
		File["Merge"]    = "Output_"+str(ind)+".root"
		cmd = "cp "+path["Resubmit"]+File["Resubmit"]+" "+path["Merge"]+File["Merge"]
		if Print:
			print(cmd)
		else:
			os.system(cmd)

	resubmitRange = 571
	for ind,i in zip(indexNonOverlap, np.arange(len(indexOverlap)+1,resubmitRange+1)):
		File["Resubmit"] = "Output_"+  str(i)+".root"
		File["Merge"]    = "Output_"+str(ind)+".root"
		cmd = "cp "+path["Resubmit"]+File["Resubmit"]+" "+path["Merge"]+File["Merge"]
		if Print:
			print(cmd)
		else:
			os.system(cmd)
		


def SaveIndex(File,index):
	df = pd.DataFrame(index)
	df.to_csv(File)

def OverlapCheck(df1,df2):
	indexOverlap, indexNonOverlap= [],[]

	Overlap,NonOverlap = 0,0
	for i in df1['index']:
		if i in list(df2['index']):
			Overlap += 1
			indexOverlap.append(i)
		else:
			NonOverlap += 1
			indexNonOverlap.append(i)
			#print(i)

	print('Total Overlap in resubmit and samples in EOS '+str(Overlap))
	print('Total NONOverlap in resubmit and samples in EOS '+str(NonOverlap))

	return indexOverlap, indexNonOverlap

##################################

def main():

	DataRun = 'F'
	############
	pathEOS = "/eos/uscms/store/user/lpchzg/corderom/data_2017/"	
	pathEG = "DoubleEG/"
	path , pathResubmit = {},{}
	path['F'] = "2017_data_legacy_trigBits_DoubleEG_Run2017F-31Mar2018-v1/"
	pathResubmit['F'] = "2017_data_legacy_trigBits_resubmit_DoubleEG_Run2017F-31Mar2018-v1/200212_053749/"

	#MergePath = pathEOS + pathEG + path[DataRun] + "MergeResubmit/"
	MergePath = pathEOS + pathEG + path[DataRun] + "FromResubmit/"
	ResubmitPath = pathEOS + pathEG + pathResubmit[DataRun]
	############
	filename = "indexDoubleEG"+DataRun+".txt"
	df = pd.read_csv(filename)

	#############
	filename = pathEOS + pathEG + path[DataRun] + "indexFailed_DoubleEG"+DataRun+".txt"
	dfOther = pd.read_csv(filename)

	#############
	print('Files in EOS not in the rerun')
	indexOverlap, indexNonOverlap= OverlapCheck(dfOther, df)
	
	SaveIndex(    "OverlapFile"+DataRun+".txt" , indexOverlap)
	SaveIndex( "NonOverlapFile"+DataRun+".txt" , indexNonOverlap)
	
	Merge(
		indexOverlap = indexOverlap, 
		indexNonOverlap = indexNonOverlap, 
		MergePath = MergePath, 
		ResubmitPath = ResubmitPath,
		Print = True,
		)
	#############

	print('Files in ReRun not in the EOS')
	OverlapCheck(df, dfOther)

	###########
	return False
main()
