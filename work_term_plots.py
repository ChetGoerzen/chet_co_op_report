'''
Must run cell by cell!!!
'''

import pandas as pd 
import matplotlib.pyplot as plt
import os
from datetime import datetime
from datetime import timedelta
import numpy as np

import sys
sys.path.append('../') #append the path to the directory containing desired scripts
from antelope_load import Load

home = os.path.expanduser('~/')

from matplotlib import rc
import matplotlib as mpl


plt.rc('font',**{'family':'dejavu-sans'})
plt.rc('text', usetex=False)
#%%

path = './data/'
db = Load(path)

#%%

clean = db.clean()

#%%

my_df = clean['clean_origin_origerr']

#%%

my_df['date'] = pd.to_datetime(my_df['time'],unit='s')
my_df.sort_values(by='time', inplace=True)
plt.hist(my_df.date, bins=25)
plt.xticks(rotation=45)
plt.ylabel('Number of Earthquakes')
plt.savefig(home + 'your_path', bbox_inches='tight')
plt.show()


#%%

fig, ax = plt.subplots(figsize=(15,10))
smap = ax.scatter(my_df.lon, my_df.lat, alpha=0.6, c=my_df.date, cmap='viridis')
cb = fig.colorbar(smap)
cb_labels = cb.ax.get_yticklabels()

#%%

my_labels = []
for l in cb_labels:
    time_stub = float(l.get_text())*1e9
    my_labels.append(datetime.utcfromtimestamp(time_stub).date())
    
#%%
   
site = db.site()
my_site = site[(site.lat < 56.5) & (site.lat > 55) & (site.lon < -120) & (site.lon > -121.5)]
fig, ax = plt.subplots(figsize=(15, 7.5))
smap = ax.scatter(my_df.lon, my_df.lat, alpha=0.6, c=my_df.date, cmap='viridis')
cb = fig.colorbar(smap)
cb.ax.set_yticklabels(my_labels) 
plt.grid()
ax.plot(my_site.lon, my_site.lat, '^', color='red', label='Seismic Stations')
plt.xticks(np.arange(-121.1, -120, step=0.1))
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.legend()
plt.savefig(home + 'your_path')
plt.show()

#%%

def get_hour(date):
    
    pacific_time = date - timedelta(hours=7)
    return pacific_time.hour

my_df["hour"] = my_df.date.apply(get_hour)

plt.hist(my_df.hour, bins=24, edgecolor='black')
plt.xlabel('Hour of day (PST)')
plt.ylabel('# of earthquakes')
plt.savefig(home + 'your_path')
plt.show()


#%%

plt.hist(my_df.ml, alpha=0.5, hatch='\\', facecolor='blue', edgecolor='black', linewidth=0.1, label='Dbevproc $M_{L}$')
plt.hist(my_df.cml, alpha=0.5, hatch='/', facecolor='orange', edgecolor='black', linewidth=0.1, label='Corrected $M_{L}$')
plt.xlabel('Magnitude ($M_{L}$)')
plt.ylabel('# of earthquakes')
plt.legend()
plt.savefig(home + 'your_path')
plt.show()

