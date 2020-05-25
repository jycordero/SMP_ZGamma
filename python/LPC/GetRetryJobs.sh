PERIOD=2017
CURPATH=/uscms/home/corderom/nobackup/$PERIOD/CMSSW_10_2_13/src/BaconProd/Ntupler/crab

STATUS=finished
###########

DATA=data
DATAPATH=${PERIOD}_${DATA}_legacy_trigBits_resubmit
DATASAMPLES=`ls $CURPATH/$DATAPATH`

#############

DATA=mc
MCPATH=${PERIOD}_${DATA}_legacy_trigBits_resubmit
MCSAMPLES=`ls $CURPATH/$MCPATH`

##############

OUTFOLDER=retryJobs/Files

for samp in $DATASAMPLES
do
	#echo $samp
	#crab status --dir=$CURPATH/$DATAPATH/$samp --long | grep $STATUS > $OUTFOLDER/${samp}_${STATUS}_Data_$PERIOD.txt

	echo $samp
	name=$(echo $samp | cut -d"_" -f2)
	Run=$(echo $samp | cut -d"_" -f3)
	Run=$(echo $Run | cut -d'-' -f1)
	crab status --dir=$CURPATH/$DATAPATH/$samp --long | grep $STATUS > $OUTFOLDER/${name}${Run}_Data_$PERIOD.txt
	
done


for samp in $MCSAMPLES
do
	echo $samp
	#crab status --dir=$CURPATH/$MCPATH/$samp --long | grep $STATUS > $OUTFOLDER/${samp}_${STATUS}_MC_$PERIOD.txt
	name=$(echo $samp | cut -d"_" -f2)
	crab status --dir=$CURPATH/$MCPATH/$samp --long | grep $STATUS > $OUTFOLDER/${name}_MC_$PERIOD.txt
done

