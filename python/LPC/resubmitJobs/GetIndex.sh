INFOLDERS=`ls Files/`

for folder in $INFOLDERS
do
	echo ${folder}
	#echo "index" > index_${folder}
	awk -F" " '{print $1}' Files/${folder} > index_${folder}

done
