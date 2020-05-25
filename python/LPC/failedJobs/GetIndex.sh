INFOLDERS=`ls Files/`

for folder in $INFOLDERS
do
	echo ${folder}
	awk -F" " '{print $1}' Files/${folder} > index_${folder}

done
