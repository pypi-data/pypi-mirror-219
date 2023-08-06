# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 09:43:25 2023

@author: anba
"""

from workhorse_adcp import workhorse_adcp as wh_adcp 
from seabird_ctd import seabird_ctd as sb_ctd 
from processing_tools import processing_tools as ptools 
from matplotlib_dhi import subplots 
import adcp_plot_tools

import matplotlib.pyplot as plt
import matplotlib as mpl
import os 




root_dir = r'C:\Users\anba\OneDrive - DHI\Desktop\misc\Ocean Sierra\Data for Andy'



## get a list of all pd0 files 
fpaths = [i for i in os.listdir(root_dir) if i.endswith('000')]



ADCP_data = {}
for i,file in enumerate(fpaths):
    ADCP_data[i] = wh_adcp(os.sep.join([root_dir,file]))
    
#%%  
    
    
    
adcp_data = ADCP_data[0]

fig,ax = adcp_plot_tools.four_beam_flood_plot(adcp_data,field = 'ECHO INTENSITY')
fig,ax = adcp_plot_tools.four_beam_flood_plot(adcp_data,field = 'CORRELATION MAGNITUDE')
fig,ax = adcp_plot_tools.four_beam_flood_plot(adcp_data,field = 'PERCENT GOOD')
fig,ax = adcp_plot_tools.four_beam_flood_plot(adcp_data,field = 'ABSOLUTE BACKSCATTER')
fig,ax = adcp_plot_tools.four_beam_flood_plot(adcp_data,field = 'SIGNAL TO NOISE RATIO')
    
    