#bin/bash!

export PARENTWORKDIR=/home/jcordero/CMS/JYCMCMS/SMP_ZG/python
export PYTHONPATH=$PYTHONPATH:/home/jcordero/CMS/JYCMCMS/SMP_ZG/python

TOPDIR=$PARENTWORKDIR
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

