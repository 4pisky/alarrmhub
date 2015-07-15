
# coding: utf-8

# In[ ]:

from __future__ import print_function
import driveami
import datetime
from driveami import keys as amikeys
import os


# In[ ]:

def ami_utc_to_datetimes(utc_str):
    """Build 'datetime' objects from AMI-format date-strings"""
    date_format = '%Y-%m-%d %H:%M:%S'
    return datetime.datetime.strptime(utc_str, date_format)


# In[ ]:

data_dir = './'
with open(os.path.join(data_dir,'all_ami_rawfiles_metadata.json')) as f:
    observations, _ = driveami.load_listing(f)
with open(os.path.join(data_dir,'all_ami_rawfiles_by_pointing.json')) as f:
    groupings, _ = driveami.load_listing(f)


# In[ ]:

print("Loaded data for", len(observations), "observations, grouped into", len(groupings), "pointings")


# In[ ]:

#Drop rawtext - this is a big bunch of raw text data output from the AMI-REDUCE pipeline 
#which is mainly just used for debugging - we're not interested in it here.
for k in observations.keys():
    observations[k].pop(amikeys.raw_obs_text, None)

#Add the group ID to each observation entry 
for group_id, group_dict in groupings.iteritems():
    for filename in group_dict[amikeys.files]:
        observations[filename][amikeys.group_name]= group_id


# So, now we have a big dictionary, ``observations``, which contains basically all the information about the AMI dataset:

# In[ ]:

observations.keys()[:10]


# In[ ]:

#e.g.
print(observations.keys()[0])
observations.values()[0]


# You can process this raw data however you like. Below I've shown a couple of quick examples of how you can use the [pandas](http://pandas.pydata.org/) library to quickly manipulate the dataset, and display it in tabular form. First, let's simply load the data into a ``DataFrame``:

# In[ ]:

import pandas as pd
df = pd.DataFrame.from_records(observations).T
df = df.drop([amikeys.comment,amikeys.pointing_hms_dms,amikeys.field],1)
df.head()


# Not a bad start, but it would be nicer if we could separate out the start/end dates into separate columns. Let's do that:

# In[ ]:

df['utc_start'] = df.time_utc.apply(lambda x: ami_utc_to_datetimes(x[0]))
df['utc_end'] = df.time_utc.apply(lambda x: ami_utc_to_datetimes(x[1]))
df['mjd_start'] = df.time_mjd.apply(lambda x: x[0])
df['mjd_end'] = df.time_mjd.apply(lambda x: x[1])
df['ra'] = df.pointing_degrees.apply(lambda x: x[0])
df['dec'] = df.pointing_degrees.apply(lambda x: x[1])
#Make a new DataFrame, 'obs', without the old columns, or the warning_flags:
obs = df.drop([amikeys.time_ut, amikeys.time_mjd, amikeys.pointing_degrees, amikeys.warnings], 1)
obs = obs.sort('utc_start')


# In[ ]:

obs.head()


# Great. Now we can use our new DataFrame to filter down the dataset and just show us what we're interested in.
# For example, what if we just want to list observations made in the last week?

# In[ ]:

now = datetime.datetime.now()
recent_obs = obs[(now - obs.utc_start) < datetime.timedelta(days=7)]
recent_obs


# Or how about just listing V404 observations?

# In[ ]:

v404 = obs[obs.group_name=='SWIFT_643949'].sort('mjd_start')
v404


# In[ ]:

# We can convert this back to a basic Python dictionary if required:
v404.T.to_dict()

