#bin/bash!

export PYTHONWORKDIR=/home/jcordero/CMS/JYCMCMS/SMP_ZG/python
export PYTHONPATH=$PYTHONPATH:/home/jcordero/CMS/JYCMCMS/SMP_ZG/python

TOPDIR=$PWD
SUBDIRS=( Plotter  Samples Selections Efficiency Corrections Cuts Common )
for DIR in ${SUBDIRS[@]} 
do
	jupyter nbconvert --to script *.ipynb
	cd $PYTHONWORKDIR/$DIR/jupyter
	echo "In " $PWD
	echo "Performing : jupyter nbconvert --to script $PYTHONWORKDIR/$DIR/*.ipynb"
	jupyter nbconvert --to script *.ipynb
	mv *.py $PYTHONWORKDIR/$DIR

	cd $TOPDIR
	printf "\n\n"
done

