'''Calculate and plot velocity data from RFD. Compare against 
GNSS derived velocities.'''

import numpy as np 
import pandas as pd
import geopandas as pgd
from matplotlib import pyplot as pp
import plotly.express as px
import datetime as dt 
import plotly.graph_objects as go


### These parameters are for filtering the data. This should be 
#handled better, but I'm hard coding for now.

plotmap = True
#During the 10/2013 eclipse, right after launch, GPS was bounding all over the place, so 
#we filter out the beginning of the flight in addition to other nonsense (lon > -106.6822)
minlon = -106.6822
maxlon = -100.7892494
minlat = 34.254928
maxlat = 35.329046735

R = 6371.e3 # Radius of Earth in meters
mm_to_m=0.001

file = 'data/RFD900_MIEMU_101423_1439_2.csv'
file = 'data/PTER_MIEMU_040824_1726.csv'

crs = {'init':'epsg:4326'}
data = pd.read_csv(file)

breakpoint()
data['Latitude'] = data['Latitude']/1e7
data['Longitude'] = data['Longitude']/1e7
data['Altitude'] = data['Altitude']/1e6

#filter out data with bad gps coordinates


# filtered_data = data[data['Latitude'] > 0]
filtered_data = data[(data['Latitude'] > minlat) & (data['Latitude'] < maxlat) \
    & (data['Longitude'] > minlon) & (data['Longitude'] < maxlon)]

first = filtered_data.iloc[0].name
maxs = filtered_data['Altitude'].idxmax()

ascent = filtered_data.loc[first:maxs]

# Plot on an open map
if plotmap:
    fig = px.scatter_mapbox(ascent, 
                            lat="Latitude", 
                            lon="Longitude", 
                            zoom=8, 
                            height=800,
                            width=800)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    point1 = ascent[ascent['Altitude']>12].iloc[0]
    lat1 = point1['Latitude']
    lon1 = point1['Longitude']
    fig.add_trace(go.Scattermapbox(
        lat=[lat1],
        lon=[lon1],
        mode='markers',
        marker={'size':10,'color':'springgreen'}
    ))

    point2 = ascent[ascent['Altitude']>24].iloc[0]
    lat2 = point2['Latitude']
    lon2 = point2['Longitude']
    fig.add_trace(go.Scattermapbox(
        lat=[lat2],
        lon=[lon2],
        mode='markers',
        marker={'size':10,'color':'red'}
    ))

    fig.show()

time = []
for index,row in ascent.iterrows():
    time.append(dt.datetime(int(row['Year']),int(row['Month']),int(row['Day']),\
        int(row['Hour']),int(row['Min']),int(row['Sec'])))

ascent['DateTime'] = time

lon = np.asarray(ascent['Longitude']*np.pi/180)
lat = np.asarray(ascent['Latitude']*np.pi/180)
deltaLon = R*np.cos(lat[1:-1])*(lon[2:]-lon[0:-2]) #in meters; 
deltaLat = R*(lat[2:]-lat[0:-2]) #in meters; 

deltatime = []
for i in np.arange(0,len(time)-2):
    deltatime.append(2*(time[i+1]-time[i]).total_seconds())

#calculate velocities using central differencing
vNorth = (deltaLat)/deltatime
vEast  = (deltaLon)/deltatime

alpha = 0.5
pp.subplot(211)
pp.plot(vEast,ascent['Altitude'][1:-1])
pp.plot(ascent['NEV']*mm_to_m,ascent['Altitude'],alpha=alpha)
pp.xlim(-20,40)
# pp.xlabel('Veloctiy (m/s)')
pp.ylabel('Altitude (km)')

pp.subplot(212)
pp.plot(vNorth,ascent['Altitude'][1:-1])
pp.plot(ascent['NNV']*mm_to_m,ascent['Altitude'],alpha=alpha)
pp.xlim(-20,40)
pp.xlabel('Veloctiy (m/s)')
pp.ylabel('Altitude (km)')
pp.savefig('plot.png')

# breakpoint()
