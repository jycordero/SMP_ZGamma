# SMP_ZGamma
Make sure to incldue the `SMP_ZGamma/python` directory in yout `$PYTHONPATH` enviromental variable when working with this repository

You could do this in two ways
  * adding it to `.bashrc` (or `.profile`) files in your home directory, 
  * if you are working with conda you can add it to your local conda enviroment `conda env config vars $PYTHONPATH=$PYTHONPATH:[FULLPATH_TO_SMPPYTHON]`
  * (if available) some branch may contain `enviroment.yml` file that you can load to your conda enviroment as shown below. 
     * `conda env update --prefix ./env --file environment.yml  --prune`
     * If you don't understand the above read https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)

(Only in certain branches)`conf/config` is a single line document that contains the projectdir path, it should be modified to say `[YOUTLOCALPATH]/SMP_Zgamma`

`json/` contains a lot of parameters that could be dynamically changed without reloading any classes. This includes bins.csv(I know is a csv and not json), ranges.csv, and others
