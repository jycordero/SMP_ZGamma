DataRun=$1
file=DoubleEG$DataRun

echo "Making index for DoubleEG$DataRun"

echo "index" > index${file}.txt
awk -F" " '{print $1}' ${file}.log >> index${file}.txt
