#bin/bash!


TOPDIR=/home/jcordero/CMS/SMP_ZGamma/python
SUBDIRS=( Plotter  Samples Corrections)
for DIR in ${SUBDIRS[@]} 
do
	cd $DIR
	echo "In " $PWD
	echo "Performing : jupyter nbconvert --to script $TOPDIR/$DIR/*.ipynb"
	jupyter nbconvert --to script $TOPDIR/$DIR/*.ipynb
	cd $TOPDIR
	printf "\n\n"
done

