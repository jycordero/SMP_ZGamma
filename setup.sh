#bin/bash!

export PYTHONWORKDIR=/home/jcordero/CMS/JYCMCMS/SMP_ZG/python
export PYTHONPATH=$PYTHONPATH:/home/jcordero/CMS/JYCMCMS/SMP_ZG/python

TOPDIR=$PWD
SUBDIRS=( Plotter  Samples Corrections )
for DIR in ${SUBDIRS[@]} 
do
	cd $PYTHONWORKDIR/$DIR
	echo "In " $PWD
	echo "Performing : jupyter nbconvert --to script $PYTHONWORKDIR/$DIR/*.ipynb"
	jupyter nbconvert --to script $PYTHONWORKDIR/$DIR/*.ipynb
	cd $TOPDIR
	printf "\n\n"
done

