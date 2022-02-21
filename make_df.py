# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 15:57:41 2022
"""

from io import StringIO
import pandas as pd

import matplotlib.pyplot as plt
import cartopy.crs as ccrs

#Split by 'start'

with open('etc-all-traj.txt') as f: #location and filename of our storm txt file.
    file = f.read()

storms = file.split('start')


# Loop through these storms and format into a pandas dataframe list 'dfs'


dfs=[]
for storm in storms:
    if len(storm)>0: #accounting for bad lines (e.g. the first line of the file!).
        storm_io = StringIO(storm)
        df = pd.read_csv(storm_io,skiprows=1,
                         header=None,
                         #added a dummy 'blank' column to account for leading tab in the file.
                         names=['blank','info1','info2','lon','lat','y','m','d','h'], #this is the column names in your data: replace info1,info2 etc with what they actually mean, I couldn't remember and check I didn't get lat and lon the wrong way round!
                         sep='	'
                         )
        
        
        df['lon']=df['lon'].where(df['lon']<180,df['lon']-360)
        
        df=df.drop(columns=['blank']) #getting rid of dummy column

        
        storm_header = 'start\t'+storm.split('\n')[0]
        df.storm_header = storm_header
        dfs.append(df)
     
        

def plot_storm(df):
    '''
    plot a storm track
    '''
    lons=df.lon
    lats=df.lat
    
    ax = plt.axes(projection=ccrs.PlateCarree()) 
    ax.plot(lons,lats,transform=ccrs.PlateCarree()) 
    ax.set_extent([min(lons)-1,max(lons)+1,min(lats)-1,max(lons)+1]) 
    ax.coastlines() #Add Coastlines
    plt.savefig('example.jpg')
    #plt.show()
    
print(dfs[6].storm_header)
print(dfs[6])


plot_storm(dfs[6])
    
