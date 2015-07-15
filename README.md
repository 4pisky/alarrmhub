#ALARRMhub

Prototype tools for viewing and co-ordinating ALARRM observations en masse.

## Installation:

From this directory:

    pip install drive-ami
    pip install ipython[notebook] pandas # (Optional)
    

Note, working in a 
[virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
is recommended, [because](http://iamzed.com/2009/05/07/a-primer-on-virtualenv/) 
[reasons](http://simononsoftware.com/virtualenv-tutorial-part-2/#_why_you_really_need_it), 
but if you prefer you can install the 
Python package to your user area - just run ``pip install --user`` instead
of ``pip install``.
    

## Getting the metadata dumps
Assuming you're on the Oxford campus:

    scp staley@astropi1.physics.ox.ac.uk:~/code/alarrmhub/*.json .
    
## Loading the metadata:
Loading the data into one big dictionary is quite simple - the first few cells 
in notebook 'load_obs_metadata.ipynb' show how to do this (or see also
'load_obs_metadata.py' for the plain-Python version. The rest of the notebook
demos how you can start to display and filter the metadata using 
[Pandas](http://pandas.pydata.org/). 

