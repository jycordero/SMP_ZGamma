MODE=$1
PORT=$2

if [ -z $MODE ]; then
	printf "\n"
	echo "Speficy  operation(remote, locally)"
	echo "--- If remote, specify port otherwise port=8889"
	printf "\n\n"
else
	if [ -z $PORT ] ; then 
		PORT=8889
	fi
	source activate CMSenv
	source setup.sh

	if [ "$MODE" = "remote" ]; then
		echo "--Running remote operation at port 8889"
		jupyter notebook --no-browser --port=$PORT
	else
		echo "--Running local operation"
		jupyter notebook 
	fi
fi
