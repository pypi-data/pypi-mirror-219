# -*- coding: utf-8 -*-
"""
Created on Sun Dec 18 10:08:43 2022

@author: anba
"""

import pandas as pd
import numpy as np
import os,sys

from scipy.ndimage import gaussian_filter1d
import argparse
import matplotlib.cm as cm
import cmocean


import vispy 
from vispy.app import use_app, Timer
from vispy import app, visuals, scene
from vispy.io import imread, load_data_file, read_mesh, read_png
from vispy.visuals.transforms import STTransform,MatrixTransform

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import * 
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

#%%
from workhorse_adcp import workhorse_adcp as wh_adcp 
from seabird_ctd import seabird_ctd as sb_ctd 
from processing_tools import processing_tools as ptools 
from matplotlib_dhi import subplots 
import adcp_plot_tools

import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd, numpy as np

#%%
# pt3_filepath = r'\\USDEN1-STOR.DHI.DK\Projects\41806287\41806287 NORI-D Data\Data\ROV\Island Pride HD14\ADCP\Config\ROV_ADCP_20161_PT3.txt'
# #adcp_filepath = r'\\USDEN1-STOR.DHI.DK\Projects\41806287\41806287 NORI-D Data\Data\ROV\Island Pride HD14\ADCP\Raw\ADCP_24142_600kHz\ROV_ADCP_12102022\_RDI_005.000'
# adcp_filepath = r'\\USDEN1-STOR.DHI.DK\Projects\41806287\41806287 NORI-D Data\Data\ROV\Island Pride HD14\ADCP\Raw\ADCP_24142_600kHz\ROV_ADCP_17102022\_RDI_005.000'


# adcp_data = wh_adcp(filepath = adcp_filepath, PT3_filepath = pt3_filepath, verbose = 1)



# USBL = pd.read_csv(r'\\USDEN1-STOR.DHI.DK\Projects\41806287\41806287 NORI-D Data\Data\ROV\Island Pride HD14\Position\Processed\01 Merge\USBL_data_all_dives.csv', index_col = [0], parse_dates = True)
# HAIN = pd.read_csv(r'\\USDEN1-STOR.DHI.DK\Projects\41806287\41806287 NORI-D Data\Data\ROV\Island Pride HD14\Position\Processed\01 Merge\HAIN_data_all_dives.csv', index_col = [0], parse_dates = True)


# pos_in = HAIN[['Easting','Northing','Depth']].copy(deep = True)
# pos_in.columns = ['x','y','z']
# pos_in['z'] = -pos_in['z']
# adcp_data.set_sensor_position(pos_in)


# orient_in = HAIN[['Pitch','Roll','Heading']]
# orient_in.columns = ['pitch','roll','heading']
# adcp_data.set_sensor_orientation(orient_in)



#%%

# ######################### Load company logos ##################################
# path = os.sep.join([script_dir,'Logos','Logos.png'])
# logos = scene.visuals.Image(read_png(path))



#%%#############################################################################
#######################  INITIALIZE VISUALIZATION  ############################
###############################################################################
class ROV_ADCP_Asset:
    def __init__(self,name,adcp_data):
        # contains data 
        self.name = name # name of the asset 
        self.adcp_data = adcp_data
        
    def init_plot(self,canvas):
        
        scene.visuals.Line(pos =  self.adcp_data.position.T, width = .1, parent  = canvas.main_view.scene)
        
        self.plane_verts = 30*np.array([[-.5,-.5,0],
                                        [-.5,.5,0],
                                        [.5,.5,0],
                                        [.5,-.5,0],
                                        [-.5,-.5,0]])
        self.plane = scene.visuals.Line(pos = np.add(self.plane_verts , self.adcp_data.position[:,0]), width = 5, parent  = canvas.main_view.scene)
        
        
        self.beams = []
        for i in range(self.adcp_data.n_beams):
            
            beam_pos = np.full((self.adcp_data.n_bins,3),0)
            
            
            # set beam direction 
            if self.adcp_data.beam_facing == 'DOWN':
                beam_dir = -1
            else: beam_dir = 1
            
            beam_pos[:,2] = beam_dir*self.adcp_data.bin_midpoints
            self.beams.append(beam_pos)
            
        theta_beam = self.adcp_data.ensemble_data[0]['FIXED LEADER']['BEAM ANGLE']
        self.beams[0] = np.dot(self.beams[0],ptools.gen_rot_x(theta_beam))
        self.beams[1] = np.dot(self.beams[1],ptools.gen_rot_x(-theta_beam))
        self.beams[2] = np.dot(self.beams[2],ptools.gen_rot_y(-theta_beam))
        self.beams[3] = np.dot(self.beams[3],ptools.gen_rot_y(theta_beam))
        
        #self.beams[2] = adcp_data.get_bin_midpoints
    
        self.beam_lines = []
        
        for i in range(self.adcp_data.n_beams):
            self.beam_lines.append(scene.visuals.Line(pos = np.add(self.beams[i],self.adcp_data.position[:,0]),
                                                width = 1,
                                                parent =canvas.main_view.scene))    
            
            
        self.asset_label  = scene.visuals.Text(self.name,
                                                  color='white',
                                                  rotation=0,
                                                  font_size = 5000,
                                                  pos = self.adcp_data.position[:,0],
                                                  parent=canvas.main_view.scene) 
            
    def update(self):
        t,curr_time = sim_params.get_sim_params()
        
        ## Build the rotation matrix
        yaw   = self.adcp_data.orientation[2][t]
        pitch = self.adcp_data.orientation[0][t]
        roll  = self.adcp_data.orientation[1][t]
        R = np.dot(ptools.gen_rot_x(roll),ptools.gen_rot_z(yaw).dot(ptools.gen_rot_y(pitch)))
        
        
        ## rotate the reference plane (ROV)
        X = np.add(self.plane_verts.dot(R), self.adcp_data.position[:,t])
        self.plane.set_data(pos= X, width = 1)
        
        
        ## rotate the beams
        for b in range(self.adcp_data.n_beams):
            X = np.add(self.beams[b].dot(R), self.adcp_data.position[:,t])
            self.beam_lines[b].set_data(pos = X)
        
        self.asset_label.pos = self.adcp_data.position[:,t]


class IP_ROV_Asset:
    # y is the forward direction
    def __init__(self,name,adcp_data):
        # contains data 
        self.name = name # name of the asset 
        self.adcp_data = adcp_data
        
        self.platform_offset = np.array([-0.36,-1.45,-0.31]) # position of the center of the instrument platform (e.g., vessel) relative to the position measurement. 
        
        self.platform_width = 1.74
        self.platform_height = 2.74
       
        
    def init_plot(self,canvas):
        
        # scene.visuals.Line(pos =  self.adcp_data.position.T, width = .1, parent  = canvas.main_view.scene)
        
        
        
        self.plane_verts = np.array([[-.5,-.5,0],
                                    [-.5,.5,0],
                                    [.5,.5,0],
                                    [.5,-.5,0],
                                    [-.5,-.5,0]])
        
        Ts = np.diag([1.74,2.74,1]) #ROV x-y dimensions
        self.plane_verts = self.plane_verts.dot(Ts) - self.platform_offset
        #self.plane = scene.visuals.Line(pos = self.plane_verts, width = 5, parent  = canvas.main_view.scene)
        self.plane = scene.visuals.Line(pos = np.add(self.plane_verts , self.adcp_data.position[:,0]), width = 5, parent  = canvas.main_view.scene)
        
        
        

        self.beam_verts = [] # store relative positions of the beams including origin
        self.beam_lines = []
        self.beam_labels = []
        for i in range(self.adcp_data.n_beams):
            origin = self.adcp_data.relative_beam_origin[:,i] 
            #pos = np.add(self.adcp_data.beam_midpoint_positions[i].T,self.adcp_data.position[:,0])
            
            pos = np.zeros((self.adcp_data.n_bins+1,3), dtype = float)
            pos[1:,:] = self.adcp_data.relative_beam_midpoint_positions[i].T
            pos[0,:] = origin
            self.beam_verts.append(pos)
           # pos = np.add(pos,self.adcp_data.position[:,0])

            
            self.beam_lines.append(scene.visuals.Line(pos = self.adcp_data.absolute_beam_midpoint_positions[i][:,:,0].T,
                                                width = 1,
                                                parent =canvas.main_view.scene))   
            
            
            
            
            self.beam_labels.append(scene.visuals.Text(f'beam {i+1}',
                                                      color='white',
                                                      rotation=0,
                                                      font_size = 1500,
                                                      pos = np.add(pos,self.adcp_data.position[:,0])[-1],
                                                      parent=canvas.main_view.scene) )
            
        self.beam_origin = scene.visuals.Markers(pos = np.add(self.adcp_data.position[:,0],self.adcp_data.relative_beam_origin.T), size = 3,parent =canvas.main_view.scene)     
        self.asset_label  = scene.visuals.Text(self.name,
                                                  color='white',
                                                  rotation=0,
                                                  font_size = 500,
                                                  pos = self.adcp_data.position[:,0]- self.platform_offset,
                                                  parent=canvas.main_view.scene) 
        
    def update(self):
        t,curr_time = sim_params.get_sim_params()     
        
        # self.asset_label.transform = STTransform(scale=(1, 1, 1), translate=self.adcp_data.position[:,t]-self.adcp_data.position[:,t-1])
        
        
        ## Build the rotation matrix
        yaw   = self.adcp_data.orientation[2][t]
        pitch = self.adcp_data.orientation[0][t]
        roll  = self.adcp_data.orientation[1][t]
        R = np.dot(ptools.gen_rot_x(roll),ptools.gen_rot_z(yaw).dot(ptools.gen_rot_y(pitch)))
        
    
        # update the platform (ROV)
        X = np.add(self.plane_verts.dot(R), self.adcp_data.position[:,t])
        self.plane.set_data(pos= X, width = 1)
        
        
        ## update the beams
        for b in range(self.adcp_data.n_beams):
            self.beam_lines[b].set_data(pos = self.adcp_data.absolute_beam_midpoint_positions[b][:,:,t].T)
            self.beam_labels[b].pos = self.adcp_data.absolute_beam_midpoint_positions[b][:,:,t].T[-1]
        
        self.asset_label.pos = self.adcp_data.position[:,t]- self.platform_offset
        
        
        self.beam_origin.set_data(pos = np.add(self.adcp_data.position[:,t],self.adcp_data.relative_beam_origin.T) )

        
        ## function to update the Asset
        
        
##To Do 

# Update CanvasWrapper to accept the Asset object and have global simulation parameters
# Before plotting resample all asset data to simulation timestep         
        

class SimParams:
    def __init__(self,timesteps):
        
        self.timestep = 1
        self.timesteps = timesteps
        
        self.t = 0
        self.curr_time = self.timesteps[self.t]
    
    def advance(self):
        # advance the simulation one timestep
        self.t = (self.t+self.timestep)%(len(self.timesteps))
        self.curr_time = self.timesteps[self.t]
        
    
    def get_sim_params(self):
        return self.t,self.curr_time
        

    
class CanvasWrapper:
    def __init__(self, assets,sim_params):
        
        #% Global Simulation Parameters 

        
        
        ##
        
        self.canvas = scene.SceneCanvas(keys='interactive',
                                        title='NORI-D Data Viewer',
                                        show=True,
                                        bgcolor = 'black',
                                        size=(1800, 1000))
        
        self.grid =  self.canvas.central_widget.add_grid()
        self.main_view =  self.grid.add_view(row=0,
                                             col=0,
                                             row_span=10,
                                             col_span = 10) # main viewer window
        
        #window for displaying company logos
        self.icon_view = self.grid.add_view(row=9,
                                            col=1,
                                            col_span = 4,
                                            row_span = 1,
                                            margin = 1,
                                            padding = 1) 
        
        #window for displaying company logos
        self.time_view = self.grid.add_view(row=8,
                                            col=7,
                                            col_span = 3,
                                            row_span =2,
                                            margin = 1,
                                            padding = 1) 
        

        self.assets = assets
        
        
        
        ## Setup the plot objects 
        self.time_display = scene.visuals.Text(sim_params.timesteps[0].strftime("%d-%b-%y %H:%M"),
                                          color='white',
                                          rotation=0,
                                          font_size = 15,
                                          pos = (380,130),
                                          parent=self.time_view.scene) 
        


        for asset in self.assets:
            asset.init_plot(self)
            
        self.main_view.camera = "turntable" #'arcball' 
    
    

        
        





class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, canvas_wrapper: CanvasWrapper, *args, **kwargs):
        super().__init__(*args, **kwargs)

        central_widget = QtWidgets.QWidget()
        main_layout = QtWidgets.QHBoxLayout()

        self.setWindowTitle("SET TITLE")
        # self.setWidth(1800)
        # self.setFixedHeight(1000)

        self.setGeometry(25, 25, 1800, 1000)

        
        self._canvas_wrapper = canvas_wrapper
        main_layout.addWidget(self._canvas_wrapper.canvas.native)
        
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)   
        
        
        quit = QtWidgets.QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)
        
        self.paused = False # paused indicator variable 

        # creating a QWidget object
        widget = QtWidgets.QWidget(self)
 
        # creating a vertical box layout
        layout = QtWidgets.QVBoxLayout(self)
 
        # push button 1
        self.PausePlayButton = QtWidgets.QPushButton("Pause", self)
        self.PausePlayButton.clicked.connect(self.pause_play)
        #self.StartButton.valueChanged[int].connect(self.pause_play)
        
        # time slider 
        self.TimeSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.TimeSlider.setRange(0,len(sim_params.timesteps))
        self.TimeSlider.valueChanged[int].connect(self.update_time)
        
        # timestep dial
        self.TimestepDial = QtWidgets.QDial()
        self.TimestepDial.valueChanged.connect(self.update_timestep)
        self.TimestepDial.setRange(-10,10)
        self.TimestepDial.setNotchesVisible(True)
        self.TimestepDial.setGeometry(220, 125, 200, 60)
        self.DialLabel = QtWidgets.QLabel(f"dt = {sim_params.timestep} min", self)
        self.DialLabel.setAlignment(Qt.AlignCenter)
        self.DialLabel.setGeometry(400, 125, 200, 60)
        
        # adding these buttons to the layout
        layout.addWidget(self.PausePlayButton)
        layout.addWidget(self.TimeSlider)
        layout.addWidget(self.DialLabel)
        layout.addWidget(self.TimestepDial)
        
        # setting the layout to the widget
        
        widget.setLayout(layout)
        widget.setAutoFillBackground(True)
        
        # Playback Dock Popout Window 
        self.PlaybackDock=QtWidgets.QDockWidget('Playback',self)
        self.PlaybackDock.setFixedSize(200, 300)
        self.PlaybackDock.setWidget(widget)        
        self.PlaybackDock.setGeometry(100, 0, 200, 30)
        self.PlaybackDock.setAllowedAreas(Qt.NoDockWidgetArea)

        
    def update_timestep(self):
        global timestep
        sim_params.timestep = self.TimestepDial.value()
        
        self.DialLabel.setText(f"dt = {sim_params.timestep} min")
        
        
    def update_time(self):
        global t
        sim_params.t = self.TimeSlider.value()
        
        canvas.main_view.update()
        
    def pause_play(self):
        if not self.paused:
            timer.stop()
            self.paused = True
            self.PausePlayButton.setText('Play')
        else:
            timer.start()
            self.paused = False
            self.PausePlayButton.setText('Pause')
        
        
    def closeEvent(self, event):
        timer.stop()

        


def update(ev):
    
    sim_params.advance()
    t,curr_time = sim_params.get_sim_params()
    
    win.TimeSlider.setValue(t)
    canvas.time_display.text = curr_time.strftime("%d-%b-%y %H:%M")
    
    for asset in canvas.assets:
          asset.update()

    
    

    
def run(assets,timesteps):

    global timer,canvas,app,win,sim_params
    
    
    sim_params = SimParams(timesteps = timesteps)
      
    app = use_app("pyqt5")
    app.create()
    
    
    canvas = CanvasWrapper(sim_params= sim_params, assets = assets)
    win = MainWindow(canvas)
    
    
    timer = Timer("auto", connect=update, start=True, app = app)
    win.destroyed.connect(timer.stop)
    
    win.show()
    app.run()    
  

#def run():


# assets =[ IP_ROV_Asset(name = 'ROV ADCP', adcp_data = adcp_data)]    
# run(assets,timesteps = adcp_data.ensemble_times)
    


#%%

# if __name__ == '__main__':
#     # assets =[data_visualizer.ROV_ADCP_Asset(name = 'HAIN', adcp_data = adcp_data1),
#     #           data_visualizer.ROV_ADCP_Asset(name = 'USBL', adcp_data = adcp_data1)]  
    
    
#     # assets =[data_visualizer.ROV_ADCP_Asset(name = 'HAIN', adcp_data = adcp_data1),
#     #           data_visualizer.ROV_ADCP_Asset(name = 'TEST', adcp_data = adcp_data1b)]  
    
#     assets =[data_visualizer.ADCP_Asset(name = 'USBL', adcp_data = adcp_data)]  
#     data_visualizer.run(assets = assets,timesteps = adcp_data.ensemble_times)


