PERIOD=2017
#DATA=data
DATA=data
INPUTPATH=/uscms/home/corderom/nobackup/$PERIOD/CMSSW_10_2_13/src/BaconProd/Ntupler/crab
INPUTFOLDER=${PERIOD}_${DATA}_legacy_trigBits

Samples=`ls -1 ${INPUTPATH}/${INPUTFOLDER} | cut -d'_' -f2`
Runs=`ls -1 ${INPUTPATH}/${INPUTFOLDER}  | cut -d'_' -f3 | cut -d'-' -f1 | cut -d'7' -f2`

for s in $Samples
do
	echo $s
done

