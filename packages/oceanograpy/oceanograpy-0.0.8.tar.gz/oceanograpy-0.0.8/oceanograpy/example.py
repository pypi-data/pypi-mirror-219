# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 17:09:09 2023

@author: anba
"""

from workhorse_adcp import workhorse_adcp as wh_adcp 
from seabird_ctd import seabird_ctd as sb_ctd 
from processing_tools import processing_tools as ptools 
from matplotlib_dhi import subplots 
import adcp_plot_tools

import matplotlib.pyplot as plt
import matplotlib as mpl

pt3_filepath = r'\\USDEN1-STOR.DHI.DK\Projects\41806287\41806287 NORI-D Data\Data\ROV\Island Pride HD14\ADCP\Config\ROV_ADCP_20161_PT3.txt'
adcp_filepath = r'\\USDEN1-STOR.DHI.DK\Projects\41806287\41806287 NORI-D Data\Data\ROV\Island Pride HD14\ADCP\Raw\ADCP_24142_600kHz\ROV_ADCP_12102022\_RDI_005.000'

adcp_filepath = r'\\USDEN1-STOR.DHI.DK\Projects\41806287\41806287 NORI-D Data\Data\ROV\Island Pride HD14\ADCP\Raw\ADCP_24142_600kHz\ROV_ADCP_17102022\_RDI_005.000'
# pt3_filepath = r'\\USDEN1-STOR.DHI.DK\Projects\41806287\41806287 NORI-D Data\Data\Fixed Stations\02_Fixed_Bottom_Current_Turbidity\02_FBCT2\01_ADCP_600kHz-24144\Config_File\FBCT02_P3_TEST_17112022.txt'
# adcp_filepath = r'\\USDEN1-STOR.DHI.DK\Projects\41806287\41806287 NORI-D Data\Data\Fixed Stations\02_Fixed_Bottom_Current_Turbidity\02_FBCT2\01_ADCP_600kHz-24144\Raw\FBCT2_Full_Download_17112022\FBCT2000.000'


adcp_data = wh_adcp(filepath = adcp_filepath, PT3_filepath = pt3_filepath, verbose = 1)

adcp_data.filter_echo_intensity_data()
adcp_data.calculate_absolute_backscatter(field_name = 'ECHO INTENSITY')







#%%









#%% Add position and orientation data 
import pandas as pd, numpy as np
import copy

USBL = pd.read_csv(r'\\USDEN1-STOR.DHI.DK\Projects\41806287\41806287 NORI-D Data\Data\ROV\Island Pride HD14\Position\Processed\01 Merge\USBL_data_all_dives.csv', index_col = [0], parse_dates = True)
HAIN = pd.read_csv(r'\\USDEN1-STOR.DHI.DK\Projects\41806287\41806287 NORI-D Data\Data\ROV\Island Pride HD14\Position\Processed\01 Merge\HAIN_data_all_dives.csv', index_col = [0], parse_dates = True)





pos_in = HAIN[['Easting','Northing','Depth']].copy()
pos_in.columns = ['x','y','z']
pos_in['z'] = -pos_in['z']
adcp_data.set_sensor_position(pos_in)

orient_in = HAIN[['Pitch','Roll','Heading']]
orient_in.columns = ['pitch','roll','heading']
adcp_data.set_sensor_orientation(orient_in)


#%%
# adcp_data1 = copy.deepcopy(adcp_data)
# adcp_data2 = copy.deepcopy(adcp_data)

# pos_in = HAIN[['Easting','Northing','Depth']].copy()
# pos_in.columns = ['x','y','z']
# pos_in['z'] = -pos_in['z']
# adcp_data.set_sensor_position(pos_in)

# orient_in = HAIN[['Pitch','Roll','Heading']]
# orient_in.columns = ['pitch','roll','heading']
# adcp_data.set_sensor_orientation(orient_in)

# pos_in = USBL[['Easting','Northing','Depth']].copy()
# pos_in.columns = ['x','y','z']
# pos_in['z'] = -pos_in['z']
# adcp_data2.set_sensor_position(pos_in)

# orient_in = USBL[['Pitch','Roll','Heading']]
# orient_in.columns = ['pitch','roll','heading']
# adcp_data2.set_sensor_orientation(orient_in)






#%% Calculate beam geometery in reference frame of the ADCP
## y is the forward direction.

ips_offset = np.array([	-0.36,-1.45,	-0.31]) # offset of the ips from the ROV center of mass - note x and y coordinates interchanged, and z direction reversed to match the ADCP reference frame, 
adcp_offset = np.array([0.23,-1.38,	-0.19]) # offset of the adcp from the ROV center of mass - note x and y coordinates interchanged, and z direction reversed to match the ADCP reference frame, 
adcp_offset -= ips_offset 
adcp_length = 0.3949
adcp_offset[2] += adcp_length # add the offset to the face of the transducers
adcp_offset[2] = -adcp_offset[2] # flip z coordinate direction

adcp_data.set_beam_relative_geometry(rotation = 45,offset = adcp_offset, dr = 0.1)
    
    
    
    
## get position of beam midpoints for every ensemble 
adcp_data.absolute_beam_midpoint_positions = []
pos = adcp_data.position  
for b in range(adcp_data.n_beams):
    beam = adcp_data.relative_beam_midpoint_positions[b]
    adcp_data.absolute_beam_midpoint_positions.append(np.full((3,adcp_data.n_bins,adcp_data.n_ensembles),0, dtype = float))
    for e in range(adcp_data.n_ensembles):
        
        #build rotation matrix
        yaw   = adcp_data.orientation[2][e]
        pitch = adcp_data.orientation[0][e]
        roll  = adcp_data.orientation[1][e]
        R = np.dot(ptools.gen_rot_x(roll),ptools.gen_rot_z(yaw).dot(ptools.gen_rot_y(pitch)))
        
        
        X = np.add(pos[:,e],beam.T.dot(R)).T
        adcp_data.absolute_beam_midpoint_positions[b][:,:,e] = X#np.add(pos[:,e],beam.T).T
    


#%%


import data_visualizer

if __name__ == '__main__':
    # assets =[data_visualizer.ROV_ADCP_Asset(name = 'HAIN', adcp_data = adcp_data1),
    #           data_visualizer.ROV_ADCP_Asset(name = 'USBL', adcp_data = adcp_data1)]  
    
    
    # assets =[data_visualizer.ROV_ADCP_Asset(name = 'HAIN', adcp_data = adcp_data1),
    #           data_visualizer.ROV_ADCP_Asset(name = 'TEST', adcp_data = adcp_data1b)]  
    
    assets =[data_visualizer.IP_ROV_Asset(name = 'IP ROV', adcp_data = adcp_data)]  
    data_visualizer.run(assets = assets,timesteps = adcp_data.ensemble_times)


#%%
'''
import adcp_plot_tools
import processing_tools as ptools
from matplotlib_dhi import subplots
import os

start_ensemble = None
end_ensemble  = None

start_bin = 500
end_bin = 1000
fig,ax = adcp_plot_tools.four_beam_flood_plot(adcp_data,field = 'ABSOLUTE BACKSCATTER', start_ensemble = start_ensemble, end_ensemble = end_ensemble,start_bin = start_bin, end_bin = end_bin)
fig,ax = adcp_plot_tools.four_beam_flood_plot(adcp_data,field = 'SIGNAL TO NOISE RATIO', start_ensemble = start_ensemble, end_ensemble = end_ensemble,start_bin = start_bin, end_bin = end_bin)
#%%
adcp_plot_tools.progressive_vector_plot(adcp_data)#, color_by , start_bin, end_bin, start_ensemble, end_ensemble, title)

fig,ax = adcp_plot_tools.four_beam_flood_plot(adcp_data,field = 'ECHO INTENSITY')
fig,ax = adcp_plot_tools.four_beam_flood_plot(adcp_data,field = 'CORRELATION MAGNITUDE')
fig,ax = adcp_plot_tools.four_beam_flood_plot(adcp_data,field = 'PERCENT GOOD')
fig,ax = adcp_plot_tools.four_beam_flood_plot(adcp_data,field = 'ABSOLUTE BACKSCATTER')
fig,ax = adcp_plot_tools.four_beam_flood_plot(adcp_data,field = 'SIGNAL TO NOISE RATIO')


fig,ax = adcp_plot_tools.error_velocity_plot(adcp_data)
fig,ax = adcp_plot_tools.single_beam_flood_plot(adcp_data,field = 'ECHO INTENSITY')
fig,ax = adcp_plot_tools.single_beam_flood_plot(adcp_data,field = 'CORRELATION MAGNITUDE')
fig,ax = adcp_plot_tools.single_beam_flood_plot(adcp_data,field = 'PERCENT GOOD')
fig,ax = adcp_plot_tools.single_beam_flood_plot(adcp_data,field = 'ABSOLUTE BACKSCATTER')
fig,ax = adcp_plot_tools.single_beam_flood_plot(adcp_data,field = 'SIGNAL TO NOISE RATIO')
fig,ax = adcp_plot_tools.metadata_table(adcp_data)

'''

#%%
fig,ax = subplots()
ensemble_times = adcp_data.ensemble_times
mask = (USBL.index>ensemble_times[0]) & (USBL.index<ensemble_times[-1])
ax.scatter(USBL.loc[mask,'Easting'],USBL.loc[mask,'Northing'], alpha = 0.7, label = 'USBL', s = 20)

mask = (HAIN.index>ensemble_times[0]) & (HAIN.index<ensemble_times[-1])
ax.scatter(HAIN.loc[mask,'Easting'],HAIN.loc[mask,'Northing'], alpha = 0.7, label = 'HAIN', s = 20)

ax.scatter(adcp_data1.position[0,:],adcp_data1.position[1,:], alpha = 0.7, label = 'ADCP 1 (HAIN)', color = 'red', s = 15)
ax.legend()


#%% 


#%% QC tool for masking the data 
#adcp_file = adcp_data
## set of masks that can be applied to ensemble data when called by the get_ensemble_array method 
## make an apply mask method
## make a remove mask method


# adcp_file.get_ensemble_array('SIGNAL TO NOISE RATIO', beam = 1)

# adcp_file.ensemble_masks = {}


#%% calculate x,y,z midpoint locations for each bin and each beam 






#%% ToDo
# calculate beam midpoint locations (accounting for beam angle, and orientation of the sensor )
# get point cloud (similar to get_ensemble_array)
# Spatially varying depths for the ensemble plots
# QC tool for masking the data 
# lump together ADCP data into single workhorse ADCP plots 




#%%



#%% Auto QAQC





#%% 









