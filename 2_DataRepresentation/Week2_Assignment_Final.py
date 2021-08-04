#!/usr/bin/env python
# coding: utf-8

# # Week 2 - Assignment

# In[1]:


get_ipython().run_line_magic('matplotlib', 'notebook')


# In[83]:


import matplotlib as mpl
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from matplotlib.artist import Artist

import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd
import numpy as np

import warnings
warnings.filterwarnings('ignore')

pd.options.display.max_rows = 4000


# In[24]:


# ------------------------- Prep data for 2005-2014 -------------------------
# Read the file
df = pd.read_csv('Course2_Resources/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')

# Top values (comparing data from all stations)
# From 165.085 to around 4.000 rows
df = df.groupby('Date').agg({'Data_Value' : (np.max, np.min)})
df = df['Data_Value']
# Setting a datetime index
df.index = pd.to_datetime(df.index)

# Pulling the data for the period 2005-2014
dfUpTo2014 = df[:'2014']

# Pulling month and day info for later comparison between years
dfUpTo2014['Year'] = dfUpTo2014.index.year
dfUpTo2014['Month'] = dfUpTo2014.index.month
dfUpTo2014['Day'] = dfUpTo2014.index.day

# Comparison for same month and day between years
# From around 4.000 rows to 360 approx.
dfUpTo2014 = dfUpTo2014.groupby(['Month', 'Day']).agg({'amax' : np.max, 'amin' : np.min})
dfUpTo2014


# ------------------------- Prep data for 2015 -------------------------
df2 = pd.read_csv('Course2_Resources/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')

# Top values (comparing data from all stations)
# From 165.085 to around 4.000 rows
df2 = df2.groupby('Date').agg({'Data_Value' : (np.max, np.min)})
df2 = df2['Data_Value']
# Setting a datetime index
df2.index = pd.to_datetime(df.index)

# Pulling the data for the year 2015
df2015 = df2['2015']

# Pulling month and day info for later comparison between years
df2015['Month'] = df2015.index.month
df2015['Day'] = df2015.index.day
df2015.set_index(['Month', 'Day'], inplace = True)
df2015.columns = ['Max 2015', 'Min 2015']
dfUpTo2014.columns = ['Max 2005-2014', 'Min 2005-2014']
comparison = pd.merge(dfUpTo2014, df2015, how = 'left', left_index = True, right_index = True)
comparison['2015 broke max record'] = comparison['Max 2015'] > comparison['Max 2005-2014']
comparison['2015 broke min record'] = comparison['Min 2015'] < comparison['Min 2005-2014']
comparison


# In[58]:


dates = []
tmax = []
tmax2015 = []
tmin = []
tmin2015 = []

for ind, row in comparison.iterrows():
    dates.append(str(ind[1]) + '/' + str(ind[0]))
    
    if row['2015 broke max record'] == True:
        tmax.append(row['Max 2015'])
        tmax2015.append(row['Max 2015'])
        
    else:
        tmax.append(row['Max 2005-2014'])
        tmax2015.append(np.nan)

for ind, row in comparison.iterrows():
    if row['2015 broke min record'] == True:
        tmin.append(row['Min 2015'])
        tmin2015.append(row['Min 2015'])
        
    else:
        tmin.append(row['Min 2005-2014'])
        tmin2015.append(np.nan)
        
# Temperature correction, dividing by 10
tmax = list(map(lambda x: x / 10, tmax))
tmax2015 = list(map(lambda x: x / 10, tmax2015))
tmin = list(map(lambda x: x / 10, tmin))
tmin2015 = list(map(lambda x: x / 10, tmin2015))


# In[84]:


plt.figure()

# Plot the max and min temperature records for period 2005 - 2015, including the latter
plt.plot(dates, tmax, '-', label = 'Max. Temperatures', c = '#F5B964')
plt.plot(dates, tmin, '-', label = 'Min. Temperatures', c = '#A6CDF5')

# highlighting those days where 2015 broke the record
plt.scatter(dates, tmax2015, s = 15, label = 'Max. Record in 2015', c = 'red')
plt.scatter(dates, tmin2015, s = 15, label = 'Min. Record in 2015',  c = 'blue')

# Fill space between both lines
plt.gca().fill_between(range(len(tmax)),
                      tmin, tmax, facecolor = 'grey', alpha = 0.05)

# Setting values of the xaxis
# We choose the positions for major ticks to show up and what values those ticks should
# show
ticks = [0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]
labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
              'September', 'October', 'November', 'December']
plt.xticks(ticks, labels)

# Pulling the xaxis ticks for later editing
x = plt.gca().xaxis

# Rotating the xaxis ticks
for item in x.get_ticklabels():
    item.set_rotation(60)
    
# Labels for the axis
plt.xlabel('Date')
plt.ylabel('Temperature (Degrees)')
plt.title('Record temperatures for the period 2005-2015')
plt.legend(loc = 'upper left', prop = fontP, frameon = False, fontsize = 'x-small')

    
plt.subplots_adjust(bottom = 0.25)

plt.savefig('Week2_Assignment_Jonathan.png')
plt.show()

