PERIOD=2017
CURPATH=/uscms/home/corderom/nobackup/$PERIOD/CMSSW_10_2_13/src/BaconProd/Ntupler/crab

STATUS=failed
###########

DATA=data
DATAPATH=${PERIOD}_${DATA}_legacy_trigBits
DATASAMPLES=`ls $CURPATH/$DATAPATH`

#############

DATA=mc
MCPATH=${PERIOD}_${DATA}_legacy_trigBits
MCSAMPLES=`ls $CURPATH/$MCPATH`

##############

OUTFOLDER=${STATUS}Jobs/Files


#for samp in $DATASAMPLES
#do
#	echo $samp
#	name=$(echo ${samp} | cut -d"_" -f2 )
#	Run=$(echo ${samp} | cut -d"_" -f3 )
#	Run=$(echo $Run | cut -d"-" -f1 )
#	echo $name
#
#	crab status --dir=$CURPATH/$DATAPATH/$samp --long | grep $STATUS > $OUTFOLDER/${name}${Run}_Data_$PERIOD.txt
#done


for samp in $MCSAMPLES
do
	echo $samp
	name=$(echo ${samp} | cut -d"_" -f2 )
	echo $name

	crab status --dir=$CURPATH/$MCPATH/$samp --long | grep $STATUS > $OUTFOLDER/${name}_MC_$PERIOD.txt
done

