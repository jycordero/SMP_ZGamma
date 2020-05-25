PERIOD=2017

#######################

function GetFileName(){
	DataMC=$1
	folder=$2	

	folder=$(echo $folder | cut -d":" -f1)
	echo $folder

	if [ $DataMC == "data" ]
	then
		name=$(echo $folder | cut -d"_" -f5)
		if [ $name == "resubmit" ]
		then
			typ=$(echo $folder | cut -d"_" -f5)
			name=$(echo $folder | cut -d"_" -f6)
			Run=$(echo $folder | cut -d"_" -f7)
			Run=$(echo $Run | cut -d"-" -f1)
		else
			typ=$(echo $folder | cut -d"_" -f4)
			name=$(echo $folder | cut -d"_" -f5)
			Run=$(echo $folder | cut -d"_" -f6)
			Run=$(echo $Run | cut -d"-" -f1)
		fi
		fileName=$typ$name$Run
	else
		name=$(echo $folder | cut -d"_" -f1)
		fileName=$name	
	fi

	return 	$filename
}
####################

DATA=mc

##########

echo -------------------$DATA
INFOLDERS=`ls ${EOSHZG}/corderom/${DATA}_${PERIOD}/trigBits/`

for folder in $INFOLDERS
do
	GetFileName $DATA $folder
	echo filename ---- $fileName
	INPATH=${EOSHZG}/corderom/${DATA}_${PERIOD}/trigBits/${folder}/${PERIOD}_${DATA}_legacy_trigBits_${folder}

	echo Path ---- $INPATH

	echo "Jobs" > index_${fileName}_${DATA}_${PERIOD}.txt
	ls $INPATH*/* | cut -d'_' -f2 | cut -d'.' -f 1 >> index_${name}_${DATA}_${PERIOD}.txt
done

#####################################################################
#####################################################################
#####################################################################

DATA=data

#########

DATATYPE=DoubleMuon
INFOLDERS=`ls ${EOSHZG}/corderom/${DATA}_${PERIOD}/${DATATYPE}`

echo -------------------$DATA-----$DATATYPE
for folder in $INFOLDERS
do
	GetFileName $DATA $folder
	echo filename ---- $fileName
	INPATH=${EOSHZG}/corderom/${DATA}_${PERIOD}/${DATATYPE}/${folder}
	
	echo Path ---- $INPATH

	echo "Jobs" > index_${fileName}_${DATA}_${PERIOD}.txt
	ls  $INPATH | cut -d'_' -f2 | cut -d'.' -f 1 >> index_${fileName}_${DATA}_${PERIOD}.txt
	#ls ${folder} | cut -d'_' -f2 | cut -d'.' -f 1 > index_${name}${Run}_Data_${PERIOD}.txt
	#ls ${folder}
done


#########################
#####################################################################
#########################

DATATYPE=DoubleEG
INFOLDERS=`ls ${EOSHZG}/corderom/${DATA}_${PERIOD}/${DATATYPE}`

echo -------------------$DATA-----$DATATYPE
for folder in $INFOLDERS
do
	GetFileName $DATA $folder
	echo filename ---- $fileName

	INPATH=${EOSHZG}/corderom/${DATA}_${PERIOD}/${DATATYPE}/${folder}
	
	echo Path ---- $INPATH

	echo "Jobs" > index_${fileName}_${DATA}_${PERIOD}.txt
	ls $INPATH/* | cut -d'_' -f2 | cut -d'.' -f 1 >> index_${fileName}_${DATA}_${PERIOD}.txt
	#ls ${folder}/*/* | cut -d'_' -f2 | cut -d'.' -f 1 > index_${name}${Run}_Data_${PERIOD}.txt
done
